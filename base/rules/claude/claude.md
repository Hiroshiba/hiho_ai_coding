## Claude Code 向けアドバイス

- `github.com` および `raw.githubusercontent.com` への WebFetch はするな
  - permissions で拒否されている
  - GitHub 情報の取得には `mcp__github__` ツールか `gh` CLI を使え
- 提案を求められたときはファイルを変更するな
  - 「diff を提案して」と言われた場合も、変更せず diff の内容だけを示せ
  - スクラッチパッドに変更後の内容を書き `git diff --no-index` を使えば、作業ツリーを変えずに diff を作れる
