# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Working Principles

Behavioral guidelines to reduce common mistakes. They bias toward caution over speed; for trivial tasks, use judgment.

### Think before coding

Don't assume. Don't hide confusion. Surface tradeoffs.

Before implementing:

- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### Simplicity first

Minimum code that solves the problem. Nothing speculative.

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### Surgical changes

Touch only what you must. Clean up only your own mess.

When editing existing code:

- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it — don't delete it.

When your changes create orphans:

- Remove imports/variables/functions that _your_ changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: every changed line should trace directly to the user's request.

### Goal-driven execution

Define success criteria. Loop until verified.

Transform tasks into verifiable goals:

- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:

```text
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

These guidelines are working if: fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and
clarifying questions come before implementation rather than after mistakes.

## Logging

```python
from loguru import logger as log
```

- **Levels:** `log.trace()`, `log.debug()`, `log.info()`, `log.warning()`, `log.error()`, `log.exception()`. Choose by
  hotness/verbosity — `trace` for per-token / hot-path detail, `debug` for routine method entry/exit, `info` for notable
  lifecycle events, `warning` / `error` / `exception` for problems.
- **Interpolate with f-strings, not loguru's `{}` positional args.** Consistent with the Code Style rule, use
  `f"…{value}"`; only add the `f` prefix when the string actually interpolates (`"START: …"` with no params stays a
  plain string).
- **`START:` / `DONE:` bracketing.** Wrap a method (or other notable operation) with a `START:` line at entry and a
  `DONE:` line at exit, both naming `ClassName: method_name` (append `: param={value}` context where useful):

  ```python
  log.debug("START: IntentBertClassifier: predict")
  ...
  log.debug(f"DONE: IntentBertClassifier: predict. Elapsed time: {perf_counter() - start_time:.5f}")
  ```

- **Timing uses `perf_counter()`, rendered `:.5f`.** Measure elapsed time with `time.perf_counter()` captured as a start
  value and subtracted at the `DONE:` line; always format the elapsed value with the `:.5f` spec:

  ```python
  from time import perf_counter

  start_time: float = perf_counter()
  ...
  log.info(f"DONE: SESSION SERVICER: DetectIntent. Elapsed time: {perf_counter() - start_time:.5f}")
  ```

  Never measure a duration with `time.time()` — reserve `time.time()` for wall-clock timestamps (epoch seconds persisted
  to a DB / proto, unique-id or filename stamps). `perf_counter()` has an undefined epoch and must not be stored or
  compared across processes.

## Docstrings

Google-style, triple double-quotes:

```python
"""
Short imperative summary line.

Args:
    param_name (type):
        Description of the parameter.

Returns:
    type:
        Description of the return value.

Raises:
    ExceptionType:
        When this exception is raised.
"""
```

## Git Commits

- **Never include Claude as author or co-author** in commit messages, PR descriptions, or any other text. Do not add
  `Co-Authored-By: Claude…` trailers, "Generated with Claude Code" footers, or any similar attribution.
- The user's own git author identity (already configured in git) is the only identity that should appear on commits.
- This rule overrides the default Claude Code commit-template guidance.
- **Never prepend the JIRA ticket ID** (e.g. `[OND211-2386]`) to the commit subject yourself. The `giticket` pre-commit
  hook reads the ticket from the branch name (`(feature|bugfix|support|hotfix)/<TICKET>-…`) and prepends `[<ticket>]`
  (with a trailing space) automatically. Writing the prefix manually produces a duplicate like
  `[OND211-2386] [OND211-2386] feat: …`. Write the subject as plain Conventional Commits (`feat: …`, `fix(scope): …`,
  `docs(types): …`) and let the hook add the prefix on commit.

## General Principles

- Follow existing patterns before introducing new abstractions.
- Keep changes minimal and consistent with surrounding code.
- Validate inputs early with descriptive, context-rich error messages.
- Use context managers for files, sockets, and thread pools.
- Prefer region comments for grouping methods in files that already use them.
- End edited Markdown and YAML files with a trailing newline.

## Client-release orchestration (`release_all_clients`)

- It **fails loudly** on a genuine client-release error: the piped sub-make runs under `bash -c 'set -o pipefail; make -C … | tee …'` (a plain sh pipe returns tee's 0 and masks failures), and a **marker file** distinguishes an "already released" SKIP from a real FAILURE (make flattens recipe exit codes to 2, so the code alone can't tell them apart). Do not regress either.
- Every token-bearing recipe line is `@`-prefixed so make never echoes a secret — `docker run -e <TOKEN>`, `echo $(TOKEN) | gh auth`, `twine … -p${PYPI_PASSWORD}`, and the credential sub-make `make release $(info)` (which expands the token at runtime and is easy to miss).

## Pre-commit upgraded (language-agnostic hook set)

Pre-commit here uses only the language-agnostic hooks — **markdownlint-cli2, pre-commit-hooks hygiene, giticket, conventional-pre-commit** — no ruff/mypy/uv (there is no Python). Generated docs (`docs/`) and any generated code are excluded via the top-level `exclude:`.

- **markdownlint MD053 is disabled** (its auto-fix deletes `[comment]: <>` reference-definition markers).
- **markdownlint RELEASE.md reformatting is content-safe**: it only strips trailing whitespace and adds blank lines around headings — the `## Release … <VERSION>` headings and `*****` separators that `ondewo_release` greps for remain intact. (Confirmed: the 6.5.0 release notes sliced correctly after the reformat.)

