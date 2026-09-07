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

* cloning the devops-accounts repository and extracting the credentials
* creating and pushing the release branch
* creating and pushing the release tag
* creating the GitHub release

The variable for the GitHub Access Token is inside the Makefile, but the value is overwritten during
`make ondewo_release`, because it is passed from the devops-accounts repo as an argument to the actual `release` command.

## Automatic Release Process - Clients

Every available Client of this API can be released from this repository, to make the release process for major and minor changes easier.

The generic `release_client` command depends on 4 variables:

* `ONDEWO_T2S_API_VERSION` -- Current API version
* `GENERIC_CLIENT` -- specifies `SSH git link` to client-repository
* `RELEASEMD` -- position of `RELEASE.md` inside the client-repository
* `GENERIC_RELEASE_NOTES` -- template text of client release notes

To release every client, use `make release_all_clients`. The clients are released **in parallel** and are
isolated from one another: a failure in one client does not abort the others, and the summary at the end
reports each client as `RELEASED`, `SKIP` (already released) or `FAILED` (see `release_run_<client>.log`).

The generated client release notes are filed under `### Improvements` by default. For a breaking API
release, override the heading and describe the break:

```bash
make release_all_clients GENERIC_RELEASE_SECTION='Breaking Changes' \
  GENERIC_RELEASE_EXTRA='* <what broke> \n'
```

If a client's `RELEASE.md` already documents the version being released, the generated boilerplate is
skipped and the hand-curated entry is kept.

## Proto Documentation

The documentation for this, and all other APIs and their available versions, can be found on [ondewo.github.io](https://ondewo.github.io). For Offline usage, it can also be found in the `docs` folder.

`make update_githubio` publishes the generated `docs/` to the `ondewo.github.io` repository. It is a
`make` target — **not** a pre-commit hook — and it preemptively stops if:

* The command is not run on the `master` branch
* There already exists a version-object with the specified version in the `data.js` of the `ondewo.github.io` repository

> :warning:  This command is dependent on your installation of NPM and NodeJS -- Make sure to install both, or run `make setup_developer_environment_locally`
