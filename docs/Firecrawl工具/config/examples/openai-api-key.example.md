# OpenAI API 凭证配置示例

> **注意**：请勿在代码仓库内存储真实 API Key。以下内容仅为使用示例。

## 获取 API Key

1. 登录 [OpenAI 控制台](https://platform.openai.com/)。
2. 在 **API Keys** 页面创建新的密钥，并立即复制备份。
3. 为不同环境（开发、测试、生产）生成独立密钥，方便追踪与撤销。

## 环境变量示例

```bash
export OPENAI_API_KEY="sk-xxxxx替换为真实密钥"
export OPENAI_API_BASE="https://api.openai.com/v1"
```

建议将上述变量写入 `.env` 或系统密钥服务，并保证 `.env` 已列入 `.gitignore`。

## Python 读取示例

```python
import os

api_key = os.environ["OPENAI_API_KEY"]
```

## 密钥管理

- 定期轮换密钥，并删除不再使用的密钥。
- 配置访问控制与审计日志，监控异常使用。
- 遇到泄露风险，立即在控制台撤销对应密钥。

