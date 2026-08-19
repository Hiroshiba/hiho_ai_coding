"""Claude Code / Codex CLI 設定同期スクリプト

このスクリプトは以下の同期処理を実行します:
- Git: main ブランチを origin/main に追従
- base/rules/*.md と base/rules/claude/*.md → ~/.claude/rules/
- base/commands/*.md → ~/.claude/commands/
- base/skills/ と base/skills/claude/ → ~/.claude/skills/
- base/agents/*.md → ~/.claude/agents/
- base/settings.json を ~/.claude/settings.json にマージ
- base/rules/*.md と base/rules/codex/*.md を結合して ~/.codex/AGENTS.md を生成
- base/config.toml を ~/.codex/config.toml にマージ
- base/agents/*.md を ~/.codex/agents/*.toml に変換・同期
- base/skills/ と base/skills/codex/ → ~/.codex/skills/
- base/commands/*.md → ~/.codex/skills/ にスキルとして変換・同期
"""

import argparse
import json
import os
import shutil
import subprocess
from copy import deepcopy
from pathlib import Path
from typing import Literal

from tomlkit import TOMLDocument, document, dumps, parse, string, table
from tomlkit.exceptions import ParseError
from tomlkit.items import Table

SkillTarget = Literal["claude", "codex"]


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


def get_project_claude_only_rules_dir() -> Path:
    """プロジェクトの base/rules/claude/ のパスを取得"""
    return get_project_rules_dir() / "claude"


def get_project_codex_only_rules_dir() -> Path:
    """プロジェクトの base/rules/codex/ のパスを取得"""
    return get_project_rules_dir() / "codex"


def get_project_commands_dir() -> Path:
    """プロジェクトの base/commands/ のパスを取得"""
    script_path = Path(__file__).resolve()
    return script_path.parent / "base" / "commands"


def get_project_skills_dir() -> Path:
    """プロジェクトの base/skills/ のパスを取得"""
    script_path = Path(__file__).resolve()
    return script_path.parent / "base" / "skills"


def get_project_scoped_skills_dir(target: SkillTarget) -> Path:
    """対象固有の base/skills/ 配下のパスを取得"""
    return get_project_skills_dir() / target


def get_project_agents_dir() -> Path:
    """プロジェクトの base/agents/ のパスを取得"""
    script_path = Path(__file__).resolve()
    return script_path.parent / "base" / "agents"


def get_project_settings_path() -> Path:
    """プロジェクトの base/settings.json のパスを取得"""
    script_path = Path(__file__).resolve()
    return script_path.parent / "base" / "settings.json"


def get_project_codex_config_path() -> Path:
    """プロジェクトの base/config.toml のパスを取得"""
    script_path = Path(__file__).resolve()
    return script_path.parent / "base" / "config.toml"


def get_project_gitignore_path() -> Path:
    """プロジェクトの base/gitignore のパスを取得"""
    script_path = Path(__file__).resolve()
    return script_path.parent / "base" / "gitignore"


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


def parse_args() -> argparse.Namespace:
    """コマンドライン引数を解析"""
    parser = argparse.ArgumentParser(
        description="Claude Code と Codex CLI の設定を同期します"
    )
    parser.add_argument(
        "--codex-home",
        type=Path,
        default=Path.home() / ".codex",
        help="Codex のホームディレクトリを指定します",
    )
    return parser.parse_args()


def get_codex_agents_path(codex_home: Path) -> Path:
    """Codex の AGENTS.md のパスを取得"""
    return codex_home / "AGENTS.md"


def get_codex_skills_dir(codex_home: Path) -> Path:
    """Codex の skills/ のパスを取得"""
    return codex_home / "skills"


def get_codex_custom_agents_dir(codex_home: Path) -> Path:
    """Codex のカスタムエージェントディレクトリのパスを取得"""
    return codex_home / "agents"


def get_managed_codex_agents_path(codex_home: Path) -> Path:
    """Codex エージェントの同期管理情報のパスを取得"""
    return codex_home / ".hiho-ai-coding-managed-agents.json"


