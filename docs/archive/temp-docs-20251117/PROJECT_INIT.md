# 🚀 HawaiiHub.net 项目初始化指南

**创建时间**: 2025-01-27
**版本**: 1.0.0

## 📋 概述

本文档提供 HawaiiHub.net 项目的完整初始化步骤，包括环境配置、依赖安装、Cursor 配置等。

## ✅ 快速开始

### 1. 运行初始化脚本

```bash
# 基础初始化（仅创建目录和配置文件）
python3 scripts/init_project.py

# 完整初始化（包括安装依赖）
python3 scripts/init_project.py --install-deps

# 开发环境初始化（包括开发依赖）
python3 scripts/init_project.py --install-deps --dev
```

### 2. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入实际配置值
# 至少需要配置：
# - FIRECRAWL_API_KEY
# - HUONIAO_API_BASE_URL
# - HUONIAO_API_KEY
```

### 3. 验证配置

```bash
# 运行初始化脚本验证配置
python3 scripts/init_project.py

# 或手动验证
python3 scripts/verify_config.py
```

## 📁 项目结构

```
HawaiiHub.net/
├── Firecrawl代码模块/      # Firecrawl 采集器核心代码
├── docs/                   # 项目文档
├── scripts/                # 工具脚本
│   ├── init_project.py    # 项目初始化脚本
│   └── verify_config.py   # 配置验证脚本
├── .cursor/                # Cursor AI 配置
│   ├── mcp.json           # MCP 服务器配置
│   └── rules/             # AI 规则文件
├── requirements.txt        # 生产依赖
├── requirements-dev.txt    # 开发依赖
├── pyproject.toml         # 项目配置（Ruff, mypy, pytest）
├── .env.example           # 环境变量模板
└── Makefile               # 常用命令
```

## 🔧 详细配置步骤

### 1. Python 环境

**要求**: Python 3.9 或更高版本

```bash
# 检查 Python 版本
python3 --version

# 创建虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

### 2. 安装依赖

```bash
# 安装生产依赖
pip install -r requirements.txt

# 或安装开发依赖（包含测试工具）
pip install -r requirements-dev.txt

# 或使用 uv（推荐，更快）
uv pip install -r requirements.txt
```

### 3. 配置环境变量

编辑 `.env` 文件，至少配置以下必需项：

```bash
# Firecrawl API（必需）
FIRECRAWL_API_KEY=your_firecrawl_api_key_here

# 火鸟门户系统 API（必需）
HUONIAO_API_BASE_URL=https://your-instance.com/api
HUONIAO_API_KEY=your_huo_niao_api_key_here
```

### 4. Cursor 配置

项目已包含完整的 Cursor 配置：

- **MCP 服务器**: 配置在 `.cursor/mcp.json`
- **AI 规则**: 配置在 `.cursor/rules/`
- **Python 规范**: `.cursor/rules/python.mdc`

**已配置的 MCP 服务器**:
- Firecrawl MCP
- GitHub MCP
- Apify MCP
- Docker MCP Gateway
- Filesystem MCP
- Context MCP

### 5. 代码质量工具

项目已配置以下工具：

```bash
# 代码检查
make lint

# 代码格式化
make format

# 类型检查
make type-check

# 运行测试
make test

# 自动修复
make fix
```

## 🧪 验证安装

### 1. 运行测试

```bash
# 运行所有测试
make test

# 或使用 pytest
pytest Firecrawl代码模块/ -v
```

### 2. 运行示例

```bash
# 运行 FastMCP 示例
make run-example

# 或直接运行
python3 Firecrawl代码模块/canvas_fastmcp_example.py
```

### 3. 检查配置

```bash
# 验证配置
python3 scripts/verify_config.py

# 检查代码质量
make check-all
```

## 📚 下一步

1. **阅读文档**
   - [README.md](README.md) - 项目概述
   - [CONTRIBUTING.md](CONTRIBUTING.md) - 贡献指南
   - [.cursor/rules/python.mdc](.cursor/rules/python.mdc) - Python 开发规范

2. **探索代码**
   - `Firecrawl代码模块/火爬采集器.py` - 主采集器
   - `Firecrawl代码模块/数据处理.py` - 数据处理
   - `Firecrawl代码模块/API集成.py` - API 集成

3. **运行示例**
   - 查看 `docs/Firecrawl工具/examples/` 中的示例
   - 运行集成测试了解完整流程

## ⚠️ 常见问题

### Q: 初始化脚本失败？

**A**: 检查以下项：
- Python 版本 >= 3.9
- 有写入权限
- 网络连接正常（如果安装依赖）

### Q: 依赖安装失败？

**A**:
- 检查网络连接
- 尝试使用 `--no-cache-dir` 选项
- 使用 `uv` 替代 `pip`（更快更可靠）

### Q: Cursor 无法识别项目？

**A**:
- 确保 `.cursor/` 目录存在
- 重启 Cursor
- 检查 `.cursor/mcp.json` 配置是否正确

### Q: 环境变量不生效？

**A**:
- 确保 `.env` 文件在项目根目录
- 检查变量名是否正确
- 重启应用/服务

## 🔗 相关资源

- [Firecrawl 官方文档](https://docs.firecrawl.dev/)
- [火鸟门户系统文档](docs/火鸟门户系统官方文档/)
- [Cursor 文档](https://docs.cursor.com/)
- [MCP 协议文档](https://modelcontextprotocol.io/)

## 📝 更新日志

- **2025-01-27**: 初始版本，包含完整的初始化脚本和配置

---

**需要帮助？** 查看 [CONTRIBUTING.md](CONTRIBUTING.md) 或提交 Issue。

