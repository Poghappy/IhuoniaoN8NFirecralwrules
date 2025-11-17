# 贡献指南

感谢您对 HawaiiHub.net 项目的关注！我们欢迎所有形式的贡献。

## 📋 目录

- [行为准则](#行为准则)
- [如何贡献](#如何贡献)
- [开发环境设置](#开发环境设置)
- [代码规范](#代码规范)
- [提交规范](#提交规范)
- [Pull Request 流程](#pull-request-流程)

## 🤝 行为准则

参与本项目时，请遵守以下行为准则：

- 尊重所有贡献者
- 接受建设性的批评
- 专注于对项目最有利的事情
- 对其他社区成员表示同理心

## 🚀 如何贡献

### 报告问题

如果您发现了 bug 或有功能建议，请：

1. 检查 [Issues](https://github.com/Poghappy/IhuoniaoN8NFirecralwrules/issues) 是否已有相关问题
2. 如果没有，创建新 Issue，包含：
   - 清晰的问题描述
   - 复现步骤
   - 预期行为 vs 实际行为
   - 环境信息（Python 版本、操作系统等）

### 贡献代码

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: 添加新功能'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 🛠️ 开发环境设置

### 1. 克隆仓库

```bash
git clone https://github.com/Poghappy/IhuoniaoN8NFirecralwrules.git
cd IhuoniaoN8NFirecralwrules
```

### 2. 安装依赖

```bash
# 使用 uv (推荐)
uv pip install -r requirements.txt

# 或使用 pip
pip install -r requirements.txt
```

### 3. 配置环境

```bash
# 复制配置示例
cp Firecrawl代码模块/配置示例.json Firecrawl代码模块/config.json

# 编辑配置文件，填入必要的 API 密钥和配置
```

### 4. 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest Firecrawl代码模块/集成测试.py

# 带覆盖率
pytest --cov=Firecrawl代码模块
```

## 📝 代码规范

### Python 代码规范

1. **类型注解**（必需）
   ```python
   def process_data(items: list[str]) -> dict[str, int]:
       """处理数据并返回统计结果。"""
       return {"count": len(items)}
   ```

2. **文档字符串**（中文）
   ```python
   def collect_article(url: str) -> dict[str, Any]:
       """采集指定 URL 的文章内容。
       
       Args:
           url: 要采集的网页 URL
           
       Returns:
           包含文章数据的字典
           
       Raises:
           ValueError: 当 URL 格式无效时
       """
   ```

3. **代码格式化**
   ```bash
   # 使用 ruff 格式化
   ruff format .
   
   # 检查代码风格
   ruff check .
   ```

4. **类型检查**
   ```bash
   mypy --strict Firecrawl代码模块/
   ```

### 命名规范

- **变量和函数**: 小写字母 + 下划线 (`snake_case`)
- **类名**: 大驼峰命名法 (`PascalCase`)
- **常量**: 大写字母 + 下划线 (`UPPER_SNAKE_CASE`)
- **私有方法**: 单下划线前缀 (`_private_method`)

## 📤 提交规范

我们使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

### 提交类型

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式调整（不影响代码运行）
- `refactor`: 代码重构
- `perf`: 性能优化
- `test`: 添加或修改测试
- `chore`: 构建过程或辅助工具的变动

### 提交格式

```
<类型>(<范围>): <描述>

[可选的正文]

[可选的脚注]
```

### 示例

```bash
feat(collector): 添加批量采集功能

支持同时采集多个 URL，提高采集效率

Closes #123
```

```bash
fix(api): 修复 API 超时问题

修复了长时间请求导致的超时错误，增加了重试机制
```

## 🔄 Pull Request 流程

### 1. 准备工作

- [ ] 代码已通过所有测试
- [ ] 代码已通过 lint 检查
- [ ] 代码已通过类型检查
- [ ] 已更新相关文档
- [ ] 提交信息符合规范

### 2. 创建 PR

1. 确保您的分支是最新的
   ```bash
   git checkout main
   git pull origin main
   git checkout your-branch
   git rebase main
   ```

2. 推送您的分支
   ```bash
   git push origin your-branch
   ```

3. 在 GitHub 上创建 Pull Request

### 3. PR 描述模板

```markdown
## 变更描述
简要描述本次 PR 的变更内容

## 变更类型
- [ ] Bug 修复
- [ ] 新功能
- [ ] 文档更新
- [ ] 代码重构
- [ ] 性能优化

## 测试
描述如何测试这些变更

## 相关 Issue
Closes #123
```

### 4. 代码审查

- 所有 PR 都需要至少一位维护者的审查
- 审查者可能会要求修改
- 请及时响应审查意见

## 🧪 测试指南

### 编写测试

- 所有新功能都应该包含测试
- 测试文件位于 `tests/` 目录
- 使用 `pytest` 作为测试框架

### 测试示例

```python
import pytest
from Firecrawl代码模块.火爬采集器 import FirecrawlCollector

def test_collect_single_page() -> None:
    """测试单页采集功能。"""
    collector = FirecrawlCollector(api_key="test_key")
    result = collector.scrape_single_page("https://example.com")
    assert result is not None
    assert "content" in result
```

## 📚 文档贡献

- 更新代码时，请同步更新相关文档
- 文档使用 Markdown 格式
- 代码示例应该可以运行
- 保持文档简洁清晰

## ❓ 需要帮助？

如果您在贡献过程中遇到问题：

1. 查看 [Issues](https://github.com/Poghappy/IhuoniaoN8NFirecralwrules/issues)
2. 查看项目文档
3. 创建新 Issue 询问

## 🙏 致谢

感谢所有为本项目做出贡献的开发者！

---

**注意**: 提交代码即表示您同意将您的贡献在项目许可证下发布。

