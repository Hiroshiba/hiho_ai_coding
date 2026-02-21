---
description: Rule を作成・修正する
disable-model-invocation: true
---

Claude Code Rules や CLAUDE.md を作成・修正してください。

## 配置先

- **デフォルト**: `~/Github/hiho_ai_coding/base/rules/`
- **ローカル環境**: ユーザーが「ローカル環境」「この環境に」「この環境の」「このリポジトリに」「このリポジトリの」などと指示した場合は、現在の作業ディレクトリの `.claude/rules/` 以下を対象とする
- **CLAUDE.md**: ユーザーが「CLAUDE.md」と指示した場合は、現在の作業ディレクトリの `.claude/CLAUDE.md` を対象とする

## 手順

1. 仕様の確認: Context7 で Claude Code の Rule / CLAUDE.md に関するドキュメントを取得する
2. 対象の特定: ユーザーの指示から対象の Rule を特定し、既存の場合は Read して現状を把握する
3. 要件の整理: ユーザーの指示から Rule の要件を整理する
4. 作成・修正の実施: 仕様と best practice に基づいて作成・修正する

ユーザーの意図がわからない場合は、`git status`や`git diff`を使って変更内容を確認して推測してください。
対象の Rule や方針がわからない場合はユーザーに Ask してください。
おかしな点があればユーザーに報告してください。

## 原則

作成・修正する内容には、AI エージェントが既に知っていることを書かないでください。コンテキストウィンドウは共有リソースなので、AI が持っていない情報だけを含めてください。

### Rule ファイル固有の原則

- Rule は常時読み込まれるため、簡潔に保つ（CLAUDE.md は ~200 行が目安）
- 1 ファイル 1 関心事で分割する（例: `python.md`, `html.md`, `programming.md`）
- 命令形で書く（「〜せよ」「〜するな」）
- 参照資料が大きい場合は Skill に移す

### paths フロントマターの書き方

- YAML リスト形式は読み込まれないバグがある [Issue #16853](https://github.com/anthropics/claude-code/issues/16853)

Good:

```yaml
paths: "**/*.{ts,tsx}"
```

Bad (YAML リスト形式):

```yaml
paths:
  - "**/*.ts"
  - "**/*.tsx"
```
