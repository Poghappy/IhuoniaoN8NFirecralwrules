# 火鸟门户系统 Firecrawl 集成优化方案

## 📋 项目概述

基于 Firecrawl Observer 项目架构和官方示例，为火鸟门户系统设计的数据采集器优化方案。

## 🔍 Firecrawl Observer 核心特性分析

### 主要功能
- **网站监控**: 支持单页面和整站监控
- **AI智能分析**: 过滤噪音，智能变化检测
- **灵活通知**: 邮件、Webhook、仪表板通知
- **安全密钥管理**: AES-256-GCM 加密存储
- **实时更新**: 可配置间隔的即时变化检测
- **现代UI**: 响应式界面，支持暗色模式

### 技术架构
```
fc-observer/
├── convex/              # 后端函数和数据库模式
│   ├── auth.ts          # 认证逻辑
│   ├── schema.ts        # 数据库模式
│   ├── firecrawl.ts     # Firecrawl 集成
│   └── aiAnalysis.ts    # AI 变化分析
├── src/
│   ├── app/            # Next.js 应用路由页面
│   ├── components/     # React 组件
│   ├── config/         # 应用配置
│   └── lib/            # 工具和助手
└── scripts/            # 测试脚本
```

## 🚀 火鸟门户系统集成方案

### 1. 核心集成模块

#### A. 数据采集引擎
```python
# firecrawl_engine.py
from firecrawl import FirecrawlApp
import json
import logging
from datetime import datetime

class FirecrawlEngine:
    def __init__(self, api_key, config_path="config.json"):
        self.app = FirecrawlApp(api_key=api_key)
        self.config = self.load_config(config_path)
        self.logger = self.setup_logging()
    
    def crawl_single_page(self, url, options=None):
        """单页面抓取"""
        try:
            result = self.app.scrape_url(url, params=options)
            return self.process_result(result)
        except Exception as e:
            self.logger.error(f"单页面抓取失败: {e}")
            return None
    
    def crawl_full_site(self, url, options=None):
        """整站抓取"""
        try:
            result = self.app.crawl_url(url, params=options)
            return self.process_crawl_result(result)
        except Exception as e:
            self.logger.error(f"整站抓取失败: {e}")
            return None
```

#### B. 智能变化检测
```python
# change_detector.py
import hashlib
from difflib import unified_diff
from datetime import datetime

class ChangeDetector:
    def __init__(self, ai_provider=None):
        self.ai_provider = ai_provider
        self.content_cache = {}
    
    def detect_changes(self, url, new_content):
        """检测内容变化"""
        content_hash = self.generate_hash(new_content)
        
        if url in self.content_cache:
            old_hash = self.content_cache[url]['hash']
            if content_hash != old_hash:
                changes = self.analyze_changes(
                    self.content_cache[url]['content'], 
                    new_content
                )
                self.content_cache[url] = {
                    'content': new_content,
                    'hash': content_hash,
                    'last_updated': datetime.now()
                }
                return changes
        else:
            self.content_cache[url] = {
                'content': new_content,
                'hash': content_hash,
                'last_updated': datetime.now()
            }
        
        return None
    
    def ai_filter_changes(self, changes, threshold=50):
        """AI智能过滤变化"""
        if not self.ai_provider or not changes:
            return changes
        
        # 调用AI分析变化重要性
        importance_score = self.ai_provider.analyze_importance(changes)
        
        if importance_score >= threshold:
            return {
                'changes': changes,
                'importance_score': importance_score,
                'ai_reasoning': self.ai_provider.get_reasoning()
            }
        
        return None
```

#### C. 通知系统
```python
# notification_system.py
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class NotificationSystem:
    def __init__(self, config):
        self.email_config = config.get('email', {})
        self.webhook_config = config.get('webhook', {})
    
    def send_email_notification(self, changes, recipients):
        """发送邮件通知"""
        if not self.email_config.get('enabled', False):
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_config['from_email']
            msg['To'] = ', '.join(recipients)
            msg['Subject'] = f"网站变化检测 - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            
            body = self.format_email_body(changes)
            msg.attach(MIMEText(body, 'html'))
            
            server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port'])
            server.starttls()
            server.login(self.email_config['username'], self.email_config['password'])
            server.send_message(msg)
            server.quit()
            
            return True
        except Exception as e:
            print(f"邮件发送失败: {e}")
            return False
    
    def send_webhook_notification(self, changes, webhook_url):
        """发送Webhook通知"""
        if not self.webhook_config.get('enabled', False):
            return False
        
        try:
            payload = {
                'timestamp': datetime.now().isoformat(),
                'changes': changes,
                'source': '火鸟门户数据采集器'
            }
            
            response = requests.post(
                webhook_url,
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            return response.status_code == 200
        except Exception as e:
            print(f"Webhook发送失败: {e}")
            return False
```

