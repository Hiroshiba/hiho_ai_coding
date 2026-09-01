# Claude AI Coding

Claude Code と Codex CLI の設定を管理するプロジェクトです。

## 使い方

### すべての設定を同期

```bash
uv run sync.py
```

**Claude Code**:

- `base/claude.json` → `~/.claude.json` にマージ
- `base/rules/*.md` → `~/.claude/rules/`
- `base/commands/*.md` → `~/.claude/commands/`
- `base/skills/<スキル名>/` → `~/.claude/skills/`
- `base/skills/claude/<スキル名>/` → `~/.claude/skills/`
- `base/agents/*.md` → `~/.claude/agents/`
- `base/settings.json` → `~/.claude/settings.json` にマージ

**Codex CLI** (`~/.codex/`):

- `base/rules/*.md` を結合して `AGENTS.md` を生成
- `base/config.toml` → `config.toml` にマージ
- `base/agents/*.md` → `agents/*.toml` に変換
- `base/skills/<スキル名>/` → `skills/`
- `base/skills/codex/<スキル名>/` → `skills/`

**グローバル gitignore**:

- `base/gitignore` のパターンを `git config --global core.excludesfile` のファイル (未設定なら `~/.config/git/ignore`) に不足分のみ追記
