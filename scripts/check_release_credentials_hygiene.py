#!/usr/bin/env python3
"""
Fail if a release credential can reach a process command line or the console.

/proc/<pid>/cmdline is world-readable, so a secret on the argv of docker, make, gh or the
`/bin/sh -c` that runs a recipe line is visible to every user on the host. make expands
`$(NAME)` / `${NAME}` INTO the recipe line before the shell runs it, so a recipe may only read a
secret as `$${NAME}` (expanded by the shell from the exported environment).

Usage: check_release_credentials_hygiene.py [FILE ...]
Without arguments it checks ./Makefile and .github/workflows/*.yml|*.yaml. A file is treated as a
workflow when its name ends in .yml / .yaml, otherwise as a Makefile.
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple

SECRET: str = r"[A-Z0-9_]*(?:TOKEN|PASSWORD|API_KEY|SECRET|PASSPHRASE|USERNAME)[A-Z0-9_]*"

# The one allowed make expansion of a secret in a recipe: printing whether it is set.
ALLOWED_SET_UNSET: re.Pattern = re.compile(rf"\$\(if \$\({SECRET}\),<set>,<unset>\)")

MAKEFILE_CHECKS: List[Tuple[re.Pattern, str]] = [
    (re.compile(rf"(?:-e|--env)[ =]+{SECRET}="), "docker -e/--env NAME=value puts the value on argv; use -e NAME"),
    (re.compile(rf"(?<!\$)\$[({{]{SECRET}[)}}]"), "make expands the secret into the recipe line; use $${NAME}"),
    (re.compile(r"\$\(info\)"), "$(info) hands credentials to a command line"),
    (re.compile(rf"(?:\bmake\b|\$\(MAKE\)).*\b{SECRET}="), "make NAME=value puts the value on argv; export it"),
    (re.compile(r"(?<![\w-])-[pu]\s*\$\$?[({]"), "-p/-u with a variable puts a credential on argv"),
    (re.compile(r"(?<![\w-])--(?:token|password)(?![\w-])"), "--token/--password on argv"),
    (re.compile(r"Authorization:", re.IGNORECASE), "Authorization header on argv"),
    (re.compile(rf"\becho\b[^|]*\$\$\{{?{SECRET}\b(?![^|]*\|)"), "echo prints the secret to the console"),
]


def check_makefile(path: Path, text: str) -> List[str]:
    """
    Return one message per leaking recipe line of a Makefile.

    Args:
        path (Path):
            File name used in the messages.
        text (str):
            Makefile content.

    Returns:
        List[str]:
            `file:line: reason` messages, empty when the Makefile is clean.
    """
    errors: List[str] = []
    for number, line in enumerate(text.splitlines(), start=1):
        if not line.startswith("\t"):
            continue
        line = ALLOWED_SET_UNSET.sub("", line)
        errors += [f"{path}:{number}: {reason}: {line.strip()}" for pattern, reason in MAKEFILE_CHECKS if pattern.search(line)]
    return errors


def check_workflow(path: Path, text: str) -> List[str]:
    """
    Return one message per workflow `run:` line that interpolates `${{ secrets.* }}`.

    Args:
        path (Path):
            File name used in the messages.
        text (str):
            Workflow YAML content.

    Returns:
        List[str]:
            `file:line: reason` messages; a secret belongs in `env:` and is read as `$NAME`.
    """
    errors: List[str] = []
    run_indent: int = -1
    for number, line in enumerate(text.splitlines(), start=1):
        indent: int = len(line) - len(line.lstrip())
        if run_indent >= 0 and line.strip() and indent <= run_indent:
            run_indent = -1
        match = re.match(r"^(\s*)(?:-\s+)?run:\s*(.*)$", line)
        if match:
            run_indent = len(match.group(1))
        if run_indent >= 0 and re.search(r"\$\{\{\s*secrets\.", line):
            errors.append(f"{path}:{number}: secrets interpolated into a run: command line; pass them via env:")
    return errors


def main(argv: List[str]) -> int:
    """
    Check the given files (default: Makefile and the GitHub workflows) and report every leak.

    Args:
        argv (List[str]):
            Paths to check.

    Returns:
        int:
            0 when clean, 1 when at least one leak was found.
    """
    paths: List[Path] = [Path(arg) for arg in argv] or [
        Path("Makefile"),
        *sorted(Path(".github/workflows").glob("*.y*ml")),
    ]
    errors: List[str] = []
    for path in paths:
        text: str = path.read_text(encoding="utf-8")
        errors += check_workflow(path, text) if path.suffix in (".yml", ".yaml") else check_makefile(path, text)
    for error in errors:
        print(error)
    print(f"{len(errors)} release credential leak(s) in {len(paths)} file(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
