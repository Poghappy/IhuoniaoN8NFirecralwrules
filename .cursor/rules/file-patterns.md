# 文件模式规则

## 📁 目录结构规范

### 核心目录
```bash
src/                    # 源代码目录
├── core/              # 核心模块
├── api/               # API相关
├── models/            # 数据模型
├── services/          # 业务服务
├── utils/             # 工具函数
└── config/            # 配置模块

config/                # 配置文件目录
├── development/       # 开发环境配置
├── production/        # 生产环境配置
├── deployment/        # 部署配置
└── monitoring/        # 监控配置

tests/                 # 测试目录
├── unit/              # 单元测试
├── integration/       # 集成测试
├── fixtures/          # 测试数据
└── mocks/             # 模拟对象

docs/                  # 文档目录
├── api/               # API文档
├── guides/            # 使用指南
├── architecture/      # 架构文档
└── deployment/        # 部署文档
```

## 📄 文件命名规范

### Python文件
```python
# 模块文件：小写+下划线
firecrawl_collector.py
data_processor.py
api_integration.py

# 测试文件：test_前缀
test_collector.py
test_processor.py
test_integration.py

# 配置文件：config_前缀
config_development.py
config_production.py
config_database.py

# 工具文件：utils_前缀
utils_logging.py
utils_validation.py
utils_helpers.py
```

### 配置文件
```bash
# JSON配置
config.json                    # 主配置文件
config.development.json        # 开发环境配置
config.production.json         # 生产环境配置

# YAML配置
docker-compose.yml             # Docker编排
docker-compose.dev.yml         # 开发环境编排
docker-compose.prod.yml        # 生产环境编排

# 环境变量
.env                          # 环境变量文件
.env.development              # 开发环境变量
.env.production               # 生产环境变量
```

### 文档文件
```bash
# Markdown文档
README.md                     # 项目说明
CHANGELOG.md                  # 变更日志
CONTRIBUTING.md               # 贡献指南
API.md                        # API文档

# 技术文档
architecture.md               # 架构设计
deployment.md                 # 部署指南
troubleshooting.md            # 故障排除
security.md                   # 安全说明
```

## 🏷️ 文件标签规范

### 版本标签
```bash
# 版本号格式：v{major}.{minor}.{patch}
v1.0.0                        # 主版本
v1.1.0                        # 次版本
v1.1.1                        # 补丁版本

# 预发布版本
v1.0.0-alpha.1                # Alpha版本
v1.0.0-beta.1                 # Beta版本
v1.0.0-rc.1                   # 候选版本
```

### 环境标签
```bash
# 环境标识
.dev                          # 开发环境
.test                         # 测试环境
.staging                      # 预生产环境
.prod                         # 生产环境

# 示例
config.dev.json
docker-compose.test.yml
deploy.staging.sh
```

### 状态标签
```bash
# 文件状态
.draft                        # 草稿状态
.review                       # 审查状态
.approved                     # 已批准
.deprecated                   # 已废弃

# 示例
api_v2.draft.md
security.review.md
old_config.deprecated.json
```

## 📋 文件内容规范

### Python文件结构
```python
"""
模块文档字符串
描述模块功能、用法和注意事项
"""

# 标准库导入
import os
import sys
from typing import Dict, List, Optional

# 第三方库导入
import requests
import pandas as pd

# 本地模块导入
from src.core.collector import Collector
from src.config.settings import Settings

# 模块级变量
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3

# 类和函数定义
class ExampleClass:
    """类文档字符串"""
    pass

def example_function() -> None:
    """函数文档字符串"""
    pass

# 模块执行代码
if __name__ == "__main__":
    # 模块执行逻辑
    pass
```

### 配置文件结构
```json
{
  "version": "1.0.0",
  "description": "配置文件描述",
  "environment": "development",
  "settings": {
    "database": {
      "host": "localhost",
      "port": 5432,
      "name": "firecrawl"
    },
    "api": {
      "base_url": "https://api.firecrawl.dev",
      "timeout": 30
    }
  }
}
```

