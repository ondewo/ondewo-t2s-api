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

## No Python, no tests, no coverage gate

`git ls-files` returns **16 files**: one `.proto`, three generated files under `docs/`, five Markdown docs,
the `Makefile`, `Dockerfile.utils`, `install_nvm.sh`, `LICENSE`, two config files and one workflow. There is
no `pyproject.toml`, no `uv.lock`, no `package.json`, no `.py`/`.ts`/`.js` file and no test directory, so the
fleet-wide loguru/docstring/pytest conventions have nothing to apply to here and the honest answer to "what
is the coverage?" is **not applicable — there is no executable code**. Do not invent a coverage gate, and do
not go looking for a `uv run --frozen …` equivalent.

The one convergence check that does exist is `git diff --exit-code docs/` after `make build_docs` (below).

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

## Pre-commit (language-agnostic hook set)

Only language-agnostic hooks — **markdownlint-cli2, pre-commit-hooks hygiene, conventional-pre-commit,
giticket** — no ruff/mypy/uv, because there is no Python. `docs/` is excluded via the top-level `exclude:`
so no hook rewrites generated output.

Run it as **`uvx pre-commit run --all-files`** (there is no `pre-commit` on `PATH`, and unlike the two
client-python repos nothing here is `language: system`, so `uvx` is sufficient — no `uv run --frozen`
needed). It exits 0 on a clean tree.

**Hook order is load-bearing: `conventional-pre-commit` MUST be declared before `giticket`.** Both are
`commit-msg`-stage hooks and pre-commit runs them in declaration order. giticket rewrites the subject to
`[OND232-835] feat: …`, which conventional-pre-commit rejects (it has no ticket-prefix option), so with the
order reversed _every_ commit on a `feature|bugfix|support|hotfix/OND###-####-…` branch fails. Measured on a
throwaway repo with this repo's config:

- giticket first → `giticket Passed` → `Conventional Commit Failed`, `[Bad commit message] >> [OND232-835]
  feat: a valid conventional subject`, nothing committed.
- conventional first → `Conventional Commit Passed` → `giticket Passed` → committed as
  `[OND232-835] feat: a valid conventional subject`.

It was invisible before only because recent work happened on `master`, where giticket's regex does not match.

Hook revs, each resolved with `git ls-remote --tags --refs … | sort -V`. Do not "upgrade" the last three —
they are already at their ceiling:

| hook | rev | note |
| --- | --- | --- |
| `DavidAnson/markdownlint-cli2` | `v0.23.2` | newest stable; upgraded from `v0.23.0` and it reformatted nothing here |
| `pre-commit/pre-commit-hooks` | `v6.0.0` | already newest |
| `compilerla/conventional-pre-commit` | `v4.4.0` | already newest **stable**; anything sorting later is a `-preN` pre-release of an already-released version — reject it |
| `milin/giticket` | `'1.92'` | already newest; `1.92`, `v1.92` and `master` are all commit `29a1ece`. **Keep the quotes** — unquoted `1.92` is a YAML float |

- **markdownlint `MD053` is disabled** in `.markdownlint-cli2.yaml` and must stay disabled: its auto-fix
  deletes `[comment]: <>` reference-definition markers that the release tooling greps for.
- **markdownlint RELEASE.md reformatting is content-safe**: it only strips trailing whitespace and adds blank
  lines around headings — the `## Release … <VERSION>` headings and `*****` separators that `ondewo_release`
  greps for remain intact. (Confirmed: every entry from 3.0.0 to 6.6.0 still slices to its `*****`
  terminator.)
- **giticket crashes, rather than failing cleanly, on an unborn `HEAD`** (`git rev-parse --abbrev-ref HEAD`
  exits 128 → a `CalledProcessError` traceback). This only bites when probing the hooks in a fresh
  `git init` scratch repo: make an initial `--no-verify` commit first.

## Release Makefile — the three things that silently corrupt a release

1. **`CURRENT_RELEASE_NOTES` terminates on `/^\*{5}/`, never on `/\*\*/`.** The old pattern matched the first
   inline markdown **bold** span inside the entry and truncated the GitHub release body there, and
   `gh release create -n "$(CURRENT_RELEASE_NOTES)"` reports no error for a short body. Proven: append a
   bullet after 6.6.0's `* **Try run of the CI/CD release flow.**` line and the old pattern drops it while
   the new one keeps it through the `*****` separator.
2. **`release_client` inserts the generated boilerplate only when the client does not already document the
   version.** Without that guard, a client whose `RELEASE.md` was curated by hand gets a second
   `## Release ONDEWO T2S <Name> Client <VERSION>` heading, which buries the curated entry (the notes slice
   takes the first match) and trips the client's own markdownlint MD024/MD025 — neither auto-fixes, so the
   client's pre-commit aborts the release.
   The guard's regex ends `[[:space:]]*$$`, **not** the bare `$$` that `ondewo-nlu-api` uses: the generated
   heading is emitted with a trailing space, so the committed headings in the nodejs / typescript / angular /
   js clients all carry one, and a bare `$$` matches only the python client — i.e. it fails open for four of
   the five.
