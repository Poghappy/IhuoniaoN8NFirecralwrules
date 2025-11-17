#!/bin/bash
# 快速执行标签创建脚本的辅助脚本
# 使用方法: ./run-label-script.sh

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}GitHub 标签创建脚本${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 检查 GITHUB_TOKEN
if [ -z "$GITHUB_TOKEN" ]; then
    echo -e "${YELLOW}⚠ GITHUB_TOKEN 环境变量未设置${NC}"
    echo ""
    echo "请选择操作："
    echo "1. 手动输入 Token（仅当前会话有效）"
    echo "2. 查看如何获取 Token"
    echo "3. 退出"
    echo ""
    read -p "请选择 (1/2/3): " choice

    case $choice in
        1)
            read -sp "请输入 GitHub Token: " token
            echo ""
            export GITHUB_TOKEN="$token"
            ;;
        2)
            echo ""
            echo -e "${GREEN}获取 GitHub Token 的步骤：${NC}"
            echo "1. 访问: https://github.com/settings/tokens"
            echo "2. 点击 'Generate new token' > 'Generate new token (classic)'"
            echo "3. 设置权限: ✅ repo (完整仓库访问权限)"
            echo "4. 点击 'Generate token' 并复制 token"
            echo ""
            echo "然后运行:"
            echo "  export GITHUB_TOKEN=your_token_here"
            echo "  $0"
            exit 0
            ;;
        3)
            echo "退出"
            exit 0
            ;;
        *)
            echo -e "${RED}无效选择${NC}"
            exit 1
            ;;
    esac
fi

# 检查脚本是否存在
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LABEL_SCRIPT="${SCRIPT_DIR}/create-labels.sh"

if [ ! -f "$LABEL_SCRIPT" ]; then
    echo -e "${RED}错误: 找不到标签创建脚本${NC}"
    echo "预期位置: $LABEL_SCRIPT"
    exit 1
fi

# 检查脚本是否可执行
if [ ! -x "$LABEL_SCRIPT" ]; then
    echo -e "${YELLOW}设置脚本执行权限...${NC}"
    chmod +x "$LABEL_SCRIPT"
fi

# 运行脚本
echo -e "${GREEN}开始执行标签创建脚本...${NC}"
echo ""
"$LABEL_SCRIPT"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "访问以下链接查看标签："
echo "https://github.com/Poghappy/IhuoniaoN8NFirecralwrules/labels"