def get_codex_config_path(codex_home: Path) -> Path:
    """Codex の config.toml のパスを取得"""
    return codex_home / "config.toml"


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
            f"{codex_dir} が見つかりません。\n"
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
    common_dir = get_project_rules_dir()
    claude_only_dir = get_project_claude_only_rules_dir()
    target_dir = get_claude_rules_dir()

    if not common_dir.exists():
        raise FileNotFoundError(f"{common_dir} が見つかりません")

    target_dir.mkdir(parents=True, exist_ok=True)

    common_files = sorted(f.name for f in common_dir.glob("*.md"))
    if not common_files:
        raise FileNotFoundError(f"{common_dir} に .md ファイルが見つかりません")

    claude_only_files: list[str] = []
    if claude_only_dir.exists():
        claude_only_files = sorted(f.name for f in claude_only_dir.glob("*.md"))

    duplicates = set(common_files) & set(claude_only_files)
    if duplicates:
        raise RuntimeError(
            f"base/rules/ と base/rules/claude/ にファイル名の重複があります: {sorted(duplicates)}"
        )

    for file_name in common_files:
        shutil.copy2(common_dir / file_name, target_dir / file_name)
        print(f"{file_name} を同期しました")

    for file_name in claude_only_files:
        shutil.copy2(claude_only_dir / file_name, target_dir / file_name)
        print(f"claude/{file_name} を同期しました")

    known_files = set(common_files) | set(claude_only_files)
    check_unexpected_files(target_dir, known_files, "rules")


def sync_commands():
    """コマンドファイルを同期"""
    source_dir = get_project_commands_dir()
    target_dir = get_claude_commands_dir()
    sync_markdown_files(source_dir, target_dir, "commands")


def get_skill_directories(
    source_dir: Path,
    excluded_names: set[str],
) -> dict[str, Path]:
    """同期元にあるスキルディレクトリを取得"""
    if not source_dir.exists():
        raise FileNotFoundError(f"{source_dir} が見つかりません")
    if not source_dir.is_dir():
        raise NotADirectoryError(f"{source_dir} がディレクトリではありません")

    skill_directories: dict[str, Path] = {}
    for skill_dir in source_dir.iterdir():
        if skill_dir.name in excluded_names or not skill_dir.is_dir():
            continue
        if not (skill_dir / "SKILL.md").is_file():
            raise FileNotFoundError(f"{skill_dir / 'SKILL.md'} が見つかりません")
        skill_directories[skill_dir.name] = skill_dir

    return skill_directories


def get_project_skill_directories(target: SkillTarget) -> dict[str, Path]:
    """共通スキルと対象固有スキルのディレクトリを取得"""
    scoped_directory_names = {"claude", "codex"}
    common_skills = get_skill_directories(
        get_project_skills_dir(),
        scoped_directory_names,
    )
    scoped_skills = get_skill_directories(
        get_project_scoped_skills_dir(target),
        set(),
    )

    duplicate_names = set(common_skills) & set(scoped_skills)
    if len(duplicate_names) > 0:
        raise RuntimeError(
            f"共通スキルと {target} 専用スキルに同名のスキルがあります: "
            f"{sorted(duplicate_names)}"
        )

    return common_skills | scoped_skills


def get_managed_skills_path(target_dir: Path) -> Path:
    """同期管理情報のパスを取得"""
    managed_skills_file_name = ".hiho-ai-coding-managed-skills.json"
    return target_dir.parent / managed_skills_file_name


def validate_managed_skill_name(skill_name: str, managed_skills_path: Path) -> None:
    """同期管理情報のスキル名を検証"""
    if skill_name in {"", ".", ".."} or Path(skill_name).name != skill_name:
        raise RuntimeError(
            f"{managed_skills_path} に不正なスキル名があります: {skill_name}"
        )


