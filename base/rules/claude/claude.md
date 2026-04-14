## Claude Code 向けアドバイス

- `github.com` および `raw.githubusercontent.com` への WebFetch はするな
  - permissions で拒否されている
  - GitHub 情報の取得には `mcp__github__` ツールか `gh` CLI を使え
