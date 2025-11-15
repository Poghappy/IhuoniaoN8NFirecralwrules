# Git Hooks 快速参考

**更新时间**: 2025-10-28
**文档版本**: v1.0.0

---

## 📖 完整文档

详细内容请参阅：[`docs/GIT_HOOKS_SPECIFICATION.md`](./GIT_HOOKS_SPECIFICATION.md)（1,000+ 行完整规范）

---

## 🚀 快速安装（5 分钟）

### 方法 1：Husky（推荐）

```bash
# 1. 安装依赖
npm install --save-dev husky lint-staged @commitlint/cli @commitlint/config-conventional

# 2. 初始化 Husky
npx husky install

# 3. 创建 Hooks
npx husky add .husky/pre-commit "npx lint-staged"
npx husky add .husky/commit-msg 'npx --no -- commitlint --edit "$1"'
npx husky add .husky/pre-push "npm test"

# 4. 配置自动安装
npm pkg set scripts.prepare="husky install"
```

### 方法 2：Pre-commit（Python）

```bash
# 1. 安装 pre-commit
pip install pre-commit

# 2. 创建配置文件（参考完整文档）
# .pre-commit-config.yaml

# 3. 安装 Hooks
pre-commit install
pre-commit install --hook-type commit-msg
```

---

## 🎯 核心功能

### Pre-commit Hooks（提交前检查）

- ✅ 代码格式化（Ruff/Black）
- ✅ Linter 检查（Ruff）
- ✅ 类型检查（mypy --strict）
- ✅ 敏感信息扫描（API 密钥、.env）
- ✅ 文件大小检查（>10MB）

### Commit-msg Hooks（提交消息验证）

- ✅ Conventional Commits 格式验证
- ✅ 提交类型检查（feat、fix、docs 等）
- ✅ 友好的错误提示

### Pre-push Hooks（推送前检查）

- ✅ 运行测试套件（pytest）
- ✅ 安全漏洞扫描（bandit，可选）
- ✅ 依赖检查（pip-audit，可选）
- ✅ 分支保护（禁止直接推送 main）

---

## 📝 提交消息格式

### 正确格式

```bash
<类型>(<范围>): <描述>

[可选的正文]

[可选的脚注]
```

### 示例

```bash
# ✅ 正确
git commit -m "feat(scraper): 添加夏威夷新闻爬虫"
git commit -m "fix(parser): 修复日期解析错误"
git commit -m "docs(readme): 更新安装指南"
git commit -m "refactor(storage): 优化数据存储格式"
git commit -m "perf(cache): 实现 Redis 缓存，节省 50% 成本"

# ❌ 错误
git commit -m "更新代码"
git commit -m "fix bug"
git commit -m "修改文件"
```

### 提交类型清单

| 类型 | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat(scraper): 添加新闻爬虫` |
| `fix` | Bug 修复 | `fix(parser): 修复日期解析` |
| `docs` | 文档更新 | `docs(api): 更新 API 文档` |
| `refactor` | 代码重构 | `refactor: 优化数据存储` |
| `perf` | 性能优化 | `perf(cache): 实现缓存机制` |
| `test` | 测试相关 | `test(scraper): 添加单元测试` |
| `chore` | 构建/工具链 | `chore(deps): 升级依赖版本` |
| `style` | 代码格式 | `style: 统一使用双引号` |

---

## 🛠️ 常用命令

### 日常使用

```bash
# 正常提交（自动触发 Hooks）
git add .
git commit -m "feat(scraper): 添加新功能"
git push

# 手动运行 lint-staged（仅检查暂存文件）
npx lint-staged

