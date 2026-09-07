# How to become a contributor and submit your own code

## Contributor License Agreements

We'd love to accept your sample apps and patches! Before we can take them, we
have to jump a couple of legal hurdles.

Please fill out either the individual or corporate Contributor License Agreement
(CLA).

* If you are an individual writing original source code and you're sure you
    own the intellectual property, then you'll need to sign an [individual CLA](TODO:).
* If you work for a company that wants to allow you to contribute your work,
    then you'll need to sign a [corporate CLA](TODO:).

Follow either of the two links above to access the appropriate CLA and
instructions for how to sign and return it. Once we receive it, we'll be able to
accept your pull requests.

## Contributing A Patch

1. Submit an issue describing your proposed change to the repo in question.
1. The repo owner will respond to your issue promptly.
1. If your proposed change is accepted, and you haven't already done so, sign a
   Contributor License Agreement (see details above).
1. Fork the desired repo, develop and test your code changes.
1. Ensure that your change adheres to the existing style of the file you are
   editing.
1. Submit a pull request.

## Changing this API

This repository holds one hand-written source file, `ondewo/t2s/text-to-speech.proto`; everything under
`docs/` is generated from it. There is no Python, Node or Go code here and therefore no test suite and no
coverage gate — the checks that do apply are:

1. **Regenerate the documentation in the same commit as the proto change.**

   ```bash
   make build_docs && git diff --exit-code docs/ ; make clean_docs_builder
   ```

   The `Generate API Documentation` workflow runs the same container on every push and pull request against
   `master` and commits the result back to `master`. Leaving `docs/` stale does not turn CI red — it makes CI
   write a follow-up commit — so treat `git diff --exit-code docs/` as the real gate.

1. **Run the hooks.** `uvx pre-commit run --all-files` must be clean. `markdownlint-cli2` auto-fixes
   Markdown, so re-stage anything it rewrites.

1. **Write plain Conventional Commits subjects** (`feat:`, `fix(scope):`, `docs:`, `chore:`). Never type the
   JIRA ticket yourself: on a `feature|bugfix|support|hotfix/OND###-####-…` branch the `giticket` hook
   prepends `[OND###-####]` for you, and it runs *after* `conventional-pre-commit` precisely so that its
   rewrite is not re-validated.

1. **Bump the version and add a `RELEASE.md` entry** for a release, keeping the
   `## Release ONDEWO T2S API <VERSION>` heading and the closing `*****************` separator intact — the
   `Makefile` slices the GitHub release body out of them.
