# 🌐 HawaiiHub新站点完整配置操作手册

## 📋 概述

本手册详细介绍如何从零开始配置一个新的HawaiiHub站点，包括系统安装、基础配置、模块设置、安全配置等完整流程。

## 🚀 系统安装

### 环境要求

```bash
# 服务器环境要求
- PHP 7.4+ (推荐 8.0+)
- MySQL 5.7+ (推荐 8.0+)
- Nginx 1.18+ 或 Apache 2.4+
- Redis 6.0+ (可选，用于缓存)
- SSL证书 (生产环境必需)
```

### 安装步骤

1. **下载系统文件**

```bash
# 下载火鸟门户系统
wget https://download.hawaiihub.net/firebird-portal-latest.zip

# 解压到网站目录
unzip firebird-portal-latest.zip -d /www/wwwroot/hawaiihub.net/
```

2. **设置文件权限**

```bash
# 设置目录权限
chmod -R 755 /www/wwwroot/hawaiihub.net/
chmod -R 777 /www/wwwroot/hawaiihub.net/uploads/
chmod -R 777 /www/wwwroot/hawaiihub.net/data/
chmod -R 777 /www/wwwroot/hawaiihub.net/templates_c/
```

3. **创建数据库**

```sql
-- 创建数据库
CREATE DATABASE hawaiihub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 创建用户并授权
CREATE USER 'hawaiihub'@'localhost' IDENTIFIED BY 'strong_password';
GRANT ALL PRIVILEGES ON hawaiihub.* TO 'hawaiihub'@'localhost';
FLUSH PRIVILEGES;
```

## ⚙️ 基础配置

### 数据库配置

编辑 `include/dbinfo.inc.php`：

```php
<?php
$cfg_dbhost = 'localhost';
$cfg_dbname = 'hawaiihub';
$cfg_dbuser = 'hawaiihub';
$cfg_dbpwd = 'strong_password';
$cfg_dbprefix = 'hn_';
$cfg_db_language = 'utf8mb4';
$cfg_dbconnect = 'mysqli';
?>
```

### 网站基础信息配置

编辑 `include/config/siteConfig.inc.php`：

```php
<?php
// 网站基础信息
$cfg_basehost = 'hawaiihub.net';
$cfg_webname = 'HawaiiHub华人生活平台';
$cfg_webdesc = '夏威夷华人生活服务平台';
$cfg_keywords = '夏威夷,华人,生活,服务,社区';

// 安全配置
$cfg_secureAccess = 'https://';
$cfg_fileUrl = 'https://hawaiihub.net';
$cfg_uploadDir = '/uploads';

// 邮件配置
$cfg_sendmail_bysmtp = 'Y';
$cfg_smtp_server = 'smtp.gmail.com';
$cfg_smtp_port = '587';
$cfg_smtp_usermail = 'noreply@hawaiihub.net';
$cfg_smtp_uname = 'noreply@hawaiihub.net';
$cfg_smtp_password = 'your_email_password';
?>
```

## 🏢 后台管理配置

### 管理员账户设置

1. **访问安装向导**
   - 浏览器访问：`https://hawaiihub.net/install/`
   - 按照向导完成基础安装

2. **创建超级管理员**

```sql
-- 插入管理员账户
INSERT INTO `hn_admin` (`username`, `password`, `email`, `logintime`, `loginip`, `state`) 
VALUES ('admin', MD5('admin123456'), 'admin@hawaiihub.net', NOW(), '127.0.0.1', 1);
```

3. **后台登录**
   - 访问：`https://hawaiihub.net/admin/`
   - 用户名：admin
   - 密码：admin123456

### 系统基础设置

1. **网站信息设置**
   - 后台 → 系统配置 → 网站信息
   - 设置网站名称、描述、关键词
   - 上传网站Logo和图标

2. **SEO配置**
   - 后台 → 系统配置 → SEO设置
   - 配置首页标题、描述、关键词
   - 设置URL重写规则

3. **安全设置**
   - 后台 → 系统配置 → 安全设置
   - 开启防SQL注入
   - 设置登录验证码
   - 配置IP白名单

## 🎨 模板和主题配置

### 选择模板

1. **前台模板**
   - 后台 → 模板管理 → 前台模板
   - 选择适合的模板主题
   - 配置模板参数

2. **手机端模板**
   - 后台 → 模板管理 → 手机模板
   - 启用响应式设计
   - 配置移动端专用功能

### 自定义配置

```php
// 模板配置文件：include/config/template.inc.php
$customTemplate = 'skin1';           // PC端模板
$customTouchTemplate = 'skin2';      // 移动端模板
$customChannelSwitch = 1;            // 启用模块
$customSeoTitle = 'HawaiiHub华人平台';
$customSeoKeyword = '夏威夷,华人,生活';
$customSeoDescription = '夏威夷华人生活服务平台';
```

## 📱 功能模块配置

### 启用核心模块

