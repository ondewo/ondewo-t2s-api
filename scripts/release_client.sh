#!/usr/bin/env bash
# Prepare, preflight, release and verify ONE ondewo-t2s-client-<language> repository.
#
# Called by the Makefile (`preflight_<x>_client`, `release_<x>_client`, `preflight_all_clients`,
# `release_all_clients`), never by hand:
#
#   release_client.sh <preflight|release> <name> <git-url> <release-md> <display-name> \
#                     <api-version> <proto-compiler-version>
#
# RELEASE_NOTES_TEMPLATE (environment) holds GENERIC_RELEASE_NOTES exactly as make stores it (literal
# `\n`, `\#`); it is turned into markdown here, in a private temporary directory. DEVOPS_ACCOUNT_DIR must
# name the driver's ondewo-devops-accounts clone (scripts/with_devops_accounts.sh provides it).
#
# The state of the client on origin decides what happens, and a half-finished release is never a SKIP:
#
#   tag <version> on origin  AND  `make release_verify` passes  -> SKIP (already released and verified)
#   tag on origin, release_verify FAILS                          -> FAILED
#   release/<version> branch on origin, but no tag               -> FAILED
#   neither                                                      -> preflight: `make release_preflight`
#                                                                   release:   `make ondewo_release`, then
#                                                                              `make release_verify`
#
# A half-finished release also leaves .incomplete_marker-<name>, so release_all_clients reports it as
# INCOMPLETE rather than as a plain FAILED.
#
# LEGACY clients. No ondewo-t2s-client-<language> repository carries the release contract yet: each has only
# `ondewo_release`, which the five original clients have always been released with. A client that has
# NEITHER release_preflight NOR release_verify is therefore released exactly as before (`make
# ondewo_release`), and this script supplies the two checks itself: the tag <version> on origin AND the
# published GitHub release <version>, asked of the GitHub REST API (CLIENT_GITHUB_API_PREFIX<name>, one
# unauthenticated call; the page github.com/.../releases/tag/<v> answers 200 for a bare tag as well):
#
#   tag AND GitHub release (HTTP 200)                            -> SKIP
#   tag or release/<version> branch, GitHub release HTTP 404     -> INCOMPLETE (.incomplete_marker-<name>)
#   tag or branch, any other answer (403/429 rate limit, 000)    -> UNKNOWN (.unknown_marker-<name>), nothing changed
#   neither                                                      -> preflight: passes with a LEGACY warning
#                                                                   release:   `make ondewo_release`, then the
#                                                                              tag + GitHub release check
#
# A client with ONE of the two contract targets but not the other FAILS: a half-implemented contract is a
# mistake, not a legacy client. Once a client implements both, the contract path above applies to it.
#
# Every exit path removes the client clone and this client's private temporary directory (the notes and
# its copy of the devops clone) (EXIT trap; INT/TERM/HUP become an exit so the trap runs for them too). No sudo: files a client
# container wrote as root are removed through a throwaway container that mounts only the clone.
set -euo pipefail
# 077 is for what THIS script writes (the notes, the private devops copy, the build log). The client clone
# and the client make run under CLIENT_UMASK instead (clone_client / run_client_target): a client builds
# docker images from its checkout and runs them with `--user $(id -u)`, and COPY keeps file modes, so a
# 0600 checkout made e.g. compile-proto-2-php.sh unreadable in the php proto-compiler image (5.5.2: `bash:
# compile-proto-2-php.sh: Permission denied`). The clone holds only public sources.
umask 077
CLIENT_UMASK=022

[ "$#" -eq 7 ] || { echo "usage: $0 <preflight|release> <name> <git-url> <release-md> <display-name> <api-version> <proto-compiler-version>" >&2; exit 2; }
mode="$1" name="$2" url="$3" release_md="$4" display_name="$5" version="$6" compiler_version="$7"

repo_dir="ondewo-t2s-client-${name}"
build_log="build_log_${name}.txt"
skip_marker=".already_released_marker-${name}"
incomplete_marker=".incomplete_marker-${name}"
unknown_marker=".unknown_marker-${name}"
# Removes files a client container left behind as root; pinned by digest, mounts only the clone.
cleanup_image="busybox:1.37.0@sha256:bdf57e528e45e4433820e045b29b4597825a1c9e38353532d90a01445013f82e"
private_root=""

