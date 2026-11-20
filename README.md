<p align="center">
    <a href="https://www.ondewo.com">
      <img alt="ONDEWO Logo" src="https://raw.githubusercontent.com/ondewo/ondewo-logos/master/github/ondewo_logo_github_2.png"/>
    </a>
</p>

# ONDEWO T2S APIs

This repository contains the original interface definitions of public ONDEWO APIs that support gRPC protocols. Reading the original interface definitions can provide a better understanding of ONDEWO APIs and help you to utilize them more efficiently. You can also use these definitions with open source tools to generate client libraries, documentation, and other artifacts.

The API documentation is generated from `ondewo/t2s/text-to-speech.proto` by the `Generate API Documentation`
workflow, in two formats:

* [html](https://ondewo.github.io/ondewo-t2s-api)
* [markdown](docs/index.md)

The core components of all the client libraries are built directly from files in this repo using [the proto compiler.](https://github.com/ondewo/ondewo-proto-compiler)

For an end-user, the APIs in this repo function mostly as documentation for the endpoints. For specific implementations, look in the following repos for working implementations:

* [Python](https://github.com/ondewo/ondewo-t2s-client-python)
* [Angular](https://github.com/ondewo/ondewo-t2s-client-angular)
* [JavaScript](https://github.com/ondewo/ondewo-t2s-client-js)
* [TypeScript](https://github.com/ondewo/ondewo-t2s-client-typescript)
* [NodeJS](https://github.com/ondewo/ondewo-t2s-client-nodejs)
* [C++](https://github.com/ondewo/ondewo-t2s-client-cpp)
* [C#](https://github.com/ondewo/ondewo-t2s-client-csharp)
* [Go](https://github.com/ondewo/ondewo-t2s-client-go)
* [Java](https://github.com/ondewo/ondewo-t2s-client-java)
* [PHP](https://github.com/ondewo/ondewo-t2s-client-php)
* [Rust](https://github.com/ondewo/ondewo-t2s-client-rust)

Please note that some of these implementations are works-in-progress. The repo will make clear the status of the implementation.

## Overview

ONDEWO APIs use [Protocol Buffers](https://github.com/google/protobuf) version 3 (proto3) as their Interface Definition Language (IDL) to define the API interface and the structure of the payload messages. The same interface definition is used for gRPC versions of the API in all languages.

There are several ways of accessing APIs:

1. Protocol Buffers over gRPC: You can access APIs published in this repository through [GRPC](https://github.com/grpc), which is a high-performance binary RPC protocol over HTTP/2. It offers many useful features, including request/response multiplex and full-duplex streaming.

2. ONDEWO Client Libraries:
You can use these libraries to access ONDEWO Cloud APIs. They are based on gRPC for better performance and provide idiomatic client surface for better developer experience.

## Discussions

Please use the issue tracker in this repo for discussions about this API, or the issue tracker in the relevant client if it is language-specific.

## Repository Structure

```bash
.
├── .github
│   └── workflows
│       └── generate-doc-and-deploy.yaml   # the only CI: regenerates and deploys docs/
├── .markdownlint-cli2.yaml
├── .pre-commit-config.yaml
├── CLAUDE.md
├── CONTRIBUTING.md
├── Dockerfile.utils
├── docs                                   # GENERATED — never hand-edit
│   ├── index.html
│   ├── index.md
│   └── style.css
├── install_nvm.sh
├── LICENSE
├── Makefile
├── ondewo
│   └── t2s
│       └── text-to-speech.proto           # the single source of truth
├── README.md
└── RELEASE.md
```

There is no Python, Node or Go source here: the only hand-written artefacts are the `.proto`, the Markdown
docs and the `Makefile`.

## Local Development

```bash
make setup_developer_environment_locally   # pre-commit hooks + nvm/node
uvx pre-commit run --all-files             # the full hook set (markdownlint + hygiene)
make build_docs                            # regenerate docs/ with the exact CI image
git diff --exit-code docs/                 # docs/ must match the proto — this is the gate
make clean_docs_builder                    # remove .tmp-protoc-gen-doc-action + the local image
```

`conventional-pre-commit` is declared **before** `giticket` in `.pre-commit-config.yaml` and the order is
load-bearing: giticket rewrites the subject to `[<TICKET>] <subject>`, which is no longer a valid
Conventional Commit, so with the order reversed every commit on a `feature/OND…` branch is rejected. Write
plain Conventional Commits subjects and let giticket add the ticket prefix.

## Generate gRPC Source Code

API client libraries can be built directly from files in this repo using [the proto compiler.](https://github.com/ondewo/ondewo-proto-compiler)

## Automatic Release Process

The entire process is automated to make development easier. The actual steps are simple:

TODOs after Pull Request was merged in:

* Checkout master:
    >git checkout master
* Pull the new stuff:
    >git pull
* (If not already, run the `setup_developer_environment_locally` command):
   >make setup_developer_environment_locally
* Update the `ONDEWO_T2S_API_VERSION` in the `Makefile`
* Add the new Release Notes in `RELEASE.md` in the format:

   ```markdown
   ## Release ONDEWO T2S API X.X.X        <---- Beginning of Notes

      ...<NOTES>...

   *****************                      <---- End of Notes
   ```

   The heading and the trailing `*****************` are both parsed by `CURRENT_RELEASE_NOTES` in the
   `Makefile`, which slices the entry for `gh release create`. Keep both exactly as shown.

* `Commit and push` the changes made in `RELEASE.md` and `Makefile`
* Release:
   >make ondewo_release

---
The `make ondewo_release` command can be divided into 4 steps:

* checking that the version is new and `RELEASE.md` has notes for it (`spc`)
* reading the GitHub token from a temporary devops-accounts clone (`scripts/with_devops_accounts.sh`), which is
  deleted before the release runs
* creating and pushing the release branch and the release tag
* creating the GitHub release

The token reaches `make release` through its environment, never as a command-line argument.

## Automatic Release Process - Clients

All eleven `ondewo-t2s-client-<language>` SDKs (`CLIENTS` in the Makefile: python nodejs typescript
angular js cpp csharp go java php rust) are released from this repository, after the API itself, by
`scripts/release_client.sh`.

```bash
make preflight_all_clients           # read-only: every client's preflight, serially
make release_all_clients             # preflight_all_clients, then all clients in parallel
make release_python_client           # one client (likewise release_<language>_client)
make preflight_python_client         # one client's preflight (likewise preflight_<language>_client)
make check_proto_compiler_is_latest  # optional: is ONDEWO_PROTO_COMPILER_VERSION the newest compiler tag?
```

What `release_all_clients` does:

1. Clones ondewo-devops-accounts **once** into a private `mktemp -d` directory outside every
   repository (`scripts/with_devops_accounts.sh`) and hands each client its own copy as
   `DEVOPS_ACCOUNT_DIR`; every copy and the clone are deleted on every exit path, Ctrl-C included.
2. Runs `preflight_all_clients`. **A single failing preflight stops the run before any client is
   released.**
3. Releases the clients in parallel, each into a fresh `release_run_<language>.log` (mode 600), and prints a
   summary: `RELEASED`, `SKIP` (already released and verified), `INCOMPLETE` (a half-finished release),
   `UNKNOWN` (GitHub would not say) or `FAILED`. One failing client does not abort the others; the run fails
   unless every client is `RELEASED` or `SKIP`.

For every client, in preflight and release alike, the driver clones the client, inserts the generated
release notes into its `RELEASE.md` (`src/RELEASE.md` for nodejs, typescript, angular and js) unless it
already documents the version under `## Release ONDEWO T2S <Name> Client <version>` (`<Name>` is the
capitalised language, except `C++` and `PHP`), and rewrites the anchored `ONDEWO_T2S_VERSION=`,
`ONDEWO_PROTO_COMPILER_GIT_BRANCH=tags/<ONDEWO_PROTO_COMPILER_VERSION>` and `(ONDEWO_)T2S_API_GIT_BRANCH=`
assignments of its Makefile.

A client that implements the release contract (`release_preflight` and `release_verify`, read-only, next
to `ondewo_release`) is handled like the ondewo-sip-api clients:

| On the client's origin | Result |
| --- | --- |
| tag `<version>` and `release_verify` passes | **SKIP**: already released and verified |
| tag `<version>` but `release_verify` fails | **INCOMPLETE**: a half-finished release; finish it by hand |
| branch `release/<version>` but no tag | **INCOMPLETE**: a half-finished release; finish or undo it by hand |
| neither | preflight: `release_preflight`; release: `ondewo_release`, then `release_verify` |

No T2S client implements the contract yet: each has only `ondewo_release`. Such a **legacy** client is
released through its `ondewo_release` exactly as before, and the driver checks the tag on origin and the
published GitHub release (one unauthenticated call to the GitHub REST API) instead:

| On the client's origin / GitHub | Result |
| --- | --- |
| tag `<version>` and a published GitHub release `<version>` | **SKIP** |
| tag or `release/<version>` branch, no GitHub release (HTTP 404) | **INCOMPLETE** |
| tag or branch, the GitHub API does not answer (403/429 rate limit, 000) | **UNKNOWN**; nothing is changed |
| neither | preflight: passes with a `LEGACY` warning; release: `ondewo_release`, then the tag + GitHub release check |

A client with only one of the two contract targets fails. The client clone is removed on every exit path;
files a client container wrote as root are removed through a digest-pinned busybox container, never `sudo`.

The generated client release notes are filed under `### Improvements` by default. For a breaking API
release, override the heading and describe the break:

```bash
make release_all_clients GENERIC_RELEASE_SECTION='Breaking Changes' \
  GENERIC_RELEASE_EXTRA='* <what broke>\n'
```

The proto compiler is pinned exactly in `ONDEWO_PROTO_COMPILER_VERSION`; move it deliberately.

**Host requirements:** git (with SSH access to GitHub and Bitbucket), make, perl, bash, curl and docker,
plus whatever each client's own release documents. The behaviour above is tested against fake client
repositories by `python3 scripts/test_release_driver.py` (also run by the `Release credential hygiene`
workflow).

## Proto Documentation

The documentation for this, and all other APIs and their available versions, can be found on [ondewo.github.io](https://ondewo.github.io). For Offline usage, it can also be found in the `docs` folder.

`make update_githubio` publishes the generated `docs/` to the `ondewo.github.io` repository. It is a
`make` target — **not** a pre-commit hook — and it preemptively stops if:

* The command is not run on the `master` branch
* There already exists a version-object with the specified version in the `data.js` of the `ondewo.github.io` repository

> :warning:  This command is dependent on your installation of NPM and NodeJS -- Make sure to install both, or run `make setup_developer_environment_locally`
