---
description: Command を作成する
disable-model-invocation: true
---

Claude Code Commands を作成してください。

## 配置先

- **デフォルト**: `~/Github/hiho_ai_coding/base/commands/`
- **ローカル環境**: ユーザーが「ローカル環境」「この環境に」「このリポジトリに」などと指示した場合は、現在の作業ディレクトリの `.claude/commands/` 以下に配置する

## 手順

1. 仕様の確認: 以下の URL を Fetch して Command の仕様と best practice を把握する
   - https://platform.claude.com/docs/en/agent-sdk/slash-commands
   - https://code.claude.com/docs/en/slash-commands
2. 要件の整理: ユーザーの指示から作成する Command の要件を整理する
3. 作成の実施: 仕様と best practice に基づいて作成する

作成対象の Command や作成方針がわからない場合はユーザーに Ask してください。
おかしな点があればユーザーに報告してください。
