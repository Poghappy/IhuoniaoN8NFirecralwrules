# 阿里云凭证示例

> **安全提示**：请勿将真实 `accessKeyId`、`accessKeySecret` 写入仓库或日志。以下示例仅用于说明配置步骤。

## 配置步骤

1. 在阿里云控制台创建具有最小权限的 RAM 用户，并生成一对访问密钥。
2. 将密钥写入本地 `.env` 或安全的凭证管理服务，例如：

```bash
export ALIYUN_ACCESS_KEY_ID="替换为真实KeyId"
export ALIYUN_ACCESS_KEY_SECRET="替换为真实KeySecret"
```

3. 若需脚本读取，可通过 `os.environ`（Python）或 `process.env`（Node.js）获取。
4. 将 `.env`、`*.local` 等文件加入 `.gitignore`，防止凭证泄露。

## 密钥轮换

- 建议每 90 天轮换一次访问密钥，并及时更新自动化任务。
- 若密钥泄露，请立即在阿里云控制台停用旧密钥并生成新密钥。

## 审计建议

- 启用操作日志与访问控制台审计。
- 为不同应用创建独立的 RAM 用户，避免共享密钥。

