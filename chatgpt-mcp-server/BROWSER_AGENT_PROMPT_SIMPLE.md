# 🤖 浏览器 Agent 配置提示词（简化版）

## 任务目标

在 ChatGPT 桌面版中配置 MCP 连接器，连接到本地 Docker MCP Gateway。

---

## 📋 前置检查

在执行前确认：
1. ✅ Docker MCP Gateway 运行在 `http://localhost:3000/sse`
2. ✅ ngrok 隧道已启动，获取 HTTPS URL（例如：`https://abc123.ngrok-free.app`）
3. ✅ ChatGPT 桌面版已打开

---

## 🎯 执行步骤

### 1. 打开设置
- 点击左下角 ⚙️ 设置图标
- 或使用快捷键：`Cmd + ,` (macOS) / `Ctrl + ,` (Windows)

### 2. 进入 Apps & Connectors
- 在设置菜单中点击 **"Apps & Connectors"** 或 **"应用与连接器"**
- 如果找不到，查找：Connectors、Integrations、Extensions

### 3. 启用开发者模式
- 滚动到页面底部
- 找到 **"Advanced settings"** 或 **"高级设置"**
- 启用 **"Developer mode"** 开关

### 4. 创建连接器
- 点击 **"Create"** 或 **"创建"** 按钮

### 5. 填写表单
- **Connector name**: `HawaiiHub MCP Gateway`
- **Description**: `本地 MCP 工具网关，提供 Firecrawl、GitHub、文件系统等工具`
- **Connector URL**: `https://your-ngrok-url.ngrok-free.app/sse`
  - ⚠️ **重要**: 使用 ngrok 的 HTTPS URL + `/sse`
  - ⚠️ **必须**: URL 必须以 `/sse` 结尾（不是 `/mcp`）

### 6. 提交
- 点击 **"Create"** 按钮
- 等待连接验证

### 7. 验证
- ✅ 成功：显示工具列表（34 个工具）
- ❌ 失败：检查 Gateway 和 ngrok 是否运行

---

## 🔍 关键检查点

### URL 格式
- ✅ 正确：`https://abc123.ngrok-free.app/sse`
- ❌ 错误：`https://abc123.ngrok-free.app/mcp`

### 获取 ngrok URL
1. 查看运行 `ngrok http 3000` 的终端
2. 找到 `Forwarding` 行
3. 复制 HTTPS URL
4. 添加 `/sse` 后缀

---

## ⚠️ 常见问题

**找不到 Developer mode**:
- 滚动到页面最底部
- 确认已登录 Plus 账户
- 查找 "Advanced" 部分

**连接失败**:
- 检查 Gateway 是否运行
- 检查 ngrok 是否运行
- 验证 URL 格式（必须以 `/sse` 结尾）

---

## ✅ 成功标志

- 连接器创建成功
- 显示 34 个工具（github: 26, firecrawl: 6, time: 2）
- 连接器状态为"已连接"

---

**执行完成后，可以在 ChatGPT 对话中使用这些工具了！**

