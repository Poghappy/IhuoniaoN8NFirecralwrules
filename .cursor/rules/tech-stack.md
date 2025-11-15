# 技术栈配置规则

## 🛠️ 核心技术栈

### Python环境
- **Python版本**: 3.9+
- **包管理**: pip + requirements.txt
- **虚拟环境**: venv
- **代码格式化**: Black + isort
- **类型检查**: mypy
- **测试框架**: pytest

### Web框架
- **API框架**: FastAPI
- **异步支持**: asyncio + aiohttp
- **数据验证**: Pydantic
- **API文档**: OpenAPI/Swagger

### 数据库
- **主数据库**: PostgreSQL
- **缓存**: Redis
- **ORM**: SQLAlchemy
- **迁移**: Alembic
- **连接池**: SQLAlchemy Pool

### 任务队列
- **任务调度**: Celery
- **消息队列**: RabbitMQ
- **结果后端**: Redis
- **监控**: Flower

### 数据处理
- **爬虫引擎**: Firecrawl API
- **数据清洗**: Pandas
- **文本处理**: NLTK/spaCy
- **AI集成**: OpenAI API

### 容器化
- **容器**: Docker
- **编排**: Docker Compose
- **多阶段构建**: 优化镜像大小
- **健康检查**: 容器健康监控

### 监控和日志
- **监控**: Prometheus
- **可视化**: Grafana
- **日志**: ELK Stack
- **错误追踪**: Sentry

### 部署
- **Web服务器**: Nginx
- **反向代理**: Nginx
- **SSL**: Let's Encrypt
- **CI/CD**: GitHub Actions

## 📦 依赖管理

### 核心依赖
```python
# Web框架
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.0.0

# 数据库
sqlalchemy>=2.0.0
alembic>=1.12.0
psycopg2-binary>=2.9.0
redis>=5.0.0

# 任务队列
celery>=5.3.0
kombu>=5.3.0

# HTTP客户端
aiohttp>=3.9.0
httpx>=0.25.0

# 数据处理
pandas>=2.1.0
numpy>=1.24.0

# 工具库
python-dotenv>=1.0.0
loguru>=0.7.0
```

### 开发依赖
```python
# 代码质量
black>=23.0.0
isort>=5.12.0
flake8>=6.0.0
mypy>=1.7.0

# 测试
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-cov>=4.1.0
httpx>=0.25.0

# 文档
mkdocs>=1.5.0
mkdocs-material>=9.4.0
```

## 🔧 配置文件规范

### 环境变量
```bash
# 数据库配置
DATABASE_URL=postgresql://user:password@localhost:5432/firecrawl
REDIS_URL=redis://localhost:6379/0

# API配置
FIRECRAWL_API_KEY=your_api_key_here
OPENAI_API_KEY=your_openai_key_here

# 应用配置
DEBUG=false
LOG_LEVEL=INFO
WORKERS=4

# 安全配置
SECRET_KEY=your_secret_key_here
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Docker配置
```dockerfile
# 多阶段构建
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim as runtime
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .
CMD ["uvicorn", "src.api_server:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🚀 部署配置

### Docker Compose
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/firecrawl
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: firecrawl
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
```

### Nginx配置
```nginx
upstream app {
    server app:8000;
}

server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 📊 监控配置

### Prometheus配置
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'firecrawl-app'
    static_configs:
      - targets: ['app:8000']
    metrics_path: '/metrics'
    scrape_interval: 5s
```

### 日志配置
```python
import logging
from loguru import logger

# 配置日志
logger.add(
    "logs/app.log",
    rotation="1 day",
    retention="30 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}"
)
```

## 🔄 开发工作流

### 代码提交规范
```bash
# 功能开发
git checkout -b feature/new-feature
git add .
git commit -m "feat: add new feature"
git push origin feature/new-feature

# 修复bug
git checkout -b fix/bug-description
git add .
git commit -m "fix: resolve bug description"
git push origin fix/bug-description

# 文档更新
git checkout -b docs/update-readme
git add .
git commit -m "docs: update README"
git push origin docs/update-readme
```

### 测试流程
```bash
# 运行测试
pytest tests/ -v --cov=src

# 代码格式化
black src/ tests/
isort src/ tests/

# 类型检查
mypy src/

# 安全检查
bandit -r src/
```

## 📈 性能优化

### 数据库优化
- 使用连接池
- 创建适当的索引
- 优化查询语句
- 实现分页查询

### 缓存策略
- Redis缓存热点数据
- 实现缓存失效机制
- 使用缓存预热
- 监控缓存命中率

### 异步处理
- 使用asyncio处理I/O密集型任务
- 实现任务队列
- 异步数据库操作
- 并发请求处理
