"""Claude Code / Codex CLI 設定同期スクリプト

このスクリプトは以下の同期処理を実行します:
- Git: main ブランチを origin/main に追従
- base/rules/*.md → ~/.claude/rules/
- base/commands/*.md → ~/.claude/commands/
- base/skills/ → ~/.claude/skills/
- base/agents/*.md → ~/.claude/agents/
- base/settings.json を ~/.claude/settings.json にマージ
- base/rules/*.md を結合して ~/.codex/AGENTS.md を生成
"""

import json
import shutil
import subprocess
from pathlib import Path


def get_project_root() -> Path:
    """プロジェクトルートディレクトリのパスを取得"""
    return Path(__file__).resolve().parent


def get_current_branch() -> str:
    """現在の Git ブランチ名を取得"""
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=get_project_root(),
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def sync_git_main():
    """main ブランチを origin/main に追従"""
    project_root = get_project_root()
    current_branch = get_current_branch()

    print("Git 同期を開始します...")
    print(f"現在のブランチ: {current_branch}")

    try:
        print("\norigin/main を fetch しています...")
        subprocess.run(
            ["git", "fetch", "origin", "main"],
            cwd=project_root,
            check=True,
        )

        print("main ブランチに切り替えています...")
        subprocess.run(
            ["git", "checkout", "main"],
            cwd=project_root,
            check=True,
        )

        print("origin/main に追従しています...")
        subprocess.run(
            ["git", "merge", "--ff-only", "origin/main"],
            cwd=project_root,
            check=True,
        )

        print("main ブランチを origin/main に追従させました")

    except subprocess.CalledProcessError as e:
        if current_branch != "main":
            print(f"\nエラーが発生したため、{current_branch} ブランチに戻します...")
            subprocess.run(
                ["git", "checkout", current_branch],
                cwd=project_root,
                check=False,
            )
        raise RuntimeError(
            f"Git 同期に失敗しました。\n"
            f"コマンドが失敗しました: {e.cmd}\n"
            f"手動で確認してください。"
        )

    finally:
        if current_branch != "main":
            print(f"\n{current_branch} ブランチに戻しています...")
            subprocess.run(
                ["git", "checkout", current_branch],
                cwd=project_root,
                check=True,
            )


def get_project_rules_dir() -> Path:
    """プロジェクトの base/rules/ のパスを取得"""
    script_path = Path(__file__).resolve()
    return script_path.parent / "base" / "rules"


def get_project_commands_dir() -> Path:
    """プロジェクトの base/commands/ のパスを取得"""
    script_path = Path(__file__).resolve()
    return script_path.parent / "base" / "commands"


def get_project_skills_dir() -> Path:
    """プロジェクトの base/skills/ のパスを取得"""
    script_path = Path(__file__).resolve()
    return script_path.parent / "base" / "skills"


def get_project_agents_dir() -> Path:
    """プロジェクトの base/agents/ のパスを取得"""
    script_path = Path(__file__).resolve()
    return script_path.parent / "base" / "agents"


def get_project_settings_path() -> Path:
    """プロジェクトの base/settings.json のパスを取得"""
    script_path = Path(__file__).resolve()
    return script_path.parent / "base" / "settings.json"


def get_claude_rules_dir() -> Path:
    """~/.claude/rules/ のパスを取得"""
    return Path.home() / ".claude" / "rules"


def get_claude_commands_dir() -> Path:
    """~/.claude/commands/ のパスを取得"""
    return Path.home() / ".claude" / "commands"


def get_claude_skills_dir() -> Path:
    """~/.claude/skills/ のパスを取得"""
    return Path.home() / ".claude" / "skills"


def get_claude_agents_dir() -> Path:
    """~/.claude/agents/ のパスを取得"""
    return Path.home() / ".claude" / "agents"


def get_claude_settings_path() -> Path:
    """~/.claude/settings.json のパスを取得"""
    return Path.home() / ".claude" / "settings.json"


