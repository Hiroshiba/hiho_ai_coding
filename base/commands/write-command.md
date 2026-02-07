---
description: Command を作成・修正する
disable-model-invocation: true
---

Claude Code Commands を作成・修正してください。

## 配置先

- **デフォルト**: `~/Github/hiho_ai_coding/base/commands/`
- **ローカル環境**: ユーザーが「ローカル環境」「この環境に」「この環境の」「このリポジトリに」「このリポジトリの」などと指示した場合は、現在の作業ディレクトリの `.claude/commands/` 以下を対象とする

## 手順

1. 仕様の確認: 以下の URL を Fetch して Command の仕様と best practice を把握する
   - https://platform.claude.com/docs/en/agent-sdk/slash-commands
   - https://code.claude.com/docs/en/slash-commands
2. 対象の特定: ユーザーの指示から対象の Command を特定し、既存の場合は Read して現状を把握する
3. 要件の整理: ユーザーの指示から Command の要件を整理する
4. 作成・修正の実施: 仕様と best practice に基づいて作成・修正する

ユーザーの意図がわからない場合は、`git status`や`git diff`を使って変更内容を確認して推測してください。
対象の Command や方針がわからない場合はユーザーに Ask してください。
おかしな点があればユーザーに報告してください。
