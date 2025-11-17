#!/bin/bash
# 项目健康检查脚本
# 检查项目配置、代码质量、文档完整性等

set -e

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 统计变量
ERRORS=0
WARNINGS=0
CHECKS=0

# 检查函数
check_pass() {
    echo -e "${GREEN}✓${NC} $1"
    CHECKS=$((CHECKS + 1))
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
    ERRORS=$((ERRORS + 1))
    CHECKS=$((CHECKS + 1))
}

check_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    WARNINGS=$((WARNINGS + 1))
    CHECKS=$((CHECKS + 1))
}

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}项目健康检查${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 1. 检查必需文件
echo -e "${BLUE}📁 检查必需文件...${NC}"
[ -f "README.md" ] && check_pass "README.md 存在" || check_fail "README.md 缺失"
[ -f "LICENSE" ] && check_pass "LICENSE 存在" || check_fail "LICENSE 缺失"
[ -f "SECURITY.md" ] && check_pass "SECURITY.md 存在" || check_fail "SECURITY.md 缺失"
[ -f "pyproject.toml" ] && check_pass "pyproject.toml 存在" || check_fail "pyproject.toml 缺失"
[ -f ".gitignore" ] && check_pass ".gitignore 存在" || check_fail ".gitignore 缺失"
[ -f ".github/workflows/ci.yml" ] && check_pass "CI 工作流存在" || check_fail "CI 工作流缺失"
echo ""

# 2. 检查配置文件
echo -e "${BLUE}⚙️  检查配置文件...${NC}"
[ -f ".github/dependabot.yml" ] && check_pass "Dependabot 配置存在" || check_warn "Dependabot 配置缺失"
[ -f ".github/CODEOWNERS" ] && check_pass "CODEOWNERS 存在" || check_warn "CODEOWNERS 缺失"
[ -f ".github/workflows/codeql.yml" ] && check_pass "CodeQL 工作流存在" || check_warn "CodeQL 工作流缺失"
echo ""

# 3. 检查 Python 代码质量工具
echo -e "${BLUE}🐍 检查 Python 工具...${NC}"
if command -v ruff &> /dev/null; then
    RUFF_VERSION=$(ruff --version | cut -d' ' -f2)
    check_pass "Ruff $RUFF_VERSION 已安装"
else
    check_warn "Ruff 未安装（运行: pip install ruff）"
fi

if command -v mypy &> /dev/null; then
    MYPY_VERSION=$(mypy --version | cut -d' ' -f2)
    check_pass "MyPy $MYPY_VERSION 已安装"
else
    check_warn "MyPy 未安装（运行: pip install mypy）"
fi

if command -v pytest &> /dev/null; then
    PYTEST_VERSION=$(pytest --version | cut -d' ' -f2)
    check_pass "Pytest $PYTEST_VERSION 已安装"
else
    check_warn "Pytest 未安装（运行: pip install pytest）"
fi
echo ""

# 4. 检查代码目录
echo -e "${BLUE}📂 检查代码目录...${NC}"
[ -d "Firecrawl代码模块" ] && check_pass "Firecrawl代码模块 目录存在" || check_fail "Firecrawl代码模块 目录缺失"
[ -d "docs/Firecrawl工具" ] && check_pass "Firecrawl工具 文档目录存在" || check_warn "Firecrawl工具 文档目录缺失"
[ -d ".github" ] && check_pass ".github 目录存在" || check_fail ".github 目录缺失"
echo ""

# 5. 检查敏感文件是否在 .gitignore 中
echo -e "${BLUE}🔒 检查安全配置...${NC}"
if grep -q "^\.env$" .gitignore 2>/dev/null; then
    check_pass ".env 已在 .gitignore 中"
else
    check_fail ".env 未在 .gitignore 中"
fi

if grep -q "^\.cursor/mcp\.json$" .gitignore 2>/dev/null; then
    check_pass ".cursor/mcp.json 已在 .gitignore 中"
else
    check_warn ".cursor/mcp.json 未在 .gitignore 中"
fi
echo ""

# 6. 检查临时文档文件
echo -e "${BLUE}📄 检查临时文档...${NC}"
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

TEMP_COUNT=0
for doc in "${TEMP_DOCS[@]}"; do
    if [ -f "$doc" ]; then
        TEMP_COUNT=$((TEMP_COUNT + 1))
    fi
done

if [ $TEMP_COUNT -gt 0 ]; then
    check_warn "发现 $TEMP_COUNT 个临时文档文件（建议归档）"
else
    check_pass "未发现临时文档文件"
fi
echo ""

# 7. 检查 Git 状态
echo -e "${BLUE}🔀 检查 Git 状态...${NC}"
if git rev-parse --git-dir > /dev/null 2>&1; then
    check_pass "Git 仓库已初始化"
    
    # 检查是否有未提交的更改
    if [ -n "$(git status --porcelain)" ]; then
        check_warn "存在未提交的更改"
    else
        check_pass "工作目录干净"
    fi
else
    check_fail "未检测到 Git 仓库"
fi
echo ""

# 总结
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}检查总结${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo "总检查数: $CHECKS"
echo -e "${GREEN}通过: $((CHECKS - ERRORS - WARNINGS))${NC}"
echo -e "${YELLOW}警告: $WARNINGS${NC}"
echo -e "${RED}错误: $ERRORS${NC}"
echo ""

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✅ 所有检查通过！项目状态良好。${NC}"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠️  项目状态良好，但有 $WARNINGS 个警告需要关注。${NC}"
    exit 0
else
    echo -e "${RED}❌ 发现 $ERRORS 个错误，请修复后重试。${NC}"
    exit 1
fi

