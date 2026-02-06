#!/bin/bash
set -euo pipefail

input=$(cat)

filename=$(echo "$input" | jq -r '.tool_input.filename // empty')

if [[ -z "$filename" ]]; then
  exit 0
fi

if [[ "$filename" != /* ]]; then
  filename="$(pwd)/$filename"
fi

if [[ "$filename" == /tmp/* ]]; then
  exit 0
fi

if [[ "$filename" == */.playwright-mcp/* ]]; then
  exit 0
fi

echo '{
  "decision": "deny",
  "reason": "スクリーンショットの保存先は /tmp/ または ./.playwright-mcp/ ディレクトリに限定されています。指定されたパス: '"$filename"'"
}' >&2
exit 2