def load_managed_skill_names(managed_skills_path: Path) -> set[str]:
    """同期管理情報からスキル名を読み込む"""
    if not managed_skills_path.exists():
        return set()

    data = json.loads(managed_skills_path.read_text())
    if not isinstance(data, dict) or set(data) != {"skills"}:
        raise RuntimeError(f"{managed_skills_path} の形式が不正です")

    skill_names = data["skills"]
    if not isinstance(skill_names, list) or not all(
        isinstance(skill_name, str) for skill_name in skill_names
    ):
        raise RuntimeError(f"{managed_skills_path} の skills が不正です")
    if len(skill_names) != len(set(skill_names)):
        raise RuntimeError(f"{managed_skills_path} の skills に重複があります")

    for skill_name in skill_names:
        validate_managed_skill_name(skill_name, managed_skills_path)

    return set(skill_names)


def save_managed_skill_names(
    managed_skills_path: Path,
    skill_names: set[str],
) -> None:
    """同期管理情報へスキル名を保存"""
    data = {"skills": sorted(skill_names)}
    managed_skills_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    )


def remove_stale_managed_skills(
    target_dir: Path,
    stale_skill_names: set[str],
) -> None:
    """同期対象から外れた管理スキルを削除"""
    for skill_name in sorted(stale_skill_names):
        target_skill_dir = target_dir / skill_name
        if not target_skill_dir.exists():
            continue
        if target_skill_dir.is_symlink() or not target_skill_dir.is_dir():
            raise RuntimeError(
                f"管理対象スキルの削除先が通常のディレクトリではありません: "
                f"{target_skill_dir}"
            )
        shutil.rmtree(target_skill_dir)
        print(f"{skill_name}/ を同期対象から削除しました")


def sync_skill_directories(
    source_skills: dict[str, Path],
    target_dir: Path,
) -> None:
    """スキルディレクトリを同期"""
    target_dir.mkdir(parents=True, exist_ok=True)
    managed_skills_path = get_managed_skills_path(target_dir)
    managed_skill_names = load_managed_skill_names(managed_skills_path)
    source_skill_names = set(source_skills)
    remove_stale_managed_skills(
        target_dir,
        managed_skill_names - source_skill_names,
    )

    for skill_name, skill_dir in sorted(source_skills.items()):
        target_skill_dir = target_dir / skill_name
        if target_skill_dir.exists():
            shutil.rmtree(target_skill_dir)
        shutil.copytree(skill_dir, target_skill_dir)
        print(f"{skill_name}/ を同期しました")

    save_managed_skill_names(managed_skills_path, source_skill_names)


def sync_skills() -> None:
    """Claude Code のスキルディレクトリを同期"""
    source_skills = get_project_skill_directories("claude")
    target_dir = get_claude_skills_dir()
    sync_skill_directories(source_skills, target_dir)


def sync_claude_agents() -> None:
    """Claude Code のエージェントファイルを同期"""
    source_dir = get_project_agents_dir()
    target_dir = get_claude_agents_dir()
    sync_markdown_files(source_dir, target_dir, "agents")


def parse_agent_frontmatter(agent_path: Path) -> tuple[dict[str, str], str]:
    """エージェントファイルの frontmatter と本文を解析"""
    lines = agent_path.read_text().splitlines()
    if len(lines) == 0 or lines[0].strip() != "---":
        raise RuntimeError(f"{agent_path} に frontmatter の開始行がありません")

    end_index: int | None = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_index = index
            break

    if end_index is None:
        raise RuntimeError(f"{agent_path} に frontmatter の終了行がありません")

    frontmatter: dict[str, str] = {}
    for line_number, line in enumerate(lines[1:end_index], start=2):
        if line.strip() == "":
            continue
        key, separator, value = line.partition(":")
        normalized_key = key.strip()
        normalized_value = value.strip()
        if separator == "" or normalized_key == "" or normalized_value == "":
            raise RuntimeError(f"{agent_path}:{line_number} の frontmatter が不正です")
        if normalized_key in frontmatter:
            raise RuntimeError(
                f"{agent_path}:{line_number} の frontmatter に "
                f"{normalized_key} が重複しています"
            )
        frontmatter[normalized_key] = normalized_value

    body = "\n".join(lines[end_index + 1 :]).strip("\n")
    if body.strip() == "":
        raise RuntimeError(f"{agent_path} に本文がありません")

    return frontmatter, body + "\n"


