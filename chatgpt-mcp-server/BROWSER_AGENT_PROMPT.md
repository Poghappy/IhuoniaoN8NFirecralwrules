# 🤖 浏览器 Agent 配置提示词

## 目标

配置 ChatGPT 桌面版连接到本地 MCP Gateway，使 ChatGPT 能够调用外部工具（Firecrawl、GitHub、文件系统等）。

---

## 📋 前置条件检查

在执行配置前，请确认：

1. **Docker MCP Gateway 已启动**
   - 检查：访问 `http://localhost:3000/sse` 应该返回响应（可能需要认证）
   - 如果未启动，运行：`cd /Users/zhiledeng/Movies/Hawaiihub.net/chatgpt-mcp-server && ./start-gateway.sh`

2. **ngrok 隧道已启动**
   - 检查：应该有 ngrok 进程运行，监听端口 3000
   - 如果未启动，运行：`ngrok http 3000`
   - 获取 HTTPS URL：从 ngrok 输出中复制 `Forwarding` 行的 HTTPS URL
   - 格式示例：`https://abc123-xx-xx-xx-xx.ngrok-free.app`

3. **ChatGPT 桌面版已打开**
   - 确保 ChatGPT 桌面应用程序正在运行

---

## 🎯 配置步骤（浏览器 Agent 执行指南）

### 步骤 1: 打开设置页面

**操作**:
1. 在 ChatGPT 桌面版界面中，找到并点击左下角的**设置图标**（⚙️ 齿轮图标）
2. 如果看不到设置图标，尝试：
   - 点击左下角的用户头像或菜单按钮
   - 查找 "Settings" 或 "设置" 选项

**验证**: 应该看到设置菜单或设置页面打开

---

### 步骤 2: 导航到 Apps & Connectors

**操作**:
1. 在设置菜单中，查找并点击 **"Apps & Connectors"** 或 **"应用与连接器"**
2. 如果找不到，尝试查找：
   - "Connectors"（连接器）
   - "Integrations"（集成）
   - "Extensions"（扩展）

**验证**: 应该看到 Apps & Connectors 页面

---

### 步骤 3: 启用开发者模式

**操作**:
1. 在 Apps & Connectors 页面中，**滚动到页面底部**
2. 查找 **"Advanced settings"** 或 **"高级设置"** 部分
3. 找到 **"Developer mode"** 或 **"开发者模式"** 开关
4. **点击开关**，将其启用（开关应该变为开启状态，通常是蓝色或绿色）

**验证**: Developer mode 开关应该显示为已启用状态

**如果找不到**:
- 检查是否已登录 ChatGPT Plus 账户
- 确认账户是否有权限启用开发者模式
- 尝试刷新页面或重启 ChatGPT

---

### 步骤 4: 创建新连接器

**操作**:
1. 在 Apps & Connectors 页面中，查找 **"Create"** 或 **"创建"** 按钮
2. 点击该按钮
3. 应该会打开一个创建连接器的对话框或表单

**验证**: 应该看到连接器创建表单，包含以下字段：
- Connector name（连接器名称）
- Description（描述）
- Connector URL（连接器 URL）

---

### 步骤 5: 填写连接器信息

**操作**:

1. **Connector name（连接器名称）**:
   - 输入：`HawaiiHub MCP Gateway`
   - 或：`本地 MCP 工具网关`

2. **Description（描述）**:
   - 输入：`本地 MCP 工具网关，提供 Firecrawl 网页抓取、GitHub 操作、文件系统访问等工具`
   - 或：`Local MCP Gateway providing Firecrawl web scraping, GitHub operations, filesystem access, and more tools`

3. **Connector URL（连接器 URL）**:
   - **重要**: 需要从 ngrok 获取 HTTPS URL
   - 格式：`https://your-ngrok-url.ngrok-free.app/sse`
   - ⚠️ **必须**: URL 必须以 `/sse` 结尾，不是 `/mcp`
   - 示例：`https://abc123-xx-xx-xx-xx.ngrok-free.app/sse`

   **如何获取 ngrok URL**:
   - 检查运行 ngrok 的终端窗口
   - 查找 `Forwarding` 行
   - 复制 HTTPS URL（例如：`https://abc123-xx-xx-xx-xx.ngrok-free.app`）
   - 在 URL 后面添加 `/sse`

**验证**: 所有字段都已填写，URL 格式正确（以 `/sse` 结尾）

---

### 步骤 6: 提交并创建连接器

**操作**:
1. 检查所有字段是否正确填写
2. 点击 **"Create"** 或 **"创建"** 按钮
3. 等待连接验证

