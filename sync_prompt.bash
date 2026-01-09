#!/bin/bash

# Claude Code用のプロンプト同期スクリプト

set -e

# 色の定義（ターミナル出力用）
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'  # 色リセット

# ディレクトリパスの定義
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="${SCRIPT_DIR}/home/rules"
TARGET_DIR="${HOME}/.claude/rules"

echo "======================================"
echo "Claude Code プロンプト同期スクリプト"
echo "======================================"
echo ""

# ソースディレクトリの存在確認
if [ ! -d "${SOURCE_DIR}" ]; then
    echo -e "${RED}エラー: ソースディレクトリが見つかりません: ${SOURCE_DIR}${NC}"
    exit 1
fi

# ターゲットディレクトリの作成（存在しない場合）
if [ ! -d "${TARGET_DIR}" ]; then
    echo "ターゲットディレクトリを作成します: ${TARGET_DIR}"
    mkdir -p "${TARGET_DIR}"
fi

# ソースディレクトリ内のファイルをリストアップ
echo "同期元: ${SOURCE_DIR}"
echo "同期先: ${TARGET_DIR}"
echo ""

# ソースファイルのリストを取得（隠しファイルを除く）
declare -a source_files
while IFS= read -r -d '' file; do
    source_files+=("$(basename "$file")")
done < <(find "${SOURCE_DIR}" -maxdepth 1 -type f ! -name ".*" -print0)

# ファイルが存在しない場合
if [ ${#source_files[@]} -eq 0 ]; then
    echo -e "${YELLOW}警告: 同期するファイルが見つかりません${NC}"
    exit 0
fi

# ファイルをコピー
echo "【ファイルコピー中】"
for file in "${source_files[@]}"; do
    cp "${SOURCE_DIR}/${file}" "${TARGET_DIR}/${file}"
    echo -e "${GREEN}✓${NC} ${file} をコピーしました"
done

echo ""
echo "【同期結果の確認】"

# ターゲットディレクトリ内のファイルをリストアップ
declare -a target_files
while IFS= read -r -d '' file; do
    target_files+=("$(basename "$file")")
done < <(find "${TARGET_DIR}" -maxdepth 1 -type f ! -name ".*" -print0)

# 余計なファイルのチェック
declare -a extra_files
for target_file in "${target_files[@]}"; do
    found=false
    for source_file in "${source_files[@]}"; do
        if [ "${target_file}" = "${source_file}" ]; then
            found=true
            break
        fi
    done

    if [ "${found}" = false ]; then
        extra_files+=("${target_file}")
    fi
done

# 余計なファイルがある場合は警告
if [ ${#extra_files[@]} -gt 0 ]; then
    echo -e "${YELLOW}⚠ 警告: 以下のファイルは同期元に存在しません（余計なファイルの可能性があります）:${NC}"
    for extra_file in "${extra_files[@]}"; do
        echo -e "  ${YELLOW}・${extra_file}${NC}"
    done
    echo ""
    echo "これらのファイルを削除する場合は、手動で削除してください。"
else
    echo -e "${GREEN}✓ 余計なファイルはありません${NC}"
fi

echo ""
echo "======================================"
echo -e "${GREEN}同期が完了しました！${NC}"
echo "======================================"
