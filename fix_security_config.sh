#!/bin/bash

# ========================================
# Docker Hub MCP Server 安全配置修复脚本
# ========================================
# 功能：修复 Docker Hub PAT 安全问题
# 作者：Cursor AI Agent
# 日期：2025-11-01
# ========================================

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Docker Hub MCP Server 安全配置修复${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# ========================================
# 1. 备份当前配置
# ========================================
echo -e "${YELLOW}[1/6] 备份当前配置...${NC}"

BACKUP_DIR=".backup/security_fix_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

if [ -f ".cursor/mcp.json" ]; then
    cp .cursor/mcp.json "$BACKUP_DIR/mcp.json.backup"
    echo -e "${GREEN}✓ 已备份 .cursor/mcp.json${NC}"
fi

if [ -f ".env" ]; then
    cp .env "$BACKUP_DIR/.env.backup"
    echo -e "${GREEN}✓ 已备份 .env${NC}"
fi

echo ""

# ========================================
# 2. 从当前配置提取 PAT
# ========================================
echo -e "${YELLOW}[2/6] 提取 Docker Hub PAT...${NC}"

# 使用 Python 提取 PAT（更可靠）
DOCKER_HUB_PAT=$(python3 << 'EOF'
import json
import sys

try:
    with open('.cursor/mcp.json', 'r') as f:
        config = json.load(f)

    args = config.get('mcpServers', {}).get('docker-hub', {}).get('args', [])

    # 查找 --pat 参数后的值
    for i, arg in enumerate(args):
        if arg == '--pat' and i + 1 < len(args):
            print(args[i + 1])
            sys.exit(0)

    print("NOT_FOUND")
except Exception as e:
    print(f"ERROR: {e}", file=sys.stderr)
    print("NOT_FOUND")
EOF
)

if [ "$DOCKER_HUB_PAT" = "NOT_FOUND" ] || [ -z "$DOCKER_HUB_PAT" ]; then
    echo -e "${RED}✗ 无法提取 Docker Hub PAT${NC}"
    echo -e "${YELLOW}请手动输入 Docker Hub PAT:${NC}"
    read -s DOCKER_HUB_PAT
    echo ""
fi

echo -e "${GREEN}✓ PAT 已提取（长度: ${#DOCKER_HUB_PAT} 字符）${NC}"
echo ""

# ========================================
# 3. 创建 .env 文件
# ========================================
echo -e "${YELLOW}[3/6] 创建 .env 文件...${NC}"

cat > .env << EOF
# ========================================
# Docker Hub MCP Server 环境变量
# ========================================
# 创建时间: $(date)
#
# 注意：此文件包含敏感信息，不应提交到 Git
# 已添加到 .gitignore
# ========================================

# Docker Hub Personal Access Token
# 获取地址: https://hub.docker.com/settings/security
DOCKER_HUB_PAT=$DOCKER_HUB_PAT

# Firecrawl API Key (可选)
# 获取地址: https://firecrawl.dev/
FIRECRAWL_API_KEY=fc-YOUR_API_KEY_HERE

# GitHub Personal Access Token (可选)
# 获取地址: https://github.com/settings/tokens
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_YOUR_TOKEN_HERE
EOF

chmod 600 .env  # 设置为仅所有者可读写
echo -e "${GREEN}✓ .env 文件已创建（权限: 600）${NC}"
echo ""

# ========================================
# 4. 更新 .cursor/mcp.json
# ========================================
echo -e "${YELLOW}[4/6] 更新 .cursor/mcp.json...${NC}"

python3 << 'EOF'
import json

# 读取当前配置
with open('.cursor/mcp.json', 'r') as f:
    config = json.load(f)

# 更新 docker-hub 配置
if 'mcpServers' in config and 'docker-hub' in config['mcpServers']:
    docker_hub = config['mcpServers']['docker-hub']

    # 查找并替换 PAT
    if 'args' in docker_hub:
        args = docker_hub['args']
        for i, arg in enumerate(args):
            if arg == '--pat' and i + 1 < len(args):
                args[i + 1] = '${env:DOCKER_HUB_PAT}'
                break

    # 添加 envFile 字段
    docker_hub['envFile'] = '${workspaceFolder}/.env'

# 更新 filesystem 配置（使用变量）
if 'mcpServers' in config and 'filesystem' in config['mcpServers']:
    filesystem = config['mcpServers']['filesystem']
    if 'args' in filesystem and len(filesystem['args']) > 2:
        # 替换路径为变量
        filesystem['args'][2] = '${workspaceFolder}'

# 写入更新后的配置
with open('.cursor/mcp.json', 'w') as f:
    json.dump(config, f, indent=2)

print("配置已更新")
EOF

echo -e "${GREEN}✓ .cursor/mcp.json 已更新${NC}"
echo ""

# ========================================
# 5. 创建配置模板
# ========================================
echo -e "${YELLOW}[5/6] 创建配置模板...${NC}"

cat > .cursor/mcp.json.example << 'EOF'
{
  "mcpServers": {
    "docker-hub": {
      "command": "uvx",
      "args": [
        "--from",
        "mcp-server-docker-hub",
        "mcp-server-docker-hub",
        "--pat",
        "${env:DOCKER_HUB_PAT}"
      ],
      "envFile": "${workspaceFolder}/.env"
    },
    "firecrawl": {
      "command": "npx",
      "args": ["-y", "firecrawl-mcp-server"],
      "env": {
        "FIRECRAWL_API_KEY": "${env:FIRECRAWL_API_KEY}"
      }
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${env:GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "${workspaceFolder}"]
    }
  }
}
EOF

echo -e "${GREEN}✓ 配置模板已创建：.cursor/mcp.json.example${NC}"
echo ""

# ========================================
# 6. 更新 .gitignore
# ========================================
echo -e "${YELLOW}[6/6] 更新 .gitignore...${NC}"

# 检查 .gitignore 是否存在
if [ ! -f ".gitignore" ]; then
    touch .gitignore
fi

# 添加 .env 到 .gitignore（如果尚未添加）
if ! grep -q "^\.env$" .gitignore; then
    echo "" >> .gitignore
    echo "# 环境变量文件（包含敏感信息）" >> .gitignore
    echo ".env" >> .gitignore
    echo ".env.local" >> .gitignore
    echo ".env.*.local" >> .gitignore
    echo -e "${GREEN}✓ 已添加 .env 到 .gitignore${NC}"
else
    echo -e "${GREEN}✓ .env 已在 .gitignore 中${NC}"
fi

echo ""

# ========================================
# 完成
# ========================================
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✓ 安全配置修复完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

echo -e "${BLUE}已完成的操作：${NC}"
echo -e "  1. ✓ 备份配置到 $BACKUP_DIR"
echo -e "  2. ✓ 创建 .env 文件（包含 Docker Hub PAT）"
echo -e "  3. ✓ 更新 .cursor/mcp.json（使用环境变量）"
echo -e "  4. ✓ 创建配置模板 .cursor/mcp.json.example"
echo -e "  5. ✓ 更新 .gitignore"
echo ""

echo -e "${BLUE}安全改进：${NC}"
echo -e "  • Docker Hub PAT 现在存储在 .env 文件中"
echo -e "  • .cursor/mcp.json 使用 \${env:DOCKER_HUB_PAT} 引用"
echo -e "  • .env 文件权限设置为 600（仅所有者可读写）"
echo -e "  • .env 已添加到 .gitignore"
echo -e "  • Filesystem 路径使用 \${workspaceFolder} 变量"
echo ""

echo -e "${YELLOW}下一步操作：${NC}"
echo -e "  1. 重启 Cursor 以加载新配置"
echo -e "  2. 测试 MCP Server 连接："
echo -e "     ${BLUE}在 Cursor 中输入：搜索 Docker Hub 上的官方 nginx 镜像${NC}"
echo -e "  3. 如需配置 Firecrawl 或 GitHub，编辑 .env 文件"
echo -e "  4. 运行验证脚本：${BLUE}./verify_setup.sh${NC}"
echo ""

echo -e "${YELLOW}备份位置：${NC}"
echo -e "  $BACKUP_DIR"
echo ""

echo -e "${RED}注意：${NC}"
echo -e "  • .env 文件包含敏感信息，请勿分享或提交到 Git"
echo -e "  • 定期轮换 Docker Hub PAT（建议每 3-6 个月）"
echo -e "  • 如需恢复配置，使用备份目录中的文件"
echo ""

# 显示当前 .cursor/mcp.json 内容（隐藏敏感信息）
echo -e "${BLUE}当前 MCP 配置（已隐藏敏感信息）：${NC}"
echo -e "${YELLOW}---${NC}"
cat .cursor/mcp.json | sed 's/dckr_pat_[a-zA-Z0-9_-]*/***HIDDEN***/g'
echo -e "${YELLOW}---${NC}"
echo ""

echo -e "${GREEN}✓ 脚本执行完成！${NC}"
