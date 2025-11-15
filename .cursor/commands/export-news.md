# 导出新闻数据

将采集的新闻数据导出为不同格式，便于分析和使用。

## 支持的导出格式

### 1. CSV 格式

适合 Excel 分析和数据处理

```csv
id,title,content,url,source,published_at,created_at
1,"新闻标题","新闻内容","https://...","新浪科技","2025-11-02 10:00:00","2025-11-02 10:05:00"
```

### 2. JSON 格式

适合程序处理和 API 对接

```json
[
  {
    "id": 1,
    "title": "新闻标题",
    "content": "新闻内容",
    "url": "https://...",
    "source": "新浪科技",
    "published_at": "2025-11-02T10:00:00",
    "created_at": "2025-11-02T10:05:00"
  }
]
```

### 3. Excel 格式

适合报表和数据展示

- 支持多个工作表
- 支持格式化和样式
- 支持图表

### 4. Markdown 格式

适合文档和报告

```markdown
# 新闻导出报告

## 新闻列表

### 1. 新闻标题

- **来源**: 新浪科技
- **发布时间**: 2025-11-02 10:00:00
- **链接**: https://...

**内容**:
新闻内容...
```

### 5. HTML 格式

适合网页展示

```html
<!DOCTYPE html>
<html>
<head>
    <title>新闻导出</title>
</head>
<body>
    <h1>新闻列表</h1>
    <article>
        <h2>新闻标题</h2>
        <p>新闻内容...</p>
    </article>
</body>
</html>
```

## 执行步骤

### 1. 选择数据范围

```python
# 按时间范围
news_data = get_news_by_date_range(
    start_date='2025-10-26',
    end_date='2025-11-02'
)

# 按数量
news_data = get_latest_news(limit=100)

# 按条件
news_data = get_news_by_filter(
    source='新浪科技',
    category='科技'
)
```

### 2. 数据预处理

```python
def preprocess_for_export(news_data):
    """数据预处理"""
    processed = []
    for news in news_data:
        processed.append({
            'id': news['id'],
            'title': clean_text(news['title']),
            'content': clean_text(news['content']),
            'url': news['url'],
            'source': news['source'],
            'published_at': format_datetime(news['published_at']),
            'created_at': format_datetime(news['created_at'])
        })
    return processed
```

### 3. 导出数据

```python
from src.exporter import export_to_csv, export_to_json

# 导出为 CSV
export_to_csv(news_data, 'news_export.csv')

# 导出为 JSON
export_to_json(news_data, 'news_export.json')
```

## 导出实现

### CSV 导出

```python
import csv
from typing import List, Dict

def export_to_csv(data: List[Dict], filename: str):
    """导出为 CSV 格式"""
    if not data:
        print("没有数据可导出")
        return

    # 获取所有字段
    fieldnames = data[0].keys()

    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"已导出 {len(data)} 条数据到 {filename}")
```

### JSON 导出

```python
import json

def export_to_json(data: List[Dict], filename: str, indent: int = 2):
    """导出为 JSON 格式"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)

    print(f"已导出 {len(data)} 条数据到 {filename}")
```

### Excel 导出

```python
import pandas as pd

def export_to_excel(data: List[Dict], filename: str):
    """导出为 Excel 格式"""
    df = pd.DataFrame(data)

    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # 主数据表
        df.to_excel(writer, sheet_name='新闻数据', index=False)

        # 统计表
        stats = {
            '总数': len(df),
            '来源数': df['source'].nunique(),
            '最早日期': df['published_at'].min(),
            '最晚日期': df['published_at'].max()
        }
        pd.DataFrame([stats]).to_excel(writer, sheet_name='统计信息', index=False)

    print(f"已导出 {len(data)} 条数据到 {filename}")
```

### Markdown 导出

```python
def export_to_markdown(data: List[Dict], filename: str):
    """导出为 Markdown 格式"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("# 新闻导出报告\n\n")
        f.write(f"**导出时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**新闻数量**: {len(data)}\n\n")
        f.write("## 新闻列表\n\n")

        for i, news in enumerate(data, 1):
            f.write(f"### {i}. {news['title']}\n\n")
            f.write(f"- **来源**: {news['source']}\n")
            f.write(f"- **发布时间**: {news['published_at']}\n")
            f.write(f"- **链接**: {news['url']}\n\n")
            f.write(f"**内容**:\n\n{news['content'][:200]}...\n\n")
            f.write("---\n\n")

    print(f"已导出 {len(data)} 条数据到 {filename}")
```

