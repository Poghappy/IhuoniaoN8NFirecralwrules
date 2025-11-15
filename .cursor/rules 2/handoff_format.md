# 统一交接格式（{HANDOFF_FORMAT}）

## 【格式说明】

所有角色交接必须使用统一的JSON格式，确保信息传递的完整性和一致性。

## 【JSON结构】

```json
{
  "inputs": {
    "description": "本角色接收的输入信息",
    "sources": [
      "上游角色的输出",
      "相关文档和资料",
      "用户需求和约束"
    ],
    "constraints": [
      "技术约束",
      "业务约束",
      "时间约束"
    ]
  },
  "decisions": [
    {
      "topic": "决策主题",
      "choice": "选择的方案",
      "rationale": "选择理由和权衡考虑",
      "alternatives": [
        "考虑过的其他方案"
      ],
      "impact": "决策的影响范围"
    }
  ],
  "artifacts": [
    {
      "path": "产出文件的路径",
      "summary": "文件内容摘要",
      "owner": "文件负责人",
      "status": "文件状态（draft/review/approved）",
      "dependencies": [
        "依赖的其他文件"
      ]
    }
  ],
  "risks": [
    {
      "name": "风险名称",
      "impact": "风险影响（高/中/低）",
      "probability": "发生概率（高/中/低）",
      "mitigation": "缓解措施",
      "owner": "风险负责人",
      "deadline": "风险处理截止时间"
    }
  ],
  "next_role": "下一个角色名称",
  "next_instruction": "给下个角色的明确待办事项",
  "quality_gates": [
    {
      "gate": "质量闸口名称",
      "status": "通过状态（passed/failed/pending）",
      "evidence": "通过证据",
      "issues": [
        "发现的问题"
      ]
    }
  ],
  "metrics": {
    "completion_percentage": 85,
    "quality_score": 4.2,
    "estimated_effort": "5人天",
    "actual_effort": "4.5人天"
  }
}
```

## 【字段详细说明】

### inputs（输入信息）

- **description**: 简要描述本角色接收的输入信息
- **sources**: 输入信息的来源列表
- **constraints**: 影响决策的约束条件

### decisions（关键决策）

- **topic**: 决策的具体主题
- **choice**: 最终选择的方案
- **rationale**: 选择理由和权衡考虑
- **alternatives**: 考虑过的其他方案
- **impact**: 决策的影响范围

### artifacts（产出工件）

- **path**: 产出文件的完整路径
- **summary**: 文件内容的核心摘要
- **owner**: 文件的负责人
- **status**: 文件的当前状态
- **dependencies**: 文件依赖的其他文件

### risks（风险识别）

- **name**: 风险的具体名称
- **impact**: 风险的影响程度
- **probability**: 风险发生的概率
- **mitigation**: 具体的缓解措施
- **owner**: 风险负责人
- **deadline**: 风险处理截止时间

### next_role（下一个角色）

- 指定下一个负责的角色名称
- 确保角色转换的连续性

### next_instruction（交接指令）

- 给下一个角色的明确待办事项
- 包含具体的任务要求和期望

### quality_gates（质量闸口）

- **gate**: 质量闸口的名称
- **status**: 质量闸口的通过状态
- **evidence**: 通过质量闸口的证据
- **issues**: 发现的问题列表

### metrics（度量指标）

- **completion_percentage**: 完成百分比
- **quality_score**: 质量评分（1-5分）
- **estimated_effort**: 预估工作量
- **actual_effort**: 实际工作量

## 【Firecrawl项目特定示例】

### 产品负责人（PO）交接示例

```json
{
  "inputs": {
    "description": "接收了业务背景、用户需求、市场分析等输入信息",
    "sources": [
      "市场调研报告",
      "用户访谈记录",
      "竞品分析文档",
      "技术可行性评估"
    ],
    "constraints": [
      "预算限制：100万人民币",
      "时间限制：6个月交付",
      "技术约束：Python + FastAPI技术栈",
      "合规要求：GDPR数据保护"
    ]
  },
  "decisions": [
    {
      "topic": "目标用户群体定位",
      "choice": "主要面向B2B企业用户，次要面向个人用户",
      "rationale": "B2B用户付费意愿强，需求稳定，有利于产品商业化",
      "alternatives": [
        "纯B2C个人用户",
        "纯B2B企业用户",
        "B2B2C混合模式"
      ],
      "impact": "影响产品功能设计、定价策略、营销策略"
    },
    {
      "topic": "核心功能优先级",
      "choice": "数据采集 + AI分析为核心功能，多租户为重要功能",
      "rationale": "数据采集是基础需求，AI分析是差异化优势，多租户是企业级必需",
      "alternatives": [
        "仅数据采集功能",
        "数据采集 + 可视化",
        "全功能平台"
      ],
      "impact": "影响开发优先级、资源分配、产品定位"
    }
  ],
  "artifacts": [
    {
      "path": "docs/PROJECT_BRIEF.md",
      "summary": "项目概述、目标用户、成功指标、约束条件",
      "owner": "PO",
      "status": "approved",
      "dependencies": []
    }
  ],
  "risks": [
    {
      "name": "用户接受度风险",
      "impact": "高",
      "probability": "中",
      "mitigation": "早期用户验证，持续用户反馈收集",
      "owner": "PM",
      "deadline": "2024-10-15"
    },
    {
      "name": "技术实现风险",
      "impact": "中",
      "probability": "低",
      "mitigation": "技术预研，原型验证",
      "owner": "Arch",
      "deadline": "2024-09-30"
    }
  ],
  "next_role": "PM",
  "next_instruction": "基于PROJECT_BRIEF创建详细的用户故事和PRD，重点关注数据采集和AI分析功能",
  "quality_gates": [
    {
      "gate": "业务目标清晰",
      "status": "passed",
      "evidence": "PROJECT_BRIEF中明确定义了目标用户、成功指标、约束条件",
      "issues": []
    }
  ],
  "metrics": {
    "completion_percentage": 100,
    "quality_score": 4.5,
    "estimated_effort": "3人天",
    "actual_effort": "2.5人天"
  }
}
```

