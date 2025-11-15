# 分析新闻数据

分析采集到的新闻数据，生成统计报告和趋势分析。

## 分析维度

### 1. 数量统计

- 总新闻数
- 按日期统计
- 按来源统计
- 按类别统计

### 2. 内容分析

- 关键词提取
- 主题分类
- 情感分析
- 热点话题

### 3. 趋势分析

- 时间趋势
- 热度变化
- 话题演变
- 来源分布

### 4. 质量评估

- 内容完整性
- 信息准确性
- 时效性
- 相关性

## 执行步骤

### 1. 数据准备

```python
from src.database import get_news_data

# 获取指定时间范围的新闻
news_data = get_news_data(
    start_date='2025-10-26',
    end_date='2025-11-02'
)
```

### 2. 基础统计

```python
def basic_statistics(news_data):
    """基础统计分析"""
    stats = {
        'total_count': len(news_data),
        'date_distribution': count_by_date(news_data),
        'source_distribution': count_by_source(news_data),
        'category_distribution': count_by_category(news_data)
    }
    return stats
```

### 3. 关键词分析

```python
from collections import Counter
import jieba

def extract_keywords(news_data, top_n=20):
    """提取高频关键词"""
    all_words = []
    for news in news_data:
        words = jieba.cut(news['content'])
        all_words.extend(words)

    # 过滤停用词
    filtered_words = filter_stopwords(all_words)

    # 统计词频
    word_freq = Counter(filtered_words)
    return word_freq.most_common(top_n)
```

### 4. 主题分类

```python
def classify_topics(news_data):
    """新闻主题分类"""
    topics = {
        '科技': [],
        '财经': [],
        '娱乐': [],
        '体育': [],
        '其他': []
    }

    for news in news_data:
        topic = predict_topic(news['content'])
        topics[topic].append(news)

    return topics
```

### 5. 趋势分析

```python
import pandas as pd
import matplotlib.pyplot as plt

def analyze_trends(news_data):
    """分析新闻趋势"""
    df = pd.DataFrame(news_data)
    df['date'] = pd.to_datetime(df['published_at'])

    # 按日期统计
    daily_counts = df.groupby(df['date'].dt.date).size()

    # 绘制趋势图
    plt.figure(figsize=(12, 6))
    daily_counts.plot(kind='line')
    plt.title('新闻发布趋势')
    plt.xlabel('日期')
    plt.ylabel('新闻数量')
    plt.savefig('news_trend.png')

    return daily_counts
```

## 分析报告格式

### 📊 数据概览

```markdown
## 数据概览

- 分析时间范围：2025-10-26 至 2025-11-02
- 新闻总数：XXX 条
- 数据来源：XX 个
- 主题分类：XX 个
```

### 📈 统计分析

```markdown
## 统计分析

### 按日期分布

| 日期 | 数量 | 占比 |
|------|------|------|
| 2025-11-02 | 50 | 25% |
| 2025-11-01 | 45 | 22.5% |
| ... | ... | ... |

### 按来源分布

| 来源 | 数量 | 占比 |
|------|------|------|
| 新浪科技 | 30 | 15% |
| 腾讯新闻 | 25 | 12.5% |
| ... | ... | ... |

### 按主题分布

| 主题 | 数量 | 占比 |
|------|------|------|
| 科技 | 80 | 40% |
| 财经 | 60 | 30% |
| ... | ... | ... |
```

### 🔥 热点分析

```markdown
## 热点分析

### Top 20 关键词

1. 人工智能 (50次)
2. 机器学习 (45次)
3. 深度学习 (40次)
...

### 热门话题

1. **AI 技术突破** (30条相关新闻)
   - 主要内容：...
   - 时间分布：...
   - 来源分布：...

2. **行业应用** (25条相关新闻)
   - 主要内容：...
   - 时间分布：...
   - 来源分布：...
```

### 📉 趋势分析

```markdown
## 趋势分析

### 发布趋势

![新闻发布趋势图](news_trend.png)

**观察结论**：
- 工作日发布量高于周末
- 每日发布高峰时段：上午 9-11 点
- 周三发布量最高

### 话题演变

- **上升话题**：AI应用、量子计算
- **下降话题**：区块链、元宇宙
- **稳定话题**：云计算、大数据
```

### 💡 洞察与建议

```markdown
## 洞察与建议

### 主要发现

1. AI 相关新闻持续增长
2. 科技类新闻占比最高
3. 新浪科技是主要来源

### 建议

1. 增加 AI 相关内容采集
2. 拓展更多新闻来源
3. 优化采集时间策略
```

## 可视化分析

### 词云图

```python
from wordcloud import WordCloud

def generate_wordcloud(keywords):
    """生成词云图"""
    wordcloud = WordCloud(
        font_path='simhei.ttf',
        width=800,
        height=400,
        background_color='white'
    ).generate_from_frequencies(dict(keywords))

    plt.figure(figsize=(12, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig('wordcloud.png')
```

### 分布图

```python
def plot_distribution(data, title, filename):
    """绘制分布图"""
    plt.figure(figsize=(10, 6))
    data.plot(kind='bar')
    plt.title(title)
    plt.xlabel('类别')
    plt.ylabel('数量')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(filename)
```

## 高级分析

### 情感分析

```python
from snownlp import SnowNLP

def sentiment_analysis(news_data):
    """情感分析"""
    sentiments = []
    for news in news_data:
        s = SnowNLP(news['content'])
        sentiments.append({
            'title': news['title'],
            'sentiment': s.sentiments,  # 0-1，越接近1越积极
            'category': 'positive' if s.sentiments > 0.6 else 'negative'
        })
    return sentiments
```

### 相似度分析

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def find_similar_news(news_data, threshold=0.8):
    """查找相似新闻"""
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([n['content'] for n in news_data])

    similarity_matrix = cosine_similarity(tfidf_matrix)

    similar_pairs = []
    for i in range(len(news_data)):
        for j in range(i+1, len(news_data)):
            if similarity_matrix[i][j] > threshold:
                similar_pairs.append((i, j, similarity_matrix[i][j]))

    return similar_pairs
```

## 输出格式

### 📊 分析报告

生成完整的 Markdown 格式分析报告，包括：
- 数据概览
- 统计分析
- 热点分析
- 趋势分析
- 洞察建议

### 📈 可视化图表

生成以下图表：
- 新闻发布趋势图
- 来源分布图
- 主题分布图
- 关键词词云图

### 📁 数据文件

导出以下数据文件：
- `analysis_report.md` - 分析报告
- `statistics.json` - 统计数据
- `keywords.csv` - 关键词列表
- `trends.csv` - 趋势数据

## 使用示例

### 示例 1：基础分析

```
/analyze-news
分析最近 7 天的新闻数据
```

### 示例 2：深度分析

```
/analyze-news
对 2025-10 月的新闻进行深度分析，包括：
1. 关键词提取
2. 主题分类
3. 趋势分析
4. 情感分析
```

### 示例 3：对比分析

```
/analyze-news
对比分析 10 月和 11 月的新闻数据，找出变化趋势
```

## 注意事项

- 确保数据库连接正常
- 分析大量数据时注意内存使用
- 定期更新停用词表
- 保存分析结果供后续参考

## 相关文档

- [数据分析指南](../../docs/使用指南/)
- [可视化配置](../../news-collector/config/)


