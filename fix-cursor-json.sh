#!/bin/bash
# Cursor JSON 文件修复脚本
# 用途: 修复 ~/.cursor 目录下损坏的 JSON 文件

set -e

echo "=== Cursor JSON 文件修复脚本 ==="
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 1. 修复空的 mcp-cache.json
echo "步骤 1: 修复空的 mcp-cache.json 文件..."
EMPTY_FILES=$(find ~/.cursor/projects -name "mcp-cache.json" -empty 2>/dev/null | wc -l | tr -d ' ')

if [ "$EMPTY_FILES" -gt 0 ]; then
    echo "  发现 $EMPTY_FILES 个空文件，正在修复..."
    find ~/.cursor/projects -name "mcp-cache.json" -empty -exec sh -c 'echo "{}" > "$1"' _ {} \;
    echo -e "  ${GREEN}✅ 修复完成${NC}"
else
    echo -e "  ${GREEN}✅ 没有发现空文件${NC}"
fi

# 2. 验证修复
echo ""
echo "步骤 2: 验证修复结果..."
FAILED=0
TOTAL=0

while IFS= read -r file; do
    TOTAL=$((TOTAL + 1))
    if ! python3 -m json.tool "$file" >/dev/null 2>&1; then
        echo -e "  ${YELLOW}⚠️  仍有问题: $file${NC}"
        FAILED=$((FAILED + 1))
    fi
done < <(find ~/.cursor/projects -name "mcp-cache.json" 2>/dev/null)

if [ "$FAILED" -eq 0 ]; then
    echo -e "  ${GREEN}✅ 所有项目文件验证通过 ($TOTAL 个文件)${NC}"
else
    echo -e "  ${YELLOW}⚠️  仍有 $FAILED 个文件需要检查${NC}"
fi

# 3. 检查扩展配置文件（仅报告，不修复）
echo ""
echo "步骤 3: 检查扩展配置文件（仅查看，不修复）..."
EXT_ISSUES=$(find ~/.cursor/extensions -name "*.json" \
  ! -path "*/vendor/*" \
  ! -path "*/node_modules/*" \
  ! -name "tsconfig*.json" \
  -exec sh -c 'if ! python3 -m json.tool "$1" >/dev/null 2>&1; then echo "$1"; fi' _ {} \; 2>/dev/null | wc -l | tr -d ' ')

if [ "$EXT_ISSUES" -gt 0 ]; then
    echo -e "  ${YELLOW}⚠️  发现 $EXT_ISSUES 个扩展配置文件可能有问题${NC}"
    echo "  注意: 这些文件可能支持 JSONC 格式（带注释），通常不需要修复"
    echo "  如需查看详情，请运行:"
    echo "    find ~/.cursor/extensions -name '*.json' ! -path '*/vendor/*' ! -path '*/node_modules/*' ! -name 'tsconfig*.json' -exec sh -c 'if ! python3 -m json.tool \"\$1\" >/dev/null 2>&1; then echo \"\$1\"; fi' _ {} \;"
else
    echo -e "  ${GREEN}✅ 扩展配置文件检查通过${NC}"
fi

echo ""
echo "=== 修复完成 ==="
echo ""
echo "提示: 如果仍有问题，请查看修复计划文档:"
echo "  .cursor/JSON文件修复计划.md"


