import shutil
from pathlib import Path

KNOWN_RULE_FILES = {"html.md", "programming.md", "python.md"}


def get_project_rules_dir() -> Path:
    """プロジェクトの home/rules/ のパスを取得"""
    script_path = Path(__file__).resolve()
    return script_path.parent / "home" / "rules"


def get_claude_rules_dir() -> Path:
    """~/.claude/rules/ のパスを取得"""
    return Path.home() / ".claude" / "rules"


def check_unexpected_files(target_dir: Path, known_files: set[str]):
    """予期しないファイルの警告を出力"""
    existing_files = {f.name for f in target_dir.iterdir() if f.is_file()}
    unexpected_files = existing_files - known_files

    if unexpected_files:
        print("\n警告: ~/.claude/rules/ に予期しないファイルが見つかりました:")
        for file_name in sorted(unexpected_files):
            print(f"  - {file_name}")
        print("これらのファイルは手動で管理されているか、削除が必要かもしれません。")


def sync_rules():
    """ルールファイルを同期"""
    source_dir = get_project_rules_dir()
    target_dir = get_claude_rules_dir()

    if not source_dir.exists():
        raise FileNotFoundError(f"{source_dir} が見つかりません")

    target_dir.mkdir(parents=True, exist_ok=True)

    for file_name in KNOWN_RULE_FILES:
        source_file = source_dir / file_name
        if not source_file.exists():
            raise FileNotFoundError(f"{source_file} が見つかりません")
        target_file = target_dir / file_name
        shutil.copy2(source_file, target_file)
        print(f"{file_name} を同期しました")

    check_unexpected_files(target_dir, KNOWN_RULE_FILES)


def main():
    """ルールファイルを ~/.claude/rules/ に同期する"""
    sync_rules()


if __name__ == "__main__":
    main()
