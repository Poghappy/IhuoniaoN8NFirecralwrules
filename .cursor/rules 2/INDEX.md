# 🤖 Prompts 索引

> AI Agent 提示词和配置文件

**最后更新**: 2024-10-29

---

## 📂 目录结构

### 📋 指南文档

#### 核心指南

- [00_guidelines.md](./00_guidelines.md) - 通用指南和最佳实践
- [README.md](./README.md) - Prompts 使用说明

#### 项目配置

- [project_config.md](./project_config.md) - 项目配置说明
- [guardrails.md](./guardrails.md) - 安全护栏和限制

---

### 🔄 开发流程

#### 流程阶段（按序号排列）

1. [10_user_story.md](./10_user_story.md) - 用户故事和需求收集
2. [20_prd.md](./20_prd.md) - 产品需求文档
3. [30_task_breakdown.md](./30_task_breakdown.md) - 任务分解
4. [40_tech_design.md](./40_tech_design.md) - 技术设计
5. [50_impl.md](./50_impl.md) - 实施指南
6. [60_test.md](./60_test.md) - 测试策略
7. [70_iteration.md](./70_iteration.md) - 迭代优化

---

### 👥 角色定义

- [roles/](./roles/) - 各类角色的 Prompt 定义
  - 产品经理
  - 架构师
  - 开发工程师
  - 测试工程师
  - DevOps 工程师
  - 等...

---

### 📊 系统 Prompt

#### 核心 Prompt

- [system_prompt.md](./system_prompt.md) - 系统级提示词
- [orchestrator.md](./orchestrator.md) - 编排器配置
- [handoff_format.md](./handoff_format.md) - 交接格式规范

#### 阶段 Prompt

- [stages/](./stages/) - 各阶段专用 Prompt

---

## 🗂️ 归档文件

- `archive.zip` - 历史 Prompt 归档
  - 包含过时的或已弃用的 Prompt 配置

---

## 🔍 快速查找

### 我想

#### 创建新功能

1. 阅读 [10_user_story.md](./10_user_story.md) 编写用户故事
2. 参考 [20_prd.md](./20_prd.md) 生成 PRD
3. 使用 [30_task_breakdown.md](./30_task_breakdown.md) 分解任务
4. 遵循 [40_tech_design.md](./40_tech_design.md) 进行设计
5. 按照 [50_impl.md](./50_impl.md) 实施
6. 根据 [60_test.md](./60_test.md) 测试
7. 参考 [70_iteration.md](./70_iteration.md) 迭代优化

#### 配置 AI Agent

- 系统配置 → [system_prompt.md](./system_prompt.md)
- 角色定义 → [roles/](./roles/)
- 安全限制 → [guardrails.md](./guardrails.md)

#### 了解规范

- 通用指南 → [00_guidelines.md](./00_guidelines.md)
- 交接规范 → [handoff_format.md](./handoff_format.md)
- 编排规则 → [orchestrator.md](./orchestrator.md)

---

## 📝 使用建议

### Prompt 开发流程

#### 1. 需求阶段

```
用户故事 → PRD → 任务分解
```

#### 2. 设计阶段

```
技术设计 → 架构评审 → 实施计划
```

#### 3. 实施阶段

```
代码实现 → 单元测试 → 集成测试
```

#### 4. 优化阶段

```
性能优化 → 代码审查 → 迭代改进
```

---

## 🎯 最佳实践

### Prompt 编写原则

1. **清晰明确** - 使用简洁清晰的语言
2. **结构化** - 保持良好的层次结构
3. **可复用** - 设计可重用的 Prompt 组件
4. **可测试** - 确保 Prompt 效果可验证

### 版本管理

- 重要变更记录版本号
- 过时的 Prompt 移至归档
- 定期审查和更新

---

**维护者**: AI 全栈工程师团队
**贡献**: 欢迎提交优化建议
