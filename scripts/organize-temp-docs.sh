#!/bin/bash
# 整理临时文档脚本
# 将临时文档移动到归档目录

set -e

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

ARCHIVE_DIR="docs/archive/temp-docs-$(date +%Y%m%d)"
TEMP_DOCS=(
    "EXECUTION_PROGRESS.md"
    "EXECUTION_SUMMARY.md"
    "NEXT_STEPS.md"
    "NEXT_ACTIONS_DETAILED.md"
    "PROJECT_STATUS_REPORT.md"
    "TASK_COMPLETION_SUMMARY.md"
    "STEP_BY_STEP_EXECUTION.md"
    "FINAL_SETUP_INSTRUCTIONS.md"
    "GITHUB_CONFIGURATION_COMPLETE.md"
    "INITIALIZATION_COMPLETE.md"
    "PROJECT_INIT.md"
    "SETUP_SUMMARY.md"
)

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}整理临时文档${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 创建归档目录
if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir -p "$ARCHIVE_DIR"
    echo -e "${GREEN}✓ 创建归档目录: $ARCHIVE_DIR${NC}"
fi

# 统计变量
MOVED=0
MISSING=0

# 移动文件
for doc in "${TEMP_DOCS[@]}"; do
    if [ -f "$doc" ]; then
        mv "$doc" "$ARCHIVE_DIR/"
        echo -e "${GREEN}✓ 已移动: $doc${NC}"
        MOVED=$((MOVED + 1))
    else
        echo -e "${YELLOW}⚠ 文件不存在: $doc${NC}"
        MISSING=$((MISSING + 1))
    fi
done

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo "移动文件数: $MOVED"
echo "缺失文件数: $MISSING"
echo "归档目录: $ARCHIVE_DIR"
echo ""

# 创建归档说明
cat > "$ARCHIVE_DIR/README.md" << 'EOF'
# 临时文档归档

本目录包含项目开发过程中的临时文档和状态报告。

## 文档说明

这些文档记录了项目配置和开发过程中的各个阶段，包括：

- 执行进度报告
- 任务完成总结
- 项目状态报告
- 配置完成报告
- 初始化文档

## 归档时间

$(date +"%Y-%m-%d %H:%M:%S")

## 注意事项

这些文档仅供参考，可能包含过时信息。如需最新信息，请查看项目主文档。
EOF

echo -e "${GREEN}✅ 临时文档整理完成！${NC}"
echo ""
echo "归档目录: $ARCHIVE_DIR"
echo ""
echo "如需恢复文件，可以从归档目录复制回根目录。"

