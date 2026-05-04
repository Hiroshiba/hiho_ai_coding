# Claude AI Coding

Claude Code と Codex CLI の設定を管理するプロジェクトです。

## 使い方

### すべての設定を同期

```bash
python sync.py
```

**Claude Code** (`~/.claude/`):

- `base/rules/*.md` → `rules/`
- `base/commands/*.md` → `commands/`
- `base/skills/` → `skills/`
- `base/agents/*.md` → `agents/`
- `base/settings.json` → `settings.json` にマージ

**Codex CLI** (`~/.codex/`):

- `base/rules/*.md` を結合して `AGENTS.md` を生成
- `base/skills/` → `skills/`

**グローバル gitignore**:

- `base/gitignore` のパターンを `git config --global core.excludesfile` のファイル (未設定なら `~/.config/git/ignore`) に不足分のみ追記
