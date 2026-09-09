#!/usr/bin/env bash
set -euo pipefail

retry_git() {
    local attempt
    local exit_code
    for attempt in 1 2 3; do
        if git "$@"; then
            return 0
        else
            exit_code=$?
        fi
        if (( attempt < 3 )); then
            printf 'git %s に失敗しました。再試行します。試行回数: %s/3\n' "$1" "$attempt" >&2
            sleep 1
        fi
    done
    return "$exit_code"
}

remote_names=$(git remote)
if grep -Fxq upstream <<< "$remote_names"; then
    remote=upstream
elif grep -Fxq origin <<< "$remote_names"; then
    remote=origin
else
    printf 'upstream と origin のどちらもありません。\n' >&2
    exit 1
fi

remote_head=$(retry_git ls-remote --symref "$remote" HEAD)
default_ref=$(awk '$1 == "ref:" && $3 == "HEAD" { print $2 }' <<< "$remote_head")
if [[ "$default_ref" != refs/heads/* ]]; then
    printf '%s のデフォルトブランチを取得できませんでした。\n' "$remote" >&2
    exit 1
fi
git check-ref-format "$default_ref"

default_branch=${default_ref#refs/heads/}
remote_branch="$remote/$default_branch"
remote_ref="refs/remotes/$remote_branch"
retry_git fetch --no-tags "$remote" "+$default_ref:$remote_ref"

behind_count=$(git rev-list --count "HEAD..$remote_ref")
printf 'リモート: %s\nデフォルトブランチ: %s\nワークツリーの基点: %s\n' "$remote" "$default_branch" "$remote_ref"
if (( behind_count == 0 )); then
    printf '現在の HEAD は %s より遅れていません。\n' "$remote_branch"
else
    printf '現在の HEAD は %s より %s コミット遅れています。\n' "$remote_branch" "$behind_count"
fi

if current_ref=$(git symbolic-ref --quiet HEAD); then
    printf '現在のブランチ: %s\n' "${current_ref#refs/heads/}"
else
    exit_code=$?
    if (( exit_code != 1 )); then
        exit "$exit_code"
    fi
    printf '現在の状態: detached HEAD。マージしません。\n'
    exit 0
fi

if [[ "$current_ref" != "$default_ref" ]]; then
    printf 'デフォルトブランチではないため、マージしません。\n'
    exit 0
fi

if (( behind_count > 0 )); then
    git merge --ff-only --no-autostash "$remote_ref"
fi
