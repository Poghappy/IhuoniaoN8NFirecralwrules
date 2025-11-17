#!/bin/bash
# 文档索引生成脚本
# 用途: 自动生成文档索引和导航
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

echo -e "${GREEN}开始生成文档索引...${NC}"

# 生成目录索引
generate_directory_index() {
    local dir="$1"
    local readme_file="$dir/README.md"
    
    if [ ! -d "$dir" ]; then
        return
    fi
    
    echo -e "${YELLOW}处理目录: $dir${NC}"
    
    # 如果 README.md 已存在，备份
    if [ -f "$readme_file" ]; then
        cp "$readme_file" "${readme_file}.bak"
    fi
    
    # 生成目录名称
    local dir_name=$(basename "$dir")
    local title=$(echo "$dir_name" | sed 's/-/ /g' | sed 's/_/ /g')
    
    # 生成 README.md 内容
    {
        echo "# $title"
        echo ""
        echo "> **最后更新**: $(date +%Y-%m-%d)"
        echo ""
        echo "## 📋 目录说明"
        echo ""
        echo "本目录包含 $title 相关的文档和资源。"
        echo ""
        echo "## 📚 文件列表"
        echo ""
        
        # 列出 Markdown 文件
        find "$dir" -maxdepth 1 -name "*.md" -type f ! -name "README.md" | sort | while read file; do
            local filename=$(basename "$file")
            local name=$(echo "$filename" | sed 's/\.md$//' | sed 's/-/ /g')
            echo "- [$name](./$filename)"
        done
        
        # 列出子目录
        find "$dir" -maxdepth 1 -type d ! -path "$dir" | sort | while read subdir; do
            local subdir_name=$(basename "$subdir")
            if [ -f "$subdir/README.md" ]; then
                echo "- [$subdir_name](./$subdir_name/)"
            fi
        done
        
        echo ""
        echo "## 🔗 相关链接"
        echo ""
        echo "- [返回项目首页](../../README.md)"
        
    } > "$readme_file"
    
    echo "  ✓ 生成: $readme_file"
}

# 生成主索引
generate_main_index() {
    echo -e "${YELLOW}生成主索引...${NC}"
    # 这里可以添加生成主 README.md 的逻辑
    echo "  ✓ 主索引已存在，跳过"
}

# 处理主要目录
directories=(
    "docs/guides"
    "docs/ai-agents"
    "docs/project"
    "docs/features"
    "docs/design"
    "code"
    "config"
    "examples"
    "scripts"
)

for dir in "${directories[@]}"; do
    if [ -d "$dir" ]; then
        generate_directory_index "$dir"
    fi
done

echo -e "${GREEN}✓ 文档索引生成完成！${NC}"
echo -e "${YELLOW}提示: 请检查生成的 README.md 文件，必要时手动调整${NC}"