# The status markers (.already_released_marker-, .incomplete_marker-, .unknown_marker-<name>) are for
# release_all_clients, which sets CLIENT_STATUS_MARKERS=yes for its release runs and reads and removes them
# afterwards; a preflight or a release run by hand leaves none behind.
mark() { if [ "${mode}" = release ] && [ "${CLIENT_STATUS_MARKERS:-}" = yes ]; then touch "$1"; fi; }
say() { printf 'release_client[%s]: %s\n' "${name}" "$*"; }
fail() { say "FAILED: $*" >&2; exit 1; }

remove_clone() {
    [ -e "${repo_dir}" ] || return 0
    rm -rf "${repo_dir}" 2>/dev/null && return 0
    say "plain rm could not remove ${repo_dir} (files written as root by a container); removing them through ${cleanup_image}"
    docker run --rm -v "${PWD}/${repo_dir}:/clone" "${cleanup_image}" \
        sh -c 'rm -rf /clone/..?* /clone/.[!.]* /clone/*' && rm -rf "${repo_dir}"
}

cleanup() {
    local status=$?
    remove_clone || { say "could not remove ${repo_dir}" >&2; status=1; }
    [ -z "${private_root}" ] || rm -rf "${private_root}"
    exit "${status}"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
trap 'exit 129' HUP

case "${mode}" in preflight | release) ;; *) fail "unknown mode '${mode}'" ;; esac
semver='^[0-9]+\.[0-9]+\.[0-9]+$'
[[ "${version}" =~ ${semver} ]] || fail "API version '${version}' is not MAJOR.MINOR.PATCH"
[[ "${compiler_version}" =~ ${semver} ]] || fail "ONDEWO_PROTO_COMPILER_VERSION '${compiler_version}' is not MAJOR.MINOR.PATCH"
if [ -z "${DEVOPS_ACCOUNT_DIR:-}" ] || [ ! -d "${DEVOPS_ACCOUNT_DIR}" ]; then
    fail "DEVOPS_ACCOUNT_DIR is not a directory; run this through the Makefile targets, which provide it"
fi
[ -n "${RELEASE_NOTES_TEMPLATE:-}" ] || fail "RELEASE_NOTES_TEMPLATE is empty; run this through the Makefile targets, which provide it"
[ -n "${CLIENT_GITHUB_API_PREFIX:-}" ] || fail "CLIENT_GITHUB_API_PREFIX is empty; run this through the Makefile targets, which provide it"
rm -f "${skip_marker}" "${incomplete_marker}" "${unknown_marker}"
remove_clone

# Absolute (the client runs as `make -C <client>`, where a relative path would not resolve).
private_root="$(cd "$(mktemp -d)" && pwd -P)"
notes="${private_root}/release-notes.md"
printf '%s' "${RELEASE_NOTES_TEMPLATE}" > "${notes}"

# Exit 0: the ref exists on origin; 1: it does not; anything else is an error and fails closed.
# `git ls-remote --exit-code` matches whole trailing ref components, so refs/tags/5.5.1 is not found by
# refs/tags/15.5.1 nor by refs/tags/5.5.10 (and the dots are not regex wildcards).
origin_has_ref() {
    local rc=0
    git ls-remote --exit-code "${url}" "$1" >/dev/null || rc=$?
    case "${rc}" in
        0) return 0 ;;
        2) return 1 ;;
        *) fail "cannot read ${url} (git ls-remote exit ${rc})" ;;
    esac
}

# Nothing of this driver's make reaches a client: make hands every command-line variable (CLIENT=...,
# ONDEWO_T2S_API_VERSION=..., ...) to its children BOTH in MAKEFLAGS and as an environment variable, and
# a client Makefile that reads one with `?=` would silently take the driver's value. So the client make
# starts without MAKEFLAGS and without each variable named in it.
driver_variables=(MAKEFLAGS MFLAGS MAKELEVEL MAKEOVERRIDES RELEASE_NOTES_TEMPLATE CLIENT_GITHUB_API_PREFIX CLIENT_STATUS_MARKERS)
if [[ "${MAKEFLAGS:-}" == *"-- "* ]]; then
    while read -r variable; do
        driver_variables+=("${variable}")
    done < <(printf '%s\n' "${MAKEFLAGS#*-- }" | grep -oE '(^| )[A-Za-z_][A-Za-z0-9_]*:?=' | tr -d ' :=')
