---
description: Agent を作成・修正する
disable-model-invocation: true
---

Claude Code Agents を作成・修正してください。

## 配置先

- **デフォルト**: 現在のディレクトリの agent configuration JSON
- **ローカル環境**: ユーザーが「ローカル環境」「この環境に」「この環境の」「このリポジトリに」「このリポジトリの」などと指示した場合は、現在の作業ディレクトリを対象とする

## 手順

1. 仕様の確認: Context7 で Claude Code の Agent に関するドキュメントを取得する
2. 対象の特定: ユーザーの指示から対象の Agent を特定し、既存の場合は Read して現状を把握する
3. 要件の整理: ユーザーの指示から Agent の要件を整理する
4. 作成・修正の実施: ベストプラクティスに基づいて作成・修正する

ユーザーの意図がわからない場合は、`git status`や`git diff`を使って変更内容を確認して推測してください。
対象の Agent や方針がわからない場合はユーザーに Ask してください。
おかしな点があればユーザーに報告してください。

## 原則

作成・修正する内容には、AI エージェントが既に知っていることを書かないでください。コンテキストウィンドウは共有リソースなので、AI が持っていない情報だけを含めてください。

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
