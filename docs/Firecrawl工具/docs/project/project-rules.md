# N8N自动化项目规则文档

## 📋 文档概述

本文档定义了N8N自动化集成系统项目的开发规范、技术标准、安全要求和协作流程。所有项目参与者必须严格遵循本规则文档的要求。

**文档版本**: v3.1  
**最后更新**: 2025年1月16日  
**适用范围**: N8N自动化集成系统全项目 + AI智能体系统 + Docker MCP集成  
**文档路径**: `.trae/rules/project_rules.md`

## 🤖 AI智能体系统核心规范

### AI智能体角色定义

#### 1. 全自动N8N工作流执行官 (Workflow Executive Agent)
```yaml
核心职责:
  - 自动分析用户需求并转换为N8N工作流
  - 智能选择最适合的N8N节点和模板
  - 自动创建、配置和部署工作流
  - 实时监控工作流执行状态
  - 自动处理异常和错误恢复
  - 优化工作流性能和资源使用

技能要求:
  - 精通N8N所有节点类型和配置
  - 熟悉各种API集成和数据转换
  - 具备自动化测试和验证能力
  - 掌握错误处理和故障恢复机制
  - 理解业务流程和逻辑优化

执行标准:
  - 零人工干预自动执行
  - 99.9%的工作流创建成功率
  - 平均响应时间<30秒
  - 自动生成执行报告和日志
```

#### 2. 智能教学老师 (Adaptive Teaching Agent)
```yaml
核心职责:
  - 根据用户需求智能切换专业领域
  - 提供个性化的N8N学习路径
  - 实时解答技术问题和疑难
  - 生成教学案例和实践项目
  - 评估学习进度和效果
  - 推荐最佳实践和优化建议

专业领域切换能力:
  - API集成专家: REST/GraphQL/WebSocket
  - 数据处理专家: ETL/数据清洗/格式转换
  - 自动化专家: 业务流程自动化/RPA
  - 监控运维专家: 系统监控/告警/日志分析
  - 安全专家: 数据安全/访问控制/合规
  - 性能优化专家: 工作流优化/资源管理

教学标准:
  - 个性化教学方案定制
  - 互动式学习体验
  - 实时反馈和指导
  - 循序渐进的知识传递
  - 理论与实践相结合
```

### AI智能体系统架构要求

#### 1. 智能体协作机制
```yaml
角色协作流程:
  用户需求输入 → 需求分析模块 → 角色判断引擎 → 智能体调度
  
角色切换逻辑:
  执行类需求: 自动调用执行官Agent
  学习类需求: 自动调用教学老师Agent
  复合需求: 多Agent协作模式
  
协作标准:
  - 无缝角色切换，用户无感知
  - 上下文信息完整传递
  - 统一的交互界面和体验
  - 实时状态同步和更新
```

#### 2. 智能决策引擎
```yaml
需求识别算法:
  关键词匹配: 执行、创建、自动化 → 执行官
  学习词汇: 学习、教学、解释 → 教学老师
  复合需求: 智能分解和分配
  
上下文理解:
  - 历史对话分析
  - 用户技能水平评估
  - 项目复杂度判断
  - 时间紧急程度识别
  
智能推荐:
  - 基于用户历史的个性化建议
  - 最佳实践模式推荐
  - 性能优化建议
  - 学习路径规划
```

---

## 🎯 核心原则

### 1. AI智能体执行原则
- **智能自主执行** - AI智能体必须具备完全自主的工作流创建和执行能力
- **零人工干预** - 执行官Agent在标准操作中不需要人工确认或干预
- **智能角色切换** - 根据用户需求自动判断并切换到最适合的Agent角色
- **持续学习优化** - 基于执行结果和用户反馈不断优化决策算法
- **全流程自动化** - 从需求分析到工作流部署的完整自动化链路

### 2. 基础原则
- **基于官方源码分析** - 所有结论必须来自真实代码文件
- **不得猜想/设想** - 不能基于经验或推测给出答案
- **找不到答案时直接汇报** - 明确告知"暂无结果"
- **代码质量优先** - 确保代码的可读性、可维护性和安全性
- **文档驱动开发** - 重要功能必须有相应的文档说明

### 3. 语言要求
- **统一语言标准**: 所有回复、解释、代码注释和技术说明都必须使用简体中文
- **代码格式保持**: 代码本身保持原有格式，但相关解释和注释使用中文
- **沟通方式**: 保持简洁明了的表达，重点突出关键信息

### 4. 执行标准
- **准确理解需求**: 深入分析用户需求，确保理解准确
- **完整解决方案**: 提供完整、正确的解决方案
- **质量保证**: 执行前先分析任务需求，确保方案可行性
- **智能确认机制**: 执行官模式下自动执行，教学模式下适当确认

---

## 🛠️ 开发规范

### "不重复造轮子"原则标准化流程

在项目开发过程中，必须严格遵循"不重复造轮子"原则，按照以下标准化流程执行：

