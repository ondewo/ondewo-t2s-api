#!/usr/bin/env bash
# Run a command with ONE clone of ondewo-devops-accounts that never outlives it.
#
# Usage:
#   with_devops_accounts.sh <command> [args ...]
#       The command runs with DEVOPS_ACCOUNT_DIR pointing at the clone. The clients' `ondewo_release`,
#       `release_preflight` and `release_verify` read their credentials from there instead of cloning.
#   with_devops_accounts.sh --github-token <command> [args ...]
#       Reads GITHUB_GH_TOKEN (anchored to its definition line), DELETES the clone, and only then runs the
#       command with the token in its environment. Used by this repository's own `ondewo_release`.
#
# Where the clone lives: `mktemp -d` (mode 700, in $TMPDIR), i.e. OUTSIDE every repository, so it can be
# neither committed, nor sent in a `docker build .` context, nor bind-mounted into a container that mounts
# a checkout. It is removed by an EXIT trap on every exit path; INT/TERM/HUP are turned into an exit so
# that trap runs for them too.
#
# When DEVOPS_ACCOUNT_DIR already names a directory (an outer invocation of this script made it), that
# directory is used and NOT deleted here - its owner deletes it - so a whole driver run clones exactly once.
#
# DEVOPS_ACCOUNT_GIT_URL overrides the repository (the tests point it at a local fixture).
set -euo pipefail
umask 077

load_github_token=no
if [ "${1:-}" = "--github-token" ]; then
    load_github_token=yes
    shift
fi
[ "$#" -gt 0 ] || { echo "usage: $0 [--github-token] <command> [args ...]" >&2; exit 2; }

devops_url="${DEVOPS_ACCOUNT_GIT_URL:-git@bitbucket.org:ondewo/ondewo-devops-accounts.git}"
owned_dir=""

remove_owned_clone() {
    if [ -n "${owned_dir}" ]; then
        rm -rf "${owned_dir}"
        owned_dir=""
    fi
}
trap remove_owned_clone EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
trap 'exit 129' HUP

# Every path handed on is ABSOLUTE: the clients run as `make -C <client>`, where a relative path such as
# ./ondewo-devops-accounts resolves to nothing and a client silently falls back to a clone of its own.
if [ -n "${DEVOPS_ACCOUNT_DIR:-}" ] && [ -d "${DEVOPS_ACCOUNT_DIR}" ]; then
    devops_dir="$(cd "${DEVOPS_ACCOUNT_DIR}" && pwd -P)"
else
    owned_dir="$(cd "$(mktemp -d)" && pwd -P)"
    chmod 700 "${owned_dir}"
    devops_dir="${owned_dir}/ondewo-devops-accounts"
    echo "Cloning ondewo-devops-accounts into a private temporary directory (removed on exit) ..."
    git clone --quiet --depth 1 "${devops_url}" "${devops_dir}"
fi

if [ "${load_github_token}" = yes ]; then
    # Anchored to the definition line; the value never reaches argv or the console.
    token_line="$(grep -h -E '^GITHUB_GH_TOKEN=' "${devops_dir}/account_github.env")" || {
        echo "ERROR: no GITHUB_GH_TOKEN= line in account_github.env of ondewo-devops-accounts" >&2
        exit 1
    }
    remove_owned_clone
    set -a
    eval "${token_line}"
    set +a
    unset token_line DEVOPS_ACCOUNT_DIR
    "$@"
else
    DEVOPS_ACCOUNT_DIR="${devops_dir}" "$@"
fi
