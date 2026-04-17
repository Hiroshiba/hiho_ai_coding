## Codex 向けアドバイス

- `gh`コマンドに権限が無い場合はサンドボックス由来を疑い、推測せずユーザーから承認を求めよ
- GitHub API の読み取りには `gh api` でなく `hiho_gh_api_read` を使え
  - rule で allow 設定済みのため承認なく実行できる
