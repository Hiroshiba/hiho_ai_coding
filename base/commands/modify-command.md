---
description: Command を修正する
disable-model-invocation: true
---

Claude Code Commands を修正してください。
Command は `~/Github/hiho_ai_coding/base/commands/` 以下にあります。

## 手順

1. 仕様の確認: 以下の URL を Fetch して Command の仕様と best practice を把握する
   - https://platform.claude.com/docs/en/agent-sdk/slash-commands
   - https://code.claude.com/docs/en/slash-commands
2. 対象 Command の特定: ユーザーの指示から修正対象の Command を特定する
3. 現状の確認: 対象 Command を Read して現在の内容を把握する
4. 修正の実施: 仕様と best practice に基づいて修正する

ユーザーの意図がわからない場合は、`git status`や`git diff`を使って変更内容を確認して推測してください。
修正対象の Command や修正方針がわからない場合はユーザーに Ask してください。
おかしな点があればユーザーに報告してください。