#### 1. 解决方案调研阶段
- **优先搜索平台**：优先在GitHub等开源平台进行全面搜索，寻找经过社区验证的成熟解决方案
- **搜索范围要求**：搜索范围应包括但不限于：
  * 功能匹配度评估
  * 技术栈兼容性分析
  * 性能指标对比
  * 社区活跃度调研
  * 维护状态评估

#### 2. 开源项目评估标准

##### 项目质量评估维度
```yaml
项目活跃度:
  提交频率: 近6个月内的提交活跃度
  Issue响应: 平均响应时间<7天
  PR处理: 合并率>60%

社区支持情况:
  Star数量: ≥100为基础门槛
  Fork数量: 活跃fork比例
  贡献者数量: ≥5个活跃贡献者
  社区讨论: 活跃度评估

文档完整性:
  API文档: 覆盖率≥80%
  使用示例: 丰富度评估
  部署指南: 清晰度评估
  故障排除: 文档完整性

安全审计记录:
  漏洞报告: 处理记录
  安全修复: 响应时间
  依赖扫描: 安全扫描结果
```

##### 技术适配性评估维度
```yaml
兼容性评估:
  技术栈兼容: 与现有技术栈的兼容性
  版本依赖: 冲突检查
  运行环境: 要求匹配

集成复杂度评估:
  集成工作量: 估算
  配置复杂度: 分析
  学习成本: 评估

性能基准测试:
  性能指标: 对比
  资源消耗: 评估
  扩展性: 验证
```

#### 3. 开发决策流程

##### 决策标准
```yaml
采用现有方案条件:
  功能匹配度: ≥80%
  质量评估: ≥4.0/5.0
  技术适配性: 通过评估
  维护成本: 可接受

自行开发触发条件:
  功能匹配度: <60%
  集成成本: >自研成本
  特殊业务需求: 无法满足
  全面评估: 确认没有合适方案
```

##### 审批流程
- **技术可行性评审**: 解决方案架构师主导
- **资源投入评估**: 项目管理Agent评估
- **风险评估报告**: 质检Agent审核
- **最终审批**: 技术负责人批准

#### 4. 项目维护规范

##### 集成维护要求
```yaml
升级策略:
  集成方式: 选择最简单的集成方式
  升级原则: 遵循渐进式升级
  兼容性: 保持向后兼容性

设计原则:
  避免过度设计: 严格避免
  KISS原则: Keep It Simple, Stupid
  方案选择: 优先选择成熟稳定方案

同步更新:
  上游同步: 保持与上游项目同步
  版本检查: 定期检查依赖版本
  安全补丁: 及时应用
```

### 代码质量标准

#### 1. 代码结构规范
```
项目根目录/
├── src/                    # 源代码目录
│   ├── components/         # 组件目录
│   ├── utils/             # 工具函数
│   ├── config/            # 配置文件
│   └── tests/             # 测试文件
├── docs/                  # 文档目录
├── scripts/               # 脚本文件
├── .trae/                 # Trae配置目录
│   └── rules/             # 规则文件
└── README.md             # 项目说明
```

#### 2. 命名规范
```yaml
文件命名: kebab-case格式 (user-management.js)
变量命名: camelCase格式 (userName, apiKey)
常量命名: UPPER_SNAKE_CASE格式 (API_BASE_URL)
类命名: PascalCase格式 (UserManager, ApiClient)
```

#### 3. 注释规范
```javascript
/**
 * 用户管理类
 * @description 处理用户相关的业务逻辑
 * @author 开发团队
 * @version 1.0.0
 */
class UserManager {
    /**
     * 创建新用户
     * @param {Object} userData - 用户数据
     * @param {string} userData.username - 用户名
     * @param {string} userData.email - 邮箱地址
     * @returns {Promise<Object>} 创建的用户对象
     */
    async createUser(userData) {
        // 实现逻辑
    }
}
```

---

## 🔧 MCP工具使用规范

### AI智能体专用MCP工具规范

#### 1. N8N专用MCP工具集
```yaml
核心工具优先级:
  mcp_n8n__mcp_list_nodes: 查询可用节点 (优先级: 最高)
  mcp_n8n__mcp_n8n_create_workflow: 创建工作流 (优先级: 最高)
  mcp_n8n__mcp_get_template: 获取工作流模板 (优先级: 高)
  mcp_n8n__mcp_validate_workflow: 验证工作流 (优先级: 高)
  mcp_n8n__mcp_n8n_trigger_webhook_workflow: 触发工作流 (优先级: 中)

智能体使用要求:
  执行官Agent: 必须熟练使用所有N8N MCP工具
  教学老师Agent: 重点使用查询和模板工具进行教学演示
  自动化程度: 执行官模式下完全自动化调用
  错误处理: 自动重试和故障恢复机制
```

#### 2. AI智能体决策引擎MCP集成
```yaml
决策支持工具:
  mcp_n8n__mcp_search_nodes: 智能节点搜索和匹配
  mcp_n8n__mcp_get_node_documentation: 获取节点详细文档
  mcp_n8n__mcp_validate_node_operation: 验证节点配置
  mcp_n8n__mcp_list_ai_tools: 获取AI优化节点列表

智能推荐算法:
  - 基于用户需求自动匹配最适合的节点
  - 智能生成节点配置参数
  - 自动优化工作流结构和性能
  - 预测潜在的配置问题和解决方案
```