### 2. 配置文件优化

#### 更新后的 config.json
```json
{
  "firecrawl": {
    "api_key": "YOUR_FIRECRAWL_API_KEY",
    "base_url": "https://api.firecrawl.dev",
    "timeout": 30,
    "retry_attempts": 3
  },
  "monitoring": {
    "enabled": true,
    "check_interval": 3600,
    "change_detection": {
      "enabled": true,
      "ai_filtering": {
        "enabled": true,
        "provider": "openai",
        "api_key": "YOUR_AI_API_KEY",
        "threshold": 50
      }
    }
  },
  "notifications": {
    "email": {
      "enabled": true,
      "smtp_server": "smtp.gmail.com",
      "smtp_port": 587,
      "username": "your_email@gmail.com",
      "password": "your_app_password",
      "from_email": "noreply@hawaiihub.net",
      "recipients": ["admin@hawaiihub.net"]
    },
    "webhook": {
      "enabled": true,
      "urls": ["https://hawaiihub.net/api/webhook/firecrawl"]
    }
  },
  "sources": [
    {
      "name": "火鸟门户首页监控",
      "url": "https://hawaiihub.net",
      "type": "single_page",
      "schedule": {
        "interval": 1800,
        "enabled": true
      },
      "processing": {
        "extract_text": true,
        "extract_links": true,
        "extract_images": false,
        "formats": ["markdown", "html"]
      },
      "monitoring": {
        "track_changes": true,
        "ai_analysis": true,
        "notification_threshold": 60
      }
    },
    {
      "name": "新闻模块监控",
      "url": "https://hawaiihub.net/news",
      "type": "full_site",
      "schedule": {
        "interval": 3600,
        "enabled": true
      },
      "crawl_options": {
        "limit": 50,
        "excludePaths": ["/admin/*", "/api/*"],
        "includePaths": ["/news/*", "/article/*"]
      }
    }
  ],
  "storage": {
    "type": "file",
    "path": "./data",
    "encryption": {
      "enabled": true,
      "algorithm": "AES-256-GCM"
    }
  },
  "security": {
    "api_key_encryption": true,
    "ssl_verify": true,
    "user_agent": "FirebirdPortal-DataCollector/1.0",
    "rate_limiting": {
      "enabled": true,
      "requests_per_minute": 60
    }
  }
}
```

### 3. 主程序集成

