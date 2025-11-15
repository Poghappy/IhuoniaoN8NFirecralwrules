# Cursor IDE 配置说明

**版本**: v3.0  
**最后更新**: 2025-11-13  
**基于**: Cursor IDE 2025 最佳实践

---

## 📁 配置结构

```
.cursor/
├── README.md                    # 本说明文档
└── rules/                       # 规则文件目录
    ├── core-principles.mdc      # 核心开发原则
    ├── development-standards.mdc # 开发规范和代码标准
    ├── mcp-tools.mdc            # MCP工具使用规范
    ├── security.mdc             # 安全规范
    ├── quality-assurance.mdc    # 质量保证和测试规范
    └── compliance.mdc           # 合规性要求
```

项目根目录:
- `AGENTS.md`                    # 主配置文件（简单易读）

---

## 🎯 配置说明

### 规则文件类型

根据 Cursor IDE 2025 最佳实践，规则文件使用 MDC 格式，支持以下类型：

1. **Always Apply** (`alwaysApply: true`)
   - 自动应用到每个聊天会话
   - 适用于核心原则、安全规范等全局规则

2. **Apply Intelligently** (`alwaysApply: false`, 有 `description`)
   - 当 Agent 判断相关时自动应用
   - 适用于特定场景的规则

3. **Apply to Specific Files** (`globs` 配置)
   - 当文件匹配指定模式时应用
   - 适用于特定文件类型的规则

4. **Apply Manually** (无 `alwaysApply`, 无 `globs`)
   - 需要手动 @ 提及才应用
   - 适用于可选规则

### 当前规则配置

| 规则文件 | 类型 | 说明 |
|---------|------|------|
| `core-principles.mdc` | Always Apply | 核心开发原则，始终应用 |
| `development-standards.mdc` | Always Apply | 开发规范，始终应用 |
| `mcp-tools.mdc` | Apply to Specific Files | MCP 工具相关文件时应用 |
| `security.mdc` | Always Apply | 安全规范，始终应用 |
| `quality-assurance.mdc` | Apply to Specific Files | 测试文件时应用 |
| `compliance.mdc` | Always Apply | 合规性要求，始终应用 |

---

## 📋 规则优先级

根据 Cursor IDE 官方文档，规则应用优先级：

1. **Team Rules** (团队规则，如果有)
2. **Project Rules** (`.cursor/rules/*.mdc`)
3. **User Rules** (用户全局规则)
4. **AGENTS.md** (项目根目录)

所有适用的规则会被合并，较早的来源在冲突时优先。

---

## 🔄 配置更新历史

### v3.0 (2025-11-13)
- ✅ 重构为 Cursor IDE 2025 最佳实践格式
- ✅ 合并去重复所有规则
- ✅ 按功能分类创建多个规则文件
- ✅ 创建 AGENTS.md 主配置文件
- ✅ 遵循规则文件不超过 500 行的最佳实践

### 合并的原始配置文件
- `global-rules.md` - 全局规则
- `user-rules.md` - 用户规则
- `n8n工具/文档/AI助手提示词.md` - AI 提示词
- `n8n工具/文档/AI助手配置.md` - AI 配置
- `n8n工具/文档/项目特定规则.md` - 项目规则
- `n8n工具/文档/项目规则.md` - 项目规则

---

## 📝 使用说明

### 查看规则状态
1. 打开 Cursor Settings (`Cmd/Ctrl + ,`)
2. 导航到 `Cursor Settings > Rules`
3. 查看所有规则及其状态

### 创建新规则
1. 使用命令面板 (`Cmd/Ctrl + Shift + P`)
2. 输入 "New Cursor Rule"
3. 或直接在 `.cursor/rules/` 目录创建 `.mdc` 文件

### 规则文件格式示例

```markdown
---
description: 规则描述
alwaysApply: true  # 或 false
globs:             # 可选，文件匹配模式
  - "**/*.test.*"
  - "**/tests/**"
---

# 规则内容

规则的具体内容...
```

---

## ✅ 最佳实践

根据 Cursor IDE 2025 官方文档：

1. **保持规则聚焦**: 每个规则文件专注于一个主题
2. **规则长度**: 保持规则在 500 行以内
3. **可组合性**: 将大规则拆分为多个可组合的规则
4. **具体示例**: 提供具体的示例或引用文件
5. **清晰指导**: 像清晰的内部文档一样编写规则，避免模糊指导
6. **可重用性**: 在聊天中重复使用规则时，创建规则文件

---

## 🔗 相关资源

- [Cursor IDE Rules 官方文档](https://cursor.com/docs/context/rules)
- [Cursor Rules 最佳实践指南](https://cursorrules.org/article)
- [Awesome Cursor Rules](https://github.com/PatrickJS/awesome-cursorrules)

---

**维护**: 本配置由项目团队共同维护，定期根据 Cursor IDE 更新和项目需求进行优化。