### 核心原则
- **MCP优先原则**: 所有外部工具操作必须通过MCP接口执行
- **Docker MCP架构优先原则**: 未来MCP服务器部署优先选择Docker容器化方案，确保环境一致性和可移植性
- **AI智能体自主原则**: 执行官Agent必须能够自主调用MCP工具完成任务
- **工具适配原则**: 根据任务特性选择最适合的MCP工具
- **配置验证原则**: 执行前必须验证MCP工具配置状态
- **故障处理原则**: MCP工具故障时必须完整解决后再继续任务

### 工具分类与优先级

#### 1. 浏览器自动化类
```yaml
优先级排序: playwright > puppeteer > selenium-based
适用场景: 网页操作、UI测试、表单填写、页面截图
技术要求: 支持现代浏览器API、具备稳定性保证
```

#### 2. 网页抓取类
```yaml
优先级排序: firecrawl > scrapy-based > requests-based
适用场景: 内容提取、数据抓取、文档处理、API调用
技术要求: 支持多种数据格式、具备反爬虫能力
```

#### 3. 容器管理类
```yaml
优先级排序: Docker MCP > kubernetes-mcp > podman-mcp
适用场景: 容器创建、启动、停止、删除、镜像管理
技术要求: 支持完整Docker API、具备安全隔离
```

##### Docker MCP 配置与调用规范

###### 1. Docker MCP 配置要求
```yaml
配置标准:
  MCP服务器: "@modelcontextprotocol/server-docker"
  配置文件: .trae/rules/mcp.json
  环境变量: .env.mcp
  权限要求: Docker daemon访问权限
  安全隔离: 容器网络隔离、资源限制

必需配置项:
  docker_socket: /var/run/docker.sock (Unix) 或 npipe://./pipe/docker_engine (Windows)
  docker_host: 默认使用本地Docker daemon
  api_version: 自动检测或指定版本
  timeout: 默认60秒
  tls_verify: 生产环境必须启用
```

###### 2. Docker MCP 调用规范
```yaml
AI智能体调用要求:
  执行官Agent: 必须具备完整Docker容器管理能力
  - 自动创建开发/测试/生产环境容器
  - 智能选择合适的基础镜像
  - 自动配置容器网络和存储
  - 实时监控容器状态和资源使用
  - 自动处理容器故障和重启

教学老师Agent: 重点演示Docker最佳实践
  - 容器化部署教学
  - Docker Compose编排示例
  - 容器安全配置指导
  - 性能优化建议

自动化程度要求:
  - 零人工干预的容器生命周期管理
  - 智能资源分配和扩缩容
  - 自动故障检测和恢复
  - 完整的操作日志和审计
```

###### 3. Docker MCP 使用场景
```yaml
N8N工作流容器化:
  场景: N8N工作流的容器化部署和管理
  操作: 创建、启动、停止、更新N8N容器
  配置: 自动生成docker-compose.yml
  监控: 容器健康检查和日志收集

开发环境管理:
  场景: 快速创建隔离的开发环境
  操作: 一键创建包含N8N、数据库、Redis的完整环境
  配置: 自动端口映射和数据卷挂载
  清理: 环境使用完毕后自动清理

CI/CD集成:
  场景: 持续集成和部署流程
  操作: 自动构建镜像、运行测试、部署容器
  配置: 多环境配置管理
  回滚: 支持快速回滚到上一版本

微服务管理:
  场景: N8N相关微服务的容器编排
  操作: 服务发现、负载均衡、健康检查
  配置: 服务间通信和依赖管理
  扩展: 根据负载自动扩缩容
```

###### 4. Docker MCP 安全规范
```yaml
安全配置要求:
  网络隔离: 
    - 使用自定义Docker网络
    - 禁止容器访问宿主机网络
    - 实施最小权限原则
  
  资源限制:
    - 设置CPU和内存限制
    - 磁盘空间配额管理
    - 进程数量限制
  
  镜像安全:
    - 使用官方或可信镜像源
    - 定期扫描镜像漏洞
    - 最小化镜像体积和攻击面
  
  访问控制:
    - Docker daemon访问权限控制
    - 容器内用户权限管理
    - 敏感数据加密存储

运行时安全:
  - 禁用特权容器模式
  - 只读文件系统配置
  - 安全计算模式(seccomp)启用
  - AppArmor/SELinux策略应用
```

###### 5. Docker MCP 性能优化
```yaml
性能配置:
  镜像优化:
    - 多阶段构建减少镜像大小
    - 合理使用镜像层缓存
    - 选择轻量级基础镜像
  
  容器配置:
    - 合理设置资源限制
    - 优化容器启动时间
    - 使用健康检查机制
  
  存储优化:
    - 使用适当的存储驱动
    - 数据卷挂载策略
    - 临时文件系统配置
  
  网络优化:
    - 选择合适的网络驱动
    - 减少网络跳数
    - 启用网络压缩
```

