# Firecrawl 任务状态检查工具

## 功能说明

`check_job_status.py` 是一个用于检查 Firecrawl 任务状态的命令行工具，支持检查爬取（crawl）和提取（extract）任务的状态。

## 使用方法

### 基本用法

```bash
# 激活虚拟环境
source .venv/bin/activate

# 检查任务状态
python3 Firecrawl代码模块/check_job_status.py <job_id>

# 示例
python3 Firecrawl代码模块/check_job_status.py fc-31ebbe4647b84fdc975318d372eebea8
```

### 任务 ID 格式

- **爬取任务 ID**: `fc-xxxxxxxxxxxxx`（通常以 `fc-` 开头）
- **提取任务 ID**: 类似格式

## API 密钥配置

脚本会按以下顺序查找 API 密钥：

1. **环境变量** `FIRECRAWL_API_KEY`
2. **`.env` 文件**（如果安装了 `python-dotenv`）
3. **`settings.json`** 文件中的 `firecrawl.api_key`

### 设置环境变量

```bash
# macOS/Linux
export FIRECRAWL_API_KEY="fc-your-api-key-here"

# 或在 .env 文件中
echo "FIRECRAWL_API_KEY=fc-your-api-key-here" >> .env
```

## 输出说明

### 成功查询

脚本会显示以下信息：

- ✅ **状态**: 任务当前状态（scraping/completed/failed/pending）
- 📄 **总页数**: 需要处理的页面总数
- ✅ **已完成**: 已完成的页面数
- 💰 **已使用积分**: 任务消耗的积分
- ⏰ **过期时间**: 任务结果过期时间
- 📦 **数据项数量**: 返回的数据项数量
- 📝 **数据预览**: 前 3 项数据的预览

### 任务完成后的操作

如果任务已完成且有数据，脚本会询问是否保存结果到 JSON 文件：

```
💾 任务已完成，是否保存结果到文件？(y/n):
```

输入 `y` 会将结果保存到 `firecrawl_result_<job_id>.json` 文件。

## 常见问题

### 1. 任务未找到（404 错误）

**错误信息**:
```
❌ 无法获取任务状态: Status code 404. Extract job not found
```

**可能原因**:
- ✅ 任务已过期（超过 24 小时）
- ✅ 任务 ID 不正确
- ✅ 任务不属于当前 API 密钥的账户

**解决方案**:
- 确认任务 ID 是否正确
- 确认任务是否在 24 小时内完成
- 确认 API 密钥是否正确

### 2. API 密钥未找到

**错误信息**:
```
❌ 未找到 Firecrawl API 密钥
```

**解决方案**:
1. 设置环境变量：
   ```bash
   export FIRECRAWL_API_KEY="fc-your-api-key-here"
   ```

2. 或在 `settings.json` 中配置：
   ```json
   {
     "firecrawl": {
       "api_key": "fc-your-api-key-here"
     }
   }
   ```

### 3. SDK 方法不可用

**错误信息**:
```
⚠️  SDK 版本可能不支持 get_crawl_status
```

**解决方案**:
- 更新 Firecrawl SDK：
  ```bash
  pip install --upgrade firecrawl-py
  ```

## 任务状态说明

### 爬取任务状态

- **scraping**: 正在爬取中
- **completed**: 已完成
- **failed**: 失败
- **pending**: 等待中

### 提取任务状态

- **running**: 正在运行
- **completed**: 已完成
- **failed**: 失败

## 注意事项

1. **任务过期时间**: Firecrawl 任务状态只能在任务完成后 24 小时内查询，过期后无法查询。

2. **分页数据**: 如果任务返回的数据超过 10MB，响应中会包含 `next` 参数，需要继续请求该 URL 获取剩余数据。

3. **API 限制**: 请遵守 Firecrawl API 的速率限制和使用条款。

## 示例输出

### 成功查询示例

```
🔍 正在检查任务状态: fc-31ebbe4647b84fdc975318d372eebea8

📋 任务 ID 格式: ✅ 正确（fc- 开头）

1️⃣  尝试检查爬取任务状态...

============================================================
📊 Firecrawl 任务状态
============================================================
✅ 状态: completed
📄 总页数: 36
✅ 已完成: 36
💰 已使用积分: 36
⏰ 过期时间: 2024-00-00T00:00:00.000Z

📦 数据项数量: 36

📝 数据预览（前3项）:
  1. https://docs.firecrawl.dev/learn/rag-llama3
  2. https://docs.firecrawl.dev/guide
  3. https://docs.firecrawl.dev/api-reference
============================================================

💾 任务已完成，是否保存结果到文件？(y/n):
```

### 任务未找到示例

```
🔍 正在检查任务状态: fc-31ebbe4647b84fdc975318d372eebea8

📋 任务 ID 格式: ✅ 正确（fc- 开头）

1️⃣  尝试检查爬取任务状态...

2️⃣  爬取任务检查失败，尝试检查提取任务...

❌ 无法获取任务状态: Status code 404. Extract job not found

💡 其他可能的原因:
  - 确认任务 ID 是否正确（格式: fc-xxxxxxxxxxxxx）
  - 确认 API 密钥是否有效
  - 确认任务是否在 24 小时内完成（过期任务无法查询）
  - 确认任务是否属于当前 API 密钥的账户
```

## 相关文档

- [Firecrawl 官方文档](https://docs.firecrawl.dev/)
- [Firecrawl API 参考](https://docs.firecrawl.dev/api-reference)
- [项目文档](../docs/Firecrawl工具/)

