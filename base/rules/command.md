## コマンドメモ

- bashでjsonを解析する際は`jq`を使え
- ホームディレクトリ全体や `/mnt/c/Users` 全体など、広い範囲を `find`・`rg`・`grep` で再帰探索するな
  - 非常に重い
- `git add -A`は使うな
- git worktree を作成する際は `$(git rev-parse --git-common-dir)/hiho-worktrees/<name>` 以下に作成せよ
  - リポジトリの親ディレクトリに `<repo>.worktrees` のような兄弟ディレクトリを作るな
  - `.git/worktrees/` はGit自身の管理領域なので使うな
