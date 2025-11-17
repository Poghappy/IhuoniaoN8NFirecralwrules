# HawaiiHub.net - Firecrawl × 火鸟门户 × n8n 采集与自动化运营

## 📋 项目简介

这是 HawaiiHub 夏威夷华人平台的采集与自动化运营仓库，整合了 Firecrawl 数据采集、火鸟门户系统 API 集成和 n8n 工作流自动化，实现内容采集、处理、发布的完整自动化流程。

## 🚀 核心功能

- **Firecrawl 数据采集**: 使用 Firecrawl API 进行网页内容采集和处理
- **火鸟门户系统集成**: 完整的 API 集成模块，支持内容发布和管理
- **n8n 工作流自动化**: 自动化工作流配置和执行
- **数据处理管道**: 数据清洗、关键词提取、分类、评分等处理流程
- **任务调度**: 支持定时任务和批量处理

## 📁 项目结构

```
├── Firecrawl代码模块/          # Firecrawl 采集器核心代码
│   ├── 火爬采集器.py           # 主采集器模块
│   ├── 数据处理.py             # 数据清洗和处理
│   ├── API集成.py              # 火鸟门户 API 集成
│   ├── 任务调度.py             # 任务调度管理
│   └── 集成测试.py             # 完整测试套件
├── docs/                       # 项目文档
│   ├── Firecrawl工具/          # Firecrawl 相关文档和代码
│   └── 火鸟门户系统官方文档/    # 火鸟门户系统完整文档
├── Nginx代理管理/              # Nginx 代理配置和管理
├── .cursor/                    # Cursor AI 配置和规则
└── 火鸟门户_*.js              # n8n 工作流配置
```

## ⚙️ 系统要求

- **Python**: 3.8+ (用于 Firecrawl 采集器)
- **Node.js**: 16+ (用于 n8n 工作流)
- **Firecrawl API**: 需要有效的 API 密钥
- **火鸟门户系统**: 已部署的系统实例和 API 访问权限

## 🔧 快速开始

### 1. 环境准备

```bash
# 安装 Python 依赖
cd Firecrawl代码模块
pip install -r requirements.txt

# 或使用 uv (推荐)
uv pip install -r requirements.txt
```

### 2. 配置设置

复制并配置必要的配置文件：

```bash
# 复制配置示例
cp Firecrawl代码模块/配置示例.json Firecrawl代码模块/config.json

# 编辑配置文件，填入：
# - Firecrawl API 密钥
# - 火鸟门户系统 API 地址和认证信息
# - 数据库连接信息（如需要）
```

### 3. 运行测试

```bash
# 运行集成测试
python Firecrawl代码模块/集成测试.py

# 或使用 pytest
pytest Firecrawl代码模块/
```

## 🔐 安全配置

### 重要安全提醒

1. **修改默认密码**: 安装后立即修改管理员默认密码
2. **配置文件保护**: 确保敏感配置文件不可直接访问
3. **定期更新**: 保持系统和依赖库的最新版本
4. **备份策略**: 建立定期备份机制

### 文件权限建议

```bash
# 配置文件只读
chmod 644 include/dbinfo.inc.php
chmod 644 api/appConfig.json

# 日志目录可写
chmod 755 log/

# 上传目录可写
chmod 755 api/upload/
```

## 📚 文档资源

### Firecrawl 工具文档
- **快速开始**: `docs/Firecrawl工具/QUICKSTART.md`
- **API 参考**: `docs/Firecrawl工具/官方资料/02-API参考/`
- **代码模块**: `Firecrawl代码模块/` 目录下的 Python 模块

### 火鸟门户系统文档
- **API 接口文档**: `docs/火鸟门户系统官方文档/02_API接口/`
- **功能模块文档**: `docs/火鸟门户系统官方文档/03_功能模块/`
- **采集插件文档**: `docs/火鸟门户系统官方文档/06_采集插件/`

### n8n 工作流
- **新闻采集工作流**: `火鸟门户_新闻采集工作流_增强版.json`
- **API 集成模块**: `火鸟门户_API集成模块.js`
- **内容处理模块**: `火鸟门户_内容处理核心模块.js`

## 🛠️ 开发指南

### 代码规范

**Python 代码**:
- 使用类型注解（必需）
- 中文 docstring
- 遵循 PEP 8 规范
- 使用 `ruff` 进行代码检查和格式化
- 使用 `mypy --strict` 进行类型检查

**测试**:
- 使用 `pytest` 进行测试
- 测试文件位于 `tests/` 目录
- 所有测试必须有类型注解和 docstring

### 开发工具

```bash
# 代码格式化
ruff format .

# 代码检查
ruff check .

# 类型检查
mypy --strict Firecrawl代码模块/

# 运行测试
pytest
```

### 工作流程

1. **采集**: 使用 `FirecrawlCollector` 采集网页内容
2. **处理**: 使用 `DataProcessor` 清洗和处理数据
3. **发布**: 使用 `APIIntegration` 发布到火鸟门户系统

## 🔐 安全注意事项

1. **API 密钥保护**:
   - 不要将 API 密钥提交到版本控制
   - 使用环境变量或配置文件（已加入 .gitignore）
   - `.cursor/mcp.json` 包含敏感信息，已排除

2. **配置文件**:
   - 敏感配置使用 `.env` 文件
   - 参考 `.env.example` 创建配置

3. **数据库**:
   - 数据库备份文件已排除在版本控制外
   - 生产环境数据库信息不要提交

## 📞 技术支持

- **问题反馈**: 请通过 [GitHub Issues](https://github.com/Poghappy/IhuoniaoN8NFirecralwrules/issues) 提交问题
- **功能建议**: 欢迎提交功能改进建议
- **安全问题**: 请通过私有渠道报告安全漏洞

## 📄 许可证

本项目采用商业许可证，使用前请确保已获得合法授权。

## 🔄 更新日志

详细更新日志请参考 [CHANGELOG.md](./CHANGELOG.md)

## 🤝 贡献指南

欢迎贡献代码！请参考 [CONTRIBUTING.md](./CONTRIBUTING.md) 了解贡献流程。

---

**注意**: 本项目包含敏感配置和商业代码，请妥善保管源代码，避免泄露。