###### 6. Docker MCP 故障处理
```yaml
故障诊断流程:
  1. 容器状态检查:
     - 检查容器运行状态
     - 查看容器日志
     - 分析资源使用情况
  
  2. 网络连通性测试:
     - 验证容器网络配置
     - 测试服务端口可达性
     - 检查DNS解析
  
  3. 存储问题排查:
     - 检查数据卷挂载
     - 验证文件权限
     - 分析磁盘空间使用
  
  4. 自动恢复机制:
     - 容器自动重启策略
     - 健康检查失败处理
     - 服务降级和熔断

故障处理优先级:
  - P0: 生产环境容器崩溃 (立即处理)
  - P1: 开发环境容器异常 (4小时内处理)
  - P2: 性能问题 (24小时内处理)
  - P3: 优化建议 (下个版本处理)
```

###### 7. Docker MCP 配置和维护指南
```yaml
配置管理:
  配置文件结构:
    - .mcp/docker/config.yml: 主配置文件
    - .mcp/docker/compose/: Docker Compose模板
    - .mcp/docker/scripts/: 自动化脚本
    - .mcp/docker/monitoring/: 监控配置

  环境变量管理:
    - DOCKER_MCP_HOST: Docker守护进程地址
    - DOCKER_MCP_TLS_VERIFY: TLS验证开关
    - DOCKER_MCP_CERT_PATH: 证书路径
    - DOCKER_MCP_REGISTRY: 镜像仓库地址
    - DOCKER_MCP_NETWORK: 默认网络名称

  配置验证:
    - 启动前自动验证配置完整性
    - 检查Docker守护进程连接状态
    - 验证镜像仓库访问权限
    - 确认网络和存储配置

维护策略:
  日常维护:
    - 定期清理未使用的镜像和容器
    - 监控磁盘空间使用情况
    - 检查容器健康状态
    - 更新安全补丁

  版本管理:
    - 镜像版本标签规范
    - 配置文件版本控制
    - 回滚策略和流程
    - 兼容性测试

  监控告警:
    - 容器资源使用监控
    - 服务可用性检查
    - 异常日志告警
    - 性能指标跟踪

  备份恢复:
    - 数据卷定期备份
    - 配置文件备份策略
    - 灾难恢复流程
    - 备份验证机制

升级维护:
  Docker引擎升级:
    - 升级前兼容性检查
    - 分阶段升级策略
    - 回滚准备和验证
    - 升级后功能测试

  MCP工具升级:
    - 新版本功能评估
    - 测试环境验证
    - 生产环境灰度升级
    - 性能对比分析

  安全维护:
    - 定期安全扫描
    - 漏洞修复跟踪
    - 访问权限审计
    - 安全策略更新
```

#### 4. N8N专用工具
```yaml
核心工具:
  - mcp_n8n__mcp_list_nodes: 查询可用节点
  - mcp_n8n__mcp_n8n_create_workflow: 创建工作流
  - mcp_n8n__mcp_get_template: 获取工作流模板
  - mcp_n8n__mcp_validate_workflow: 验证工作流
```

### MCP工具选择流程

#### 1. 需求分析阶段
- **任务类型识别**: 明确任务属于哪个工具分类
- **功能需求评估**: 列出具体功能要求和性能指标
- **技术约束分析**: 评估现有技术栈兼容性
- **安全要求确认**: 确定安全级别和合规要求

#### 2. 工具评估阶段
- **候选工具筛选**: 基于分类优先级筛选候选工具
- **功能匹配度评估**: 评估工具功能与需求匹配程度
- **技术适配性评估**: 验证与现有系统集成复杂度
- **性能基准测试**: 对比不同工具性能表现

#### 3. 配置验证阶段
- **配置状态检查**: 验证MCP工具是否已正确配置
- **连接测试**: 测试MCP工具与目标系统连接状态
- **权限验证**: 确认工具具备执行任务所需权限
- **功能验证**: 执行简单测试确保工具功能正常

### 故障处理流程

#### 1. 自动决策流程
```yaml
系统评估:
  - 自动评估任务需求
  - 判断是否需要启用sequentialthinking MCP
  - 根据任务复杂度选择最优MCP工具
```

#### 2. 故障处理优先级
```yaml
处理步骤:
  a) 执行完整问题诊断:
     - 全面扫描系统状态
     - 记录详细错误日志
     - 分析错误根源
  
  b) 解决方案优先级:
     - 优先调用context7 MCP
     - 通过浏览器/fetch查阅官方最新文档
     - 严格按官方说明进行配置修复
```

#### 3. 执行要求
- **彻底解决**: 必须彻底解决问题后方可继续任务
- **禁止规避**: 禁止跳过故障或改用其他MCP工具规避问题
- **操作文档**: 每个操作步骤需附带清晰的操作说明文档
- **可追溯性**: 确保所有修复操作可追溯、可验证

---

## 🔒 安全规范

