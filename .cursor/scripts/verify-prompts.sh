#!/bin/bash

# Firecrawl数据采集器 - Prompts 配置验证脚本
# 版本: v2.0.0
# 最后更新: 2025-10-29

set -e

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[⚠]${NC} $1"
}

log_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# 验证计数器
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0

# 检查函数
check_file() {
    local file=$1
    local description=$2
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))

    if [ -f "$file" ]; then
        log_success "$description: $file"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
        return 0
    else
        log_error "$description 缺失: $file"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
        return 1
    fi
}

check_dir() {
    local dir=$1
    local description=$2
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))

    if [ -d "$dir" ]; then
        log_success "$description: $dir"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
        return 0
    else
        log_error "$description 缺失: $dir"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
        return 1
    fi
}

echo "=================================="
echo "  Cursor Prompts 配置验证工具"
echo "=================================="
echo ""

# 1. 检查主规则文件
log_info "检查 Cursor 主规则文件..."
check_file ".cursorrules" "主规则文件"
echo ""

# 2. 检查 .cursor 目录结构
log_info "检查 .cursor 目录结构..."
check_dir ".cursor" ".cursor 目录"
check_dir ".cursor/prompts" "Prompts 目录"
check_dir ".cursor/scripts" "Scripts 目录"
check_dir ".cursor/hooks" "Hooks 目录"
echo ""

# 3. 检查核心 Prompts 文件
log_info "检查核心 Prompts 文件..."
check_file ".cursor/prompts/README.md" "Prompts README"
check_file ".cursor/prompts/INDEX.md" "Prompts 索引"
check_file ".cursor/prompts/system_prompt.md" "系统提示词"
check_file ".cursor/prompts/orchestrator.md" "编排器配置"
check_file ".cursor/prompts/project_config.md" "项目配置"
check_file ".cursor/prompts/handoff_format.md" "交接格式"
check_file ".cursor/prompts/guardrails.md" "质量闸口"
echo ""

# 4. 检查角色文件
log_info "检查角色文件..."
check_dir ".cursor/prompts/roles" "角色目录"

roles=(
    "01_product_owner.md"
    "02_product_manager.md"
    "03_business_analyst.md"
    "05_architect.md"
    "06_llm_engineer.md"
    "07_developer.md"
    "08_qa_engineer.md"
    "09_devops.md"
    "10_technical_writer.md"
)

for role in "${roles[@]}"; do
    check_file ".cursor/prompts/roles/$role" "角色文件 $role"
done
echo ""

# 5. 检查工作流文件
log_info "检查工作流文件..."
workflows=(
    "10_user_story.md"
    "20_prd.md"
    "30_task_breakdown.md"
    "40_tech_design.md"
    "50_impl.md"
    "60_test.md"
    "70_iteration.md"
)

for workflow in "${workflows[@]}"; do
    if [ -f ".cursor/prompts/$workflow" ]; then
        check_file ".cursor/prompts/$workflow" "工作流文件 $workflow"
    else
        log_warning "工作流文件可选: $workflow (未找到)"
    fi
done
echo ""

# 6. 检查项目配置
log_info "检查项目配置..."
if [ -f ".cursor/project-config.json" ]; then
    check_file ".cursor/project-config.json" "项目配置"

    # 验证 JSON 格式
    if command -v jq &> /dev/null; then
        if jq empty .cursor/project-config.json 2>/dev/null; then
            log_success "project-config.json 格式正确"
            PASSED_CHECKS=$((PASSED_CHECKS + 1))
        else
            log_error "project-config.json 格式错误"
            FAILED_CHECKS=$((FAILED_CHECKS + 1))
        fi
        TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    else
        log_warning "jq 未安装，跳过 JSON 格式验证"
    fi
else
    log_warning "项目配置文件可选 (未找到)"
fi
echo ""

# 7. 检查脚本权限
log_info "检查脚本权限..."
scripts=(
    ".cursor/scripts/verify-prompts.sh"
    ".cursor/scripts/check-roles.sh"
    ".cursor/scripts/generate-docs.sh"
)

for script in "${scripts[@]}"; do
    if [ -f "$script" ]; then
        if [ -x "$script" ]; then
            log_success "脚本可执行: $script"
            PASSED_CHECKS=$((PASSED_CHECKS + 1))
        else
            log_warning "脚本不可执行: $script (正在修复...)"
            chmod +x "$script"
            log_success "已添加执行权限: $script"
            PASSED_CHECKS=$((PASSED_CHECKS + 1))
        fi
        TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    fi
done
echo ""

# 8. 检查 Git Hooks
log_info "检查 Git Hooks..."
hooks=(
    ".cursor/hooks/pre-commit"
    ".cursor/hooks/pre-push"
)

for hook in "${hooks[@]}"; do
    if [ -f "$hook" ]; then
        check_file "$hook" "Git Hook $hook"
        if [ ! -x "$hook" ]; then
            log_warning "Hook 不可执行: $hook (正在修复...)"
            chmod +x "$hook"
            log_success "已添加执行权限: $hook"
        fi
    else
        log_warning "Git Hook 可选: $hook (未找到)"
    fi
done
echo ""

# 9. 检查文档链接
log_info "检查关键文档..."
check_file "docs/INDEX.md" "文档索引"
if [ -f "docs/PROJECT_BRIEF.md" ]; then
    log_success "项目概要文档存在"
    PASSED_CHECKS=$((PASSED_CHECKS + 1))
else
    log_warning "建议创建 docs/PROJECT_BRIEF.md"
fi
TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
echo ""

# 10. 总结报告
echo "=================================="
echo "  验证结果总结"
echo "=================================="
echo ""
echo "总检查项: $TOTAL_CHECKS"
echo -e "${GREEN}通过: $PASSED_CHECKS${NC}"
echo -e "${RED}失败: $FAILED_CHECKS${NC}"
echo ""

# 计算通过率
PASS_RATE=$((PASSED_CHECKS * 100 / TOTAL_CHECKS))
echo "通过率: ${PASS_RATE}%"
echo ""

# 给出建议
if [ $FAILED_CHECKS -eq 0 ]; then
    echo -e "${GREEN}✓ 所有检查通过！Cursor Prompts 配置完整。${NC}"
    echo ""
    echo "接下来你可以："
    echo "  1. 重启 Cursor 以加载新配置"
    echo "  2. 在 Cursor 中开始使用多角色 Agent 系统"
    echo "  3. 运行 'make verify-cursor-config' 进行完整测试"
    exit 0
elif [ $PASS_RATE -ge 80 ]; then
    echo -e "${YELLOW}⚠ 配置基本完整，但有 $FAILED_CHECKS 项需要注意。${NC}"
    echo ""
    echo "建议："
    echo "  1. 查看上述失败项并补充缺失文件"
    echo "  2. 重新运行此脚本验证"
    exit 1
else
    echo -e "${RED}✗ 配置不完整，请检查缺失项。${NC}"
    echo ""
    echo "修复步骤："
    echo "  1. 确保运行了完整的迁移脚本"
    echo "  2. 检查文件权限"
    echo "  3. 重新运行验证"
    exit 2
fi