def get_codex_agents_path() -> Path:
    """~/.codex/AGENTS.md のパスを取得"""
    return Path.home() / ".codex" / "AGENTS.md"


def check_claude_installed(claude_dir: Path):
    """Claude Code のインストール確認"""
    if not claude_dir.exists():
        raise FileNotFoundError(
            "エラー: Claude Code がインストールされていません。\n"
            "~/.claude ディレクトリが見つかりません。\n"
            "Claude Code をインストールしてから再度実行してください。"
        )


def check_codex_installed(codex_dir: Path):
    """Codex CLI のインストール確認"""
    if not codex_dir.exists():
        raise FileNotFoundError(
            "エラー: Codex CLI がインストールされていません。\n"
            "~/.codex ディレクトリが見つかりません。\n"
            "Codex CLI をインストールしてから再度実行してください。"
        )


def check_unexpected_files(target_dir: Path, known_files: set[str], dir_name: str):
    """予期しないファイルの警告を出力"""
    existing_files = {f.name for f in target_dir.iterdir() if f.is_file()}
    unexpected_files = existing_files - known_files

    if unexpected_files:
        print(f"\n警告: ~/.claude/{dir_name}/ に予期しないファイルが見つかりました:")
        for file_name in sorted(unexpected_files):
            print(f"  - {file_name}")
        print("これらのファイルは手動で管理されているか、削除が必要かもしれません。")


def sync_markdown_files(source_dir: Path, target_dir: Path, dir_name: str):
    """汎用的な Markdown ファイル同期"""
    if not source_dir.exists():
        raise FileNotFoundError(f"{source_dir} が見つかりません")

    target_dir.mkdir(parents=True, exist_ok=True)

    source_files = {f.name for f in source_dir.glob("*.md")}
    if not source_files:
        raise FileNotFoundError(f"{source_dir} に .md ファイルが見つかりません")

    for file_name in sorted(source_files):
        source_file = source_dir / file_name
        target_file = target_dir / file_name
        shutil.copy2(source_file, target_file)
        print(f"{file_name} を同期しました")

    check_unexpected_files(target_dir, source_files, dir_name)


def sync_rules():
    """ルールファイルを同期"""
    source_dir = get_project_rules_dir()
    target_dir = get_claude_rules_dir()
    sync_markdown_files(source_dir, target_dir, "rules")


def sync_commands():
    """コマンドファイルを同期"""
    source_dir = get_project_commands_dir()
    target_dir = get_claude_commands_dir()
    sync_markdown_files(source_dir, target_dir, "commands")


def sync_skills():
    """スキルディレクトリを同期"""
    source_dir = get_project_skills_dir()
    target_dir = get_claude_skills_dir()

    if not source_dir.exists():
        raise FileNotFoundError(f"{source_dir} が見つかりません")

    target_dir.mkdir(parents=True, exist_ok=True)

    for skill_dir in source_dir.iterdir():
        if skill_dir.is_dir():
            target_skill_dir = target_dir / skill_dir.name
            if target_skill_dir.exists():
                shutil.rmtree(target_skill_dir)
            shutil.copytree(skill_dir, target_skill_dir)
            print(f"{skill_dir.name}/ を同期しました")


def sync_agents():
    """エージェントファイルを同期"""
    source_dir = get_project_agents_dir()
    target_dir = get_claude_agents_dir()
    sync_markdown_files(source_dir, target_dir, "agents")


def load_json_file(file_path: Path) -> dict:
    """JSON ファイルを読み込む"""
    return json.loads(file_path.read_text())


