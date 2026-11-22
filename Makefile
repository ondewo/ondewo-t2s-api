# There is deliberately NO bare `export` here. It exported EVERY variable of this file into every recipe,
# and so into each client's `ondewo_release` (including the GITHUB_GH_TOKEN placeholder and a relative
# DEVOPS_ACCOUNT_DIR). A recipe that needs a value from the environment gets it from the environment it was
# started with; the client release scripts hand each client only DEVOPS_ACCOUNT_DIR.
# ---------------- BEFORE RELEASE ----------------
# 1 - Update Version Number
# 2 - Update RELEASE.md
# 3 - Commit and push both
# -------------- Release Process Steps (make ondewo_release) --------------
# 1 - spc: branch and tag are new (locally and on origin), RELEASE.md has notes for the version
# 2 - Get the GitHub token from a temporary devops-accounts clone, delete the clone
# 3 - create the release branch and the tag, create the GitHub release

########################################################
# 		Variables
########################################################

# MUST BE THE SAME AS API in Mayor and Minor Version Number
# example: API 2.9.0 --> Client 2.9.X
ONDEWO_T2S_API_VERSION=6.8.0

# You need to setup an access token at https://github.com/settings/tokens - permissions are important
GITHUB_GH_TOKEN?=ENTER_YOUR_TOKEN_HERE

# Terminate on the ***** separator that actually delimits release entries, NOT on /\*\*/ - that matched the
# first inline markdown **bold** span INSIDE the entry and silently truncated the notes there, with no error
# from `gh release create -n "$(CURRENT_RELEASE_NOTES)"`. Measured on a scratch copy of this RELEASE.md with
# one bold bullet added to the 5.4.0 entry: old pattern 5 lines, new pattern 8. Safe because every separator
# in RELEASE.md is a run of exactly 17 asterisks (12 of them), so /^\*{5}/ can only match a separator.
#
# The opening heading is ANCHORED and the version quoted (\Q..\E): unanchored, `5.5.1` also opened the
# range on a `5.5.10` heading (and on any line merely mentioning the heading text), and its dots matched
# any character.
CURRENT_RELEASE_NOTES=`cat RELEASE.md \
	| perl -ne 'print if /^\#+ Release ONDEWO T2S API \Q${ONDEWO_T2S_API_VERSION}\E$$/../^\*{5}/'`

GH_REPO="https://github.com/ondewo/ondewo-t2s-api"
DEVOPS_ACCOUNT_GIT=ondewo-devops-accounts
# scripts/with_devops_accounts.sh clones this ONCE per run into `mktemp -d` and removes it on every exit path.
DEVOPS_ACCOUNT_GIT_URL?=git@bitbucket.org:ondewo/${DEVOPS_ACCOUNT_GIT}.git
IMAGE_UTILS_NAME=ondewo-t2s-api-utils:${ONDEWO_T2S_API_VERSION}
.DEFAULT_GOAL := help

########################################################
#       ONDEWO Standard Make Targets
########################################################

setup_developer_environment_locally: install_precommit_hooks install_nvm ## Sets up local development environment !! Forcefully closes current terminal

install_nvm: ## Install NVM, node and npm !! Forcefully closes current terminal
	@curl https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash
	@sh install_nvm.sh
	$(eval PID:=$(shell ps -ft $(ps | tail -1 | cut -c 8-13) | head -2 | tail -1 | cut -c 1-8))
	@node --version & npm --version || (kill -KILL ${PID})

install_precommit_hooks: ## Installs pre-commit hooks and sets them up for the repo
	pip install pre-commit
	pre-commit install
	pre-commit install --hook-type commit-msg

precommit_hooks_run_all_files: ## Runs all pre-commit hooks on all files and not just the changed ones
	pre-commit run --all-file