### 数据安全

#### 1. 敏感信息处理
```yaml
分类标准:
  - 高敏感: API密钥、数据库密码、用户隐私数据
  - 中敏感: 配置信息、业务数据、日志信息
  - 低敏感: 公开文档、系统状态信息

处理要求:
  - 高敏感: 必须加密存储，使用环境变量
  - 中敏感: 访问控制，定期审计
  - 低敏感: 基础访问控制
```

#### 2. API安全
```javascript
// API密钥管理示例
const crypto = require('crypto');

class ApiKeyManager {
    /**
     * 生成API密钥
     * @returns {string} 生成的API密钥
     */
    generateApiKey() {
        return crypto.randomBytes(32).toString('hex');
    }
    
    /**
     * 验证API密钥
     * @param {string} providedKey - 提供的密钥
     * @param {string} storedKey - 存储的密钥
     * @returns {boolean} 验证结果
     */
    validateApiKey(providedKey, storedKey) {
        return crypto.timingSafeEqual(
            Buffer.from(providedKey),
            Buffer.from(storedKey)
        );
    }
}
```

### 网络安全

#### 1. HTTPS强制
```yaml
要求:
  - 所有API调用必须使用HTTPS
  - 禁用不安全的HTTP连接
  - 使用有效的SSL证书
  - 定期更新证书
```

#### 2. 防火墙配置
```bash
# 防火墙规则示例
# 允许HTTP和HTTPS流量
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# 允许N8N端口（仅内网）
sudo ufw allow from 192.168.1.0/24 to any port 5678

# 允许数据库端口（仅本地）
sudo ufw allow from 127.0.0.1 to any port 3306
sudo ufw allow from 127.0.0.1 to any port 5432

# 启用防火墙
sudo ufw enable
```

### 访问控制

#### 1. 基于角色的访问控制(RBAC)
```yaml
角色定义:
  admin:
    permissions:
      - workflow.create
      - workflow.read
      - workflow.update
      - workflow.delete
      - user.manage
      - system.config
  
  developer:
    permissions:
      - workflow.create
      - workflow.read
      - workflow.update
      - workflow.test
  
  viewer:
    permissions:
      - workflow.read
      - execution.read
```

---

## 📊 质量保证

### 测试规范

#### 1. 测试分类
```yaml
单元测试:
  覆盖率要求: ≥80%
  测试框架: Jest (Node.js), PHPUnit (PHP)
  执行频率: 每次代码提交

集成测试:
  覆盖率要求: ≥60%
  测试范围: API接口、数据库操作、外部服务集成
  执行频率: 每日构建

端到端测试:
  覆盖率要求: 核心业务流程100%
  测试工具: Playwright, Cypress
  执行频率: 发布前
```

#### 2. 测试用例示例
```javascript
// N8N工作流测试示例
describe('N8N工作流测试', () => {
    test('应该成功创建用户注册工作流', async () => {
        const workflow = {
            name: '用户注册自动化',
            nodes: [
                {
                    name: 'Webhook',
                    type: 'n8n-nodes-base.webhook',
                    parameters: {
                        httpMethod: 'POST',
                        path: 'user-register'
                    }
                },
                {
                    name: 'MySQL',
                    type: 'n8n-nodes-base.mysql',
                    parameters: {
                        operation: 'insert',
                        table: 'users'
                    }
                }
            ],
            connections: {
                'Webhook': {
                    'main': [
                        [{ 'node': 'MySQL', 'type': 'main', 'index': 0 }]
                    ]
                }
            }
        };
        
        const result = await n8nClient.createWorkflow(workflow);
        expect(result.success).toBe(true);
        expect(result.workflow.id).toBeDefined();
    });
});
```

### 代码审查

#### 1. 审查清单
```yaml
功能性检查:
  - [ ] 功能实现是否符合需求
  - [ ] 错误处理是否完善
  - [ ] 边界条件是否考虑
  - [ ] 性能是否满足要求

代码质量检查:
  - [ ] 代码结构是否清晰
  - [ ] 命名是否规范
  - [ ] 注释是否充分
  - [ ] 是否遵循编码规范

安全性检查:
  - [ ] 是否存在安全漏洞
  - [ ] 敏感信息是否正确处理
  - [ ] 输入验证是否充分
  - [ ] 权限控制是否正确
```

---

## 📈 性能规范

### 性能指标

#### 1. 响应时间要求
```yaml
API响应时间:
  - 简单查询: <200ms
  - 复杂查询: <1s
  - 批量操作: <5s
  - 文件上传: <30s

工作流执行时间:
  - 简单工作流: <5s
  - 复杂工作流: <30s
  - 批量处理: <5min
  - 长时间任务: 异步处理
```

#### 2. 并发处理能力
```yaml
并发要求:
  - API并发: 1000 req/s
  - 工作流并发: 100 workflows/min
  - 数据库连接: 最大200个连接
  - 内存使用: <2GB per process
```

### 性能优化