fi
unset_driver_variables=()
for variable in "${driver_variables[@]}"; do unset_driver_variables+=(-u "${variable}"); done

# Runs a client target with a private copy of the devops clone, so a client that deletes "its" clone
# cannot pull it from under a client releasing in parallel.
run_client_target() {
    local devops_copy="${private_root}/ondewo-devops-accounts"
    rm -rf "${devops_copy}"
    cp -R "${DEVOPS_ACCOUNT_DIR}" "${devops_copy}"
    (umask "${CLIENT_UMASK}" && exec env "${unset_driver_variables[@]}" DEVOPS_ACCOUNT_DIR="${devops_copy}" make -C "${repo_dir}" "$1")
}

client_has_target() {
    grep -Eq "^$1[[:space:]]*:([^=]|\$)" "${repo_dir}/Makefile"
}

# ---------------------------------------------------------------- clone and prepare
say "${mode} ${display_name} client ${version} (proto compiler ${compiler_version}) from ${url}"
(umask "${CLIENT_UMASK}" && exec git clone --quiet "${url}" "${repo_dir}")

client_has_target ondewo_release || fail "client ${name} lacks ondewo_release"
if client_has_target release_preflight && client_has_target release_verify; then
    contract=yes
elif client_has_target release_preflight || client_has_target release_verify; then
    for target in release_preflight release_verify; do
        client_has_target "${target}" || fail "client ${name} lacks ${target} (it has the other contract target: a client provides both release_preflight and release_verify, or neither)"
    done
else
    contract=no
    say "LEGACY client: no release_preflight / release_verify - released through ondewo_release as before, verified by the tag and the published GitHub release"
fi

# Legacy only: the HTTP status of GitHub's published release <version> of this client (200, 404, 403, 000, ...).
github_release_status() {
    curl -s -o /dev/null -w '%{http_code}' -L "${CLIENT_GITHUB_API_PREFIX}${name}/releases/tags/${version}" || true
}

# Legacy only: the release_verify a legacy client does not have. 0 = tag and GitHub release, 1 = the GitHub
# API says there is no release (404), 2 = the GitHub API gave no answer either way.
legacy_verify() {
    local status
    origin_has_ref "refs/tags/${version}" || { say "no tag ${version} on origin"; return 1; }
    status="$(github_release_status)"
    case "${status}" in
        200) say "tag ${version} and the published GitHub release ${version} exist"; return 0 ;;
        404) say "tag ${version} exists but GitHub has no published release ${version} (GitHub API: HTTP 404)"; return 1 ;;
        *) say "the GitHub API did not say whether release ${version} is published (HTTP ${status}; 403/429 = rate limit, 000 = no connection)"; return 2 ;;
    esac
}

# GENERIC_RELEASE_NOTES -> markdown: `\n` is a newline, every other backslash goes, exactly ONE final newline.
DISPLAY_NAME="${display_name}" perl -0777 -i -pe 's/\\n/\n/g; s/\\//g; s/REPONAME/$ENV{DISPLAY_NAME}/g; s/\n*\z/\n/' "${notes}"

# Insert the generated notes only when the client does not document this version yet: a second heading
# would bury a curated entry and trips markdownlint MD024, which does not auto-fix. Anchored and quoted:
# a `5.5.10` heading does not count as `5.5.1`.
if # The [ \t]* tail is defensive: an older generator emitted the heading with a trailing space.
DISPLAY_NAME="${display_name}" VERSION="${version}" perl -ne \
    'if (/^#+ Release ONDEWO T2S \Q$ENV{DISPLAY_NAME}\E Client \Q$ENV{VERSION}\E[ \t]*$/) { $found = 1; last } END { exit($found ? 0 : 1) }' \
    "${repo_dir}/${release_md}"; then
    say "${release_md} already documents ${version} - keeping the curated entry"