## GitHub Actions — the documentation workflow is a required gate

`.github/workflows/generate-doc-and-deploy.yaml` ("Generate API Documentation") is the only CI this repository has,
and it is a **required gate, not advisory**: it runs on every push and every pull request against `master` (plus
manual `workflow_dispatch`), and its last step writes generated documentation back into `master`. Treat a red run as
a blocked merge.

**The file is `.yaml`, not `.yml`** — a `.github/workflows/*.yml` glob matches nothing here and reads as "this repo
has no CI".

The single job (`generate-doc-and-deploy`, `ubuntu-latest`) declares exactly three steps:

1. **`Checkout 🛎️`** — `actions/checkout@v5` with `submodules: true`. There is no `.gitmodules`, so the submodule
   flag is a no-op today; do not read it as evidence that a submodule exists.
2. **`Generate documentation from ONDEWO proto files 🔧`** — `ondewo/ondewo-protoc-gen-doc-action@master`, a Docker
   action built `FROM pseudomuto/protoc-gen-doc`. Once per output format it runs
   `protoc -I. -Igoogleapis --doc_opt=/resources/templates/<format>.tmpl,index.<format> --doc_out=docs` over
   `$(find ondewo -name '*.proto' | sort)`.
3. **`Deploy 🚀`** — `JamesIves/github-pages-deploy-action@v4` with `branch: master`, `folder: docs`,
   `target-folder: docs`, guarded by `if: ${{ !env.ACT }}` so a local `act` run skips it.

### Reproducing it locally

`make build_docs` **is** step 2 — same action repository, same image, same arguments — so use it rather than
approximating:

```bash
make build_docs               # clone + docker build + docker run, exactly as CI does
git diff --exit-code docs/    # THE gate: regenerated docs must match what is committed
make clean_docs_builder
```

Three fidelity rules, each of which silently changes the result if broken:

- **Build the image from `ondewo/ondewo-protoc-gen-doc-action@master`; never substitute a locally installed `protoc`
  plus `protoc-gen-doc`.** The output is rendered by that repository's `resources/templates/{html,md}.tmpl`, so a
  stock protoc-gen-doc emits different Markdown and HTML and the `git diff` above degenerates into noise that hides
  a genuinely stale `docs/`.
- **Pass exactly `html,md index`.** The workflow supplies no `with:` block, so `action.yaml`'s defaults
  (`formats: html,md`, `filename: index`) are what CI actually uses.
- **Keep `--user "$(id -u):$(id -g)"` on the `docker run`.** CI runs the container as root and then throws the runner
  away; locally, dropping it leaves root-owned files in your `docs/` that you cannot subsequently rewrite.

### Sharp edges found while actually running this

- **The gate is convergence, not exit status.** Step 2 exits `0` whatever the proto contains — what a reviewer
  catches is `docs/` disagreeing with `ondewo/t2s/text-to-speech.proto`. Always finish with
  `git diff --exit-code docs/`.
- **A stale `docs/` makes CI commit to `master`.** Step 3 pushes the regenerated folder back as
  `Deploying to master from @ ondewo/ondewo-t2s-api@<sha> 🚀`. Those commits are **authored as the human who pushed**,
  not as a bot, so searching history for a bot account will not find them. Regenerate and commit `docs/` in the same
  commit as any `.proto` change, and CI is left with nothing to write.
- **`googleapis: warning: directory does not exist.`, printed once per format, is expected and benign.** The action's
  entrypoint hardcodes `-Igoogleapis` and this repository has no such directory; the proto imports only
  `google/protobuf/empty.proto` and `google/protobuf/struct.proto`, which ship inside protoc. Adding a
  `google/api/*` import would turn that warning into a hard failure with no include path available to satisfy it.
- **`make build_docs` clones into `.tmp-protoc-gen-doc-action/`, which is not in `.gitignore`**, so it lingers as an
  untracked directory. `make clean_docs_builder` removes it — do not `git add -A` in between.
- **The action is pinned to a moving ref (`@master`).** Generated documentation can therefore change with no commit
  in this repository at all, so an unexplained `docs/` diff may be an upstream template change rather than your edit.
- **There is no Python gate here** — no `pyproject.toml`, no `uv.lock`, no ruff, mypy, pytest or coverage threshold.
  Do not go hunting for a `uv run --frozen …` equivalent; the pre-commit hooks (markdownlint, hygiene, giticket,
  conventional-pre-commit) are language-agnostic and are **not** part of this workflow.
