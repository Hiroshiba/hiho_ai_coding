---
description: Agent を作成する
disable-model-invocation: true
---

Claude Code Agents を作成してください。

## 配置先

- **デフォルト**: 現在のディレクトリに agent configuration JSON を作成
- **ローカル環境**: ユーザーが「ローカル環境」「この環境に」「このリポジトリに」などと指示した場合は、現在の作業ディレクトリに配置する

## 手順

1. 仕様の確認: Context7 で Agent 作成のベストプラクティスを調査
   - mcp\_\_context7\_\_resolve-library-id で "claude code" を検索
   - mcp\_\_context7\_\_query-docs で agent 作成方法を取得
2. 要件の整理: ユーザーの指示から作成する Agent の要件を整理
3. Configuration の設計:
   - identifier: lowercase + hyphen、3-50 文字
   - whenToUse: トリガー条件 + example blocks
   - systemPrompt: 責任、プロセス、出力形式
4. JSON の生成: Agent configuration JSON を作成

作成対象の Agent や作成方針がわからない場合はユーザーに Ask してください。
おかしな点があればユーザーに報告してください。

## Agent Configuration の構造

### identifier

命名規則: lowercase、hyphen、3-50 文字で具体的で機能を表す名前を使用する。

Good:

- `code-quality-reviewer`
- `api-docs-writer`
- `test-generator`

Bad 1 (generic):

- `helper`
- `utils`

Bad 2 (uppercase):

- `Code-Reviewer`

### whenToUse

明確なトリガー条件を記述し、`<example>` ブロックで具体的な使用シーンを示す。

Good:

```text
Use this agent when the user has written code and needs quality review.

<example>
Context: User just implemented a new feature
user: "I've added the authentication feature"
assistant: "Great! Let me review the code quality."
<commentary>
Code was written, trigger code-quality-reviewer agent.
</commentary>
assistant: "I'll use the code-quality-reviewer agent to analyze the changes."
</example>
```

Bad 1 (examples なし):

```text
Use this agent when reviewing code.
```

Bad 2 (曖昧):

```text
Use this agent when needed.
```

### systemPrompt

具体的な責任を列挙し、プロセスを明確化し、出力形式を指定する。

Good:

```text
You are an expert code quality reviewer.

**Your Core Responsibilities:**
1. Analyze code changes for quality issues
2. Identify security vulnerabilities
3. Check adherence to best practices

**Review Process:**
1. Read the code changes
2. Analyze for issues
3. Provide specific recommendations

**Output Format:**
1. Summary
2. Critical Issues
3. Major Issues
4. Minor Issues
```

Bad 1 (vague):

```text
You are a helper that reviews code.
```

Bad 2 (missing output format):

```text
You are an expert code reviewer. Review code and find issues.
```
