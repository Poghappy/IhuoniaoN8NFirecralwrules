#!/bin/bash

# Docker Hub MCP Server 配置验证脚本
# 使用方法: ./verify_setup.sh

set -e

echo "🔍 Docker Hub MCP Server 配置验证"
echo "=================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查函数
check_pass() {
    echo -e "${GREEN}✅ $1${NC}"
}

check_fail() {
    echo -e "${RED}❌ $1${NC}"
}

check_warn() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# 1. 检查 Docker 是否安装
echo "1️⃣  检查 Docker 安装..."
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    check_pass "Docker 已安装: $DOCKER_VERSION"
else
    check_fail "Docker 未安装"
    echo "   请访问 https://www.docker.com/products/docker-desktop 安装 Docker Desktop"
    exit 1
fi

# 2. 检查 Docker 是否运行
echo ""
echo "2️⃣  检查 Docker 运行状态..."
if docker ps &> /dev/null; then
    check_pass "Docker 正在运行"
else
    check_fail "Docker 未运行"
    echo "   请启动 Docker Desktop"
    exit 1
fi

# 3. 检查 MCP 配置文件
echo ""
echo "3️⃣  检查 MCP 配置文件..."
MCP_CONFIG=".cursor/mcp.json"
if [ -f "$MCP_CONFIG" ]; then
    check_pass "MCP 配置文件存在: $MCP_CONFIG"

    # 检查是否包含占位符
    if grep -q "YOUR_DOCKER_HUB_USERNAME" "$MCP_CONFIG"; then
        check_warn "配置文件包含占位符 'YOUR_DOCKER_HUB_USERNAME'"
        echo "   请替换为你的 Docker Hub 用户名"
    fi

    if grep -q "YOUR_DOCKER_HUB_PERSONAL_ACCESS_TOKEN" "$MCP_CONFIG"; then
        check_warn "配置文件包含占位符 'YOUR_DOCKER_HUB_PERSONAL_ACCESS_TOKEN'"
        echo "   请替换为你的个人访问令牌"
    fi
else
    check_fail "MCP 配置文件不存在: $MCP_CONFIG"
    exit 1
fi

# 4. 检查 Docker Hub MCP Server 镜像
echo ""
echo "4️⃣  检查 Docker Hub MCP Server 镜像..."
if docker images | grep -q "docker/hub-mcp-server"; then
    IMAGE_INFO=$(docker images docker/hub-mcp-server:latest --format "{{.Repository}}:{{.Tag}} ({{.Size}})")
    check_pass "镜像已存在: $IMAGE_INFO"
else
    check_warn "镜像未找到,正在拉取..."
    if docker pull docker/hub-mcp-server:latest; then
        check_pass "镜像拉取成功"
    else
        check_fail "镜像拉取失败"
        echo "   请检查网络连接或尝试使用镜像加速"
        exit 1
    fi
fi

# 5. 测试镜像运行
echo ""
echo "5️⃣  测试镜像运行..."
if docker run --rm docker/hub-mcp-server:latest --help &> /dev/null; then
    check_pass "镜像可以正常运行"
else
    check_fail "镜像运行失败"
    exit 1
fi

# 6. 检查 .gitignore
echo ""
echo "6️⃣  检查 .gitignore 配置..."
if [ -f ".gitignore" ]; then
    if grep -q ".cursor/mcp.json" ".gitignore"; then
        check_pass ".gitignore 已配置保护敏感信息"
    else
        check_warn ".gitignore 未包含 .cursor/mcp.json"
        echo "   建议添加以防止提交敏感信息"
    fi
else
    check_warn ".gitignore 文件不存在"
fi

# 7. 检查文档
echo ""
echo "7️⃣  检查文档完整性..."
DOCS=("README.md" "QUICK_START.md" "EXAMPLES.md")
for doc in "${DOCS[@]}"; do
    if [ -f "$doc" ]; then
        check_pass "$doc 存在"
    else
        check_warn "$doc 不存在"
    fi
done

# 总结
echo ""
echo "=================================="
echo "📊 验证总结"
echo "=================================="
echo ""

# 检查是否所有关键步骤都通过
if docker ps &> /dev/null && [ -f "$MCP_CONFIG" ]; then
    echo -e "${GREEN}🎉 基础配置验证通过!${NC}"
    echo ""
    echo "📝 下一步操作:"
    echo ""
    echo "1. 编辑 .cursor/mcp.json 文件"
    echo "   - 替换 YOUR_DOCKER_HUB_USERNAME 为你的用户名"
    echo "   - 替换 YOUR_DOCKER_HUB_PERSONAL_ACCESS_TOKEN 为你的令牌"
    echo ""
    echo "2. 获取个人访问令牌:"
    echo "   https://hub.docker.com/settings/security"
    echo ""
    echo "3. 重启 Cursor"
    echo "   - 完全退出 Cursor"
    echo "   - 重新打开 Cursor"
    echo ""
    echo "4. 启动 MCP Server"
    echo "   - Cmd+Shift+P (或 Ctrl+Shift+P)"
    echo "   - 输入: MCP: List Servers"
    echo "   - 选择: docker-hub"
    echo "   - 点击: Start Server"
    echo ""
    echo "5. 测试功能"
    echo "   在 Cursor 中输入: \"List all repositories in my namespace\""
    echo ""
    echo "📚 查看完整文档:"
    echo "   - 快速开始: cat QUICK_START.md"
    echo "   - 详细说明: cat README.md"
    echo "   - 使用示例: cat EXAMPLES.md"
    echo ""
else
    echo -e "${RED}❌ 验证失败,请检查上述错误信息${NC}"
    exit 1
fi
