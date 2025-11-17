#!/bin/bash
# 文档验证脚本
# 用途: 自动化检查文档链接和格式
# 版本: v1.0

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo -e "${GREEN}开始验证文档...${NC}"

# 统计变量
total_files=0
files_with_metadata=0
files_without_metadata=0
broken_links=0
valid_links=0

# 检查文档元数据
check_metadata() {
    local file="$1"
    if head -5 "$file" 2>/dev/null | grep -q "版本\|创建时间\|最后更新"; then
        files_with_metadata=$((files_with_metadata + 1))
        return 0
    else
        files_without_metadata=$((files_without_metadata + 1))
        echo -e "  ${YELLOW}⚠️  缺少元数据: $file${NC}"
        return 1
    fi
}

# 检查文件命名规范
check_naming() {
    local file="$1"
    local basename=$(basename "$file")
    # 检查是否符合 kebab-case 或允许的中文命名
    if [[ ! "$basename" =~ ^[a-z0-9]+(-[a-z0-9]+)*\.(md|py|json|mdc|yml|yaml)$ ]] && \
       [[ ! "$basename" =~ ^[^#]*\.(md|py|json|mdc|yml|yaml)$ ]]; then
        echo -e "  ${YELLOW}⚠️  命名不规范: $file${NC}"
        return 1
    fi
    return 0
}

# 验证内部链接
validate_links() {
    local file="$1"
    # 提取 Markdown 链接
    while IFS= read -r line || [ -n "$line" ]; do
        # 匹配 [text](path) 格式 - 使用 grep 提取链接
        echo "$line" | grep -oE '\[([^\]]+)\]\(([^)]+)\)' | while IFS= read -r match; do
            # 提取链接路径部分
            link_path=$(echo "$match" | sed -E 's/\[([^\]]+)\]\(([^)]+)\)/\2/')
            # 跳过外部链接
            if echo "$link_path" | grep -qE '^(http|https|mailto|#|mdc:)'; then
                continue
            fi
            # 解析相对路径
            local file_dir=$(dirname "$file")
            local resolved_path=""
            if [ -d "$file_dir" ]; then
                resolved_path=$(cd "$file_dir" 2>/dev/null && realpath -m "$link_path" 2>/dev/null || echo "")
            fi
            if [ -z "$resolved_path" ] || [ ! -e "$resolved_path" ]; then
                echo -e "  ${RED}❌ 无效链接: $file -> $link_path${NC}"
                broken_links=$((broken_links + 1))
            else
                valid_links=$((valid_links + 1))
            fi
        done
    done < "$file"
}

# 主验证流程
echo -e "${YELLOW}步骤 1: 检查文档元数据...${NC}"
while IFS= read -r file; do
    total_files=$((total_files + 1))
    check_metadata "$file"
    check_naming "$file"
done < <(find . -name "*.md" -type f ! -path "./.git/*" ! -path "./.backup/*" ! -path "./node_modules/*" 2>/dev/null)

echo -e "${YELLOW}步骤 2: 验证文档链接...${NC}"
while IFS= read -r file; do
    validate_links "$file"
done < <(find . -name "*.md" -type f ! -path "./.git/*" ! -path "./.backup/*" ! -path "./node_modules/*" 2>/dev/null)

# 输出统计结果
echo ""
echo -e "${GREEN}验证完成！${NC}"
echo -e "  总文件数: $total_files"
echo -e "  有元数据: $files_with_metadata"
echo -e "  缺少元数据: $files_without_metadata"
echo -e "  有效链接: $valid_links"
echo -e "  无效链接: $broken_links"

if [ $broken_links -gt 0 ] || [ $files_without_metadata -gt 0 ]; then
    echo -e "${YELLOW}提示: 发现一些问题，请检查上述输出${NC}"
    exit 1
else
    echo -e "${GREEN}✓ 所有检查通过！${NC}"
    exit 0
fi