else
    NOTES="${notes}" perl -i -ne 'BEGIN { open my $f, "<", $ENV{NOTES} or die "$ENV{NOTES}: $!"; @notes = <$f>; close $f }
        print; if (!$done && /^#+ Release History\s*$/) { print @notes; $done = 1 } END { exit($done ? 0 : 1) }' \
        "${repo_dir}/${release_md}" || fail "${release_md} has no '# Release History' heading to insert the notes under"
fi

# Anchored on the ASSIGNMENT at the start of a line; unanchored, the rewrite also hit lines that merely
# mention the variable (it cut quotes off echo lines in the go client and truncated a comment in csharp).
makefile="${repo_dir}/Makefile"
perl -i -pe "s/^ONDEWO_T2S_VERSION\\s*=.*/ONDEWO_T2S_VERSION=${version}/" "${makefile}"
perl -i -pe "s{^ONDEWO_PROTO_COMPILER_GIT_BRANCH\\s*=.*}{ONDEWO_PROTO_COMPILER_GIT_BRANCH=tags/${compiler_version}}" "${makefile}"
perl -i -pe "s{^((?:ONDEWO_)?T2S_API_GIT_BRANCH)\\s*=.*}{\$1=tags/${version}}" "${makefile}"
grep -qxF "ONDEWO_T2S_VERSION=${version}" "${makefile}" || fail "Makefile has no ONDEWO_T2S_VERSION= assignment"
grep -qxF "ONDEWO_PROTO_COMPILER_GIT_BRANCH=tags/${compiler_version}" "${makefile}" \
    || fail "Makefile has no ONDEWO_PROTO_COMPILER_GIT_BRANCH= assignment"
grep -qxE "(ONDEWO_)?T2S_API_GIT_BRANCH=tags/${version//./\\.}" "${makefile}" \
    || fail "Makefile has no (ONDEWO_)T2S_API_GIT_BRANCH= assignment"

# ---------------------------------------------------------------- what origin already has
if [ "${contract}" = no ]; then
    if origin_has_ref "refs/tags/${version}" || origin_has_ref "refs/heads/release/${version}"; then
        say "tag or branch release/${version} exists on origin - asking GitHub whether release ${version} is published"
        rc=0
        legacy_verify || rc=$?
        case "${rc}" in
            0)
                say "SKIP: ${version} is already released (tag and GitHub release)"
                mark "${skip_marker}"
                exit 0
                ;;
            1)
                mark "${incomplete_marker}"
                fail "INCOMPLETE: origin has the tag or the branch release/${version} but not both the tag and the published GitHub release: a HALF-FINISHED release. Finish it by hand (the client README names the remaining steps); a re-run reports it as already released once both exist"
                ;;
            *)
                mark "${unknown_marker}"
                fail "UNKNOWN: origin has the tag or the branch release/${version}, but whether it is released could not be determined - nothing was changed, re-run later"
                ;;
        esac
    fi
    if [ "${mode}" = preflight ]; then
        say "PREFLIGHT OK (LEGACY client without release_preflight: checked only that ${version} is new on origin and that the client's RELEASE.md and Makefile can be prepared)"
        exit 0
    fi
    rm -f "${build_log}"
    run_client_target ondewo_release 2>&1 | tee "${build_log}" || fail "ondewo_release failed (see ${build_log})"
    rc=0
    legacy_verify || rc=$?
    case "${rc}" in
        0) ;;
        1) mark "${incomplete_marker}"; fail "ondewo_release finished but the tag or the GitHub release ${version} is missing" ;;
        *) mark "${unknown_marker}"; fail "ondewo_release finished but the GitHub API did not confirm release ${version}; check it by hand" ;;
    esac
    say "RELEASED ${version}"
    exit 0
fi

if origin_has_ref "refs/tags/${version}"; then
    say "tag ${version} exists on origin - running release_verify to tell a finished release from a half-finished one"
    if run_client_target release_verify; then
        say "SKIP: ${version} is already released and release_verify passes"
        mark "${skip_marker}"
        exit 0
    fi
    mark "${incomplete_marker}"
    fail "tag ${version} exists on origin but release_verify fails: a HALF-FINISHED release. Finish it by hand (the client README names the remaining steps); a re-run reports it as already released once release_verify passes"
fi
if origin_has_ref "refs/heads/release/${version}"; then
    mark "${incomplete_marker}"
    fail "branch release/${version} exists on origin but tag ${version} does not: a HALF-FINISHED release. Finish or undo it by hand, then re-run"
fi

# ---------------------------------------------------------------- preflight / release
if [ "${mode}" = preflight ]; then
    run_client_target release_preflight || fail "release_preflight failed"
    say "PREFLIGHT OK"
    exit 0
fi

rm -f "${build_log}"
run_client_target ondewo_release 2>&1 | tee "${build_log}" || fail "ondewo_release failed (see ${build_log})"
run_client_target release_verify || fail "ondewo_release finished but release_verify fails"
say "RELEASED ${version}"