def parse_codex_agent_mcp_tools(
    tools_value: str,
    agent_path: Path,
) -> dict[str, list[str]]:
    """Claude Code のツール一覧を Codex の MCP ツール一覧へ変換"""
    raw_tool_names = tools_value.split(",")
    if any(raw_tool_name.strip() == "" for raw_tool_name in raw_tool_names):
        raise RuntimeError(f"{agent_path} の tools に空のツール名があります")

    tool_names = [raw_tool_name.strip() for raw_tool_name in raw_tool_names]
    if len(tool_names) != len(set(tool_names)):
        raise RuntimeError(f"{agent_path} の tools に重複があります")

    mcp_tools: dict[str, list[str]] = {}
    for tool_name in tool_names:
        if tool_name == "TodoWrite":
            continue
        if not tool_name.startswith("mcp__"):
            raise RuntimeError(
                f"{agent_path} に Codex へ変換できないツールがあります: {tool_name}"
            )

        server_name, separator, mcp_tool_name = tool_name.removeprefix(
            "mcp__"
        ).partition("__")
        if separator == "" or server_name == "" or mcp_tool_name == "":
            raise RuntimeError(f"{agent_path} の MCP ツール名が不正です: {tool_name}")

        if server_name not in mcp_tools:
            mcp_tools[server_name] = []
        mcp_tools[server_name].append(mcp_tool_name)

    return mcp_tools


def convert_claude_agent_model_to_codex(
    claude_model: str,
    agent_path: Path,
) -> tuple[str, str]:
    """Claude Code のモデル指定を Codex のモデル指定へ変換"""
    if claude_model == "sonnet":
        return "gpt-5.6-luna", "max"
    raise RuntimeError(
        f"{agent_path} に Codex へ変換できないモデル指定があります: {claude_model}"
    )


def convert_agent_to_codex_toml(
    agent_path: Path,
    mcp_server_configs: Table,
) -> tuple[str, str]:
    """Claude Code のエージェントを Codex の TOML へ変換"""
    frontmatter, body = parse_agent_frontmatter(agent_path)
    supported_fields = {"name", "description", "tools", "model", "color"}
    unexpected_fields = set(frontmatter) - supported_fields
    if len(unexpected_fields) > 0:
        raise RuntimeError(
            f"{agent_path} に Codex へ変換できない frontmatter 項目があります: "
            f"{sorted(unexpected_fields)}"
        )

    required_fields = {"name", "description"}
    missing_fields = required_fields - set(frontmatter)
    if len(missing_fields) > 0:
        raise RuntimeError(
            f"{agent_path} の frontmatter に必須項目がありません: "
            f"{sorted(missing_fields)}"
        )

    agent_name = frontmatter["name"]
    if agent_name != agent_path.stem:
        raise RuntimeError(
            f"{agent_path} のファイル名と name が一致しません: {agent_name}"
        )

    mcp_tools: dict[str, list[str]] = {}
    tools_value = frontmatter.get("tools")
    if tools_value is not None:
        mcp_tools = parse_codex_agent_mcp_tools(tools_value, agent_path)

    model_value = frontmatter.get("model")

    agent_document = document()
    agent_document["name"] = agent_name
    agent_document["description"] = frontmatter["description"]
    if model_value is not None:
        codex_model, reasoning_effort = convert_claude_agent_model_to_codex(
            model_value,
            agent_path,
        )
        agent_document["model"] = codex_model
        agent_document["model_reasoning_effort"] = reasoning_effort
    agent_document["developer_instructions"] = string(body, multiline=True)

    if len(mcp_tools) > 0:
        mcp_servers = table()
        for server_name in sorted(mcp_tools):
            source_server_config = mcp_server_configs.get(server_name)
            if not isinstance(source_server_config, Table):
                raise RuntimeError(
                    f"{get_project_codex_config_path()} に "
                    f"MCP サーバー設定がありません: {server_name}"
                )
            transport_fields = {"command", "url"} & set(source_server_config)
            if len(transport_fields) != 1:
                raise RuntimeError(
                    f"{get_project_codex_config_path()} の MCP サーバーには "
                    f"command または url のどちらか一方が必要です: {server_name}"
                )
            server_config = deepcopy(source_server_config)
            server_config["enabled_tools"] = mcp_tools[server_name]
            mcp_servers[server_name] = server_config
        agent_document["mcp_servers"] = mcp_servers

    content = dumps(agent_document)
    if not content.endswith("\n"):
        content += "\n"

    return f"{agent_name}.toml", content


