r"""Reflow the proto comments protoc-gen-doc renders through its `p` filter: one source line per paragraph.

protoc-gen-doc's html template renders file, service, message and enum descriptions with `{{p .Description}}`,
whose filter splits on EVERY newline (`(\n|\r|\r\n)\s*`) and wraps each piece in <p>. A comment wrapped at ~120
characters therefore renders as one paragraph per source line, i.e. broken mid-sentence. Field, enum-value and
method descriptions are inserted raw (newlines are spaces), so they are left alone.

Usage: reflow_proto_docs.py [--check] FILE...
"""

import re
import sys
from typing import List, Tuple

DECL = re.compile(r"^\s*(message|enum|service)\s+\w+\s*\{")
SYNTAX = re.compile(r"^\s*syntax\s*=")
COMMENT = re.compile(r"^(\s*)//(.*)$")
P_TAG = re.compile(r"</?p>", re.IGNORECASE)


def paragraphs(texts: List[str]) -> Tuple[List[str], List[str]]:
    """Join a comment block's lines into paragraphs; return (paragraphs, problems)."""
    problems: List[str] = []
    joined = "\n".join(texts)
    # inside <pre> a newline must survive the filter: &#10; renders as one and is not split on
    joined = re.sub(
        r"<pre>.*?</pre>", lambda m: m.group(0).replace("\n", "&#10;"), joined, flags=re.IGNORECASE | re.DOTALL
    )
    # an explicit <p> or </p> is a paragraph boundary; the filter adds its own tags
    joined = P_TAG.sub("\n\n", joined)
    paras: List[str] = []
    for block in re.split(r"\n\s*\n", joined):
        words = " ".join(part.strip() for part in block.split("\n") if part.strip())
        if words:
            paras.append(words)
    return paras, problems


def reflow(lines: List[str]) -> Tuple[List[str], List[str]]:
    out: List[str] = []
    problems: List[str] = []
    i = 0
    while i < len(lines):
        m = COMMENT.match(lines[i])
        if not m:
            out.append(lines[i])
            i += 1
            continue
        j = i
        while j < len(lines) and COMMENT.match(lines[j]):
            j += 1
        block = lines[i:j]
        nxt = lines[j] if j < len(lines) else ""
        if DECL.match(nxt) or SYNTAX.match(nxt):
            indent = m.group(1)
            texts = [COMMENT.match(b).group(2) for b in block]  # type: ignore[union-attr]
            texts = [t[1:] if t.startswith(" ") else t for t in texts]
            paras, probs = paragraphs(texts)
            problems += [f"line {i + 1}: {p}" for p in probs]
            new: List[str] = []
            for k, para in enumerate(paras):
                if k:
                    new.append(f"{indent}//")
                new.append(f"{indent}// {para}")
            out += new
        else:
            out += block
        i = j
    return out, problems


def main() -> int:
    check = "--check" in sys.argv
    files = [a for a in sys.argv[1:] if a != "--check"]
    changed = 0
    for path in files:
        src = open(path, encoding="utf-8").read().split("\n")
        new, problems = reflow(src)
        for p in problems:
            print(f"{path}: {p}")
        if new != src:
            changed += 1
            if check:
                print(f"{path}: a file/service/message/enum description wraps a paragraph across lines")
            else:
                open(path, "w", encoding="utf-8").write("\n".join(new))
    return 1 if (check and changed) else 0


if __name__ == "__main__":
    sys.exit(main())