**验证**:
- 如果成功：应该看到工具列表（显示 34 个工具：github: 26, firecrawl: 6, time: 2）
- 如果失败：会显示错误消息

---

### 步骤 7: 验证连接（如果成功）

**操作**:
1. 查看连接器列表，确认新创建的连接器已出现
2. 检查连接器状态（应该显示为已连接或活跃）
3. 查看工具列表，确认显示了可用的工具

**预期结果**:
- 连接器名称：HawaiiHub MCP Gateway
- 状态：已连接 / Active
- 工具数量：34 个工具

---

## 🔍 故障排查指南

### 问题 1: 找不到设置按钮

**可能原因**:
- ChatGPT 版本过旧
- 界面布局不同

**解决方案**:
- 尝试使用快捷键：`Cmd + ,` (macOS) 或 `Ctrl + ,` (Windows)
- 查找菜单栏中的 "Settings" 选项
- 检查 ChatGPT 是否需要更新

---

### 问题 2: 找不到 "Apps & Connectors"

**可能原因**:
- 功能名称可能不同
- 需要特定版本的 ChatGPT

**解决方案**:
- 查找类似的选项：Connectors、Integrations、Extensions
- 确认 ChatGPT 桌面版版本是否支持此功能
- 检查是否已登录 ChatGPT Plus 账户

---

### 问题 3: 找不到 "Developer mode" 开关

**可能原因**:
- 需要滚动到页面底部
- 账户权限不足
- 功能位置不同

**解决方案**:
- 仔细滚动到页面最底部
- 查找 "Advanced" 或 "高级" 部分
- 确认账户类型（需要 Plus 订阅）
- 尝试刷新页面

---

### 问题 4: 连接失败

**可能原因**:
- Gateway 未运行
- ngrok 未运行
- URL 格式错误
- 网络问题

**检查清单**:
- [ ] Gateway 是否正在运行（检查终端 1）
- [ ] ngrok 是否正在运行（检查终端 2）
- [ ] URL 是否正确（必须以 `/sse` 结尾）
- [ ] 是否可以访问 ngrok URL（在浏览器中测试）

**解决方案**:
1. 检查 Gateway 日志（终端 1）
2. 检查 ngrok 状态（终端 2）
3. 验证 URL 格式：`https://xxx.ngrok-free.app/sse`
4. 重新创建连接器

---

### 问题 5: URL 格式错误

**常见错误**:
- ❌ `https://xxx.ngrok-free.app/mcp`（错误：使用了 `/mcp`）
- ✅ `https://xxx.ngrok-free.app/sse`（正确：使用 `/sse`）

**解决方案**:
- 确保 URL 以 `/sse` 结尾
- 不要使用 `/mcp` 端点

---

## 📝 浏览器 Agent 执行检查清单

在执行配置时，请按以下顺序检查：

- [ ] 步骤 1: 已打开设置页面
- [ ] 步骤 2: 已导航到 Apps & Connectors
- [ ] 步骤 3: 已找到并启用 Developer mode
- [ ] 步骤 4: 已点击 Create 按钮
- [ ] 步骤 5: 已填写所有字段
  - [ ] Connector name: `HawaiiHub MCP Gateway`
  - [ ] Description: 已填写描述
  - [ ] Connector URL: `https://xxx.ngrok-free.app/sse`（以 `/sse` 结尾）
- [ ] 步骤 6: 已点击 Create 按钮
- [ ] 步骤 7: 已验证连接成功（显示工具列表）

---

## 🎯 关键信息摘要

### 必须填写的信息

1. **Connector name**: `HawaiiHub MCP Gateway`
2. **Connector URL**: `https://your-ngrok-url.ngrok-free.app/sse`
   - ⚠️ **重要**: 必须以 `/sse` 结尾

### 获取 ngrok URL 的方法

1. 查看运行 `ngrok http 3000` 的终端
2. 找到 `Forwarding` 行
3. 复制 HTTPS URL
4. 添加 `/sse` 后缀

### 验证成功的标志

- 连接器创建成功
- 显示工具列表（34 个工具）
- 连接器状态为"已连接"

---

## 🔗 相关资源

- Gateway 启动脚本: `chatgpt-mcp-server/start-gateway.sh`
- 完整配置指南: `CHATGPT_MCP_SETUP.md`
- 快速启动指南: `chatgpt-mcp-server/QUICK_START.md`

---

**提示**: 如果遇到任何问题，请参考故障排查部分，或查看详细文档。