def validate_managed_codex_agent_file_name(
    file_name: str,
    managed_agents_path: Path,
) -> None:
    """Codex エージェントの同期管理ファイル名を検証"""
    if (
        file_name in {"", ".", ".."}
        or Path(file_name).name != file_name
        or Path(file_name).suffix != ".toml"
    ):
        raise RuntimeError(
            f"{managed_agents_path} に不正なファイル名があります: {file_name}"
        )


def load_managed_codex_agent_file_names(managed_agents_path: Path) -> set[str]:
    """同期管理情報から Codex エージェントのファイル名を読み込む"""
    if managed_agents_path.is_symlink():
        raise RuntimeError(
            f"Codex エージェントの同期管理情報が通常のファイルではありません: "
            f"{managed_agents_path}"
        )
    if not managed_agents_path.exists():
        return set()
    if not managed_agents_path.is_file():
        raise RuntimeError(
            f"Codex エージェントの同期管理情報が通常のファイルではありません: "
            f"{managed_agents_path}"
        )

    data = json.loads(managed_agents_path.read_text())
    if not isinstance(data, dict) or set(data) != {"agents"}:
        raise RuntimeError(f"{managed_agents_path} の形式が不正です")

    file_names = data["agents"]
    if not isinstance(file_names, list) or not all(
        isinstance(file_name, str) for file_name in file_names
    ):
        raise RuntimeError(f"{managed_agents_path} の agents が不正です")
    if len(file_names) != len(set(file_names)):
        raise RuntimeError(f"{managed_agents_path} の agents に重複があります")

    for file_name in file_names:
        validate_managed_codex_agent_file_name(file_name, managed_agents_path)

    return set(file_names)


def save_managed_codex_agent_file_names(
    managed_agents_path: Path,
    file_names: set[str],
) -> None:
    """同期管理情報へ Codex エージェントのファイル名を保存"""
    data = {"agents": sorted(file_names)}
    managed_agents_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    )


