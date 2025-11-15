# Firecrawl数据采集器项目规则

## 📋 项目概述
基于Firecrawl API的智能数据采集系统，支持网页爬取、数据清洗、存储和分析。项目采用模块化设计，支持多种数据源和输出格式，为火鸟门户系统提供数据支持。

## 🎯 核心价值
- **智能采集**: 基于AI的内容过滤和重要性分析
- **高效处理**: 异步并发处理，支持大规模数据采集
- **灵活集成**: 支持多种数据源和输出格式
- **自动化运维**: 完整的监控、告警和部署自动化

## 🏗️ 项目结构规范

### 目录结构
```
Firecrawl数据采集器/
├── src/                    # 核心源代码
│   ├── firecrawl_collector.py
│   ├── data_processor.py
│   ├── database_models.py
│   ├── api_integration.py
│   ├── task_scheduler.py
│   └── pipeline_config.py
├── config/                 # 配置文件
│   ├── config.json
│   ├── config_example.json
│   ├── deployment/         # 部署配置
│   └── nginx/             # Nginx配置
├── tests/                  # 测试文件
├── scripts/               # 脚本文件
├── docs/                  # 文档
├── data/                  # 数据存储
├── logs/                  # 日志文件
└── results/               # 结果文件
```

## 🔧 开发规范

### Python代码规范
- 遵循PEP 8编码规范
- 使用类型提示（Type Hints）
- 函数和类添加文档字符串
- 使用Black进行代码格式化
- 使用isort进行导入排序

### 文件命名规范
- 使用小写字母和下划线
- 避免中文文件名
- 测试文件以`test_`开头
- 配置文件使用`.json`或`.yml`扩展名
- 文档文件使用`.md`扩展名

### 导入规范
```python
# 标准库导入
import os
import sys
from typing import Dict, List, Optional

# 第三方库导入
import requests
import pandas as pd

# 本地模块导入
from src.firecrawl_collector import FirecrawlCollector
from config.firecrawl_config import Config
```

## 🚀 部署规范

### Docker配置
- 使用多阶段构建优化镜像大小
- 配置健康检查
- 设置适当的资源限制
- 使用非root用户运行

### 环境变量
- 敏感信息使用环境变量
- 提供`.env.example`文件
- 配置验证和默认值

## 📊 数据处理规范

### 数据采集
- 实现智能限流和重试机制
- 支持断点续传
- 记录详细的采集日志
- 实现并发控制

### 数据清洗
- 标准化数据格式
- 去除重复数据
- 验证数据完整性
- 处理异常数据

### 存储管理
- 支持多种存储后端
- 实现数据压缩
- 配置数据分区
- 设置数据保留策略

## 🔒 安全规范

### API安全
- 实现API认证
- 配置访问控制
- 添加速率限制
- 记录访问日志

### 数据安全
- 敏感数据加密
- 传输加密（HTTPS）
- 存储加密
- 访问审计

## 📈 性能优化

### 采集性能
- 并发采集优化
- 内存使用优化
- 网络请求优化
- 缓存策略实施

### 数据处理
- 批量处理优化
- 数据库查询优化
- 异步处理
- 资源池管理

## 🧪 测试策略

### 单元测试
- 函数级别测试
- 模拟外部依赖
- 边界条件测试
- 测试覆盖率>90%

### 集成测试
- API接口测试
- 数据库集成测试
- 外部服务集成测试
- 端到端流程测试

## 🔄 维护规范

### 版本管理
- 语义化版本控制
- 变更日志维护
- 分支管理策略
- 代码审查流程

### 文档维护
- 保持文档更新
- 提供使用示例
- 记录API变更
- 维护故障排除指南
