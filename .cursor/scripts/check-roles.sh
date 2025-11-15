#!/bin/bash

# 角色完整性检查脚本
# 版本: v2.0.0

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo "检查角色文件完整性..."
echo ""

roles=(
    "01_product_owner:PO"
    "02_product_manager:PM"
    "03_business_analyst:BA"
    "05_architect:Arch"
    "06_llm_engineer:LLME"
    "07_developer:DEV"
    "08_qa_engineer:QA"
    "09_devops:Ops"
    "10_technical_writer:TW"
)

missing=0

for role_info in "${roles[@]}"; do
    IFS=':' read -r filename code <<< "$role_info"
    file=".cursor/prompts/roles/${filename}.md"

    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $code: $file"
    else
        echo -e "${RED}✗${NC} $code: $file (缺失)"
        missing=$((missing + 1))
    fi
done

echo ""
if [ $missing -eq 0 ]; then
    echo -e "${GREEN}所有角色文件完整！${NC}"
    exit 0
else
    echo -e "${RED}缺失 $missing 个角色文件${NC}"
    exit 1
fi
