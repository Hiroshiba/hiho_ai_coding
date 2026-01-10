---
name: voicevox-github-contrib
description: VOICEVOX Organization のリポジトリで Issue や PR を作成する。テンプレートの取得方法とフォーマットを案内。VOICEVOX への貢献時に使用。
---

# VOICEVOX GitHub 貢献

VOICEVOX Organization のリポジトリに Issue や PR を作成する際のガイド。

## テンプレートの優先順位

1. **対象リポジトリの `.github/` を先に確認**
2. なければ **VOICEVOX/.github リポジトリ**を参照

一部のリポジトリ（voicevox_core 等）は専用テンプレートを持つ。

## テンプレートの取得

### Issue テンプレート確認

```bash
# 1. 対象リポジトリを確認
gh api repos/VOICEVOX/{repo}/.github/ISSUE_TEMPLATE --jq '.[].name' 2>/dev/null

# 2. なければグローバルを確認
gh api repos/VOICEVOX/.github/contents/.github/ISSUE_TEMPLATE --jq '.[].name'
```

### Issue テンプレート取得

```bash
# 対象リポジトリから取得（存在する場合）
gh api repos/VOICEVOX/{repo}/contents/.github/ISSUE_TEMPLATE/{template}.md --jq '.content' | base64 -d

# グローバルから取得
gh api repos/VOICEVOX/.github/contents/.github/ISSUE_TEMPLATE/{template}.md --jq '.content' | base64 -d
```

利用可能なテンプレート名:

- `bugreport.md` - バグ報告
- `featurerequest.md` - 機能リクエスト
- `question.md` - 質問

### PR テンプレート確認・取得

```bash
# 1. 対象リポジトリを確認
gh api repos/VOICEVOX/{repo}/contents/.github/PULL_REQUEST_TEMPLATE.md --jq '.content' 2>/dev/null | base64 -d

# 2. なければグローバルを確認
gh api repos/VOICEVOX/.github/contents/.github/PULL_REQUEST_TEMPLATE.md --jq '.content' | base64 -d
```

## 注意事項

- `{repo}` は対象リポジトリ名に置き換える（例: `voicevox`, `voicevox_core`, `voicevox_engine`）
