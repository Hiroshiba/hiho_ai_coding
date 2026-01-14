---
description: Skill を作成する
disable-model-invocation: true
---

Claude Code Skills を作成してください。
Skill は `~/Github/hiho_ai_coding/base/skills/` 以下に配置します。

## 手順

1. 仕様の確認: 以下の URL を Fetch して Skill の仕様と best practice を把握する
   - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
   - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
2. 要件の整理: ユーザーの指示から作成する Skill の要件を整理する
3. 作成の実施: 仕様と best practice に基づいて作成する

作成対象の Skill や作成方針がわからない場合はユーザーに Ask してください。
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
