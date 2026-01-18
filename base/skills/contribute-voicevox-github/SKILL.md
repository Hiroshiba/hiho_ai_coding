---
name: contribute-voicevox-github
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

## 文章の書き方

### 文体の把握

Issue や PR を作成する前に、依頼者の過去の Issue や PR を確認して文体を把握する。

```bash
# 依頼者の Issue を確認
gh issue list --repo VOICEVOX/{repo} --author {username} --state all --limit 5

# 依頼者の PR を確認
gh pr list --repo VOICEVOX/{repo} --author {username} --state all --limit 5
```

### 体言止めを避ける

本文は体言止めを使わず、文章として完結させる。箇条書き（Pros/Cons 等）は体言止めで問題ない。

Good:

```markdown
ブランチ制限がなく、フォークリポジトリで全ブランチに対してワークフローが実行されてしまいます。
```

Bad (本文が体言止め):

```markdown
ブランチ制限がなく、フォークリポジトリで全ブランチに対してワークフローが実行される状態。
```

## Issue 作成

テンプレートに従い、依頼者の文体に合わせて作成する。

## PR 作成

### ブランチ

VOICEVOX Organization のデフォルトブランチから新規作成する。現在のブランチから続ける方が適切な場合はそのまま進める。

### 説明文

テンプレートに従い、依頼者の文体に合わせて作成する。

**端的に書く**: 1-2 行で済むなら短く。文脈が複雑な場合のみ詳細に説明。

**リンク必須**:

- 関連 Issue
- 起点となったコメント
- 関連 PR スレッド

**方針が不明な場合は Ask**: 文章内容・分量・含めるべき項目が判断できない場合のみ確認する。「念のため」の確認は不要。
