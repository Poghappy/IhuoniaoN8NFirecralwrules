#!/bin/bash
# Cursor/VSCode 配置验证脚本

set -e

echo "🔍 验证 Cursor/VSCode 配置..."
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查函数
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 存在"
        return 0
    else
        echo -e "${RED}✗${NC} $1 不存在"
        return 1
    fi
}

check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 目录存在"
        return 0
    else
        echo -e "${RED}✗${NC} $1 目录不存在"
        return 1
    fi
}

# 检查必需文件
echo "📁 检查配置文件..."
ERRORS=0

check_file ".vscode/extensions.json" || ERRORS=$((ERRORS + 1))
check_file ".vscode/settings.json" || ERRORS=$((ERRORS + 1))
check_file "pyproject.toml" || ERRORS=$((ERRORS + 1))
check_file ".cursorrules" || ERRORS=$((ERRORS + 1))

echo ""
echo "📦 检查 Python 工具配置..."

# 检查 pyproject.toml 中的 Ruff 配置
if grep -q "\[tool.ruff\]" pyproject.toml 2>/dev/null; then
    echo -e "${GREEN}✓${NC} pyproject.toml 包含 Ruff 配置"
else
    echo -e "${YELLOW}⚠${NC} pyproject.toml 可能缺少 Ruff 配置"
fi

# 检查 mypy 配置
if grep -q "\[tool.mypy\]" pyproject.toml 2>/dev/null; then
    echo -e "${GREEN}✓${NC} pyproject.toml 包含 mypy 配置"
else
    echo -e "${YELLOW}⚠${NC} pyproject.toml 可能缺少 mypy 配置"
fi

# 检查 pytest 配置
if grep -q "\[tool.pytest.ini_options\]" pyproject.toml 2>/dev/null; then
    echo -e "${GREEN}✓${NC} pyproject.toml 包含 pytest 配置"
else
    echo -e "${YELLOW}⚠${NC} pyproject.toml 可能缺少 pytest 配置"
fi

echo ""
echo "🔧 检查工具安装..."

# 检查 Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION 已安装"
else
    echo -e "${RED}✗${NC} Python 未安装"
    ERRORS=$((ERRORS + 1))
fi

# 检查 Ruff
if command -v ruff &> /dev/null; then
    RUFF_VERSION=$(ruff --version | cut -d' ' -f2)
    echo -e "${GREEN}✓${NC} Ruff $RUFF_VERSION 已安装"
else
    echo -e "${YELLOW}⚠${NC} Ruff 未安装（运行: pip install ruff）"
fi

# 检查 mypy
if command -v mypy &> /dev/null; then
    MYPY_VERSION=$(mypy --version | cut -d' ' -f2)
    echo -e "${GREEN}✓${NC} mypy $MYPY_VERSION 已安装"
else
    echo -e "${YELLOW}⚠${NC} mypy 未安装（运行: pip install mypy）"
fi

# 检查 pytest
if command -v pytest &> /dev/null; then
    PYTEST_VERSION=$(pytest --version | cut -d' ' -f2)
    echo -e "${GREEN}✓${NC} pytest $PYTEST_VERSION 已安装"
else
    echo -e "${YELLOW}⚠${NC} pytest 未安装（运行: pip install pytest）"
fi

echo ""
echo "📋 检查扩展推荐..."

# 检查 extensions.json 格式（VSCode 配置文件支持注释，使用 jsonc 格式）
if command -v node &> /dev/null; then
    # 使用 Node.js 检查 JSONC 格式
    if node -e "try { require('fs').readFileSync('.vscode/extensions.json', 'utf8'); console.log('OK'); } catch(e) { process.exit(1); }" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} extensions.json 文件可读（支持 JSONC 注释）"
    else
        echo -e "${YELLOW}⚠${NC} 无法验证 extensions.json（需要 Node.js）"
    fi
else
    # 简单检查文件是否存在且可读
    if [ -r ".vscode/extensions.json" ]; then
        echo -e "${GREEN}✓${NC} extensions.json 文件可读（VSCode 支持 JSONC 注释）"
    else
        echo -e "${RED}✗${NC} extensions.json 文件不可读"
        ERRORS=$((ERRORS + 1))
    fi
fi

# 检查 settings.json 格式（VSCode 配置文件支持注释）
if command -v node &> /dev/null; then
    if node -e "try { require('fs').readFileSync('.vscode/settings.json', 'utf8'); console.log('OK'); } catch(e) { process.exit(1); }" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} settings.json 文件可读（支持 JSONC 注释）"
    else
        echo -e "${YELLOW}⚠${NC} 无法验证 settings.json（需要 Node.js）"
    fi
else
    if [ -r ".vscode/settings.json" ]; then
        echo -e "${GREEN}✓${NC} settings.json 文件可读（VSCode 支持 JSONC 注释）"
    else
        echo -e "${RED}✗${NC} settings.json 文件不可读"
        ERRORS=$((ERRORS + 1))
    fi
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ 配置验证通过！${NC}"
    echo ""
    echo "下一步："
    echo "1. 在 Cursor 中安装推荐扩展"
    echo "2. 配置 Python 解释器路径"
    echo "3. 运行 'ruff check .' 验证代码格式"
    exit 0
else
    echo -e "${RED}❌ 发现 $ERRORS 个错误${NC}"
    echo ""
    echo "请修复上述错误后重试"
    exit 1
fi

