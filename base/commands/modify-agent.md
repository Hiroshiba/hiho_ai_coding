---
description: Agent を修正する
disable-model-invocation: true
---

Claude Code Agents を修正してください。

## 対象の配置場所

- **デフォルト**: 現在のディレクトリの agent configuration JSON
- **ローカル環境**: ユーザーが「ローカル環境」「この環境の」「このリポジトリの」などと指示した場合は、現在の作業ディレクトリを対象とする

## 手順

1. 仕様の確認: Context7 で Agent のベストプラクティスを調査
   - mcp\_\_context7\_\_resolve-library-id で "claude code" を検索
   - mcp\_\_context7\_\_query-docs で agent 最適化方法を取得
2. 対象 Agent の特定: ユーザーの指示から修正対象の Agent を特定
3. 現状の確認: 対象 Agent configuration を Read して現在の内容を把握
4. 修正の実施: ベストプラクティスに基づいて修正

ユーザーの意図がわからない場合は、`git status`や`git diff`を使って変更内容を確認して推測してください。
修正対象の Agent や修正方針がわからない場合はユーザーに Ask してください。
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
