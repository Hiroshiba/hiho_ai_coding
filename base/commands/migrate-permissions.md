---
description: ローカルパーミッションを base に移行する
disable-model-invocation: true
---

`.claude/settings.local.json` のパーミッションを `~/Github/hiho_ai_coding/base/settings.json` に移行してください。

## 手順

1. **読み込み**: 以下のファイルを読み込む
   - カレントディレクトリの `.claude/settings.local.json`
   - `~/Github/hiho_ai_coding/base/settings.json`

2. **分類**: `permissions.allow` の各項目を以下に分類
   - **汎用（移行対象）**: 下記の汎用パーミッション判定基準を参照
   - **リポジトリ固有（移行しない）**: 探索で判定
   - **判断困難（ユーザー確認）**: 上記で判断できないもの

3. **重複確認**: 移行対象から、すでに `base/settings.json` に存在するものを除外

4. **ユーザー確認**: 移行対象とその理由を一覧表示し、AskUserQuestion で確認

5. **移行実行**: 確認後、`base/settings.json` の `permissions.allow` に追加

6. **削除実行**: 移行した項目と base に存在する項目を `settings.local.json` から削除

7. **報告**: 移行結果（移行した項目、スキップした項目、削除した項目）を報告

## 汎用パーミッションの判定基準

### 基本的に汎用（移行OK）

- **WebFetch**: ドキュメントサイト等は汎用。ただしプロジェクト固有のドメインは除く
- **WebSearch**: 汎用
- **Bash read-only コマンド**: wc, tree, jq, ls, find, grep, rg, cat, head, tail, file, stat 等
- **mcp__github__ 系の read 操作**: get_*, list_*, search_* 等

### リポジトリ固有の可能性が高い（探索で判定）

- **Bash(pnpm run \*)** / **Bash(npm run \*)**: `package.json` のスクリプトを確認
  - そのスクリプトがカレントリポジトリの `package.json` にあれば固有
  - 汎用的なスクリプト名（lint, test, build, format 等）でも、特殊なオプションがあれば固有
- **Bash(python \*)** / **Bash(uv run \*)**: カレントリポジトリ内のファイルを実行していれば固有

### 判断困難（ユーザー確認）

- 上記に当てはまらないもの
- カスタムスクリプトやエイリアス

## 出力フォーマット例

```
## 移行対象（汎用）
- WebFetch(domain:example.com) - ドキュメントサイト
- Bash(jq:*) - read-only コマンド

## リポジトリ固有（移行しない）
- Bash(pnpm run buildSpecificThing:*) - package.json にスクリプトが存在

## すでに base に存在（local.json から削除）
- Bash(tree:*) - base/settings.json に存在

## ユーザー確認が必要
- Bash(custom-command:*) - 用途不明
```