#### 更新后的 main.py
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
火鸟门户系统 Firecrawl 数据采集器
集成 Observer 功能的增强版本
"""

import os
import sys
import json
import time
import schedule
from datetime import datetime
from firecrawl_engine import FirecrawlEngine
from change_detector import ChangeDetector
from notification_system import NotificationSystem
from ai_provider import AIProvider

class FirebirdDataCollector:
    def __init__(self, config_path="config.json"):
        self.config = self.load_config(config_path)
        self.engine = FirecrawlEngine(
            api_key=self.config['firecrawl']['api_key'],
            config_path=config_path
        )
        
        # 初始化AI提供商（如果启用）
        ai_config = self.config['monitoring']['change_detection']['ai_filtering']
        self.ai_provider = None
        if ai_config.get('enabled', False):
            self.ai_provider = AIProvider(
                provider=ai_config['provider'],
                api_key=ai_config['api_key']
            )
        
        self.change_detector = ChangeDetector(self.ai_provider)
        self.notification_system = NotificationSystem(self.config['notifications'])
        
        self.setup_scheduler()
    
    def load_config(self, config_path):
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"配置文件加载失败: {e}")
            sys.exit(1)
    
    def setup_scheduler(self):
        """设置定时任务"""
        for source in self.config['sources']:
            if source['schedule']['enabled']:
                interval = source['schedule']['interval']
                schedule.every(interval).seconds.do(
                    self.process_source, source
                )
    
    def process_source(self, source):
        """处理单个数据源"""
        print(f"开始处理数据源: {source['name']}")
        
        try:
            if source['type'] == 'single_page':
                result = self.engine.crawl_single_page(
                    source['url'], 
                    source.get('processing', {})
                )
            elif source['type'] == 'full_site':
                result = self.engine.crawl_full_site(
                    source['url'],
                    source.get('crawl_options', {})
                )
            else:
                print(f"未知的数据源类型: {source['type']}")
                return
            
            if result and source.get('monitoring', {}).get('track_changes', False):
                self.check_for_changes(source, result)
            
            self.save_result(source, result)
            
        except Exception as e:
            print(f"处理数据源失败 {source['name']}: {e}")
    
    def check_for_changes(self, source, result):
        """检查内容变化"""
        content = result.get('content', '')
        changes = self.change_detector.detect_changes(source['url'], content)
        
        if changes:
            print(f"检测到变化: {source['name']}")
            
            # AI智能过滤（如果启用）
            if source.get('monitoring', {}).get('ai_analysis', False):
                threshold = source.get('monitoring', {}).get('notification_threshold', 50)
                filtered_changes = self.change_detector.ai_filter_changes(changes, threshold)
                
                if filtered_changes:
                    self.send_notifications(source, filtered_changes)
            else:
                self.send_notifications(source, changes)
    
    def send_notifications(self, source, changes):
        """发送通知"""
        # 邮件通知
        if self.config['notifications']['email']['enabled']:
            recipients = self.config['notifications']['email']['recipients']
            self.notification_system.send_email_notification(changes, recipients)
        
        # Webhook通知
        if self.config['notifications']['webhook']['enabled']:
            for webhook_url in self.config['notifications']['webhook']['urls']:
                self.notification_system.send_webhook_notification(changes, webhook_url)
    
    def save_result(self, source, result):
        """保存采集结果"""
        if not result:
            return
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{source['name']}_{timestamp}.json"
        filepath = os.path.join(self.config['storage']['path'], filename)
        
        os.makedirs(self.config['storage']['path'], exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"结果已保存: {filepath}")
    
    def run(self):
        """运行采集器"""
        print("🔥 火鸟门户数据采集器启动")
        print(f"配置的数据源数量: {len(self.config['sources'])}")
        print(f"监控功能: {'启用' if self.config['monitoring']['enabled'] else '禁用'}")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n采集器已停止")
        except Exception as e:
            print(f"运行时错误: {e}")

if __name__ == "__main__":
    collector = FirebirdDataCollector()
    collector.run()
```

## 🔧 部署和使用

### 1. 环境准备
```bash
# 激活虚拟环境
source firecrawl_env/bin/activate

# 安装额外依赖
pip install schedule requests python-dotenv
```

### 2. 配置密钥
```bash
# 创建环境变量文件
echo "FIRECRAWL_API_KEY=your_api_key_here" > .env
echo "OPENAI_API_KEY=your_openai_key_here" >> .env
```

### 3. 运行采集器
```bash
# 测试运行
python main.py

# 后台运行
nohup python main.py > collector.log 2>&1 &
```

## 📊 监控和维护

### 1. 日志监控
```bash
# 查看实时日志
tail -f collector.log

# 查看错误日志
grep "ERROR" collector.log
```

### 2. 性能优化
- 调整检查间隔避免API限制
- 使用AI过滤减少无效通知
- 定期清理历史数据

### 3. 安全建议
- 定期轮换API密钥
- 启用SSL验证
- 使用加密存储敏感数据

## 🚀 扩展功能

### 1. 集成火鸟门户API
- 自动发布采集内容到门户
- 同步用户权限和分类
- 实时数据推送

### 2. 高级分析
- 内容质量评分
- 趋势分析和预测
- 自动标签和分类

### 3. 多源聚合
- 社交媒体监控
- 竞品分析
- 行业资讯聚合

---

**注意**: 本方案基于 Firecrawl Observer 的最佳实践，结合火鸟门户系统的具体需求设计。使用前请确保已获得相应的API密钥和权限。