def sync_codex_agents(codex_home: Path) -> None:
    """Codex のカスタムエージェントを変換して同期"""
    source_dir = get_project_agents_dir()
    if not source_dir.exists():
        raise FileNotFoundError(f"{source_dir} が見つかりません")
    if not source_dir.is_dir():
        raise NotADirectoryError(f"{source_dir} がディレクトリではありません")

    source_files = sorted(source_dir.glob("*.md"))
    if len(source_files) == 0:
        raise FileNotFoundError(f"{source_dir} に .md ファイルが見つかりません")

    config_path = get_project_codex_config_path()
    mcp_server_configs = load_toml_document(config_path).get("mcp_servers")
    if not isinstance(mcp_server_configs, Table):
        raise RuntimeError(f"{config_path} に mcp_servers がありません")

    generated_agents: dict[str, str] = {}
    for source_file in source_files:
        if source_file.is_symlink() or not source_file.is_file():
            raise RuntimeError(
                f"エージェントの同期元が通常のファイルではありません: {source_file}"
            )
        file_name, content = convert_agent_to_codex_toml(
            source_file,
            mcp_server_configs,
        )
        if file_name in generated_agents:
            raise RuntimeError(
                f"Codex エージェントの出力ファイル名が重複しています: {file_name}"
            )
        generated_agents[file_name] = content

    target_dir = get_codex_custom_agents_dir(codex_home)
    if target_dir.is_symlink():
        raise RuntimeError(
            f"Codex エージェントの同期先が通常のディレクトリではありません: "
            f"{target_dir}"
        )
    if target_dir.exists() and not target_dir.is_dir():
        raise RuntimeError(
            f"Codex エージェントの同期先が通常のディレクトリではありません: "
            f"{target_dir}"
        )

    managed_agents_path = get_managed_codex_agents_path(codex_home)
    managed_file_names = load_managed_codex_agent_file_names(managed_agents_path)
    generated_file_names = set(generated_agents)

    for file_name in sorted(managed_file_names | generated_file_names):
        target_file = target_dir / file_name
        if target_file.is_symlink():
            raise RuntimeError(
                f"Codex エージェントの同期先が通常のファイルではありません: "
                f"{target_file}"
            )
        if target_file.exists() and not target_file.is_file():
            raise RuntimeError(
                f"Codex エージェントの同期先が通常のファイルではありません: "
                f"{target_file}"
            )
        if target_file.exists() and file_name not in managed_file_names:
            raise RuntimeError(
                f"管理対象外の Codex エージェントを上書きできません: {target_file}"
            )

    target_dir.mkdir(parents=True, exist_ok=True)

    stale_file_names = managed_file_names - generated_file_names
    for file_name in sorted(stale_file_names):
        target_file = target_dir / file_name
        if not target_file.exists():
            continue
        target_file.unlink()
        print(f"{file_name} を Codex エージェントの同期対象から削除しました")

    for file_name, content in sorted(generated_agents.items()):
        (target_dir / file_name).write_text(content)
        print(f"{file_name} を Codex エージェントとして同期しました")

    save_managed_codex_agent_file_names(
        managed_agents_path,
        generated_file_names,
    )


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
    existing_permissions = existing.get("permissions", {})
    new_permissions = new.get("permissions", {})

    existing_allow = set(existing_permissions.get("allow", []))
    existing_ask = set(existing_permissions.get("ask", []))
    existing_deny = set(existing_permissions.get("deny", []))

    new_allow = set(new_permissions.get("allow", []))
    new_ask = set(new_permissions.get("ask", []))
    new_deny = set(new_permissions.get("deny", []))

    merged_allow = sorted(existing_allow | new_allow)
    merged_ask = sorted(existing_ask | new_ask)
    merged_deny = sorted(existing_deny | new_deny)

    result = existing.copy()

    for key in new:
        if key not in ("permissions", "env"):
            result[key] = new[key]

    merged_permissions = existing_permissions.copy()
    for key, value in new_permissions.items():
        if key not in ("allow", "ask", "deny"):
            merged_permissions[key] = value
    merged_permissions["allow"] = merged_allow
    merged_permissions["ask"] = merged_ask
    merged_permissions["deny"] = merged_deny
    result["permissions"] = merged_permissions

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


