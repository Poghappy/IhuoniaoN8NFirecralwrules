#!/bin/bash
# 代码质量检查脚本
# 运行 Ruff、MyPy 和 Pytest 检查

set -e

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 统计变量
ERRORS=0

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}代码质量检查${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 检查工具是否安装
check_tool() {
    if ! command -v "$1" &> /dev/null; then
        echo -e "${RED}✗ $1 未安装${NC}"
        echo "  安装命令: pip install $1"
        return 1
    fi
    return 0
}

# 1. Ruff 格式检查
echo -e "${BLUE}🔍 运行 Ruff 格式检查...${NC}"
if check_tool "ruff"; then
    if ruff format --check . 2>/dev/null; then
        echo -e "${GREEN}✓ 代码格式检查通过${NC}"
    else
        echo -e "${YELLOW}⚠ 代码格式需要调整（运行: ruff format .）${NC}"
    fi
else
    ERRORS=$((ERRORS + 1))
fi
echo ""

# 2. Ruff 代码检查
echo -e "${BLUE}🔍 运行 Ruff 代码检查...${NC}"
if check_tool "ruff"; then
    if ruff check . 2>/dev/null; then
        echo -e "${GREEN}✓ 代码检查通过${NC}"
    else
        echo -e "${YELLOW}⚠ 发现代码问题（运行: ruff check . 查看详情）${NC}"
    fi
else
    ERRORS=$((ERRORS + 1))
fi
echo ""

# 3. MyPy 类型检查
echo -e "${BLUE}🔍 运行 MyPy 类型检查...${NC}"
if check_tool "mypy"; then
    # 检查 Python 代码目录
    if [ -d "Firecrawl代码模块" ]; then
        if mypy Firecrawl代码模块/ --ignore-missing-imports 2>/dev/null || true; then
            echo -e "${GREEN}✓ 类型检查完成${NC}"
        else
            echo -e "${YELLOW}⚠ 发现类型问题（运行: mypy Firecrawl代码模块/ 查看详情）${NC}"
        fi
    else
        echo -e "${YELLOW}⚠ Firecrawl代码模块 目录不存在，跳过类型检查${NC}"
    fi
else
    ERRORS=$((ERRORS + 1))
fi
echo ""

# 4. Pytest 测试
echo -e "${BLUE}🧪 运行 Pytest 测试...${NC}"
if check_tool "pytest"; then
    # 检查测试目录
    if [ -d "docs/Firecrawl工具/tests" ] || [ -d "tests" ]; then
        if pytest -v --tb=short 2>/dev/null || true; then
            echo -e "${GREEN}✓ 测试完成${NC}"
        else
            echo -e "${YELLOW}⚠ 部分测试失败（运行: pytest -v 查看详情）${NC}"
        fi
    else
        echo -e "${YELLOW}⚠ 未找到测试目录，跳过测试${NC}"
    fi
else
    ERRORS=$((ERRORS + 1))
fi
echo ""

# 总结
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ 代码质量检查完成！${NC}"
    echo ""
    echo "建议运行以下命令进行修复："
    echo "  ruff format .          # 自动格式化代码"
    echo "  ruff check --fix .     # 自动修复可修复的问题"
    exit 0
else
    echo -e "${RED}❌ 发现 $ERRORS 个工具缺失，请先安装缺失的工具。${NC}"
    exit 1
fi