#### 1. 数据库优化
```sql
-- 索引优化示例
-- 用户表索引
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_status_created ON users(status, created_at);

-- 工作流执行表索引
CREATE INDEX idx_executions_workflow_status ON executions(workflow_id, status);
CREATE INDEX idx_executions_created_at ON executions(created_at DESC);

-- 复合索引
CREATE INDEX idx_users_email_status ON users(email, status);
```

#### 2. 缓存策略
```javascript
// Redis缓存示例
class CacheManager {
    constructor(redisClient) {
        this.redis = redisClient;
        this.defaultTTL = 3600; // 1小时
    }
    
    /**
     * 设置缓存
     * @param {string} key - 缓存键
     * @param {any} value - 缓存值
     * @param {number} ttl - 过期时间（秒）
     */
    async set(key, value, ttl = this.defaultTTL) {
        const serializedValue = JSON.stringify(value);
        await this.redis.setex(key, ttl, serializedValue);
    }
    
    /**
     * 获取缓存
     * @param {string} key - 缓存键
     * @returns {any} 缓存值
     */
    async get(key) {
        const value = await this.redis.get(key);
        return value ? JSON.parse(value) : null;
    }
}
```

---

## 📚 文档规范

### 文档分类

#### 1. 技术文档
```yaml
API文档:
  格式: OpenAPI 3.0
  内容: 接口定义、参数说明、示例代码
  更新: 代码变更时同步更新

架构文档:
  格式: Markdown + 图表
  内容: 系统架构、组件关系、数据流
  更新: 架构变更时更新

部署文档:
  格式: Markdown
  内容: 环境要求、安装步骤、配置说明
  更新: 部署流程变更时更新
```

#### 2. 用户文档
```yaml
用户手册:
  格式: Markdown
  内容: 功能介绍、操作指南、常见问题
  更新: 功能发布时更新

快速开始:
  格式: Markdown
  内容: 安装指南、基础配置、示例演示
  更新: 重大版本发布时更新
```

### 文档编写规范

#### 1. 格式规范
```markdown
# 一级标题
## 二级标题
### 三级标题

**粗体文本**
*斜体文本*
`代码片段`

```javascript
// 代码块
function example() {
    return 'Hello World';
}
```

| 列1 | 列2 | 列3 |
|-----|-----|-----|
| 值1 | 值2 | 值3 |

- 无序列表项1
- 无序列表项2

1. 有序列表项1
2. 有序列表项2
```

#### 2. 内容规范
```yaml
标题规范:
  - 使用清晰、描述性的标题
  - 遵循层级结构
  - 避免过深的嵌套

内容规范:
  - 语言简洁明了
  - 逻辑结构清晰
  - 包含必要的示例
  - 及时更新过时信息

代码示例:
  - 提供完整可运行的示例
  - 包含必要的注释
  - 遵循代码规范
  - 测试示例的正确性
```

---

## 🚀 部署规范

### 环境管理

#### 1. 环境分类
```yaml
开发环境 (Development):
  用途: 日常开发和调试
  数据: 测试数据
  配置: 开发配置
  访问: 开发团队

测试环境 (Testing):
  用途: 功能测试和集成测试
  数据: 模拟生产数据
  配置: 接近生产配置
  访问: 测试团队

预发布环境 (Staging):
  用途: 发布前最终验证
  数据: 生产数据副本
  配置: 生产配置
  访问: 核心团队

生产环境 (Production):
  用途: 正式服务
  数据: 真实业务数据
  配置: 生产配置
  访问: 运维团队
```

#### 2. 配置管理
```yaml
环境变量管理:
  开发环境: .env.development
  测试环境: .env.testing
  预发布环境: .env.staging
  生产环境: .env.production

配置优先级:
  1. 环境变量
  2. 配置文件
  3. 默认值

敏感信息:
  存储方式: 环境变量或密钥管理系统
  访问控制: 最小权限原则
  轮换策略: 定期更新
```

### 部署流程

#### 1. 自动化部署
```yaml
CI/CD流程:
  1. 代码提交触发构建
  2. 自动化测试执行
  3. 代码质量检查
  4. 安全扫描
  5. 构建Docker镜像
  6. 部署到测试环境
  7. 自动化测试验证
  8. 部署到预发布环境
  9. 手动验证
  10. 部署到生产环境
```

#### 2. 部署脚本示例
```bash
#!/bin/bash
# 部署脚本示例

set -e  # 遇到错误立即退出

# 配置变量
APP_NAME="n8n-automation"
ENVIRONMENT=${1:-staging}
VERSION=${2:-latest}

echo "开始部署 $APP_NAME 到 $ENVIRONMENT 环境，版本: $VERSION"

# 1. 拉取最新代码
git pull origin main

# 2. 构建Docker镜像
docker build -t $APP_NAME:$VERSION .

# 3. 停止旧容器
docker-compose -f docker-compose.$ENVIRONMENT.yml down

# 4. 启动新容器
docker-compose -f docker-compose.$ENVIRONMENT.yml up -d

# 5. 健康检查
echo "等待服务启动..."
sleep 30

# 检查服务状态
if curl -f http://localhost:5678/healthz; then
    echo "部署成功！"
else
    echo "部署失败，正在回滚..."
    docker-compose -f docker-compose.$ENVIRONMENT.yml down
    docker-compose -f docker-compose.$ENVIRONMENT.yml up -d
    exit 1
fi

echo "部署完成！"
```

