import json
from pathlib import Path


def check_claude_installed(claude_dir: Path):
    """Claude Code のインストール確認"""
    if not claude_dir.exists():
        raise FileNotFoundError(
            "エラー: Claude Code がインストールされていません。\n"
            "~/.claude ディレクトリが見つかりません。\n"
            "Claude Code をインストールしてから再度実行してください。"
        )


def get_project_settings_path() -> Path:
    """プロジェクトの home/rules/settings.json のパスを取得"""
    script_path = Path(__file__).resolve()
    return script_path.parent / "home" / "rules" / "settings.json"


def get_claude_settings_path() -> Path:
    """~/.claude/settings.json のパスを取得"""
    return Path.home() / ".claude" / "settings.json"


def load_json_file(file_path: Path) -> dict:
    """JSON ファイルを読み込む"""
    return json.loads(file_path.read_text())


def save_json_file(file_path: Path, data: dict):
    """JSON ファイルを保存"""
    file_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def merge_permissions(existing: dict, new: dict) -> dict:
    """permissions をマージ"""
    existing_allow = set(existing.get("permissions", {}).get("allow", []))
    existing_deny = set(existing.get("permissions", {}).get("deny", []))

    new_allow = set(new.get("permissions", {}).get("allow", []))
    new_deny = set(new.get("permissions", {}).get("deny", []))

    merged_allow = sorted(existing_allow | new_allow)
    merged_deny = sorted(existing_deny | new_deny)

    result = existing.copy()
    result["permissions"] = {"allow": merged_allow, "deny": merged_deny}

    return result


def main():
    """settings.json を ~/.claude/settings.json にマージする"""
    claude_dir = Path.home() / ".claude"
    check_claude_installed(claude_dir)

    project_settings_path = get_project_settings_path()
    claude_settings_path = get_claude_settings_path()

    new_settings = load_json_file(project_settings_path)

    if claude_settings_path.exists():
        existing_settings = load_json_file(claude_settings_path)
    else:
        existing_settings = {}

    merged_settings = merge_permissions(existing_settings, new_settings)
    save_json_file(claude_settings_path, merged_settings)

    print("settings.json を正常にマージしました")


if __name__ == "__main__":
    main()
