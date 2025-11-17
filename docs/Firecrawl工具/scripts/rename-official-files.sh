#!/bin/bash
# 规范化官方资料文件命名脚本
# 用途: 将 # 开头的文件重命名为 kebab-case
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
OFFICIAL_DIR="$PROJECT_ROOT/官方资料/01-快速开始"

cd "$OFFICIAL_DIR"

echo -e "${GREEN}开始规范化官方资料文件命名...${NC}"

# 文件重命名映射
declare -A RENAME_MAP=(
    ["# AI Platforms.md"]="ai-platforms.md"
    ["# Batch Scrape.md"]="batch-scrape.md"
    ["# Change Tracking.md"]="change-tracking.md"
    ["# Crawl.md"]="crawl.md"
    ["# Deep Research.md"]="deep-research.md"
    ["# Event Types.md"]="event-types.md"
    ["# Extract.md"]="extract.md"
    ["# Faster Scraping.md"]="faster-scraping.md"
    ["# JSON mode - Structured result.md"]="json-mode-structured-result.md"
    ["# Map.md"]="map.md"
    ["# Open Source vs Cloud.ini"]="open-source-vs-cloud.ini"
    ["# Product & E-commerce.md"]="product-ecommerce.md"
    ["# Proxies.md"]="proxies.md"
    ["# Scrape.md"]="scrape.md"
    ["# Search.md"]="search.md"
    ["# Security.md"]="security.md"
    ["# SEO Platforms.md"]="seo-platforms.md"
    ["# Stealth Mode.md"]="stealth-mode.md"
    ["# Testing & Debugging.md"]="testing-debugging.md"
    ["# Use Cases"]="use-cases.md"
)

# 执行重命名
renamed_count=0
for old_name in "${!RENAME_MAP[@]}"; do
    new_name="${RENAME_MAP[$old_name]}"
    if [ -f "$old_name" ] || [ -d "$old_name" ]; then
        mv "$old_name" "$new_name" 2>/dev/null && {
            echo "  ✓ $old_name → $new_name"
            ((renamed_count++))
        } || echo "  ⚠️  跳过: $old_name (可能不存在)"
    fi
done

echo -e "${GREEN}✓ 文件重命名完成，共重命名 $renamed_count 个文件${NC}"
echo -e "${YELLOW}提示: 请更新所有引用这些文件的链接${NC}"