---

## 🔄 版本管理

### Git工作流

#### 1. 分支策略
```yaml
主分支 (main):
  用途: 生产代码
  保护: 禁止直接推送
  合并: 通过Pull Request

开发分支 (develop):
  用途: 集成开发代码
  来源: feature分支合并
  目标: 发布到测试环境

功能分支 (feature/*):
  用途: 新功能开发
  命名: feature/功能名称
  生命周期: 功能完成后删除

修复分支 (hotfix/*):
  用途: 紧急修复
  来源: main分支
  目标: main和develop分支

发布分支 (release/*):
  用途: 发布准备
  来源: develop分支
  目标: main分支
```

#### 2. 提交规范
```yaml
提交信息格式:
  <类型>(<范围>): <描述>
  
  [可选的正文]
  
  [可选的脚注]

类型说明:
  feat: 新功能
  fix: 修复bug
  docs: 文档更新
  style: 代码格式调整
  refactor: 代码重构
  test: 测试相关
  chore: 构建过程或辅助工具的变动

示例:
  feat(auth): 添加用户登录功能
  fix(api): 修复用户注册接口返回错误
  docs(readme): 更新安装说明
```

---

## 📞 协作规范

### AI智能体团队协作

#### 1. AI智能体角色协作
```yaml
执行官Agent (Workflow Executive):
  协作对象: 用户、教学老师Agent、系统监控
  协作方式: 
    - 接收用户需求并自动执行
    - 向教学老师Agent请求专业知识支持
    - 向系统反馈执行状态和结果
  响应时间: <30秒自动响应
  协作标准: 零延迟切换，实时状态同步

教学老师Agent (Teaching):
  协作对象: 用户、执行官Agent、知识库
  协作方式:
    - 为用户提供个性化教学服务
    - 为执行官Agent提供专业知识支持
    - 从知识库获取最新技术信息
  响应时间: <10秒交互响应
  协作标准: 上下文完整传递，学习路径连续

智能调度中心:
  职责: 
    - 分析用户需求类型
    - 智能分配合适的Agent
    - 协调多Agent协作
    - 监控Agent性能状态
  决策算法: 基于关键词、上下文、用户历史
  切换标准: 无缝切换，用户无感知
```

#### 2. 人机协作模式
```yaml
用户交互层:
  - 统一交互界面
  - 自然语言理解
  - 多模态输入支持
  - 实时反馈机制

Agent协作层:
  - 角色自动识别
  - 任务智能分解
  - 并行处理能力
  - 结果整合输出

系统集成层:
  - N8N平台集成
  - MCP工具调用
  - 数据库操作
  - 外部API集成
```

### 传统团队协作

#### 1. 角色职责
```yaml
产品负责人 (PO):
  - 需求管理和优先级排序
  - 用户故事编写
  - 验收标准定义
  - 业务价值评估
  - AI智能体需求定义

技术负责人 (TL):
  - 技术方案设计
  - 代码审查
  - 技术难点攻关
  - 团队技术指导
  - AI智能体架构设计

AI智能体工程师 (AI Engineer):
  - AI智能体开发和训练
  - 决策算法优化
  - 自然语言处理
  - 机器学习模型调优
  - 智能体性能监控

开发工程师 (Dev):
  - 功能开发实现
  - 单元测试编写
  - 代码质量保证
  - 技术文档编写
  - AI智能体集成开发

测试工程师 (QA):
  - 测试用例设计
  - 功能测试执行
  - 缺陷跟踪管理
  - 质量报告输出
  - AI智能体测试验证

运维工程师 (Ops):
  - 环境搭建维护
  - 部署流程管理
  - 监控告警配置
  - 故障处理响应
  - AI智能体运行监控
```

#### 2. 沟通机制
```yaml
日常沟通:
  - 每日站会: 15分钟，同步进展和问题
  - 周会: 1小时，回顾和计划
  - 月会: 2小时，总结和改进

项目沟通:
  - 需求评审: 产品、开发、测试参与
  - 技术评审: 技术团队内部讨论
  - 发布评审: 全团队参与决策

问题沟通:
  - 紧急问题: 立即沟通，电话或即时消息
  - 一般问题: 24小时内响应
  - 技术讨论: 预约会议深入讨论
```

---

## 🚀 MCP服务器部署策略

### Docker容器化部署优先原则

#### 1. 部署架构决策
```yaml
优先级排序:
  1. Docker容器化部署 (首选方案)
     - 环境一致性保证
     - 快速部署和扩展
     - 资源隔离和安全性
     - 版本管理和回滚便利
  
  2. 传统进程部署 (备选方案)
     - 仅在Docker不可用时使用
     - 需要额外的环境配置管理
     - 手动依赖管理和版本控制

技术优势:
  - 环境标准化: 开发、测试、生产环境完全一致
  - 快速部署: 一键部署，秒级启动
  - 资源优化: 精确的资源分配和限制
  - 安全隔离: 容器级别的安全隔离
  - 易于维护: 统一的管理和监控
```