def save_json_file(file_path: Path, data: dict):
    """JSON ファイルを保存"""
    file_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def merge_env(existing_env: dict[str, str], new_env: dict[str, str]) -> dict[str, str]:
    """env をマージ"""
    overwritten_keys = {}
    for key in existing_env:
        if key in new_env and existing_env[key] != new_env[key]:
            overwritten_keys[key] = (existing_env[key], new_env[key])

    if overwritten_keys:
        print("\n警告: settings.json の env に上書きされるキーが見つかりました:")
        for key, (old_val, new_val) in sorted(overwritten_keys.items()):
            print(f"  - {key}: '{old_val}' → '{new_val}'")

    result = existing_env.copy()
    result.update(new_env)
    return result


def merge_settings(existing: dict, new: dict) -> dict:
    """settings.json をマージ"""
    existing_allow = set(existing.get("permissions", {}).get("allow", []))
    existing_ask = set(existing.get("permissions", {}).get("ask", []))
    existing_deny = set(existing.get("permissions", {}).get("deny", []))

    new_allow = set(new.get("permissions", {}).get("allow", []))
    new_ask = set(new.get("permissions", {}).get("ask", []))
    new_deny = set(new.get("permissions", {}).get("deny", []))

    merged_allow = sorted(existing_allow | new_allow)
    merged_ask = sorted(existing_ask | new_ask)
    merged_deny = sorted(existing_deny | new_deny)

    result = existing.copy()

    for key in new:
        if key not in ("permissions", "env"):
            result[key] = new[key]

    result["permissions"] = {
        "allow": merged_allow,
        "ask": merged_ask,
        "deny": merged_deny,
    }

    existing_env = existing.get("env", {})
    new_env = new.get("env", {})
    if new_env:
        result["env"] = merge_env(existing_env, new_env)

    return result


def sync_settings():
    """設定ファイルをマージ"""
    project_settings_path = get_project_settings_path()
    claude_settings_path = get_claude_settings_path()

    new_settings = load_json_file(project_settings_path)

    if claude_settings_path.exists():
        existing_settings = load_json_file(claude_settings_path)
    else:
        existing_settings = {}

    merged_settings = merge_settings(existing_settings, new_settings)
    save_json_file(claude_settings_path, merged_settings)

    print("settings.json を正常にマージしました")


def strip_frontmatter(text: str) -> str:
    """YAML frontmatter を除去"""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return text

    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            remaining = lines[i + 1 :]
            while remaining and remaining[0].strip() == "":
                remaining.pop(0)
            return "\n".join(remaining)

    return text


def build_codex_agents_md(rules_dir: Path) -> str:
    """rules/*.md を結合して AGENTS.md 本文を生成"""
    priority_files = ["text.md", "programming.md"]

    for filename in priority_files:
        if not (rules_dir / filename).exists():
            raise FileNotFoundError(f"{rules_dir / filename} が見つかりません")

    other_files = sorted(
        f.name for f in rules_dir.glob("*.md") if f.name not in priority_files
    )

    sections = []
    for filename in priority_files + other_files:
        content = (rules_dir / filename).read_text()
        stripped = strip_frontmatter(content)
        if stripped.strip():
            sections.append(stripped.rstrip())

    return "\n\n".join(sections) + "\n"


def sync_codex_rules():
    """rules から ~/.codex/AGENTS.md を生成"""
    rules_dir = get_project_rules_dir()
    agents_path = get_codex_agents_path()

    agents_path.parent.mkdir(parents=True, exist_ok=True)
    agents_path.write_text(build_codex_agents_md(rules_dir))

    print("AGENTS.md を生成しました")


def main():
    """Claude Code と Codex CLI の設定を同期"""
    sync_git_main()

    claude_dir = Path.home() / ".claude"
    codex_dir = Path.home() / ".codex"
    check_claude_installed(claude_dir)
    check_codex_installed(codex_dir)

    print("\n設定ファイルの同期を開始します...")
    sync_rules()
    sync_commands()
    sync_skills()
    sync_agents()
    sync_settings()

    print("\nCodex 設定の同期を開始します...")
    sync_codex_rules()

    print("\n全ての同期が完了しました")


if __name__ == "__main__":
    main()
