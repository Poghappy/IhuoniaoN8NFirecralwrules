#!/bin/bash
# 配置验证脚本
# 验证项目配置文件是否正确

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

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}配置验证${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 检查函数
check_pass() {
    echo -e "${GREEN}✓${NC} $1"
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
    ERRORS=$((ERRORS + 1))
}

check_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    WARNINGS=$((WARNINGS + 1))
}

# 1. 验证 pyproject.toml
echo -e "${BLUE}📦 验证 pyproject.toml...${NC}"
if [ -f "pyproject.toml" ]; then
    # 检查基本字段
    if grep -q "^\[project\]" pyproject.toml; then
        check_pass "pyproject.toml 包含 [project] 部分"
    else
        check_fail "pyproject.toml 缺少 [project] 部分"
    fi
    
    if grep -q "^name = " pyproject.toml; then
        check_pass "pyproject.toml 包含项目名称"
    else
        check_fail "pyproject.toml 缺少项目名称"
    fi
    
    if grep -q "^version = " pyproject.toml; then
        check_pass "pyproject.toml 包含版本号"
    else
        check_fail "pyproject.toml 缺少版本号"
    fi
    
    # 检查 Ruff 配置
    if grep -q "^\[tool.ruff\]" pyproject.toml; then
        check_pass "pyproject.toml 包含 Ruff 配置"
    else
        check_warn "pyproject.toml 缺少 Ruff 配置"
    fi
    
    # 检查 MyPy 配置
    if grep -q "^\[tool.mypy\]" pyproject.toml; then
        check_pass "pyproject.toml 包含 MyPy 配置"
    else
        check_warn "pyproject.toml 缺少 MyPy 配置"
    fi
    
    # 检查 Pytest 配置
    if grep -q "^\[tool.pytest.ini_options\]" pyproject.toml; then
        check_pass "pyproject.toml 包含 Pytest 配置"
    else
        check_warn "pyproject.toml 缺少 Pytest 配置"
    fi
else
    check_fail "pyproject.toml 文件不存在"
fi
echo ""

# 2. 验证 .gitignore
echo -e "${BLUE}🔒 验证 .gitignore...${NC}"
if [ -f ".gitignore" ]; then
    check_pass ".gitignore 文件存在"
    
    # 检查关键条目
    if grep -q "^\.env$" .gitignore; then
        check_pass ".env 在 .gitignore 中"
    else
        check_fail ".env 未在 .gitignore 中"
    fi
    
    if grep -q "^__pycache__" .gitignore; then
        check_pass "__pycache__ 在 .gitignore 中"
    else
        check_warn "__pycache__ 未在 .gitignore 中"
    fi
    
    if grep -q "^\.pytest_cache" .gitignore; then
        check_pass ".pytest_cache 在 .gitignore 中"
    else
        check_warn ".pytest_cache 未在 .gitignore 中"
    fi
else
    check_fail ".gitignore 文件不存在"
fi
echo ""

# 3. 验证 GitHub 配置
echo -e "${BLUE}🐙 验证 GitHub 配置...${NC}"
if [ -d ".github" ]; then
    check_pass ".github 目录存在"
    
    # 检查工作流
    if [ -f ".github/workflows/ci.yml" ]; then
        check_pass "CI 工作流存在"
    else
        check_warn "CI 工作流缺失"
    fi
    
    if [ -f ".github/workflows/codeql.yml" ]; then
        check_pass "CodeQL 工作流存在"
    else
        check_warn "CodeQL 工作流缺失"
    fi
    
    # 检查模板
    if [ -d ".github/ISSUE_TEMPLATE" ]; then
        check_pass "Issue 模板目录存在"
    else
        check_warn "Issue 模板目录缺失"
    fi
    
    if [ -f ".github/PULL_REQUEST_TEMPLATE.md" ]; then
        check_pass "PR 模板存在"
    else
        check_warn "PR 模板缺失"
    fi
    
    # 检查 Dependabot
    if [ -f ".github/dependabot.yml" ]; then
        check_pass "Dependabot 配置存在"
    else
        check_warn "Dependabot 配置缺失"
    fi
    
    # 检查 CODEOWNERS
    if [ -f ".github/CODEOWNERS" ]; then
        check_pass "CODEOWNERS 存在"
    else
        check_warn "CODEOWNERS 缺失"
    fi
else
    check_fail ".github 目录不存在"
fi
echo ""

# 4. 验证项目文档
echo -e "${BLUE}📚 验证项目文档...${NC}"
[ -f "README.md" ] && check_pass "README.md 存在" || check_fail "README.md 缺失"
[ -f "LICENSE" ] && check_pass "LICENSE 存在" || check_warn "LICENSE 缺失"
[ -f "SECURITY.md" ] && check_pass "SECURITY.md 存在" || check_warn "SECURITY.md 缺失"
[ -f "CHANGELOG.md" ] && check_pass "CHANGELOG.md 存在" || check_warn "CHANGELOG.md 缺失"
[ -f "CONTRIBUTING.md" ] && check_pass "CONTRIBUTING.md 存在" || check_warn "CONTRIBUTING.md 缺失"
echo ""

# 5. 验证代码目录
echo -e "${BLUE}📂 验证代码目录...${NC}"
[ -d "Firecrawl代码模块" ] && check_pass "Firecrawl代码模块 目录存在" || check_fail "Firecrawl代码模块 目录缺失"
[ -d "docs/Firecrawl工具" ] && check_pass "Firecrawl工具 文档目录存在" || check_warn "Firecrawl工具 文档目录缺失"
[ -d "scripts" ] && check_pass "scripts 目录存在" || check_warn "scripts 目录缺失"
echo ""

# 总结
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo "错误: $ERRORS"
echo "警告: $WARNINGS"
echo ""

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✅ 所有配置验证通过！${NC}"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠️  配置基本正确，但有 $WARNINGS 个警告需要关注。${NC}"
    exit 0
else
    echo -e "${RED}❌ 发现 $ERRORS 个配置错误，请修复后重试。${NC}"
    exit 1
fi

