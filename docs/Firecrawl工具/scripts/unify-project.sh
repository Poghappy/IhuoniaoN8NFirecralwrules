#!/bin/bash

# 项目统一清理和合并脚本
# 用途: 统一多项目合并后的目录结构
# 版本: v1.0

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  项目统一清理和合并脚本${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 检查 Git 状态
if ! git diff --quiet || ! git diff --cached --quiet; then
    echo -e "${YELLOW}⚠️  警告: Git 工作区有未提交的更改${NC}"
    echo -e "${YELLOW}建议先提交或暂存当前更改${NC}"
    read -p "是否继续? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 创建备份
echo -e "${YELLOW}步骤 1: 创建备份...${NC}"
BACKUP_DIR=".backup/unify_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
echo "备份目录: $BACKUP_DIR"
echo ""

# 阶段一：合并代码目录
echo -e "${YELLOW}阶段一: 合并代码目录${NC}"
echo ""

# 方案：将 code/ 合并到 代码模块/core/
echo -e "${BLUE}步骤 1.1: 创建代码模块/core/ 目录...${NC}"
mkdir -p "代码模块/core"
echo -e "${GREEN}✓ 目录创建完成${NC}"

echo -e "${BLUE}步骤 1.2: 移动 code/ 文件到 代码模块/core/...${NC}"
if [ -f "code/flask-storage.py" ]; then
    cp "code/flask-storage.py" "代码模块/core/flask-storage.py"
    echo -e "${GREEN}✓ flask-storage.py${NC}"
fi
if [ -f "code/supabase-client.py" ]; then
    cp "code/supabase-client.py" "代码模块/core/supabase-client.py"
    echo -e "${GREEN}✓ supabase-client.py${NC}"
fi
if [ -f "code/README.md" ]; then
    cp "code/README.md" "代码模块/core/README.md"
    echo -e "${GREEN}✓ README.md${NC}"
fi

# 备份原 code/ 目录
if [ -d "code" ]; then
    cp -r "code" "$BACKUP_DIR/code_backup"
    echo -e "${GREEN}✓ code/ 目录已备份${NC}"
fi

echo ""

# 阶段二：合并文档目录
echo -e "${YELLOW}阶段二: 合并文档目录${NC}"
echo ""

if [ -d "文档" ] && [ "$(ls -A 文档 2>/dev/null)" ]; then
    echo -e "${BLUE}步骤 2.1: 移动 文档/ 内容到 docs/guides/...${NC}"
    # 文档目录已在之前移动，这里只是检查
    if [ -f "docs/guides/n8n-integration-guide.md" ]; then
        echo -e "${GREEN}✓ 文档已合并${NC}"
    fi
else
    echo -e "${GREEN}✓ 文档目录已合并或为空${NC}"
fi

echo ""

# 阶段三：更新链接和导入
echo -e "${YELLOW}阶段三: 更新链接和导入${NC}"
echo ""

echo -e "${BLUE}步骤 3.1: 更新测试文件中的导入路径...${NC}"

# 更新 test_flask_storage.py
if [ -f "tests/test_flask_storage.py" ]; then
    sed -i.bak 's/from code\.flask_storage/from 代码模块.core.flask_storage/g' "tests/test_flask_storage.py" 2>/dev/null || \
    sed -i '' 's/from code\.flask_storage/from 代码模块.core.flask_storage/g' "tests/test_flask_storage.py"
    echo -e "${GREEN}✓ test_flask_storage.py${NC}"
fi

# 更新 test_supabase_client.py
if [ -f "tests/test_supabase_client.py" ]; then
    sed -i.bak 's/from code\.supabase_client/from 代码模块.core.supabase_client/g' "tests/test_supabase_client.py" 2>/dev/null || \
    sed -i '' 's/from code\.supabase_client/from 代码模块.core.supabase_client/g' "tests/test_supabase_client.py"
    echo -e "${GREEN}✓ test_supabase_client.py${NC}"
fi

# 清理备份文件
find tests -name "*.bak" -delete 2>/dev/null || true

echo ""

# 阶段四：更新文档链接
echo -e "${YELLOW}阶段四: 更新文档链接${NC}"
echo ""

echo -e "${BLUE}步骤 4.1: 更新 README.md 中的链接...${NC}"
# 这里需要手动更新，因为涉及多个文件
echo -e "${YELLOW}⚠️  需要手动更新以下文档中的链接:${NC}"
echo "  - README.md"
echo "  - QUICKSTART.md"
echo "  - docs/guides/code-modules-guide.md"
echo "  - 其他引用 code/ 或 代码模块/ 的文档"

echo ""

# 阶段五：清理冗余目录（可选）
echo -e "${YELLOW}阶段五: 清理冗余目录（可选）${NC}"
echo ""

read -p "是否删除冗余目录 (myproject/, Users/)? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ -d "myproject" ]; then
        echo -e "${BLUE}备份 myproject/ 目录...${NC}"
        cp -r "myproject" "$BACKUP_DIR/myproject_backup" 2>/dev/null || true
        echo -e "${GREEN}✓ myproject/ 已备份${NC}"
        # 注意：不实际删除，因为已在 .gitignore 中
        echo -e "${YELLOW}⚠️  myproject/ 已在 .gitignore 中，建议手动删除${NC}"
    fi
    
    if [ -d "Users" ]; then
        echo -e "${BLUE}备份 Users/ 目录...${NC}"
        cp -r "Users" "$BACKUP_DIR/Users_backup" 2>/dev/null || true
        echo -e "${GREEN}✓ Users/ 已备份${NC}"
        # 注意：不实际删除，因为已在 .gitignore 中
        echo -e "${YELLOW}⚠️  Users/ 已在 .gitignore 中，建议手动删除${NC}"
    fi
fi

echo ""

# 完成
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  统一清理完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}备份位置: $BACKUP_DIR${NC}"
echo ""
echo -e "${YELLOW}下一步操作:${NC}"
echo "1. 检查更改: git status"
echo "2. 测试代码: pytest tests/ -v"
echo "3. 更新文档链接（手动）"
echo "4. 提交更改: git add -A && git commit -m 'chore: 统一项目结构'"
echo ""

