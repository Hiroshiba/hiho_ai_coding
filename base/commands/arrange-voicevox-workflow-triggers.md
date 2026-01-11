---
description: VOICEVOX 向け GitHub Workflow トリガー整理（一時コマンド）
disable-model-invocation: true
---

このリポジトリの `.github/workflows/` 内のワークフローファイルの `on:` セクションを整理してください。

## 目的

フォークリポジトリで無駄なワークフロー実行を防ぐ。

## 整理ルール

### 1. `on.push` には必ずブランチ制限を追加

```yaml
# NG: フォークの全ブランチで実行されてしまう
on:
  push:

# OK
on:
  push:
    branches:
      - main  # または master（リポジトリのデフォルトブランチに合わせる）
```

### 2. `on.push` と `on.pull_request` の関係

`on.push: branches: [main]` だけだと PR 時にワークフローが実行されない。

**PR でも実行したい場合** → `pull_request` を追加:

```yaml
on:
  push:
    branches:
      - main
  pull_request: # PR 時にも実行される
```

**main マージ時のみで良い場合** → `push` のみ:

```yaml
on:
  push:
    branches:
      - main
# pull_request は不要（licenses チェックなど）
```

### 3. `workflow_dispatch` を追加

全てのワークフローに追加する。`on.push` にブランチ制限をつけても、PR 作成前にテストを実行したい場合は手動実行で対応できる。

### 4. 既存設定は保持

- `paths` フィルター
- `workflow_call`
- `schedule`
- `release`
- その他

## 除外対象

以下のファイルは VOICEVOX/preview-pages リポジトリ由来のため、変更しないこと:

- `DANGEROUS_trigger_preview_pages.yml`
- `merge_gatekeeper.yml`
- `build_preview_pages.yml`

## 作業前の確認

デフォルトブランチ名（main か master か）を確認してから作業を開始すること。