# 手动运行所有检查
pre-commit run --all-files
```

### 紧急情况（跳过 Hooks）

```bash
# ⚠️ 仅紧急情况使用！
git commit --no-verify -m "hotfix: 紧急修复生产环境错误"
git push --no-verify
```

**警告**：跳过 Hooks 后必须尽快补充修复！

---

## 🔒 安全检查详情

### 阻止的操作

1. **提交 .env 文件**

   ```bash
   ❌ 错误：尝试提交 .env 文件！
   请将 .env 添加到 .gitignore
   ```

2. **硬编码 API 密钥**

   ```bash
   ❌ 警告：检测到可能的硬编码 API 密钥！
   请使用环境变量：os.getenv('API_KEY')
   ```

3. **大文件提交（>10MB）**

   ```bash
   ❌ 错误：检测到大文件（>10MB）
   建议：使用 Git LFS 或外部存储
   ```

4. **直接推送到 main 分支**

   ```bash
   ❌ 错误：禁止直接推送到 main 分支！
   请创建 feature 分支并提交 Pull Request
   ```

---

## 🐛 故障排查

### 问题 1：Hooks 未执行

```bash
# 解决：添加执行权限
chmod +x .husky/*
chmod +x .git/hooks/*
```

### 问题 2：Husky 安装失败

```bash
# 解决：清理缓存重新安装
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### 问题 3：Commit-msg 验证失败

```bash
# 错误示例
git commit -m "更新代码"  # ❌

# 正确示例
git commit -m "feat(scraper): 添加新闻爬虫"  # ✅
```

### 问题 4：Pre-commit 检查太慢

```bash
# 解决：使用 lint-staged 仅检查变更文件
# 配置 package.json:
{
  "lint-staged": {
    "*.py": ["ruff format", "ruff check --fix"]
  }
}
```

### 问题 5：Pre-push 测试失败

```bash
# 本地运行测试查看详情
pytest tests/ -v

# 紧急情况跳过（不推荐）
git push --no-verify
```

---

## 📚 团队协作

### 配置共享

```bash
# 1. 将 Hooks 配置提交到 Git
git add .husky/ package.json commitlint.config.js
git commit -m "chore: 添加 Git Hooks 配置"
git push

# 2. 团队成员拉取后自动安装
git pull
npm install    # 自动运行 husky install
```

### CI/CD 集成

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: 安装依赖
        run: pip install ruff mypy pytest
      - name: Ruff 检查
        run: ruff check .
      - name: 类型检查
        run: mypy --strict src/
      - name: 运行测试
        run: pytest tests/
```

---

## 📖 相关文档

### 核心文档

- 📘 [Git Hooks 完整规范](./GIT_HOOKS_SPECIFICATION.md)（1,000+ 行）
- 📗 [AGENTS.md](../AGENTS.md)（AI 助手规范）
- 📙 [CHANGELOG.md](../CHANGELOG.md)（变更日志）

### 在线资源

- [Husky 官方文档](https://typicode.github.io/husky/)
- [lint-staged](https://github.com/okonet/lint-staged)
- [commitlint](https://commitlint.js.org/)
- [Conventional Commits](https://www.conventionalcommits.org/zh-hans/)
- [Pre-commit（Python）](https://pre-commit.com/)

---

## 🎓 最佳实践

1. **✅ 始终遵循 Conventional Commits**
   - 提交消息清晰明了
   - 便于自动生成 CHANGELOG
   - 支持语义化版本管理

2. **✅ 使用 lint-staged 提高效率**
   - 仅检查变更文件
   - 快速反馈
   - 节省时间

3. **✅ 团队共享 Hooks 配置**
   - 统一代码质量标准
   - 减少审查成本
   - 提高协作效率

4. **⚠️ 谨慎使用 --no-verify**
   - 仅紧急情况使用
   - 事后必须补充修复
   - 记录跳过原因

5. **✅ CI/CD 双重验证**
   - 本地 Hooks + 服务端检查
   - 防止绕过 Hooks
   - 确保代码质量

---

## 💡 提示

### 第一次使用？

1. 阅读完整规范：`docs/GIT_HOOKS_SPECIFICATION.md`
2. 选择安装方案（Husky 推荐）
3. 测试提交一次代码
4. 查看 Hook 执行结果

### 遇到问题？

1. 查看故障排查章节
2. 阅读完整规范的详细说明
3. 检查相关配置文件

### 想要自定义？

参考完整规范的"最佳实践"章节，了解如何：

- 添加自定义检查
- 调整 Hook 逻辑
- 集成其他工具

---

**维护者**: HawaiiHub AI Team
**版本**: v1.0.0
**最后更新**: 2025-10-28

**快速跳转**：[📘 完整规范](./GIT_HOOKS_SPECIFICATION.md) | [📗 AGENTS.md](../AGENTS.md) | [📙 CHANGELOG.md](../CHANGELOG.md)