### HTML 导出

```python
def export_to_html(data: List[Dict], filename: str):
    """导出为 HTML 格式"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>新闻导出</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            article { border: 1px solid #ddd; padding: 15px; margin-bottom: 20px; }
            h2 { color: #333; }
            .meta { color: #666; font-size: 0.9em; }
        </style>
    </head>
    <body>
        <h1>新闻列表</h1>
    """

    for news in data:
        html += f"""
        <article>
            <h2>{news['title']}</h2>
            <div class="meta">
                来源: {news['source']} |
                发布时间: {news['published_at']} |
                <a href="{news['url']}" target="_blank">查看原文</a>
            </div>
            <p>{news['content'][:300]}...</p>
        </article>
        """

    html += """
    </body>
    </html>
    """

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"已导出 {len(data)} 条数据到 {filename}")
```

## 高级功能

### 分批导出

```python
def export_in_batches(data: List[Dict], batch_size: int = 1000, format: str = 'csv'):
    """分批导出大量数据"""
    total = len(data)
    batches = (total + batch_size - 1) // batch_size

    for i in range(batches):
        start = i * batch_size
        end = min((i + 1) * batch_size, total)
        batch_data = data[start:end]

        filename = f"news_export_batch_{i+1}.{format}"
        if format == 'csv':
            export_to_csv(batch_data, filename)
        elif format == 'json':
            export_to_json(batch_data, filename)

        print(f"已导出批次 {i+1}/{batches}")
```

### 压缩导出

```python
import zipfile

def export_and_compress(data: List[Dict], base_filename: str):
    """导出并压缩"""
    # 导出为多种格式
    export_to_csv(data, f"{base_filename}.csv")
    export_to_json(data, f"{base_filename}.json")
    export_to_markdown(data, f"{base_filename}.md")

    # 压缩为 zip
    with zipfile.ZipFile(f"{base_filename}.zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(f"{base_filename}.csv")
        zipf.write(f"{base_filename}.json")
        zipf.write(f"{base_filename}.md")

    print(f"已导出并压缩到 {base_filename}.zip")
```

### 自定义字段

```python
def export_custom_fields(data: List[Dict], fields: List[str], filename: str):
    """导出自定义字段"""
    custom_data = []
    for news in data:
        custom_data.append({
            field: news.get(field, '') for field in fields
        })

    export_to_csv(custom_data, filename)
```

## 输出格式

### 📊 导出结果

```markdown
## 导出结果

- 导出格式：CSV
- 文件名：news_export.csv
- 数据条数：100
- 文件大小：2.5 MB
- 导出时间：2025-11-02 15:30:00
```

### 📁 文件列表

```markdown
## 导出文件

1. news_export.csv - CSV 格式数据
2. news_export.json - JSON 格式数据
3. news_export.xlsx - Excel 格式数据
4. news_export.md - Markdown 格式报告
5. news_export.html - HTML 格式网页
```

### ✅ 验证结果

```markdown
## 数据验证

- 数据完整性：✅ 通过
- 字段完整性：✅ 通过
- 编码正确性：✅ UTF-8
- 文件可读性：✅ 通过
```

## 使用示例

### 示例 1：导出最近 100 条新闻

```
/export-news
导出最近 100 条新闻为 CSV 格式
```

### 示例 2：导出指定时间范围

```
/export-news
导出 2025-10-26 至 2025-11-02 的新闻，格式：Excel
```

### 示例 3：导出多种格式

```
/export-news
导出最近一周的新闻，生成以下格式：
1. CSV（用于数据分析）
2. JSON（用于 API 对接）
3. Markdown（用于报告）
```

### 示例 4：自定义字段导出

```
/export-news
导出以下字段：标题、来源、发布时间、链接
格式：CSV
```

## 注意事项

- 大量数据建议分批导出
- CSV 使用 UTF-8-BOM 编码确保 Excel 正确显示中文
- JSON 导出时注意日期格式
- Excel 导出注意单元格字符限制（32,767 字符）
- 导出前确保有足够的磁盘空间

## 相关文档

- [数据导出指南](../../docs/使用指南/)
- [新闻采集器配置](../../news-collector/config/)


