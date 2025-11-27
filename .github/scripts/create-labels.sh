#!/bin/bash
# GitHub 标签创建脚本
# 使用方法: ./create-labels.sh
# 需要设置 GITHUB_TOKEN 环境变量

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 配置
REPO="Poghappy/IhuoniaoN8NFirecralwrules"
API_URL="https://api.github.com/repos/${REPO}/labels"

# 检查 GITHUB_TOKEN
if [ -z "$GITHUB_TOKEN" ]; then
    echo -e "${RED}错误: 请设置 GITHUB_TOKEN 环境变量${NC}"
    echo "export GITHUB_TOKEN=your_token_here"
    exit 1
fi

# 标签定义
declare -a LABELS=(
    # 类型标签
    "bug|Bug 报告|d73a4a"
    "feature|新功能|0e8a16"
    "enhancement|功能增强|0052cc"
    "documentation|文档更新|0075ca"
    "question|问题咨询|d876e3"
    # 优先级标签
    "priority: high|高优先级|b60205"
    "priority: medium|中优先级|fbca04"
    "priority: low|低优先级|e4e669"
    # 状态标签
    "status: in-progress|进行中|1d76db"
    "status: blocked|已阻塞|ee0701"
    "status: needs-review|需要审查|fef2c0"
    "status: ready|就绪|0e8a16"
    # 技术标签
    "python|Python 相关|0052cc"
    "javascript|JavaScript 相关|d4c5f9"
    "api|API 相关|7057ff"
    "database|数据库相关|ededed"
    # 依赖标签
    "dependencies|依赖更新|0366d6"
    "github-actions|GitHub Actions|000000"
)

# 创建标签函数
create_label() {
    local name=$1
    local description=$2
    local color=$3

    echo -e "${YELLOW}创建标签: ${name}${NC}"

    # 检查标签是否已存在
    if curl -s -H "Authorization: token ${GITHUB_TOKEN}" \
            -H "Accept: application/vnd.github.v3+json" \
            "${API_URL}/${name}" | grep -q '"name"'; then
        echo -e "${YELLOW}  标签已存在，跳过${NC}"
        return
    fi

    # 创建标签
    response=$(curl -s -w "\n%{http_code}" -X POST \
        -H "Authorization: token ${GITHUB_TOKEN}" \
        -H "Accept: application/vnd.github.v3+json" \
        -H "Content-Type: application/json" \
        "${API_URL}" \
        -d "{\"name\":\"${name}\",\"description\":\"${description}\",\"color\":\"${color}\"}")

    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')

    if [ "$http_code" -eq 201 ]; then
        echo -e "${GREEN}  ✓ 标签创建成功${NC}"
    elif [ "$http_code" -eq 422 ]; then
        echo -e "${YELLOW}  ⚠ 标签可能已存在${NC}"
    else
        echo -e "${RED}  ✗ 创建失败 (HTTP ${http_code})${NC}"
        echo "$body" | jq '.' 2>/dev/null || echo "$body"
    fi
}

# 主函数
main() {
    echo -e "${GREEN}开始创建 GitHub 标签...${NC}"
    echo "仓库: ${REPO}"
    echo ""

    for label in "${LABELS[@]}"; do
        IFS='|' read -r name description color <<< "$label"
        create_label "$name" "$description" "$color"
    done

    echo ""
    echo -e "${GREEN}标签创建完成！${NC}"
    echo "访问 https://github.com/${REPO}/labels 查看所有标签"
}

# 运行主函数
main

