---
description: Skill を作成・修正する
disable-model-invocation: true
---

Claude Code Skills を作成・修正してください。

## 配置先

- **デフォルト**: `~/Github/hiho_ai_coding/base/skills/`
- **ローカル環境**: ユーザーが「ローカル環境」「この環境に」「この環境の」「このリポジトリに」「このリポジトリの」などと指示した場合は、現在の作業ディレクトリの `.claude/skills/` 以下を対象とする

## 手順

1. 仕様の確認: 以下の URL を Fetch して Skill の仕様と best practice を把握する
   - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
   - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
2. 対象の特定: ユーザーの指示から対象の Skill を特定し、既存の場合は Read して現状を把握する
3. 要件の整理: ユーザーの指示から Skill の要件を整理する
4. 作成・修正の実施: 仕様と best practice に基づいて作成・修正する

ユーザーの意図がわからない場合は、`git status`や`git diff`を使って変更内容を確認して推測してください。
対象の Skill や方針がわからない場合はユーザーに Ask してください。
おかしな点があればユーザーに報告してください。

## Good/Bad 例の構成

- Good を先に示し、それに対する Bad を後に配置する
- Good と Bad の対応が複数ある場合は交互に出す
- Bad が複数ある場合は着眼点を書く

Good 1:

```markdown
Good:
Bad 1 (any を使う):
Bad 2 (型定義が不十分):
```

Bad 1 (着眼点がない):

```markdown
Good:
Bad 1:
Bad 2:
```

Good 2:

```markdown
Good 1:
Bad 1-1 (any を使う):
Bad 1-2 (型定義が不十分):
Good 2:
```

Bad 2 (Good と Bad の順番がおかしい):

```markdown
Good 1:
Good 2:
Bad 1-1 (any を使う):
Bad 1-2 (型定義が不十分):
```