### 文档文件结构
```markdown
# 文档标题

## 概述
文档简要描述

## 功能特性
- 特性1
- 特性2

## 使用方法
### 基本用法
```python
# 代码示例
```

## 配置说明
配置参数说明

## 注意事项
重要提醒

## 相关链接
- [链接1](url1)
- [链接2](url2)
```

## 🔍 文件检查规则

### 必需文件
```bash
# 项目根目录必需文件
README.md                     # 项目说明
requirements.txt              # Python依赖
.gitignore                    # Git忽略规则
LICENSE                       # 许可证

# 源代码目录
__init__.py                   # Python包标识
main.py                       # 主程序入口

# 配置目录
config.json                   # 主配置文件
.env.example                  # 环境变量示例

# 测试目录
conftest.py                   # pytest配置
test_*.py                     # 测试文件

# 文档目录
README.md                     # 项目说明
CHANGELOG.md                  # 变更日志
```

### 文件大小限制
```bash
# 代码文件
Python文件: < 1000行
配置文件: < 500行
文档文件: < 2000行

# 数据文件
JSON文件: < 10MB
日志文件: < 100MB
数据库文件: < 1GB
```

### 文件编码规范
```bash
# 文本文件编码
Python文件: UTF-8
配置文件: UTF-8
文档文件: UTF-8
脚本文件: UTF-8

# 行尾符规范
Unix系统: LF (\n)
Windows系统: CRLF (\r\n)
```

## 🚫 禁止模式

### 文件名禁止
```bash
# 禁止使用的字符
空格、中文、特殊符号
# 示例：bad file name.py ❌

# 禁止的命名模式
test_*.py                     # 测试文件不应在生产代码中
temp_*.py                     # 临时文件应清理
old_*.py                      # 旧文件应归档或删除
```

### 文件内容禁止
```bash
# 禁止硬编码
API密钥、密码、敏感信息
# 示例：api_key = "secret123" ❌

# 禁止的导入模式
import *                      # 避免通配符导入
from module import *          # 避免通配符导入
```

## 📊 文件统计规则

### 代码统计
```bash
# 统计指标
总行数、有效行数、注释行数
函数数量、类数量、复杂度
测试覆盖率、文档覆盖率
```

### 质量指标
```bash
# 质量要求
代码重复率 < 5%
圈复杂度 < 10
函数长度 < 50行
类长度 < 200行
```

## 🔄 文件生命周期

### 文件状态流转
```bash
创建 → 开发 → 测试 → 审查 → 发布 → 维护 → 废弃
```

### 文件清理规则
```bash
# 定期清理
临时文件: 立即清理
日志文件: 30天清理
备份文件: 90天清理
废弃文件: 归档处理
```

## 📝 文件模板

### Python模块模板
```python
"""
{module_name}.py

{module_description}

Author: {author}
Date: {date}
Version: {version}
"""

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class {ClassName}:
    """{class_description}"""
    
    def __init__(self, config: Dict[str, Any]) -> None:
        """初始化{ClassName}"""
        self.config = config
        logger.info(f"Initializing {ClassName}")
    
    def method_name(self, param: str) -> Optional[str]:
        """{method_description}
        
        Args:
            param: {param_description}
            
        Returns:
            {return_description}
            
        Raises:
            ValueError: {error_description}
        """
        try:
            # 实现逻辑
            return result
        except Exception as e:
            logger.error(f"Error in method_name: {e}")
            raise


def main() -> None:
    """主函数"""
    pass


if __name__ == "__main__":
    main()
```

### 配置文件模板
```json
{
  "version": "1.0.0",
  "description": "{config_description}",
  "environment": "{environment}",
  "created_at": "{timestamp}",
  "settings": {
    "database": {
      "host": "{db_host}",
      "port": {db_port},
      "name": "{db_name}",
      "user": "{db_user}",
      "password": "{db_password}"
    },
    "api": {
      "base_url": "{api_url}",
      "timeout": {timeout},
      "retries": {retries}
    },
    "logging": {
      "level": "{log_level}",
      "file": "{log_file}",
      "max_size": "{max_size}"
    }
  }
}
```
