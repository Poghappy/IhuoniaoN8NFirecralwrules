#!/bin/bash
# 文档整理执行脚本
# 用途: 自动重命名和重组文档文件
# 版本: v1.0

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo -e "${GREEN}开始文档整理...${NC}"

# 1. 创建备份
echo -e "${YELLOW}步骤 1: 创建备份...${NC}"
BACKUP_DIR=".backup/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp -r * "$BACKUP_DIR/" 2>/dev/null || true
echo -e "${GREEN}✓ 备份完成: $BACKUP_DIR${NC}"

# 2. 创建新目录结构
echo -e "${YELLOW}步骤 2: 创建目录结构...${NC}"
mkdir -p .cursor/rules
mkdir -p docs/{guides,ai-agents,project,features,design}
mkdir -p config/examples
mkdir -p code
echo -e "${GREEN}✓ 目录结构创建完成${NC}"

# 3. 移动规则文件
echo -e "${YELLOW}步骤 3: 移动规则文件...${NC}"
[ -f "agents.mdc" ] && mv "agents.mdc" .cursor/rules/ && echo "  ✓ agents.mdc"
[ -f "core-principles.mdc" ] && mv "core-principles.mdc" .cursor/rules/ && echo "  ✓ core-principles.mdc"
[ -f "development-standards.mdc" ] && mv "development-standards.mdc" .cursor/rules/ && echo "  ✓ development-standards.mdc"
[ -f "mcp-tools.mdc" ] && mv "mcp-tools.mdc" .cursor/rules/ && echo "  ✓ mcp-tools.mdc"
[ -f "quality-assurance.mdc" ] && mv "quality-assurance.mdc" .cursor/rules/ && echo "  ✓ quality-assurance.mdc"

# 4. 重命名和移动核心文档
echo -e "${YELLOW}步骤 4: 重命名和移动文档...${NC}"

# AI 智能体文档
[ -f "AI助手配置.md" ] && mv "AI助手配置.md" docs/ai-agents/ai-agent-config.md && echo "  ✓ AI助手配置.md → docs/ai-agents/ai-agent-config.md"
[ -f "AI助手提示词.md" ] && mv "AI助手提示词.md" docs/ai-agents/ai-agent-prompts.md && echo "  ✓ AI助手提示词.md → docs/ai-agents/ai-agent-prompts.md"
[ -f "AGENTS.md" ] && mv "AGENTS.md" docs/ai-agents/agents.md && echo "  ✓ AGENTS.md → docs/ai-agents/agents.md"

# 项目文档
[ -f "项目规则.md" ] && mv "项目规则.md" docs/project/project-rules.md && echo "  ✓ 项目规则.md → docs/project/project-rules.md"
[ -f "项目特定规则.md" ] && mv "项目特定规则.md" docs/project/project-specific-rules.md && echo "  ✓ 项目特定规则.md → docs/project/project-specific-rules.md"
[ -f "资源索引.md" ] && mv "资源索引.md" docs/project/resource-index.md && echo "  ✓ 资源索引.md → docs/project/resource-index.md"
[ -f "文档合并方案与最佳实践.md" ] && mv "文档合并方案与最佳实践.md" docs/project/docs-merge-plan-and-best-practices.md && echo "  ✓ 文档合并方案与最佳实践.md → docs/project/docs-merge-plan-and-best-practices.md"
[ -f "文档合并执行总结.md" ] && mv "文档合并执行总结.md" docs/project/docs-merge-summary.md && echo "  ✓ 文档合并执行总结.md → docs/project/docs-merge-summary.md"

# 功能特性文档
[ -f "爬取规则特性.md" ] && mv "爬取规则特性.md" docs/features/crawl-rules-features.md && echo "  ✓ 爬取规则特性.md → docs/features/crawl-rules-features.md"

# 设计文档
[ -f "DESIGN_Firecrawl文档整理.md" ] && mv "DESIGN_Firecrawl文档整理.md" docs/design/design-firecrawl-docs-organization.md && echo "  ✓ DESIGN_Firecrawl文档整理.md → docs/design/design-firecrawl-docs-organization.md"

# 指南文档
[ -f "Docker说明.md" ] && mv "Docker说明.md" docs/guides/docker-guide.md && echo "  ✓ Docker说明.md → docs/guides/docker-guide.md"
[ -f "CURSOR_CONFIG_MIGRATION.md" ] && mv "CURSOR_CONFIG_MIGRATION.md" docs/guides/cursor-config-migration.md && echo "  ✓ CURSOR_CONFIG_MIGRATION.md → docs/guides/cursor-config-migration.md"
[ -f "MCP_SETUP_GUIDE.md" ] && mv "MCP_SETUP_GUIDE.md" docs/guides/mcp-setup-guide.md && echo "  ✓ MCP_SETUP_GUIDE.md → docs/guides/mcp-setup-guide.md"
[ -f "cursor-git-guide.md" ] && mv "cursor-git-guide.md" docs/guides/cursor-git-guide.md && echo "  ✓ cursor-git-guide.md → docs/guides/cursor-git-guide.md"

# 5. 移动配置文件
echo -e "${YELLOW}步骤 5: 移动配置文件...${NC}"
[ -f "default-settings.json" ] && mv "default-settings.json" config/ && echo "  ✓ default-settings.json → config/"
[ -f "vercel.json" ] && mv "vercel.json" config/ && echo "  ✓ vercel.json → config/"
[ -f "aliyun-credentials.example.md" ] && mv "aliyun-credentials.example.md" config/examples/ && echo "  ✓ aliyun-credentials.example.md → config/examples/"
[ -f "openai-api-key.example.md" ] && mv "openai-api-key.example.md" config/examples/ && echo "  ✓ openai-api-key.example.md → config/examples/"
[ -f "requirements-project-bootstrap.md" ] && mv "requirements-project-bootstrap.md" config/examples/ && echo "  ✓ requirements-project-bootstrap.md → config/examples/"

# 删除重复文件
[ -f "defaultSettings.json" ] && rm -f "defaultSettings.json" && echo "  ✓ 删除重复文件: defaultSettings.json"

# 6. 移动代码文件
echo -e "${YELLOW}步骤 6: 移动代码文件...${NC}"
[ -f "flask_storage.py" ] && mv "flask_storage.py" code/flask-storage.py && echo "  ✓ flask_storage.py → code/flask-storage.py"
[ -f "supabase_client.py" ] && mv "supabase_client.py" code/supabase-client.py && echo "  ✓ supabase_client.py → code/supabase-client.py"

# 7. 移动其他规则文件
echo -e "${YELLOW}步骤 7: 移动其他规则文件...${NC}"
[ -f "global-rules.md" ] && mv "global-rules.md" docs/project/global-rules.md && echo "  ✓ global-rules.md → docs/project/global-rules.md"
[ -f "user-rules.md" ] && mv "user-rules.md" docs/project/user-rules.md && echo "  ✓ user-rules.md → docs/project/user-rules.md"

echo -e "${GREEN}✓ 文档整理完成！${NC}"
echo -e "${YELLOW}提示: 请检查整理结果，如有问题可从备份恢复: $BACKUP_DIR${NC}"