3. **`GENERIC_RELEASE_SECTION` / `GENERIC_RELEASE_EXTRA`** drive the client release-note heading, so a
   breaking API bump does not publish five client majors under "Improvements":
   `make release_all_clients GENERIC_RELEASE_SECTION='Breaking Changes' GENERIC_RELEASE_EXTRA='* … \n'`.

Verify any change to these with `make TEST` (prints the sliced notes, masks the token) and
`make -n release_client GENERIC_CLIENT=… RELEASEMD=…` — the dry run expands the whole recipe without cloning
anything. Note the dry run still executes `release_client`'s `$(eval … $(shell curl …))` (see below).

## Proto-compiler: no submodule here, and no pin to bump

There is no `.gitmodules` and no `ONDEWO_PROTO_COMPILER_GIT_BRANCH` variable in this repo — those live in the
five client repos. What this repo does is _push_ a version into them: `release_client` runs

```make
$(eval PROTO_COMPILER:= $(shell curl https://api.github.com/repos/ondewo/ondewo-proto-compiler/tags | grep "\"name\"" | head -1 | cut -d '"' -f 4))
```

and rewrites the cloned client's `ONDEWO_PROTO_COMPILER_GIT_BRANCH=tags/${PROTO_COMPILER}`. It resolves to
**5.14.0** today (verified against the live API, whose listing comes back newest-first). It is a `head -1` of
GitHub's tag listing, not a semver sort, so an out-of-band tag would be picked up blindly.

Bumping the compiler is therefore a **client-repo** change (move the submodule gitlink to the tag's peeled
commit + set that Makefile variable) and it never regenerates stubs on its own. Do not write "regenerated
with proto-compiler X" into a `RELEASE.md` entry unless `make build` actually ran in that client.

## Makefile targets that were removed, and why they are not coming back

`install_python_requirements` (and with it the `flake8` and `mypy` targets, plus the `.flake8` / `mypy.ini` /
`requirements*.txt` entries in `.gitignore`) is gone. It `wget`-ed four files from
`ondewo-t2s-client-python/master` — `requirements.txt`, `requirements-dev.txt`, `.flake8`, `mypy.ini` — and
**all four now 404** because that repo moved to `uv` + `pyproject.toml`. `wget -q -O <file>` on a 404 leaves
an empty file and exits non-zero, so it took `setup_developer_environment_locally` down with it. The
prerequisite had to be dropped in the same edit as the target: deleting one without the other turns a recipe
failure into a make _parse_ failure and kills `install_precommit_hooks` too.

## GitHub Actions — the documentation workflow is a required gate

`.github/workflows/generate-doc-and-deploy.yaml` ("Generate API Documentation") is the only CI this repository has,
and it is a **required gate, not advisory**: it runs on every push and every pull request against `master` (plus
manual `workflow_dispatch`), and its last step writes generated documentation back into `master`. Treat a red run as
a blocked merge.

**The workflow declares no `run:` blocks** — all three steps are `uses:` — so "run the CI commands locally"
means building and running the Docker action yourself (see below), not copying shell out of the YAML.

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

To prove the gate against a _clean_ tree — so an uncommitted edit cannot fake a green run — generate from a
`git archive` export instead. This is the form last run here; step 2 exited 0 and all three files came back
byte-identical:

```bash
git clone --depth 1 https://github.com/ondewo/ondewo-protoc-gen-doc-action.git /tmp/gendoc-action
docker build -t local/ondewo-protoc-gen-doc-action:t2s /tmp/gendoc-action
WS=/tmp/gendoc-ws && rm -rf "$WS" && mkdir -p "$WS"
git archive HEAD | tar -x -C "$WS" && rm -rf "$WS/docs"
docker run --rm -v "$WS":/github/workspace -w /github/workspace --user "$(id -u):$(id -g)" \
  local/ondewo-protoc-gen-doc-action:t2s html,md index    # must exit 0; do NOT pipe into `tail`, it eats the code
diff -q docs/index.html "$WS/docs/index.html" && diff -q docs/index.md "$WS/docs/index.md" \
  && diff -q docs/style.css "$WS/docs/style.css"
```

Rebuild the image every time. The action is referenced `@master` and its own base image is untagged
(`FROM pseudomuto/protoc-gen-doc`), so a stale local image is the one way this check goes green while CI does
not.

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
- **`make build_docs` clones into `.tmp-protoc-gen-doc-action/` and leaves it behind.** It is now listed in
  `.gitignore` (it was not, and a `git add -A` in between would have committed the whole clone), but still
  finish with `make clean_docs_builder`, which also drops the `ondewo-protoc-gen-doc:local` image.
- **The action is pinned to a moving ref (`@master`).** Generated documentation can therefore change with no commit
  in this repository at all, so an unexplained `docs/` diff may be an upstream template change rather than your edit.
- **The pre-commit hooks are not part of this workflow.** Nothing in CI runs markdownlint, giticket or
  conventional-pre-commit; a red `uvx pre-commit run --all-files` is therefore invisible to GitHub and has to
  be caught locally.