#### 2. MCP服务器容器化配置
```yaml
基础配置:
  基础镜像: node:18-alpine
  工作目录: /app
  端口映射: 3000:3000
  环境变量: 通过.env文件管理
  数据持久化: 使用Docker volumes

Dockerfile示例:
  FROM node:18-alpine
  WORKDIR /app
  COPY package*.json ./
  RUN npm ci --only=production
  COPY . .
  EXPOSE 3000
  CMD ["npm", "start"]

docker-compose配置:
  version: '3.8'
  services:
    mcp-server:
      build: .
      ports:
        - "3000:3000"
      environment:
        - NODE_ENV=production
      volumes:
        - mcp-data:/app/data
      restart: unless-stopped
```

#### 3. 部署流程标准化
```yaml
开发环境部署:
  1. 本地Docker环境验证
  2. 容器构建和测试
  3. 功能验证和调试
  4. 性能基准测试

测试环境部署:
  1. 自动化构建流程
  2. 集成测试执行
  3. 安全扫描验证
  4. 性能压力测试

生产环境部署:
  1. 蓝绿部署策略
  2. 健康检查验证
  3. 监控告警配置
  4. 备份和恢复验证
```

#### 4. 容器编排和管理
```yaml
单机部署:
  工具: Docker Compose
  适用场景: 开发、测试、小规模生产
  管理方式: 手动或脚本自动化

集群部署:
  工具: Kubernetes / Docker Swarm
  适用场景: 大规模生产环境
  管理方式: 声明式配置管理
  
监控和日志:
  容器监控: cAdvisor + Prometheus
  日志收集: Fluentd + Elasticsearch
  告警通知: Alertmanager
```

---

## 📋 附录

### 检查清单

#### 1. 开发检查清单
```yaml
代码提交前:
  - [ ] 代码符合编码规范
  - [ ] 单元测试通过
  - [ ] 代码审查完成
  - [ ] 文档更新完成
  - [ ] 安全检查通过

功能开发完成:
  - [ ] 需求实现完整
  - [ ] 边界条件处理
  - [ ] 错误处理完善
  - [ ] 性能满足要求
  - [ ] 用户体验良好

发布准备:
  - [ ] 集成测试通过
  - [ ] 性能测试通过
  - [ ] 安全测试通过
  - [ ] 文档更新完成
  - [ ] 发布说明准备
```

#### 2. 部署检查清单
```yaml
部署前检查:
  - [ ] 环境配置正确
  - [ ] 数据库迁移完成
  - [ ] 依赖服务正常
  - [ ] 备份策略就绪
  - [ ] 回滚方案准备

部署后验证:
  - [ ] 服务启动正常
  - [ ] 健康检查通过
  - [ ] 核心功能验证
  - [ ] 监控告警配置
  - [ ] 日志输出正常
```

### 常用命令

#### 1. Git命令
```bash
# 创建功能分支
git checkout -b feature/new-feature

# 提交代码
git add .
git commit -m "feat(api): 添加用户管理接口"

# 推送分支
git push origin feature/new-feature

# 合并分支
git checkout develop
git merge feature/new-feature

# 删除分支
git branch -d feature/new-feature
```

#### 2. Docker命令
```bash
# 构建镜像
docker build -t n8n-automation:latest .

# 运行容器
docker run -d --name n8n-app -p 5678:5678 n8n-automation:latest

# 查看日志
docker logs -f n8n-app

# 进入容器
docker exec -it n8n-app /bin/bash

# 停止容器
docker stop n8n-app

# 删除容器
docker rm n8n-app
```

#### 3. N8N命令
```bash
# 启动N8N
n8n start

# 导出工作流
n8n export:workflow --all --output=workflows.json

# 导入工作流
n8n import:workflow --input=workflows.json

# 执行工作流
n8n execute --id=workflow-id
```

### 参考资源

#### 1. 官方文档
- [N8N官方文档](https://docs.n8n.io/)
- [Docker官方文档](https://docs.docker.com/)
- [Git官方文档](https://git-scm.com/doc)

#### 2. 最佳实践
- [代码审查最佳实践](https://github.com/features/code-review/)
- [API设计最佳实践](https://restfulapi.net/)
- [安全开发最佳实践](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)

#### 3. 工具推荐
- [VSCode](https://code.visualstudio.com/): 代码编辑器
- [Postman](https://www.postman.com/): API测试工具
- [Docker Desktop](https://www.docker.com/products/docker-desktop): 容器管理
- [Git](https://git-scm.com/): 版本控制

---

**文档维护**: 本文档由项目团队共同维护，如有问题或建议，请通过GitHub Issues反馈。

**最后更新**: 2025年1月16日  
**下次审查**: 2025年2月16日  
**文档路径**: `.trae/rules/project_rules.md`