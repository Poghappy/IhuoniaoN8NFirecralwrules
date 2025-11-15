# Cursor Agent 开发规范指南

## 📝 文件命名规范

### 目录结构

```
docs/           # 项目文档
├── PROJECT_BRIEF.md      # 项目概览
├── USER_STORIES.md       # 用户故事
├── PRD.md               # 产品需求文档
├── TECH_DESIGN.md       # 技术设计文档
├── TEST_PLAN.md         # 测试计划
└── CHANGELOG.md         # 变更记录

prompts/        # 提示词模板
├── 00_guidelines.md     # 开发规范
├── 10_user_story.md     # 用户故事模板
├── 20_prd.md           # PRD模板
├── 30_task_breakdown.md # 任务分解模板
├── 40_tech_design.md   # 技术设计模板
├── 50_impl.md          # 实现模板
├── 60_test.md          # 测试模板
└── 70_iteration.md     # 迭代模板

src/            # 源代码
├── core/       # 核心模块
├── api/        # API接口
├── services/   # 业务服务
├── models/     # 数据模型
└── utils/      # 工具函数

tests/          # 测试代码
├── unit/       # 单元测试
├── integration/ # 集成测试
└── e2e/        # 端到端测试
```

### 文件命名约定

- **Python文件**: `snake_case.py`
- **配置文件**: `kebab-case.json/yaml`
- **文档文件**: `UPPER_SNAKE_CASE.md`
- **测试文件**: `test_*.py`

## 📤 输出位置规范

### 文档输出

- 用户故事 → `docs/USER_STORIES.md`
- 需求文档 → `docs/PRD.md`
- 技术设计 → `docs/TECH_DESIGN.md`
- 测试计划 → `docs/TEST_PLAN.md`
- 变更记录 → `docs/CHANGELOG.md`

### 代码输出

- 核心业务逻辑 → `src/core/`
- API接口 → `src/api/`
- 数据模型 → `src/models/`
- 工具函数 → `src/utils/`

### 测试输出

- 单元测试 → `tests/unit/`
- 集成测试 → `tests/integration/`
- 端到端测试 → `tests/e2e/`

## 🔄 提交风格规范

### Conventional Commits

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### 类型说明

- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

### 示例

```
feat(api): add user authentication endpoint
fix(collector): handle timeout errors gracefully
docs(readme): update installation instructions
test(unit): add tests for data processor
```

## 💻 代码与注释要求

### Python代码规范

- 遵循PEP 8标准
- 使用类型提示 (Type Hints)
- 函数和类必须有docstring
- 复杂逻辑必须添加注释

### 注释规范

```python
def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    处理采集的原始数据
    
    Args:
        data: 原始数据字典
        
    Returns:
        处理后的结构化数据
        
    Raises:
        ValueError: 当数据格式不正确时
        ProcessingError: 当处理过程中发生错误时
    """
    # 数据验证
    if not isinstance(data, dict):
        raise ValueError("数据必须是字典格式")
    
    # 数据清洗逻辑
    cleaned_data = self._clean_data(data)
    
    return cleaned_data
```

## 🧪 测试覆盖要求

### 覆盖率门槛

- 单元测试覆盖率 ≥ 80%
- 集成测试覆盖率 ≥ 60%
- 关键业务逻辑覆盖率 ≥ 95%

### 测试要求

- 每个新功能必须包含测试用例
- 测试用例必须包含正常和异常场景
- 集成测试必须验证API接口
- 性能测试必须验证关键指标

## 🔒 安全要求

### 敏感信息处理

- 所有密钥和配置信息写入 `.env.example`
- 不得在代码中硬编码敏感信息
- 使用环境变量管理配置
- 定期更新依赖包版本

### 数据保护

- 采集的数据必须脱敏处理
- 遵守数据保留政策
- 支持数据删除功能
- 记录数据访问日志

## 📊 质量检查清单

### 代码提交前检查

- [ ] 代码通过 `make lint` 检查
- [ ] 所有测试通过 `make test`
- [ ] 代码覆盖率达标
- [ ] 文档已更新
- [ ] 提交信息符合规范

### 功能完成定义 (DoD)

- [ ] 功能实现完整
- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] 文档已更新
- [ ] 代码审查通过

## 🚀 部署要求

### 环境配置

- 支持Docker容器化部署
- 提供docker-compose配置
- 支持环境变量配置
- 提供健康检查接口

### 监控要求

- 提供Prometheus指标
- 集成Grafana仪表板
- 配置告警规则
- 记录结构化日志

## 📈 性能要求

### 响应时间

- API响应时间 ≤ 2秒
- 数据采集时间 ≤ 30秒
- 数据库查询时间 ≤ 1秒

### 并发能力

- 支持100个并发请求
- 支持1000个并发采集任务
- 支持水平扩展

## 🔧 工具链要求

### 开发工具

- 使用Black进行代码格式化
- 使用Ruff进行代码检查
- 使用MyPy进行类型检查
- 使用Pytest进行测试

### 自动化工具

- 使用pre-commit进行提交前检查
- 使用GitHub Actions进行CI/CD
- 使用Makefile提供一键命令
- 使用Docker进行环境隔离
