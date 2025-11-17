#!/bin/bash
# 更新内部链接脚本
# 用途: 更新所有 Markdown 文件中的内部链接路径
# 版本: v1.0

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo -e "${GREEN}开始更新内部链接...${NC}"

# 文件路径映射表（旧路径 -> 新路径）
declare -A LINK_MAP=(
    # 项目文档
    ["项目规则.md"]="docs/project/project-rules.md"
    ["项目特定规则.md"]="docs/project/project-specific-rules.md"
    ["资源索引.md"]="docs/project/resource-index.md"
    ["文档合并方案与最佳实践.md"]="docs/project/docs-merge-plan-and-best-practices.md"
    ["文档合并执行总结.md"]="docs/project/docs-merge-summary.md"
    ["global-rules.md"]="docs/project/global-rules.md"
    ["user-rules.md"]="docs/project/user-rules.md"
    
    # AI 智能体文档
    ["AI助手配置.md"]="docs/ai-agents/ai-agent-config.md"
    ["AI助手提示词.md"]="docs/ai-agents/ai-agent-prompts.md"
    ["AGENTS.md"]="docs/ai-agents/agents.md"
    
    # 功能特性
    ["爬取规则特性.md"]="docs/features/crawl-rules-features.md"
    
    # 设计文档
    ["DESIGN_Firecrawl文档整理.md"]="docs/design/design-firecrawl-docs-organization.md"
    
    # 指南文档
    ["Docker说明.md"]="docs/guides/docker-guide.md"
    ["CURSOR_CONFIG_MIGRATION.md"]="docs/guides/cursor-config-migration.md"
    ["MCP_SETUP_GUIDE.md"]="docs/guides/mcp-setup-guide.md"
    ["cursor-git-guide.md"]="docs/guides/cursor-git-guide.md"
    
    # 配置文件
    ["default-settings.json"]="config/default-settings.json"
    ["vercel.json"]="config/vercel.json"
    ["aliyun-credentials.example.md"]="config/examples/aliyun-credentials.example.md"
    ["openai-api-key.example.md"]="config/examples/openai-api-key.example.md"
    
    # 代码文件
    ["flask_storage.py"]="code/flask-storage.py"
    ["supabase_client.py"]="code/supabase-client.py"
)

# 更新文档中的链接
update_links_in_file() {
    local file="$1"
    local updated=0
    
    for old_path in "${!LINK_MAP[@]}"; do
        local new_path="${LINK_MAP[$old_path]}"
        
        # 处理相对路径链接
        if grep -q "\[.*\](\\.\\?/.*${old_path})" "$file" 2>/dev/null; then
            # 计算相对路径
            local file_dir=$(dirname "$file")
            local relative_path=$(python3 -c "
import os
old = '$old_path'
new = '$new_path'
file_dir = '$file_dir'
# 计算从 file_dir 到 new_path 的相对路径
if file_dir == '.':
    rel = new
else:
    rel = os.path.relpath(new, file_dir)
print(rel)
" 2>/dev/null || echo "$new_path")
            
            # 更新链接
            sed -i.bak "s|(\\.\\?/.*${old_path})|(${relative_path})|g" "$file" 2>/dev/null && updated=1
            rm -f "${file}.bak" 2>/dev/null || true
        fi
        
        # 处理直接文件名链接
        if grep -q "\[.*\](${old_path})" "$file" 2>/dev/null; then
            local file_dir=$(dirname "$file")
            local relative_path=$(python3 -c "
import os
old = '$old_path'
new = '$new_path'
file_dir = '$file_dir'
if file_dir == '.':
    rel = new
else:
    rel = os.path.relpath(new, file_dir)
print(rel)
" 2>/dev/null || echo "$new_path")
            
            sed -i.bak "s|(${old_path})|(${relative_path})|g" "$file" 2>/dev/null && updated=1
            rm -f "${file}.bak" 2>/dev/null || true
        fi
    done
    
    if [ $updated -eq 1 ]; then
        echo "  ✓ 更新: $file"
    fi
}

# 查找所有 Markdown 文件并更新链接
echo -e "${YELLOW}步骤 1: 更新 Markdown 文件中的链接...${NC}"
find . -name "*.md" -type f ! -path "./.git/*" ! -path "./.backup/*" | while read file; do
    update_links_in_file "$file"
done

echo -e "${GREEN}✓ 链接更新完成${NC}"

# 验证链接有效性
echo -e "${YELLOW}步骤 2: 验证链接有效性...${NC}"
python3 << 'PYTHON_SCRIPT'
import os
import re
from pathlib import Path

def find_markdown_files(root_dir):
    """查找所有 Markdown 文件"""
    md_files = []
    for root, dirs, files in os.walk(root_dir):
        # 跳过 .git 和 .backup 目录
        dirs[:] = [d for d in dirs if d not in ['.git', '.backup', 'node_modules']]
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    return md_files

def extract_links(content, file_path):
    """提取文件中的所有链接"""
    links = []
    # 匹配 Markdown 链接格式 [text](path)
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    for match in re.finditer(pattern, content):
        text = match.group(1)
        link_path = match.group(2)
        # 跳过外部链接
        if link_path.startswith('http://') or link_path.startswith('https://') or link_path.startswith('mailto:'):
            continue
        # 跳过锚点链接
        if link_path.startswith('#'):
            continue
        links.append({
            'text': text,
            'path': link_path,
            'file': file_path
        })
    return links

def resolve_path(link_path, base_file):
    """解析链接路径"""
    base_dir = os.path.dirname(base_file)
    # 处理相对路径
    if link_path.startswith('./'):
        link_path = link_path[2:]
    elif link_path.startswith('../'):
        # 计算相对路径
        full_path = os.path.normpath(os.path.join(base_dir, link_path))
        return full_path
    else:
        full_path = os.path.normpath(os.path.join(base_dir, link_path))
        return full_path

def validate_links(root_dir):
    """验证所有链接"""
    md_files = find_markdown_files(root_dir)
    broken_links = []
    valid_links = []
    
    for md_file in md_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            links = extract_links(content, md_file)
            
            for link in links:
                resolved_path = resolve_path(link['path'], md_file)
                # 检查文件是否存在
                if os.path.exists(resolved_path):
                    valid_links.append(link)
                else:
                    # 检查是否是目录（可能指向目录中的 README.md）
                    if os.path.isdir(resolved_path):
                        readme_path = os.path.join(resolved_path, 'README.md')
                        if os.path.exists(readme_path):
                            valid_links.append(link)
                        else:
                            broken_links.append({
                                'file': md_file,
                                'link': link['path'],
                                'resolved': resolved_path,
                                'text': link['text']
                            })
                    else:
                        broken_links.append({
                            'file': md_file,
                            'link': link['path'],
                            'resolved': resolved_path,
                            'text': link['text']
                        })
        except Exception as e:
            print(f"  错误: 无法读取文件 {md_file}: {e}")
    
    return valid_links, broken_links

# 执行验证
root_dir = os.getcwd()
print(f"  正在验证链接...")
valid_links, broken_links = validate_links(root_dir)

print(f"  ✓ 有效链接: {len(valid_links)}")
if broken_links:
    print(f"  ⚠️  无效链接: {len(broken_links)}")
    for link in broken_links[:10]:  # 只显示前10个
        print(f"    - {link['file']}: {link['link']} -> {link['resolved']}")
    if len(broken_links) > 10:
        print(f"    ... 还有 {len(broken_links) - 10} 个无效链接")
else:
    print(f"  ✓ 所有链接有效！")

PYTHON_SCRIPT

echo -e "${GREEN}✓ 链接验证完成${NC}"