help: ## Print usage info about help targets
	# (first comment after target starting with double hashes ##)
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-40s\033[0m %s\n", $$1, $$2}'

makefile_chapters: ## Shows all sections of Makefile
	@echo `cat Makefile| grep "########################################################" -A 1 | grep -v "########################################################"`

build_docs: ## Build documentation locally using the same Docker image as CI/CD
	@echo "Building documentation using ondewo-protoc-gen-doc-action..."
	@if [ ! -d ".tmp-protoc-gen-doc-action" ]; then \
		echo "Cloning ondewo-protoc-gen-doc-action..."; \
		git clone --depth 1 https://github.com/ondewo/ondewo-protoc-gen-doc-action.git .tmp-protoc-gen-doc-action; \
	fi
	@echo "Building Docker image with ONDEWO templates..."
	@docker build -t ondewo-protoc-gen-doc:local .tmp-protoc-gen-doc-action
	@echo "Generating documentation..."
	@docker run --rm \
		--user "$(shell id -u):$(shell id -g)" \
		-v "$(shell pwd):/workspace" \
		-w /workspace \
		ondewo-protoc-gen-doc:local \
		html,md index
	@echo "✓ Documentation generated in docs/ directory"
	@echo "  Open docs/index.html in your browser to view"

clean_docs_builder: ## Remove the cloned protoc-gen-doc-action repo and Docker image
	@echo "Cleaning up documentation builder..."
	@rm -rf .tmp-protoc-gen-doc-action
	@docker rmi ondewo-protoc-gen-doc:local 2>/dev/null || true
	@echo "✓ Cleanup complete"

TEST:
	@echo "----------------------------------------------\nGITHUB_GH_TOKEN\n----------------------------------------------\n$(if $(GITHUB_GH_TOKEN),<set>,<unset>)\n"
	@echo "----------------------------------------------\nCURRENT_RELEASE_NOTES\n----------------------------------------------\n${CURRENT_RELEASE_NOTES}\n"

githubio_logic_pre:
	$(eval REPO_NAME:= $(shell echo ${GH_REPO} | cut -d "-" -f 2 ))
	$(eval REPO_NAME_UPPER:= $(shell echo ${GH_REPO} | cut -d "-" -f 2 | perl -pe 's/(.*)/\U$$1/'))
	$(eval DOCS_DIR:=ondewo.github.io/docs/ondewo-${REPO_NAME}-api/${ONDEWO_T2S_API_VERSION})
	@perl -i -ne "print unless /\{ number: '${ONDEWO_T2S_API_VERSION}', link: 'ondewo-${REPO_NAME}-api\/${ONDEWO_T2S_API_VERSION}\/' \},/" ondewo.github.io/data.js
	@rm -rf ${DOCS_DIR}
	@mkdir "${DOCS_DIR}"
	@cp docs/* ${DOCS_DIR}
	@perl -i -pe "s/h1>Protocol Documentation/h1>${REPO_NAME_UPPER} ${ONDEWO_T2S_API_VERSION} Documentation/" ${DOCS_DIR}/index.html

githubio_logic: | githubio_logic_pre
	$(eval REPO_NAME:= $(shell echo ${GH_REPO} | cut -d "-" -f 2 ))
	$(eval REPO_NAME_UPPER:= $(shell echo ${GH_REPO} | cut -d "-" -f 2 | perl -pe 's/(.*)/\U$$1/'))
	@git branch | grep "*" | grep -q "master" || (echo "Not on master branch"  & rm -rf ondewo.github.io && exit 1)
	@! cat ondewo.github.io/data.js | perl -ne "print if /name: '${REPO_NAME_UPPER}'/../end: ''/" | grep -q "number: '${ONDEWO_T2S_API_VERSION}'" || (echo "Already Released" && exit 1)
	$(eval VERSION_LINE:= $(shell cat -n ondewo.github.io/data.js | perl -ne "print if /name: '${REPO_NAME_UPPER}'/../end: ''/" | grep "versions: " -A 1 | tail -1 | grep -o -E '[0-9]+' | head -1 | perl -pe 's/^0+//'))
	@perl -pe "s/VERSION/${ONDEWO_T2S_API_VERSION}/g; s/TECHNOLOGY/${REPO_NAME}/g" ondewo.github.io/script_object.txt > ondewo.github.io/.insert_version.txt
	@perl -i -pe 'BEGIN { open(my $$f, "<", "ondewo.github.io/.insert_version.txt") or die $$!; $$line = <$$f>; close($$f); chomp $$line } print "$$line\n" if $$. == ${VERSION_LINE}' ondewo.github.io/data.js
	@rm -f ondewo.github.io/.insert_version.txt
	@npm install prettier && cd ondewo.github.io && npx prettier -w --single-quote data.js
	$(eval DOCS_DIR:=ondewo.github.io/docs/ondewo-${REPO_NAME}-api/${ONDEWO_T2S_API_VERSION})
	@rm -rf ${DOCS_DIR}
	@mkdir "${DOCS_DIR}"
	@cp docs/* ${DOCS_DIR}
	@perl -i -pe "s/h1>Protocol Documentation/h1>${REPO_NAME_UPPER} ${ONDEWO_T2S_API_VERSION} Documentation/" ${DOCS_DIR}/index.html
	$(eval HEADER_LINE:= $(shell cat ${DOCS_DIR}/index.html | grep -n "${REPO_NAME_UPPER} ${ONDEWO_T2S_API_VERSION} Documentation" | grep -o -E '[0-9]+' | head -1 | perl -pe 's/^0+//'))
	$(eval TEMP_CALC:= $(shell expr ${HEADER_LINE} ))
	@perl -i -pe 'BEGIN { open(my $$f, "<", "ondewo.github.io/script_image.txt") or die $$!; $$line = <$$f>; close($$f); chomp $$line } print "$$line\n" if $$. == ${TEMP_CALC}' ${DOCS_DIR}/index.html
	head -30 ${DOCS_DIR}/index.html
	cat ondewo.github.io/data.js | perl -ne "print if /name: '${REPO_NAME_UPPER}'/../end: ''/"
	@git -C ondewo.github.io status
	@git -C ondewo.github.io add data.js
	@git -C ondewo.github.io add docs
	@git -C ondewo.github.io status
	@git -C ondewo.github.io commit -m "Added ${REPO_NAME} Documentation for ${ONDEWO_T2S_API_VERSION}"
	@git -C ondewo.github.io push

update_githubio:
	@if [ -d "ondewo.github.io" ]; then \
		echo "Removing existing directory ondewo.github.io"; \
		rm -rf ondewo.github.io; sleep 3s; \
	fi
	@git clone git@github.com:ondewo/ondewo.github.io.git
	. ~/.nvm/nvm.sh && make githubio_logic || (echo "Done")
	@rm -rf ondewo.github.io

########################################################
#       Repo Specific Make Targets
########################################################
#		Release

# ORDER IS LOAD-BEARING AND MAKE ONLY GUARANTEES IT SERIALLY, hence the `.NOTPARALLEL:` below.
# Prerequisites are made left to right under a serial make, but `make -j` is free to run them
# concurrently and in any order: the GitHub release could be created before the tag it names was pushed,
# and preflight_all_clients could run beside, or after, the client releases it exists to gate
# (release_all_clients_after_preflight). `.NOTPARALLEL:` with no prerequisites restores the listed order
# on every make version; the targeted `.NOTPARALLEL: release` needs make >= 4.4 and silently means the
# bare form on 4.3. Nothing in this makefile is written to be parallel-safe, so it costs nothing.
.NOTPARALLEL:

release: create_release_branch create_release_tag build_and_release_to_github_via_docker ## Automate the entire release process
	@echo "Release Finished"

create_release_branch: ## Create Release Branch and push it to origin
	git checkout -b "release/${ONDEWO_T2S_API_VERSION}"
	git push -u origin "release/${ONDEWO_T2S_API_VERSION}"

create_release_tag: ## Create Release Tag and push it to origin
	git tag -a ${ONDEWO_T2S_API_VERSION} -m "release/${ONDEWO_T2S_API_VERSION}"
	git push origin ${ONDEWO_T2S_API_VERSION}

# gh reads the token from GH_TOKEN of the ONE command that needs it: no `gh auth login`, so nothing is
# persisted in a gh config anywhere, and the value never reaches argv (`$${...}` is expanded by the shell).
build_gh_release: ## Generate Github Release with CLI; refuses empty release notes
	@notes="$(CURRENT_RELEASE_NOTES)"; \
	if [ -z "$$notes" ]; then echo "ERROR: RELEASE.md has no notes for ${ONDEWO_T2S_API_VERSION}; refusing an empty GitHub release" && exit 1; fi; \
	GH_TOKEN="$${GITHUB_GH_TOKEN}" gh release create --repo $(GH_REPO) "$(ONDEWO_T2S_API_VERSION)" -n "$$notes" -t "Release ${ONDEWO_T2S_API_VERSION}"

# Every published ondewo-t2s-client-<language> SDK; scripts/release_client.sh drives all eleven alike. The
# client release contract is `release_preflight` (read-only: credentials valid, version new on origin and
# registry, notes present, host tools there), `ondewo_release`, and `release_verify` (read-only: tag, GitHub
# release body and the registry serving the version). A client with neither contract target (every T2S
# client today) is a LEGACY client: released through its `ondewo_release` exactly as before, and verified by
# the tag on origin plus the published GitHub release (CLIENT_GITHUB_API_PREFIX).
CLIENTS := python nodejs typescript angular js cpp csharp go java php rust

# The ondewo-proto-compiler every client is built with, pinned EXACTLY and written into each client's
# ONDEWO_PROTO_COMPILER_GIT_BRANCH as tags/<version>. It used to be "the first tag the GitHub API
# returned": unauthenticated (60 requests/hour, so a rate-limited run wrote an empty `tags/`), in an
# undocumented order, and any new compiler tag silently moved every client's pin mid-release. Move it
# deliberately; `make check_proto_compiler_is_latest` tells you when a newer tag exists.
ONDEWO_PROTO_COMPILER_VERSION=5.17.0

CLIENT_GIT_URL_PREFIX?=git@github.com:ondewo/ondewo-t2s-client-
# The RELEASE.md a client's release slices its notes from (the js family keeps it in src/).
CLIENT_RELEASE_MD=$(if $(filter nodejs typescript angular js,$(1)),src/RELEASE.md,RELEASE.md)
# How the client's RELEASE.md headings spell the language: capitalised name, except "C++" and "PHP".
CLIENT_DISPLAY_NAME_cpp=C++
CLIENT_DISPLAY_NAME_php=PHP
CLIENT_DISPLAY_NAME=$(or $(CLIENT_DISPLAY_NAME_$(1)),$(shell printf '%s' '$(1)' | perl -pe 's/^(.)/\u$$1/'))

# Emitted markdownlint-clean, and deliberately on ONE line. Every ` \n` used to leave a trailing space on
# each generated line and a leading space on the list item, and make's line-continuation collapses
# `\<newline><tab>` to a further space, so the block tripped MD009/MD007/MD022/MD012/MD032 in EVERY client and the
# first pre-commit run of every release `Failed - files were modified by this hook` (10 auto-fixes in the
# Python client for 8.6.0 alone). It self-healed on the re-run, but it also left the heading as
# `\#\# Release ... <VERSION> ` WITH a trailing space, so nothing can anchor a `$$` grep on that heading.
# Keep this byte-identical to what markdownlint normalises to: no trailing spaces, a blank line around
# the heading and around the list. It reaches scripts/release_client.sh VERBATIM through the environment
# (RELEASE_NOTES_TEMPLATE below), never on a command line, so a backtick in a note is never
# command-substituted; the script turns `\n` into newlines, drops the other backslashes and ends the
# notes in exactly one newline.
#
# The section heading is driven by GENERIC_RELEASE_SECTION so a breaking API release does not publish every
# client major under "Improvements". On a major bump, override it and describe the break:
#   make release_all_clients GENERIC_RELEASE_SECTION='Breaking Changes' \
#     GENERIC_RELEASE_EXTRA='* <what broke>\n'
GENERIC_RELEASE_SECTION?=Improvements
GENERIC_RELEASE_EXTRA?=
GENERIC_RELEASE_NOTES=\n*****************\n\n\\\#\\\# Release ONDEWO T2S REPONAME Client ${ONDEWO_T2S_API_VERSION}\n\n\\\#\\\#\\\# ${GENERIC_RELEASE_SECTION}\n\n* Tracking API Version [${ONDEWO_T2S_API_VERSION}](https://github.com/ondewo/ondewo-t2s-api/releases/tag/${ONDEWO_T2S_API_VERSION}) ( [Documentation](https://ondewo.github.io/ondewo-t2s-api/) )\n${GENERIC_RELEASE_EXTRA}

# Legacy clients only: where scripts/release_client.sh asks whether GitHub has published release <version>
# of ondewo-t2s-client-<language> (`<prefix><language>/releases/tags/<version>`, one unauthenticated call).
CLIENT_GITHUB_API_PREFIX?=https://api.github.com/repos/ondewo/ondewo-t2s-client-

# One devops-accounts clone per run: reuses DEVOPS_ACCOUNT_DIR when an outer target already made one.
#
# The lines that start the wrapper call `make`, NOT `$(MAKE)`, on purpose: make EXECUTES every recipe line
# that mentions $(MAKE) even under `make -n`, so `make -n release_all_clients` used to clone
# ondewo-devops-accounts for real. With a plain `make` a dry run only prints the wrapper line; dry-run the
# inner targets (release_all_clients_after_preflight, release_client CLIENT=<x>, release) to see the steps.
WITH_DEVOPS_ACCOUNTS=DEVOPS_ACCOUNT_GIT_URL="$(DEVOPS_ACCOUNT_GIT_URL)" scripts/with_devops_accounts.sh

# $(call run_client_script,<preflight|release>,<client>)
run_client_script=$(if $(filter $(2),$(CLIENTS)),,$(error CLIENT='$(2)' is not one of: $(CLIENTS)))$(WITH_DEVOPS_ACCOUNTS) scripts/release_client.sh $(1) $(2) "$(CLIENT_GIT_URL_PREFIX)$(2).git" "$(call CLIENT_RELEASE_MD,$(2))" "$(call CLIENT_DISPLAY_NAME,$(2))" "$(ONDEWO_T2S_API_VERSION)" "$(ONDEWO_PROTO_COMPILER_VERSION)"
preflight_client release_client: export RELEASE_NOTES_TEMPLATE=$(GENERIC_RELEASE_NOTES)
preflight_client release_client: export CLIENT_GITHUB_API_PREFIX:=$(CLIENT_GITHUB_API_PREFIX)

release_all_clients: ## Preflight EVERY client, then release them IN PARALLEL; one failing client does not abort the others
	@$(WITH_DEVOPS_ACCOUNTS) make --no-print-directory release_all_clients_after_preflight

# preflight_all_clients is a PREREQUISITE: a single failing preflight stops the run before any client
# releases. `.NOTPARALLEL:` (see `release`) keeps it ahead of the recipe even under `make -j`.
# A client counts as released only when its release_verify (a legacy client: its tag and GitHub release)
# passed; SKIP means "already released AND verified". A half-finished release is INCOMPLETE, a legacy client
# whose state the GitHub API would not tell is UNKNOWN, anything else that fails is FAILED - never SKIP
# (scripts/release_client.sh). make flattens every failure to exit code 2, so the marker files tell them apart.
release_all_clients_after_preflight: preflight_all_clients
	@umask 077; \
	echo "Releasing all clients in parallel for ${ONDEWO_T2S_API_VERSION} ..."; \
	rm -f .already_released_marker-* .incomplete_marker-* .unknown_marker-* .client_status-*; \
	for c in $(CLIENTS); do \
		rm -f release_run_$$c.log; \
		( if CLIENT_STATUS_MARKERS=yes $(MAKE) --no-print-directory release_client CLIENT=$$c > release_run_$$c.log 2>&1; then \
			if [ -f .already_released_marker-$$c ]; then echo SKIP > .client_status-$$c; else echo RELEASED > .client_status-$$c; fi; \
		  elif [ -f .incomplete_marker-$$c ]; then echo INCOMPLETE > .client_status-$$c; \
		  elif [ -f .unknown_marker-$$c ]; then echo UNKNOWN > .client_status-$$c; \
		  else echo FAILED > .client_status-$$c; fi ) & \
	done; \
	wait; \
	echo ""; echo "=============== CLIENT RELEASE SUMMARY (${ONDEWO_T2S_API_VERSION}) ==============="; \
	failed=0; \
	for c in $(CLIENTS); do \
		s=$$(cat .client_status-$$c 2>/dev/null || echo NO_STATUS); \
		echo "  $$c : $$s"; \
		case "$$s" in RELEASED|SKIP) ;; *) failed=1; echo "      -> see release_run_$$c.log";; esac; \
	done; \
	echo "==============================================================="; \
	rm -f .already_released_marker-* .incomplete_marker-* .unknown_marker-* .client_status-*; \
	if [ "$$failed" = 1 ]; then echo "RESULT: one or more clients FAILED, are INCOMPLETE or UNKNOWN (the others released independently)."; exit 1; fi; \
	echo "RESULT: all clients released and verified, or already released and verified."

preflight_all_clients: ## Run every client's read-only release_preflight, serially; fails if ANY client fails
	@$(WITH_DEVOPS_ACCOUNTS) make --no-print-directory preflight_all_clients_with_devops

preflight_all_clients_with_devops:
	@failed=""; \
	for c in $(CLIENTS); do \
		$(MAKE) --no-print-directory preflight_client CLIENT=$$c || failed="$$failed $$c"; \
	done; \
	if [ -n "$$failed" ]; then echo "PREFLIGHT FAILED for:$$failed - nothing was released"; exit 1; fi; \
	echo "PREFLIGHT OK for: $(CLIENTS)"

preflight_client: ## Preflight ONE client: make preflight_client CLIENT=<language>
	@$(call run_client_script,preflight,$(CLIENT))

release_client: ## Release ONE client (its own release starts with release_preflight): make release_client CLIENT=<language>
	@$(call run_client_script,release,$(CLIENT))

# make release_<language>_client / make preflight_<language>_client, e.g. release_python_client
release_%_client:
	@$(MAKE) --no-print-directory release_client CLIENT=$*

preflight_%_client:
	@$(MAKE) --no-print-directory preflight_client CLIENT=$*

check_proto_compiler_is_latest: ## Fail when ondewo-proto-compiler has a newer release tag than ONDEWO_PROTO_COMPILER_VERSION (needs gh)
	@latest=$$(gh api --paginate repos/ondewo/ondewo-proto-compiler/tags --jq '.[].name' | grep -E '^[0-9]+\.[0-9]+\.[0-9]+$$' | sort -V | tail -1); \
	if [ -z "$$latest" ]; then echo "ERROR: could not read the ondewo-proto-compiler tags" && exit 2; fi; \
	if [ "$$latest" = "$(ONDEWO_PROTO_COMPILER_VERSION)" ]; then echo "ONDEWO_PROTO_COMPILER_VERSION=$(ONDEWO_PROTO_COMPILER_VERSION) is the newest tag"; \
	else echo "ondewo-proto-compiler $$latest is newer than ONDEWO_PROTO_COMPILER_VERSION=$(ONDEWO_PROTO_COMPILER_VERSION)" && exit 1; fi

########################################################
#		GITHUB

build_and_release_to_github_via_docker: build_utils_docker_image release_to_github_via_docker_image ## Release automation for building and releasing on GitHub via a docker image

build_utils_docker_image: ## Build utils docker image
	docker build -f Dockerfile.utils -t ${IMAGE_UTILS_NAME} .

push_to_gh: build_gh_release ## Creates the GitHub release
	@echo 'Released to Github'

release_to_github_via_docker_image: ## Release to Github via docker
	@docker run --rm \
		-e GITHUB_GH_TOKEN \
		${IMAGE_UTILS_NAME} make push_to_gh

########################################################
#		DEVOPS-ACCOUNTS

# scripts/with_devops_accounts.sh --github-token clones ondewo-devops-accounts into a private `mktemp -d`,
# reads GITHUB_GH_TOKEN (anchored to its definition line) into the ENVIRONMENT of the sub-make, deletes the
# clone, and only then runs the release. Nothing is cloned into this checkout, the token never reaches
# argv (`make release NAME=<value>` would put it in /proc/<pid>/cmdline), and the clone is removed on every
# exit path, including a failure or Ctrl-C.
ondewo_release: spc ## Release with the GitHub token from a temporary devops-accounts clone
	@$(WITH_DEVOPS_ACCOUNTS) --github-token make release

ondewo_unrelease: ## Unrelease with the GitHub token from a temporary devops-accounts clone
	@$(WITH_DEVOPS_ACCOUNTS) --github-token make unrelease

# Read-only. Anchored throughout: `git rev-parse --verify` and `git ls-remote --exit-code` match whole
# refs, so neither 15.5.0 nor 5.5.0x stands in for 5.5.0. An origin that cannot be read fails closed.
spc: ## Checks the version is new (no release branch or tag, locally or on origin) and RELEASE.md has notes for it
	@echo "${ONDEWO_T2S_API_VERSION}" | grep -qxE '[0-9]+\.[0-9]+\.[0-9]+' || { echo "-- ONDEWO_T2S_API_VERSION '${ONDEWO_T2S_API_VERSION}' is not MAJOR.MINOR.PATCH" && exit 1; }
	@rc=0; git ls-remote --exit-code --heads origin "refs/heads/release/${ONDEWO_T2S_API_VERSION}" >/dev/null || rc=$$?; \
	if [ $$rc -eq 0 ] || git rev-parse -q --verify "refs/heads/release/${ONDEWO_T2S_API_VERSION}" >/dev/null; then echo "-- Test 1: Branch release/${ONDEWO_T2S_API_VERSION} exists!!" && exit 1; \
	elif [ $$rc -ne 2 ]; then echo "-- Test 1: cannot read origin (git ls-remote exit $$rc)" && exit 1; \
	else echo "-- Test 1: Branch is fine"; fi
	@rc=0; git ls-remote --exit-code --tags origin "refs/tags/${ONDEWO_T2S_API_VERSION}" >/dev/null || rc=$$?; \
	if [ $$rc -eq 0 ] || git rev-parse -q --verify "refs/tags/${ONDEWO_T2S_API_VERSION}" >/dev/null; then echo "-- Test 2: Tag ${ONDEWO_T2S_API_VERSION} exists!!" && exit 1; \
	elif [ $$rc -ne 2 ]; then echo "-- Test 2: cannot read origin (git ls-remote exit $$rc)" && exit 1; \
	else echo "-- Test 2: Tag is fine"; fi
	@notes="$(CURRENT_RELEASE_NOTES)"; \
	if printf '%s\n' "$$notes" | grep -vE '^(#+ Release ONDEWO T2S API |\*+[[:space:]]*$$|[[:space:]]*$$)' | grep -q .; then echo "-- Test 3: RELEASE.md has notes for ${ONDEWO_T2S_API_VERSION}"; \
	else echo "-- Test 3: RELEASE.md has no '## Release ONDEWO T2S API ${ONDEWO_T2S_API_VERSION}' section with content!!" && exit 1; fi

########################################################
#		UNRELEASE

unrelease: build_utils_docker_image unrelease_to_github_via_docker_image ## Undo a release: delete the GitHub release, release branch, and release tag
	-git branch -d "release/${ONDEWO_T2S_API_VERSION}"
	-git tag -d "${ONDEWO_T2S_API_VERSION}"
	-git fetch --prune
	@echo "Unrelease of ${ONDEWO_T2S_API_VERSION} complete"

unrelease_to_github_via_docker_image: ## Unrelease from Github via docker
	@docker run --rm \
		-e GITHUB_GH_TOKEN \
		${IMAGE_UTILS_NAME} make delete_gh_release

delete_gh_release: ## Delete GitHub Release, release branch and release tag via gh CLI
	-@GH_TOKEN="$${GITHUB_GH_TOKEN}" gh release delete --repo $(GH_REPO) "$(ONDEWO_T2S_API_VERSION)" --yes
	-@GH_TOKEN="$${GITHUB_GH_TOKEN}" gh api repos/ondewo/ondewo-t2s-api/git/refs/heads/release/${ONDEWO_T2S_API_VERSION} -X DELETE
	-@GH_TOKEN="$${GITHUB_GH_TOKEN}" gh api repos/ondewo/ondewo-t2s-api/git/refs/tags/${ONDEWO_T2S_API_VERSION} -X DELETE
