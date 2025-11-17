#!/bin/bash
# 规范化官方资料文件命名脚本 v2
# 用途: 将 # 开头的文件重命名为 kebab-case
# 版本: v2.0

set -e

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
OFFICIAL_DIR="$PROJECT_ROOT/官方资料/01-快速开始"

cd "$OFFICIAL_DIR"

echo -e "${GREEN}开始规范化官方资料文件命名...${NC}"

renamed_count=0

# 重命名文件
rename_file() {
    local old_name="$1"
    local new_name="$2"
    if [ -e "$old_name" ]; then
        mv "$old_name" "$new_name" && {
            echo "  ✓ $old_name → $new_name"
            ((renamed_count++))
        }
    fi
}

# 执行重命名
rename_file "# AI Platforms.md" "ai-platforms.md"
rename_file "# Batch Scrape.md" "batch-scrape.md"
rename_file "# Change Tracking.md" "change-tracking.md"
rename_file "# Crawl.md" "crawl.md"
rename_file "# Deep Research.md" "deep-research.md"
rename_file "# Event Types.md" "event-types.md"
rename_file "# Extract.md" "extract.md"
rename_file "# Faster Scraping.md" "faster-scraping.md"
rename_file "# JSON mode - Structured result.md" "json-mode-structured-result.md"
rename_file "# Map.md" "map.md"
rename_file "# Open Source vs Cloud.ini" "open-source-vs-cloud.ini"
rename_file "# Product & E-commerce.md" "product-ecommerce.md"
rename_file "# Proxies.md" "proxies.md"
rename_file "# Scrape.md" "scrape.md"
rename_file "# Search.md" "search.md"
rename_file "# Security.md" "security.md"
rename_file "# SEO Platforms.md" "seo-platforms.md"
rename_file "# Stealth Mode.md" "stealth-mode.md"
rename_file "# Testing & Debugging.md" "testing-debugging.md"
if [ -d "# Use Cases" ]; then
    rename_file "# Use Cases" "use-cases.md"
elif [ -f "# Use Cases" ]; then
    rename_file "# Use Cases" "use-cases.md"
fi

echo -e "${GREEN}✓ 文件重命名完成，共重命名 $renamed_count 个文件${NC}"
echo -e "${YELLOW}提示: 请更新所有引用这些文件的链接${NC}"

