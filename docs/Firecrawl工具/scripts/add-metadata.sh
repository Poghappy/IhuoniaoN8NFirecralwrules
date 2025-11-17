#!/bin/bash
# 为文档添加元数据脚本
# 用途: 为缺少元数据的 Markdown 文档添加统一的元数据头部
# 版本: v1.0

set -e

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo -e "${GREEN}检查文档元数据...${NC}"

# 检查文件是否有元数据
check_metadata() {
    local file="$1"
    if [ -f "$file" ] && [ "${file##*.}" = "md" ]; then
        # 检查前 5 行是否包含元数据标记
        if ! head -5 "$file" | grep -q "^\*\*版本\*\*\|^\*\*创建时间\*\*\|^\*\*最后更新\*\*"; then
            echo "$file"
        fi
    fi
}

# 为文件添加元数据
add_metadata() {
    local file="$1"
    local title=$(basename "$file" .md)
    local dir=$(dirname "$file")
    local relative_dir=$(echo "$dir" | sed "s|^$PROJECT_ROOT/||")
    
    # 生成元数据
    local metadata="> **版本**: v1.0  
> **最后更新**: $(date +%Y-%m-%d)  
> **维护者**: AI Agent Team

"
    
    # 检查文件是否以 # 开头（已有标题）
    if head -1 "$file" | grep -q "^# "; then
        # 在标题后插入元数据
        sed -i.bak "1a\\
\\
$metadata" "$file"
        rm -f "${file}.bak"
    else
        # 在文件开头添加标题和元数据
        local title_text=$(echo "$title" | sed 's/-/ /g' | sed 's/_/ /g')
        {
            echo "# $title_text"
            echo ""
            echo "$metadata"
            cat "$file"
        } > "${file}.tmp" && mv "${file}.tmp" "$file"
    fi
}

# 查找需要添加元数据的文件
files_to_update=()
while IFS= read -r file; do
    if [ -n "$file" ]; then
        files_to_update+=("$file")
    fi
done < <(find docs/ 文档/ -name "*.md" -type f 2>/dev/null | while read file; do
    check_metadata "$file"
done)

if [ ${#files_to_update[@]} -eq 0 ]; then
    echo -e "${GREEN}✓ 所有文档都已包含元数据${NC}"
    exit 0
fi

echo -e "${YELLOW}发现 ${#files_to_update[@]} 个文件需要添加元数据${NC}"
echo -e "${YELLOW}提示: 此操作会修改文件，建议先备份${NC}"

# 询问是否继续
read -p "是否继续? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "已取消"
    exit 0
fi

# 为文件添加元数据
for file in "${files_to_update[@]}"; do
    echo "  处理: $file"
    add_metadata "$file"
done

echo -e "${GREEN}✓ 元数据添加完成${NC}"

