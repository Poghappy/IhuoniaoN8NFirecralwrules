# 项目脚本说明

本目录包含项目维护和开发相关的自动化脚本。

## 📋 脚本列表

### 1. `project-health-check.sh` - 项目健康检查

**功能**: 全面检查项目配置、代码质量、文档完整性等。

**使用方法**:
```bash
./scripts/project-health-check.sh
```

**检查项**:
- ✅ 必需文件（README.md, LICENSE, SECURITY.md 等）
- ✅ 配置文件（pyproject.toml, .gitignore 等）
- ✅ Python 工具安装状态（Ruff, MyPy, Pytest）
- ✅ 代码目录结构
- ✅ 安全配置（.gitignore 中的敏感文件）
- ✅ 临时文档文件
- ✅ Git 状态

### 2. `code-quality-check.sh` - 代码质量检查

**功能**: 运行 Ruff、MyPy 和 Pytest 进行代码质量检查。

**使用方法**:
```bash
./scripts/code-quality-check.sh
```

**检查项**:
- 🔍 Ruff 格式检查
- 🔍 Ruff 代码检查
- 🔍 MyPy 类型检查
- 🧪 Pytest 测试

**修复建议**:
```bash
# 自动格式化代码
ruff format .

# 自动修复可修复的问题
ruff check --fix .
```

### 3. `verify-config.sh` - 配置验证

**功能**: 验证项目配置文件是否正确。

**使用方法**:
```bash
./scripts/verify-config.sh
```

**检查项**:
- 📦 pyproject.toml 配置
- 🔒 .gitignore 配置
- 🐙 GitHub 配置（工作流、模板等）
- 📚 项目文档
- 📂 代码目录结构

### 4. `organize-temp-docs.sh` - 整理临时文档

**功能**: 将根目录的临时文档移动到归档目录。

**使用方法**:
```bash
./scripts/organize-temp-docs.sh
```

**功能说明**:
- 自动识别临时文档文件
- 创建归档目录（`docs/archive/temp-docs-YYYYMMDD`）
- 移动文件到归档目录
- 创建归档说明文档

### 5. `verify-cursor-config.sh` - Cursor 配置验证

**功能**: 验证 Cursor/VSCode 配置是否正确。

**使用方法**:
```bash
./scripts/verify-cursor-config.sh
```

## 🚀 快速开始

### 运行所有检查

```bash
# 1. 项目健康检查
./scripts/project-health-check.sh

# 2. 配置验证
./scripts/verify-config.sh

# 3. 代码质量检查
./scripts/code-quality-check.sh
```

### 整理项目

```bash
# 整理临时文档
./scripts/organize-temp-docs.sh
```

## 📝 脚本开发规范

### 脚本要求

1. **可执行权限**: 所有脚本必须有可执行权限
2. **错误处理**: 使用 `set -e` 确保错误时退出
3. **颜色输出**: 使用颜色代码提高可读性
4. **退出码**: 正确设置退出码（0=成功，1=失败）

### 脚本模板

```bash
#!/bin/bash
# 脚本描述

set -e

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 脚本逻辑
echo -e "${BLUE}开始执行...${NC}"

# 检查函数
check_pass() {
    echo -e "${GREEN}✓${NC} $1"
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
    exit 1
}

# 执行检查
check_pass "检查通过"

echo -e "${GREEN}✅ 完成！${NC}"
```

## 🔧 维护

### 添加新脚本

1. 在 `scripts/` 目录创建新脚本
2. 添加可执行权限: `chmod +x scripts/new-script.sh`
3. 更新本 README.md
4. 测试脚本功能

### 更新脚本

1. 修改脚本文件
2. 测试功能
3. 更新文档（如需要）

## 📚 相关文档

- [项目规则](../docs/Firecrawl工具/docs/project/project-rules.md)
- [GitHub 配置清单](../docs/Firecrawl工具/docs/project/github-configuration-checklist.md)
- [待办事项清单](../docs/Firecrawl工具/docs/project/pending-tasks.md)

---

**最后更新**: 2025-01-27
**维护者**: AI Agent Team