def get_global_gitignore_path() -> Path:
    """グローバル gitignore のパスを取得"""
    result = subprocess.run(
        ["git", "config", "--global", "--get", "core.excludesfile"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0 and result.stdout.strip():
        return Path(result.stdout.strip()).expanduser()

    xdg_config_home = os.environ.get("XDG_CONFIG_HOME", "")
    if xdg_config_home:
        return Path(xdg_config_home) / "git" / "ignore"
    return Path.home() / ".config" / "git" / "ignore"


def sync_gitignore():
    """グローバル gitignore に必要なパターンを追記"""
    target_path = get_global_gitignore_path()
    source_path = get_project_gitignore_path()

    if target_path.exists():
        existing_lines = {
            line.strip()
            for line in target_path.read_text().splitlines()
            if line.strip() and not line.strip().startswith("#")
        }
    else:
        existing_lines = set()

    source_patterns = [
        line.strip() for line in source_path.read_text().splitlines() if line.strip()
    ]
    missing_patterns = [p for p in source_patterns if p not in existing_lines]

    if not missing_patterns:
        print("グローバル gitignore は最新です")
        return

    target_path.parent.mkdir(parents=True, exist_ok=True)
    existing_content = target_path.read_text() if target_path.exists() else ""
    if existing_content and not existing_content.endswith("\n"):
        existing_content += "\n"
    target_path.write_text(existing_content + "\n".join(missing_patterns) + "\n")

    for pattern in missing_patterns:
        print(f"{pattern} をグローバル gitignore に追加しました")


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


def build_codex_agents_md(rules_dir: Path, codex_only_dir: Path) -> str:
    """rules/*.md と rules/codex/*.md を結合して AGENTS.md 本文を生成"""
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

    if codex_only_dir.exists():
        codex_only_files = sorted(f.name for f in codex_only_dir.glob("*.md"))
        for filename in codex_only_files:
            content = (codex_only_dir / filename).read_text()
            stripped = strip_frontmatter(content)
            if stripped.strip():
                sections.append(stripped.rstrip())

    return "\n\n".join(sections) + "\n"


def sync_codex_rules(codex_home: Path):
    """rules から Codex の AGENTS.md を生成"""
    rules_dir = get_project_rules_dir()
    codex_only_dir = get_project_codex_only_rules_dir()
    agents_path = get_codex_agents_path(codex_home)

    agents_path.parent.mkdir(parents=True, exist_ok=True)
    agents_path.write_text(build_codex_agents_md(rules_dir, codex_only_dir))

    print("AGENTS.md を生成しました")


def load_toml_document(file_path: Path) -> TOMLDocument:
    """TOMLファイルを読み込む"""
    try:
        return parse(file_path.read_text())
    except ParseError as error:
        raise RuntimeError(f"{file_path} のTOMLを解析できません") from error


def merge_toml_tables(
    existing_table: TOMLDocument | Table,
    new_table: TOMLDocument | Table,
) -> None:
    """TOMLテーブルを再帰的にマージする"""
    for key in new_table:
        new_item = new_table.item(key)
        if key in existing_table:
            existing_item = existing_table.item(key)
            if isinstance(existing_item, Table) and isinstance(new_item, Table):
                merge_toml_tables(existing_item, new_item)
                continue

        existing_table[key] = deepcopy(new_item)


def merge_toml_documents(
    existing_document: TOMLDocument,
    new_document: TOMLDocument,
) -> TOMLDocument:
    """TOML文書を再帰的にマージする"""
    merged_document = deepcopy(existing_document)
    merge_toml_tables(merged_document, new_document)
    return merged_document


def sync_codex_config(codex_home: Path):
    """Codex の config.toml をマージ"""
    source_path = get_project_codex_config_path()
    target_path = get_codex_config_path(codex_home)
    new_document = load_toml_document(source_path)
    if len(new_document) == 0:
        raise RuntimeError(f"{source_path} に設定が見つかりません")

    if target_path.exists():
        existing_document = load_toml_document(target_path)
    else:
        existing_document = document()

    target_path.parent.mkdir(parents=True, exist_ok=True)
    merged_document = merge_toml_documents(existing_document, new_document)
    merged_content = dumps(merged_document)
    if not merged_content.endswith("\n"):
        merged_content += "\n"
    target_path.write_text(merged_content)

    print("config.toml を正常にマージしました")


def sync_codex_skills(codex_home: Path) -> None:
    """Codex のスキルディレクトリを同期"""
    source_skills = get_project_skill_directories("codex")
    target_dir = get_codex_skills_dir(codex_home)
    sync_skill_directories(source_skills, target_dir)


def parse_command_frontmatter(content: str) -> tuple[dict[str, str], str]:
    """コマンドファイルの frontmatter と本文を分離"""
    lines = content.splitlines()

    if not lines or lines[0].strip() != "---":
        return {}, content

    end_index = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_index = i
            break

    if end_index is None:
        return {}, content

    frontmatter: dict[str, str] = {}
    for line in lines[1:end_index]:
        key, sep, value = line.partition(":")
        if sep:
            frontmatter[key.strip()] = value.strip()

    body = "\n".join(lines[end_index + 1 :])
    return frontmatter, body


def build_codex_openai_yaml(
    skill_name: str,
    disable_model_invocation: bool,
    argument_hint: str | None,
) -> str:
    """Codex の agents/openai.yaml を生成"""
    sections = []

    if argument_hint is not None:
        sections.append(
            f'interface:\n  default_prompt: "${skill_name} {argument_hint}"'
        )

    if disable_model_invocation:
        sections.append("policy:\n  allow_implicit_invocation: false")

    return "\n\n".join(sections) + "\n"


def convert_command_to_codex_skill(command_path: Path) -> tuple[str, str | None]:
    """コマンドファイルを Codex SKILL.md と openai.yaml に変換"""
    content = command_path.read_text()
    skill_name = command_path.stem
    frontmatter, body = parse_command_frontmatter(content)

    description = frontmatter.get("description", skill_name)

    skill_md = f"---\nname: {skill_name}\ndescription: {description}\n---\n{body}"
    if not skill_md.endswith("\n"):
        skill_md += "\n"

    disable_model_invocation = frontmatter.get("disable-model-invocation") == "true"
    argument_hint = frontmatter.get("argument-hint")

    openai_yaml = None
    if disable_model_invocation or argument_hint is not None:
        openai_yaml = build_codex_openai_yaml(
            skill_name, disable_model_invocation, argument_hint
        )

    return skill_md, openai_yaml


def sync_codex_commands(codex_home: Path) -> None:
    """コマンドを Codex スキルに変換して同期"""
    commands_dir = get_project_commands_dir()
    target_dir = get_codex_skills_dir(codex_home)

    if not commands_dir.exists():
        raise FileNotFoundError(f"{commands_dir} が見つかりません")

    target_dir.mkdir(parents=True, exist_ok=True)

    existing_skills = set(get_project_skill_directories("codex"))

    for command_file in sorted(commands_dir.glob("*.md")):
        skill_name = command_file.stem

        if skill_name in existing_skills:
            print(
                f"{skill_name} はスキルとして既に存在するため、コマンドからの変換をスキップしました"
            )
            continue

        skill_dir = target_dir / skill_name
        if skill_dir.exists():
            shutil.rmtree(skill_dir)
        skill_dir.mkdir(parents=True, exist_ok=True)

        skill_content, openai_yaml = convert_command_to_codex_skill(command_file)
        (skill_dir / "SKILL.md").write_text(skill_content)

        if openai_yaml is not None:
            agents_dir = skill_dir / "agents"
            agents_dir.mkdir(parents=True, exist_ok=True)
            (agents_dir / "openai.yaml").write_text(openai_yaml)

        print(f"{skill_name} をコマンドからスキルに変換しました")


def main():
    """Claude Code と Codex CLI の設定を同期"""
    args = parse_args()
    sync_git_main()

    claude_dir = Path.home() / ".claude"
    codex_dir = args.codex_home
    check_claude_installed(claude_dir)
    check_codex_installed(codex_dir)

    print("\n設定ファイルの同期を開始します...")
    sync_rules()
    sync_commands()
    sync_skills()
    sync_claude_agents()
    sync_settings()

    print("\nCodex 設定の同期を開始します...")
    sync_codex_rules(codex_dir)
    sync_codex_config(codex_dir)
    sync_codex_agents(codex_dir)
    sync_codex_skills(codex_dir)
    sync_codex_commands(codex_dir)

    print("\nグローバル gitignore の同期を開始します...")
    sync_gitignore()

    print("\n全ての同期が完了しました")


if __name__ == "__main__":
    main()
