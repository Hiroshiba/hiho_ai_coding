## コマンドメモ

- bashでjsonを解析する際は`jq`を使え
- ホームディレクトリ全体や `/mnt/c/Users` 全体など、広い範囲を `find`・`rg`・`grep` で再帰探索するな
  - 非常に重い
- `git add -A`は使うな
- `hiho` で始まるファイル・ディレクトリはグローバル gitignore で無視される
  - リポジトリ内に一時ファイルを作るなら `hiho` を頭に付けよ
- git worktree を作成する際は `<リポジトリのルート>/hiho_git_worktrees/<name>` に作成せよ
  - ルートは `dirname "$(git rev-parse --path-format=absolute --git-common-dir)"` で求めよ
- ブランチを最新に追従させるときは `git rebase` ではなく `git merge` を使え
  - rebase すると force push が必要になり、GitHub の PR コメントが参照先を見失うため