1. **信息资讯模块**

```php
// include/config/article.inc.php
$customChannelName = '信息资讯';
$customChannelSwitch = 1;  // 启用模块
$customTemplate = 'skin1';
$customSeoTitle = '夏威夷华人资讯';
```

2. **分类信息模块**

```php
// include/config/info.inc.php
$customChannelName = '本地同城';
$customChannelSwitch = 1;
$customFabuCheck = 0;      // 发布审核：0-不审核，1-审核
$customCommentCheck = 0;   // 评论审核
```

3. **招聘求职模块**

```php
// include/config/job.inc.php
$customChannelName = '招聘求职';
$customChannelSwitch = 1;
$customSeoTitle = '夏威夷华人招聘';
```

### 配置支付系统

1. **支付宝配置**

```php
// api/payment/alipay/config.php
$alipay_config = array(
    'partner' => 'your_partner_id',
    'key' => 'your_key',
    'seller_email' => 'your_email@example.com',
    'sign_type' => 'MD5',
    'input_charset' => 'utf-8',
    'transport' => 'https'
);
```

2. **微信支付配置**

```php
// api/payment/wxpay/config.php
$wxpay_config = array(
    'appid' => 'your_app_id',
    'mchid' => 'your_mch_id',
    'key' => 'your_api_key',
    'appsecret' => 'your_app_secret'
);
```

## 🔐 安全和性能优化

### SSL证书配置

1. **Nginx配置**

```nginx
server {
    listen 443 ssl http2;
    server_name hawaiihub.net www.hawaiihub.net;
    
    ssl_certificate /etc/ssl/certs/hawaiihub.crt;
    ssl_certificate_key /etc/ssl/private/hawaiihub.key;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    
    root /www/wwwroot/hawaiihub.net;
    index index.php index.html;
    
    location ~ \.php$ {
        fastcgi_pass 127.0.0.1:9000;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
}
```

2. **强制HTTPS重定向**

```nginx
server {
    listen 80;
    server_name hawaiihub.net www.hawaiihub.net;
    return 301 https://$server_name$request_uri;
}
```

### 性能优化

1. **开启缓存**

```php
// include/config/cache.inc.php
$cfg_cache_type = 'redis';
$cfg_cache_time = 3600;
$cfg_redis_host = '127.0.0.1';
$cfg_redis_port = 6379;
$cfg_redis_auth = 'your_redis_password';
```

2. **数据库优化**

```sql
-- 创建索引
CREATE INDEX idx_pubdate ON hn_article (pubdate);
CREATE INDEX idx_typeid ON hn_article (typeid);
CREATE INDEX idx_city ON hn_info (city);

-- 优化配置
SET GLOBAL innodb_buffer_pool_size = 1073741824;  -- 1GB
SET GLOBAL query_cache_size = 268435456;          -- 256MB
```

## 📊 监控和维护

### 日志配置

1. **错误日志**

```php
// include/config/log.inc.php
$cfg_error_log = 1;
$cfg_log_path = '/www/wwwroot/hawaiihub.net/data/logs/';
$cfg_log_level = 'error';
```

2. **访问日志**

```nginx
# Nginx访问日志
access_log /var/log/nginx/hawaiihub_access.log combined;
error_log /var/log/nginx/hawaiihub_error.log;
```

### 备份策略

1. **数据库备份**

```bash
#!/bin/bash
# 每日数据库备份脚本
DATE=$(date +%Y%m%d_%H%M%S)
mysqldump -u hawaiihub -p hawaiihub > /backup/hawaiihub_$DATE.sql
find /backup -name "hawaiihub_*.sql" -mtime +7 -delete
```

2. **文件备份**

```bash
#!/bin/bash
# 每周文件备份脚本
DATE=$(date +%Y%m%d)
tar -czf /backup/hawaiihub_files_$DATE.tar.gz /www/wwwroot/hawaiihub.net/
find /backup -name "hawaiihub_files_*.tar.gz" -mtime +30 -delete
```

## 🚀 上线检查清单

### 上线前检查

- [ ] 数据库连接正常
- [ ] 文件权限设置正确
- [ ] SSL证书配置完成
- [ ] 邮件发送功能正常
- [ ] 支付系统测试通过
- [ ] 备份策略已部署
- [ ] 监控系统已配置
- [ ] 安全设置已启用
- [ ] 性能优化已完成
- [ ] 域名解析已配置

### 上线后验证

- [ ] 网站首页正常访问
- [ ] 用户注册登录正常
- [ ] 各功能模块正常
- [ ] 移动端适配正常
- [ ] 搜索引擎收录正常
- [ ] 监控告警正常
- [ ] 备份任务正常执行

## 📞 技术支持

- **官方文档**: <https://docs.hawaiihub.net>
- **技术支持**: <support@hawaiihub.net>
- **紧急联系**: +1-808-123-4567
- **社区论坛**: <https://community.hawaiihub.net>
