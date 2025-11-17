# 代码文件目录

> **最后更新**: 2025-01-27

## 📋 目录说明

本目录包含项目中的**核心工具代码**，提供基础功能支持。

## 📚 文件列表

### 核心工具
- [Flask 存储](./flask-storage.py) - Flask 应用存储实现
- [Supabase 客户端](./supabase-client.py) - Supabase 数据库客户端

## 🔗 与代码模块的关系

### 目录分工
- **`code/`** (本目录): 核心工具和基础功能
  - Flask 存储适配器
  - Supabase 客户端封装
  - 提供基础服务支持

- **`代码模块/`**: 业务逻辑和功能模块
  - Firecrawl 数据采集
  - 数据处理和转换
  - API 集成
  - 任务调度
  - 使用 `code/` 中的核心工具

### 使用关系
```python
# 代码模块中的代码可以使用 code/ 中的工具
from code.flask_storage import FlaskSessionStorage
from code.supabase_client import get_supabase
```

## 📝 使用说明

### Flask 存储
用于 Flask 应用中的数据存储功能，为 Supabase 客户端提供会话存储支持。

### Supabase 客户端
用于连接和操作 Supabase 数据库，提供统一的数据库访问接口。

## 🔗 相关链接

- [返回项目首页](../README.md)
- [代码模块](../代码模块/) - 业务代码模块
- [配置示例](../config/examples/)
- [测试文件](../tests/)

---

**维护者**: AI Agent Team