### 产品经理（PM）交接示例

```json
{
  "inputs": {
    "description": "接收了PROJECT_BRIEF、用户需求、业务目标等输入信息",
    "sources": [
      "docs/PROJECT_BRIEF.md",
      "用户访谈记录",
      "竞品分析报告",
      "技术可行性评估"
    ],
    "constraints": [
      "6个月交付时间",
      "Python + FastAPI技术栈",
      "多租户架构要求",
      "AI功能集成需求"
    ]
  },
  "decisions": [
    {
      "topic": "功能优先级排序",
      "choice": "MoSCoW优先级：数据采集(Must)、AI分析(Should)、多租户(Should)、可视化(Could)",
      "rationale": "数据采集是核心功能，AI分析是差异化优势，多租户是企业级必需，可视化是用户体验提升",
      "alternatives": [
        "所有功能同等优先级",
        "仅核心功能优先"
      ],
      "impact": "影响开发计划、资源分配、产品迭代"
    },
    {
      "topic": "用户界面设计",
      "choice": "采用现代化Web界面，支持响应式设计，集成AI聊天功能",
      "rationale": "现代化界面提升用户体验，响应式设计支持多设备访问，AI聊天降低使用门槛",
      "alternatives": [
        "传统Web界面",
        "移动端优先设计"
      ],
      "impact": "影响前端开发、用户体验、技术选型"
    }
  ],
  "artifacts": [
    {
      "path": "docs/USER_STORIES.md",
      "summary": "7个核心用户故事，包含验收标准",
      "owner": "PM",
      "status": "review",
      "dependencies": ["docs/PROJECT_BRIEF.md"]
    },
    {
      "path": "docs/PRD.md",
      "summary": "完整的产品需求文档，包含功能规格、接口设计、验收标准",
      "owner": "PM",
      "status": "draft",
      "dependencies": ["docs/USER_STORIES.md"]
    }
  ],
  "risks": [
    {
      "name": "需求变更风险",
      "impact": "中",
      "probability": "高",
      "mitigation": "敏捷开发，快速迭代，用户反馈收集",
      "owner": "PM",
      "deadline": "持续"
    },
    {
      "name": "AI功能准确性风险",
      "impact": "高",
      "probability": "中",
      "mitigation": "AI模型训练，用户反馈优化，人工校正功能",
      "owner": "LLME",
      "deadline": "2024-10-30"
    }
  ],
  "next_role": "BA",
  "next_instruction": "基于PRD进行详细需求分析，补充技术需求，完善接口设计",
  "quality_gates": [
    {
      "gate": "用户故事完整",
      "status": "passed",
      "evidence": "7个用户故事覆盖主要使用场景，包含验收标准",
      "issues": []
    },
    {
      "gate": "PRD可执行",
      "status": "pending",
      "evidence": "PRD文档正在完善中",
      "issues": ["需要补充技术细节"]
    }
  ],
  "metrics": {
    "completion_percentage": 80,
    "quality_score": 4.0,
    "estimated_effort": "5人天",
    "actual_effort": "4人天"
  }
}
```

## 【质量检查清单】

### 交接格式检查

- [ ] JSON格式正确
- [ ] 所有必填字段完整
- [ ] 字段内容准确
- [ ] 逻辑关系清晰

### 内容质量检查

- [ ] 输入信息充分
- [ ] 决策理由合理
- [ ] 产出工件完整
- [ ] 风险识别全面

### 交接连续性检查

- [ ] 下一个角色明确
- [ ] 交接指令具体
- [ ] 依赖关系清晰
- [ ] 质量闸口通过

---

**格式版本**: v1.0.0  
**适用项目**: Firecrawl数据采集器  
**维护者**: AI Assistant  
**最后更新**: 2024-09-22
