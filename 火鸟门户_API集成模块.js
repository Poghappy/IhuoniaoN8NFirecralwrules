/**
 * 火鸟门户API集成模块
 * 
 * 基于火鸟门户API文档实现的完整集成方案
 * 支持内容发布、修改、删除、查询等操作
 */

class HuoNiaoAPIClient {
    constructor(config = {}) {
        this.baseUrl = config.baseUrl || 'https://hawaiihub.net/include/ajax.php';
        this.sessionId = config.sessionId || '1ru3hf75ah15qm2ckm1en18lij';
        this.service = 'article';
        this.timeout = config.timeout || 30000;
        this.retryCount = config.retryCount || 3;
        this.retryDelay = config.retryDelay || 2000;
    }

    /**
     * 通用API请求方法
     */
    async request(action, params = {}, method = 'GET') {
        const url = new URL(this.baseUrl);
        url.searchParams.set('service', this.service);
        url.searchParams.set('action', action);

        const options = {
            method: method,
            headers: {
                'Cookie': `PHPSESSID=${this.sessionId}`,
                'User-Agent': 'HuoNiao-Content-Collector/3.0',
                'Accept': 'application/json, text/plain, */*'
            },
            timeout: this.timeout
        };

        if (method === 'GET' && Object.keys(params).length > 0) {
            Object.entries(params).forEach(([key, value]) => {
                if (value !== null && value !== undefined) {
                    url.searchParams.set(key, value);
                }
            });
        }

        if (method === 'POST') {
            const formData = new URLSearchParams();
            Object.entries(params).forEach(([key, value]) => {
                if (value !== null && value !== undefined) {
                    formData.append(key, value);
                }
            });
            
            options.body = formData;
            options.headers['Content-Type'] = 'application/x-www-form-urlencoded';
        }

        let lastError;
        
        for (let i = 0; i < this.retryCount; i++) {
            try {
                console.log(`API请求 (尝试 ${i + 1}/${this.retryCount}):`, {
                    url: url.toString(),
                    method: method,
                    action: action
                });

                const response = await fetch(url.toString(), options);
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }

                const data = await response.json();
                
                console.log(`API响应:`, {
                    action: action,
                    state: data.state,
                    success: data.state === 100
                });

                return data;

            } catch (error) {
                lastError = error;
                console.error(`API请求失败 (尝试 ${i + 1}/${this.retryCount}):`, error.message);
                
                if (i < this.retryCount - 1) {
                    await this.delay(this.retryDelay * (i + 1));
                }
            }
        }

        throw new Error(`API请求最终失败: ${lastError.message}`);
    }

    /**
     * 延迟函数
     */
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * 获取新闻分类列表
     */
    async getCategories(params = {}) {
        const defaultParams = {
            mold: 0,
            type: 0,
            son: 1,
            page: 1,
            pageSize: 100
        };

        return await this.request('type', { ...defaultParams, ...params });
    }

    /**
     * 获取分类详情
     */
    async getCategoryDetail(categoryId) {
        return await this.request('typeDetail', { id: categoryId });
    }

    /**
     * 获取新闻列表
     */
    async getArticleList(params = {}) {
        const defaultParams = {
            page: 1,
            pageSize: 20,
            orderby: 1 // 按发布时间排序
        };

        return await this.request('alist', { ...defaultParams, ...params });
    }

    /**
     * 获取新闻详情
     */
    async getArticleDetail(articleId) {
        return await this.request('detail', { id: articleId });
    }

    /**
     * 发布新闻
     */
    async publishArticle(articleData) {
        // 验证必填字段
        const requiredFields = ['title', 'typeid', 'body', 'writer', 'source'];
        for (const field of requiredFields) {
            if (!articleData[field]) {
                throw new Error(`缺少必填字段: ${field}`);
            }
        }

        // 构建发布参数
        const publishParams = {
            title: this.sanitizeText(articleData.title, 60),
            typeid: parseInt(articleData.typeid) || 1,
            body: this.sanitizeHtml(articleData.body, 2000),
            writer: this.sanitizeText(articleData.writer, 20),
            source: this.sanitizeText(articleData.source, 30),
            keywords: this.sanitizeText(articleData.keywords || '', 50),
            description: this.sanitizeText(articleData.description || '', 255),
            litpic: articleData.litpic || '',
            article_prop: parseInt(articleData.article_prop) || 0,
            typeset: parseInt(articleData.typeset) || 0
        };

        // 可选字段
        if (articleData.sourceurl) {
            publishParams.sourceurl = articleData.sourceurl;
        }
        
        if (articleData.imglist) {
            publishParams.imglist = JSON.stringify(articleData.imglist);
        }

        if (articleData.videotype) {
            publishParams.videotype = parseInt(articleData.videotype);
            publishParams.videourl = articleData.videourl || '';
        }

        if (articleData.pubdate) {
            publishParams.pubdate = parseInt(articleData.pubdate);
        }

        console.log('发布文章参数:', publishParams);

        return await this.request('put', publishParams, 'POST');
    }

    /**
     * 修改新闻
     */
    async updateArticle(articleId, articleData) {
        if (!articleId) {
            throw new Error('文章ID不能为空');
        }

        const updateParams = {
            id: parseInt(articleId),
            ...articleData
        };

        return await this.request('edit', updateParams, 'POST');
    }

    /**
     * 删除新闻
     */
    async deleteArticle(articleId) {
        if (!articleId) {
            throw new Error('文章ID不能为空');
        }

        return await this.request('del', { id: parseInt(articleId) }, 'POST');
    }

    /**
     * 获取评论列表
     */
    async getComments(articleId, params = {}) {
        const defaultParams = {
            fid: articleId,
            page: 1,
            pageSize: 50
        };

        return await this.request('getCommonList', { ...defaultParams, ...params });
    }

    /**
     * 发表评论
     */
    async postComment(articleId, content, replyToId = null) {
        const commentParams = {
            aid: parseInt(articleId),
            content: this.sanitizeText(content, 250)
        };

        if (replyToId) {
            commentParams.id = parseInt(replyToId);
        }

        return await this.request('sendCommon', commentParams, 'POST');
    }

    /**
     * 点赞评论
     */
    async likeComment(commentId) {
        return await this.request('dingCommon', { id: parseInt(commentId) }, 'POST');
    }

    /**
     * 获取专题列表
     */
    async getSpecialTopics(params = {}) {
        const defaultParams = {
            page: 1,
            pageSize: 20
        };

        return await this.request('zhuantiList', { ...defaultParams, ...params });
    }

    /**
     * 获取专题详情
     */
    async getSpecialTopicDetail(topicId) {
        return await this.request('zhuantiDetail', { id: topicId });
    }

    /**
     * 批量发布文章
     */
    async batchPublishArticles(articles, options = {}) {
        const results = [];
        const batchSize = options.batchSize || 5;
        const delay = options.delay || 2000;

        console.log(`开始批量发布 ${articles.length} 篇文章，批次大小: ${batchSize}`);

        for (let i = 0; i < articles.length; i += batchSize) {
            const batch = articles.slice(i, i + batchSize);
            const batchResults = [];

            console.log(`处理批次 ${Math.floor(i / batchSize) + 1}/${Math.ceil(articles.length / batchSize)}`);

            // 并行处理当前批次
            const promises = batch.map(async (article, index) => {
                try {
                    const result = await this.publishArticle(article);
                    return {
                        index: i + index,
                        article: article,
                        result: result,
                        success: result.state === 100,
                        error: null
                    };
                } catch (error) {
                    return {
                        index: i + index,
                        article: article,
                        result: null,
                        success: false,
                        error: error.message
                    };
                }
            });

            const batchResults_ = await Promise.all(promises);
            batchResults.push(...batchResults_);
            results.push(...batchResults_);

            // 批次间延迟
            if (i + batchSize < articles.length) {
                console.log(`批次完成，等待 ${delay}ms 后继续...`);
                await this.delay(delay);
            }
        }

        // 统计结果
        const successCount = results.filter(r => r.success).length;
        const failureCount = results.filter(r => !r.success).length;

        console.log(`批量发布完成: 成功 ${successCount} 篇，失败 ${failureCount} 篇`);

        return {
            total: articles.length,
            success: successCount,
            failure: failureCount,
            results: results
        };
    }

    /**
     * 检查文章是否存在
     */
    async checkArticleExists(title, threshold = 0.85) {
        try {
            const searchResult = await this.getArticleList({
                title: title.substring(0, 20), // 使用标题前20个字符搜索
                pageSize: 10
            });

            if (searchResult.state === 100 && searchResult.info && searchResult.info.list) {
                for (const article of searchResult.info.list) {
                    const similarity = this.calculateSimilarity(title, article.title);
                    if (similarity > threshold) {
                        return {
                            exists: true,
                            similarArticle: article,
                            similarity: similarity
                        };
                    }
                }
            }

            return { exists: false };
        } catch (error) {
            console.error('检查文章重复性时出错:', error);
            return { exists: false, error: error.message };
        }
    }

    /**
     * 计算文本相似度
     */
    calculateSimilarity(text1, text2) {
        if (!text1 || !text2) return 0;
        
        const set1 = new Set(text1.toLowerCase().split(''));
        const set2 = new Set(text2.toLowerCase().split(''));
        
        const intersection = new Set([...set1].filter(x => set2.has(x)));
        const union = new Set([...set1, ...set2]);
        
        return intersection.size / union.size;
    }

    /**
     * 文本清理和截断
     */
    sanitizeText(text, maxLength) {
        if (!text) return '';
        
        // 移除HTML标签
        let cleaned = text.replace(/<[^>]*>/g, '');
        
        // 移除多余的空白字符
        cleaned = cleaned.replace(/\s+/g, ' ').trim();
        
        // 截断到指定长度
        if (cleaned.length > maxLength) {
            cleaned = cleaned.substring(0, maxLength - 3) + '...';
        }
        
        return cleaned;
    }

    /**
     * HTML内容清理
     */
    sanitizeHtml(html, maxLength) {
        if (!html) return '';
        
        // 保留基本的HTML标签
        const allowedTags = ['p', 'br', 'strong', 'b', 'em', 'i', 'u', 'a', 'img'];
        let cleaned = html;
        
        // 移除不允许的标签
        cleaned = cleaned.replace(/<(?!\/?(?:p|br|strong|b|em|i|u|a|img)\b)[^>]*>/gi, '');
        
        // 清理属性，只保留必要的
        cleaned = cleaned.replace(/<a\s+[^>]*href\s*=\s*["']([^"']*)["'][^>]*>/gi, '<a href="$1">');
        cleaned = cleaned.replace(/<img\s+[^>]*src\s*=\s*["']([^"']*)["'][^>]*>/gi, '<img src="$1">');
        
        // 截断长度
        if (cleaned.length > maxLength) {
            cleaned = cleaned.substring(0, maxLength - 3) + '...';
        }
        
        return cleaned;
    }

    /**
     * 获取系统配置
     */
    async getSystemConfig(params = []) {
        const paramStr = Array.isArray(params) ? params.join(',') : params;
        return await this.request('config', paramStr ? { param: paramStr } : {});
    }

    /**
     * 健康检查
     */
    async healthCheck() {
        try {
            const result = await this.getSystemConfig(['channelName']);
            return {
                healthy: result.state === 100,
                response: result
            };
        } catch (error) {
            return {
                healthy: false,
                error: error.message
            };
        }
    }
}

// 导出模块
if (typeof module !== 'undefined' && module.exports) {
    module.exports = HuoNiaoAPIClient;
}

// n8n 使用示例
function createHuoNiaoClient() {
    return new HuoNiaoAPIClient({
        baseUrl: 'https://hawaiihub.net/include/ajax.php',
        sessionId: '1ru3hf75ah15qm2ckm1en18lij',
        timeout: 30000,
        retryCount: 3,
        retryDelay: 2000
    });
}

// 如果在n8n中使用
if (typeof $input !== 'undefined') {
    const client = createHuoNiaoClient();
    
    // 根据不同的操作类型执行相应的方法
    const operation = $input.first().json.operation || 'publish';
    const data = $input.first().json;
    
    switch (operation) {
        case 'publish':
            return client.publishArticle(data.article);
        case 'update':
            return client.updateArticle(data.articleId, data.article);
        case 'delete':
            return client.deleteArticle(data.articleId);
        case 'getList':
            return client.getArticleList(data.params);
        case 'getDetail':
            return client.getArticleDetail(data.articleId);
        case 'batchPublish':
            return client.batchPublishArticles(data.articles, data.options);
        case 'healthCheck':
            return client.healthCheck();
        default:
            throw new Error(`不支持的操作类型: ${operation}`);
    }
}

/**
 * 火鸟门户新闻模块API轻量级网关
 * 作为n8n与火鸟后台之间的中间层
 * 提供统一的RESTful接口，解决会话管理、去重、限流、安全和监控等问题
 * 
 * @author AI Assistant
 * @version 2.0.0
 * @date 2025-01-18
 */

const crypto = require('crypto');
const axios = require('axios');

/**
 * 火鸟门户API轻量级网关类
 */
class HuoNiaoAPIGateway {
    constructor(config = {}) {
        // 基础配置
        this.config = {
            baseUrl: config.baseUrl || 'https://hawaiihub.net',
            apiPath: config.apiPath || '/include/ajax.php',
            timeout: config.timeout || 30000,
            maxRetries: config.maxRetries || 3,
            retryDelay: config.retryDelay || 1000,
            rateLimit: config.rateLimit || 10, // 每分钟最大请求数
            secretKey: config.secretKey || 'huoniao_gateway_secret_2025',
            enableSecurity: config.enableSecurity !== false,
            enableLogging: config.enableLogging !== false,
            ...config
        };

        // 内部状态
        this.sessionId = null;
        this.sessionExpiry = null;
        this.requestQueue = [];
        this.rateLimitCounter = new Map();
        this.dedupeCache = new Map();
        this.categoryMapping = new Map();
        
        // 初始化
        this.initializeCategoryMapping();
        this.startCleanupTimer();
        this.startSessionMaintenance();
    }

    /**
     * 初始化分类映射
     */
    initializeCategoryMapping() {
        // 根据火鸟系统的实际分类配置
        const mappings = {
            // 科技类 - ID: 1
            1: ['科技', 'tech', 'technology', 'ai', '人工智能', '互联网', 'it', '数码', '电子', '软件', '硬件'],
            // 新闻类 - ID: 2  
            2: ['新闻', 'news', '资讯', '时事', '热点', '头条', '快讯', '报道'],
            // 娱乐类 - ID: 3
            3: ['娱乐', 'entertainment', '明星', '电影', '音乐', '综艺', '八卦', '影视'],
            // 体育类 - ID: 4
            4: ['体育', 'sports', '足球', '篮球', '运动', '健身', '比赛', '赛事'],
            // 财经类 - ID: 5
            5: ['财经', 'finance', '经济', '金融', '股票', '投资', '理财', '商业'],
            // 汽车类 - ID: 6
            6: ['汽车', 'auto', 'car', '车辆', '驾驶', '交通', '新车'],
            // 房产类 - ID: 7
            7: ['房产', 'realestate', '房屋', '楼市', '装修', '家居'],
            // 教育类 - ID: 8
            8: ['教育', 'education', '学习', '培训', '考试', '学校'],
            // 健康类 - ID: 9
            9: ['健康', 'health', '医疗', '养生', '保健', '疾病'],
            // 旅游类 - ID: 10
            10: ['旅游', 'travel', '旅行', '景点', '度假', '酒店'],
            // 美食类 - ID: 11
            11: ['美食', 'food', '餐饮', '菜谱', '烹饪', '小吃'],
            // 时尚类 - ID: 12
            12: ['时尚', 'fashion', '服装', '美容', '化妆', '穿搭'],
            // 文化类 - ID: 13
            13: ['文化', 'culture', '艺术', '历史', '传统', '文学'],
            // 社会类 - ID: 14
            14: ['社会', 'society', '民生', '公益', '法律', '政策']
        };
        
        // 构建映射表
        for (const [categoryId, keywords] of Object.entries(mappings)) {
            const id = parseInt(categoryId);
            keywords.forEach(keyword => {
                this.categoryMapping.set(keyword.toLowerCase(), id);
                // 同时添加标准化后的关键词
                this.categoryMapping.set(this.normalizeCategory(keyword), id);
            });
        }
        
        this.log('debug', '分类映射表初始化完成', { 
            totalMappings: this.categoryMapping.size,
            categories: Object.keys(mappings).length
        });
    }

    /**
     * 启动清理定时器
     */
    startCleanupTimer() {
        // 每小时清理一次过期缓存
        setInterval(() => {
            this.cleanupExpiredCache();
        }, 3600000);
    }

    /**
     * 清理过期缓存
     */
    cleanupExpiredCache() {
        const now = Date.now();
        
        // 清理去重缓存（保留24小时）
        for (const [key, data] of this.dedupeCache.entries()) {
            if (now - data.timestamp > 86400000) {
                this.dedupeCache.delete(key);
            }
        }

        // 清理限流计数器（保留1小时）
        for (const [key, data] of this.rateLimitCounter.entries()) {
            if (now - data.timestamp > 3600000) {
                this.rateLimitCounter.delete(key);
            }
        }

        this.log('info', '缓存清理完成', {
            dedupeCache: this.dedupeCache.size,
            rateLimitCounter: this.rateLimitCounter.size
        });
    }

    /**
     * RESTful API 路由处理
     */
    async handleRequest(method, path, data = {}, headers = {}) {
        const startTime = Date.now();
        const requestId = crypto.randomUUID();
        
        try {
            this.log('info', '收到请求', { 
                requestId,
                method, 
                path, 
                dataKeys: Object.keys(data),
                userAgent: headers['user-agent'] || 'unknown'
            });

            // 安全验证
            if (this.config.enableSecurity && method !== 'GET' && path !== '/v1/health') {
                const signature = headers['x-signature'];
                const timestamp = headers['x-timestamp'];
                
                if (!signature || !timestamp) {
                    throw new Error('缺少安全验证头部');
                }
                
                this.validateSignature(data, signature, timestamp);
                this.log('debug', '安全验证通过', { requestId });
            }

            // 限流检查
            await this.checkRateLimit(headers['x-client-id'] || 'default');

            let result;
            // 路由分发
            switch (`${method.toUpperCase()} ${path}`) {
                case 'POST /v1/articles':
                    result = await this.createArticle(data);
                    break;
                
                case 'PUT /v1/articles':
                    result = await this.updateArticle(data);
                    break;
                
                case 'DELETE /v1/articles':
                    result = await this.deleteArticle(data);
                    break;
                
                case 'GET /v1/categories':
                    result = await this.getCategories();
                    break;
                
                case 'GET /v1/articles':
                    result = await this.getArticles(data);
                    break;
                
                case 'POST /v1/articles/batch':
                    result = await this.batchCreateArticles(data);
                    break;
                
                case 'GET /v1/health':
                    result = await this.healthCheck();
                    break;
                
                default:
                    throw new Error(`不支持的API路径: ${method} ${path}`);
            }
            
            const duration = Date.now() - startTime;
            this.log('info', '请求处理成功', { 
                requestId,
                method, 
                path, 
                duration,
                success: result.success !== false
            });
            
            return {
                ...result,
                requestId,
                timestamp: new Date().toISOString(),
                duration
            };
            
        } catch (error) {
            const duration = Date.now() - startTime;
            this.log('error', 'API请求处理失败', { 
                requestId,
                method, 
                path, 
                duration,
                error: error.message,
                stack: error.stack
            });
            
            return {
                success: false,
                error: {
                    code: this.getErrorCode(error),
                    message: error.message,
                    type: error.constructor.name,
                    requestId,
                    timestamp: new Date().toISOString(),
                    duration
                }
            };
        }
    }

    /**
     * 获取错误代码
     */
    getErrorCode(error) {
        const message = error.message.toLowerCase();
        
        if (message.includes('签名') || message.includes('安全')) {
            return 'SECURITY_ERROR';
        }
        if (message.includes('限流') || message.includes('rate limit')) {
            return 'RATE_LIMIT_ERROR';
        }
        if (message.includes('重复') || message.includes('duplicate')) {
            return 'DUPLICATE_ERROR';
        }
        if (message.includes('验证') || message.includes('validation')) {
            return 'VALIDATION_ERROR';
        }
        if (message.includes('会话') || message.includes('session')) {
            return 'SESSION_ERROR';
        }
        if (message.includes('网络') || message.includes('network') || message.includes('timeout')) {
            return 'NETWORK_ERROR';
        }
        
        return 'UNKNOWN_ERROR';
    }

    /**
     * 创建文章
     */
    async createArticle(data) {
        // 数据验证
        this.validateArticleData(data);

        // 增强的去重检查
        const duplicationResult = await this.checkDuplication(data);
        if (duplicationResult.isDuplicate) {
            this.log('info', '检测到重复文章，返回已存在的文章ID', { 
                dedupeKey: duplicationResult.dedupeKey,
                existingId: duplicationResult.existingId,
                source: duplicationResult.source
            });
            return {
                success: true,
                data: { id: duplicationResult.existingId },
                message: `文章已存在（来源：${duplicationResult.source}）`,
                isDuplicate: true,
                source: duplicationResult.source
            };
        }

        // 字段映射和清洗
        const mappedData = this.mapAndCleanFields(data);

        // 确保会话有效
        await this.ensureValidSession();

        // 发布文章
        const result = await this.publishArticle(mappedData);

        // 缓存结果用于去重
        if (result.success && result.data.id) {
            this.dedupeCache.set(duplicationResult.dedupeKey, {
                articleId: result.data.id,
                timestamp: Date.now(),
                originalData: data
            });
        }

        return result;
    }

    /**
     * 批量创建文章
     */
    async batchCreateArticles(data) {
        const { articles = [], batchSize = 3, delayBetweenBatches = 3000 } = data;
        
        if (!Array.isArray(articles) || articles.length === 0) {
            throw new Error('articles字段必须是非空数组');
        }

        const results = [];
        const batches = [];
        
        // 分批处理
        for (let i = 0; i < articles.length; i += batchSize) {
            batches.push(articles.slice(i, i + batchSize));
        }

        this.log('info', '开始批量处理文章', {
            totalArticles: articles.length,
            batchCount: batches.length,
            batchSize
        });

        for (let i = 0; i < batches.length; i++) {
            const batch = batches[i];
            const batchResults = [];

            // 串行处理以避免限流冲突
            for (let j = 0; j < batch.length; j++) {
                const article = batch[j];
                const globalIndex = i * batchSize + j;
                
                try {
                    const result = await this.createArticle(article);
                    batchResults.push({
                        index: globalIndex,
                        success: true,
                        data: result
                    });
                    
                    // 文章间小延迟
                    if (j < batch.length - 1) {
                        await this.delay(800);
                    }
                } catch (error) {
                    batchResults.push({
                        index: globalIndex,
                        success: false,
                        error: error.message,
                        originalData: article
                    });
                }
            }

            results.push(...batchResults);

            // 批次间延迟
            if (i < batches.length - 1) {
                await this.delay(delayBetweenBatches);
            }

            this.log('info', `批次 ${i + 1}/${batches.length} 处理完成`, {
                batchSize: batch.length,
                successCount: batchResults.filter(r => r.success).length,
                errorCount: batchResults.filter(r => !r.success).length
            });
        }

        const summary = {
            total: articles.length,
            success: results.filter(r => r.success).length,
            failed: results.filter(r => !r.success).length,
            duplicates: results.filter(r => r.success && r.data && r.data.isDuplicate).length
        };

        return {
            success: true,
            data: {
                summary,
                results
            },
            message: `批量处理完成: 成功${summary.success}篇，失败${summary.failed}篇，重复${summary.duplicates}篇`
        };
    }

    /**
     * 验证请求签名
     */
    validateSignature(data, signature, timestamp) {
        if (!this.config.enableSecurity) {
            return true;
        }
        
        const secretKey = this.config.secretKey;
        if (!secretKey) {
            throw new Error('安全模式已启用但未配置密钥');
        }
        
        // 检查时间戳（防重放攻击）
        const now = Date.now();
        const requestTime = parseInt(timestamp);
        const maxAge = this.config.signatureMaxAge || 300000; // 5分钟
        
        if (Math.abs(now - requestTime) > maxAge) {
            throw new Error('请求时间戳过期');
        }
        
        // 生成期望的签名
        const payload = JSON.stringify(data) + timestamp;
        const expectedSignature = crypto
            .createHmac('sha256', secretKey)
            .update(payload)
            .digest('hex');
        
        if (signature !== expectedSignature) {
            throw new Error('签名验证失败');
        }
        
        return true;
    }

    /**
     * 生成请求签名
     */
    generateSignature(data, timestamp) {
        const secretKey = this.config.secretKey;
        if (!secretKey) {
            return null;
        }
        
        const payload = JSON.stringify(data) + timestamp;
        return crypto
            .createHmac('sha256', secretKey)
            .update(payload)
            .digest('hex');
    }

    /**
     * 更新文章
     */
    async updateArticle(data) {
        if (!data.id) {
            throw new Error('更新文章需要提供文章ID');
        }

        this.validateArticleData(data, false);
        const mappedData = this.mapAndCleanFields(data);
        await this.ensureValidSession();

        return await this.modifyArticle(data.id, mappedData);
    }

    /**
     * 删除文章
     */
    async deleteArticle(data) {
        if (!data.id) {
            throw new Error('删除文章需要提供文章ID');
        }

        await this.ensureValidSession();
        return await this.removeArticle(data.id);
    }

    /**
     * 获取分类列表
     */
    async getCategories() {
        await this.ensureValidSession();
        
        const response = await this.makeRequest({
            service: 'article',
            action: 'type'
        });

        return {
            success: true,
            data: response.info || [],
            message: '获取分类列表成功'
        };
    }

    /**
     * 获取文章列表
     */
    async getArticles(params = {}) {
        await this.ensureValidSession();
        
        const response = await this.makeRequest({
            service: 'article',
            action: 'alist',
            ...params
        });

        return {
            success: true,
            data: response.info || {},
            message: '获取文章列表成功'
        };
    }

    /**
     * 健康检查
     */
    async healthCheck() {
        try {
            await this.ensureValidSession();
            
            const response = await this.makeRequest({
                service: 'article',
                action: 'config'
            });

            return {
                success: true,
                data: {
                    status: 'healthy',
                    timestamp: new Date().toISOString(),
                    session: !!this.sessionId,
                    config: response.info || {}
                },
                message: '系统运行正常'
            };
        } catch (error) {
            return {
                success: false,
                data: {
                    status: 'unhealthy',
                    timestamp: new Date().toISOString(),
                    error: error.message
                },
                message: '系统异常'
            };
        }
    }

    /**
     * 数据验证
     */
    validateArticleData(data, requireContent = true) {
        const errors = [];

        if (!data.title || typeof data.title !== 'string' || data.title.trim() === '') {
            errors.push('标题不能为空');
        }

        if (requireContent && (!data.content || typeof data.content !== 'string' || data.content.trim() === '')) {
            errors.push('内容不能为空');
        }

        if (data.source_url && !this.isValidUrl(data.source_url)) {
            errors.push('来源URL格式无效');
        }

        if (data.image_url && !this.isValidUrl(data.image_url)) {
            errors.push('图片URL格式无效');
        }

        if (errors.length > 0) {
            throw new Error(`数据验证失败: ${errors.join(', ')}`);
        }
    }

    /**
     * URL格式验证
     */
    isValidUrl(string) {
        try {
            new URL(string);
            return true;
        } catch (_) {
            return false;
        }
    }

    /**
     * 生成去重键
     */
    generateDedupeKey(data) {
        if (data.dedupe_key) {
            return data.dedupe_key;
        }
        
        // 使用标题+来源URL生成去重键
        const key = `${data.title || ''}|${data.source_url || ''}`;
        return crypto.createHash('md5').update(key).digest('hex');
    }

    /**
     * 检查内容重复性
     */
    async checkDuplication(data) {
        const dedupeKey = this.generateDedupeKey(data);
        
        // 检查本地缓存
        const cachedResult = this.dedupeCache.get(dedupeKey);
        if (cachedResult) {
            this.log('info', '发现重复内容（本地缓存）', {
                dedupeKey,
                cachedId: cachedResult.articleId,
                title: data.title
            });
            return {
                isDuplicate: true,
                existingId: cachedResult.articleId,
                source: 'cache'
            };
        }
        
        // 检查远程数据库（通过标题搜索）
        try {
            const searchResult = await this.searchExistingArticle(data.title);
            if (searchResult && searchResult.length > 0) {
                // 缓存结果
                this.dedupeCache.set(dedupeKey, {
                    articleId: searchResult[0].id,
                    timestamp: Date.now(),
                    originalData: data
                });
                
                this.log('info', '发现重复内容（远程数据库）', {
                    dedupeKey,
                    existingId: searchResult[0].id,
                    title: data.title
                });
                
                return {
                    isDuplicate: true,
                    existingId: searchResult[0].id,
                    source: 'database'
                };
            }
        } catch (error) {
            this.log('warn', '远程去重检查失败', { error: error.message });
        }
        
        return {
            isDuplicate: false,
            dedupeKey
        };
    }

    /**
     * 搜索已存在的文章
     */
    async searchExistingArticle(title) {
        try {
            await this.ensureValidSession();
            
            const response = await this.makeRequest({
                service: 'article',
                action: 'alist',
                keyword: title.substring(0, 20), // 使用标题前20个字符搜索
                pageSize: 5
            });
            
            if (response && response.state === 100 && response.info && response.info.list) {
                // 精确匹配标题
                return response.info.list.filter(article => 
                    article.title && article.title.trim() === title.trim()
                );
            }
        } catch (error) {
            this.log('warn', '搜索已存在文章失败', { error: error.message });
        }
        
        return [];
    }

    /**
     * 字段映射和清洗
     */
    mapAndCleanFields(data) {
        const mapped = {};

        // 标题处理 - 必填字段
        mapped.title = this.cleanText(data.title || '').substring(0, 60);
        if (!mapped.title) {
            throw new Error('文章标题不能为空');
        }

        // 分类映射 - 必填字段
        mapped.typeid = this.mapCategory(data.category) || 1;

        // 内容处理 - 必填字段
        if (data.content) {
            mapped.body = this.cleanHtmlContent(data.content);
            // 确保内容不为空
            if (!this.cleanText(mapped.body)) {
                mapped.body = mapped.title; // 使用标题作为内容
            }
        } else {
            mapped.body = mapped.title; // 使用标题作为内容
        }

        // 作者处理
        mapped.writer = this.cleanText(data.author || data.writer || 'AI采集').substring(0, 20);

        // 来源处理
        mapped.source = this.cleanText(data.source || data.from || 'API采集').substring(0, 30);

        // 关键词生成和清洗
        mapped.keywords = this.generateKeywords(data.title, data.keywords || data.tags).substring(0, 50);

        // 描述处理
        const description = data.description || data.summary || data.excerpt || '';
        mapped.description = this.cleanText(description).substring(0, 255) || 
                           this.cleanText(mapped.body).substring(0, 255);

        // 缩略图处理
        mapped.litpic = this.validateAndCleanImageUrl(data.image_url || data.litpic || data.thumbnail || '');

        // 发布时间处理
        mapped.pubdate = this.formatPublishDate(data.publish_date || data.pubdate || data.created_at);

        // 权重设置
        mapped.weight = parseInt(data.weight || data.priority || 0);

        // 状态设置
        mapped.arcrank = parseInt(data.status || data.arcrank || 0); // 0=正常，-1=待审核

        // 点击数初始化
        mapped.click = parseInt(data.click || data.views || Math.floor(Math.random() * 100));

        // 其他字段
        if (data.redirect_url || data.redirecturl) {
            mapped.redirecturl = this.validateAndCleanUrl(data.redirect_url || data.redirecturl);
        }

        // 自定义字段映射
        if (data.custom_fields && typeof data.custom_fields === 'object') {
            Object.keys(data.custom_fields).forEach(key => {
                if (key.startsWith('field_')) {
                    mapped[key] = this.cleanText(data.custom_fields[key]);
                }
            });
        }

        this.log('debug', '字段映射完成', {
            originalKeys: Object.keys(data),
            mappedKeys: Object.keys(mapped),
            title: mapped.title
        });

        return mapped;
    }

    /**
     * 验证和清洗图片URL
     */
    validateAndCleanImageUrl(url) {
        if (!url) return '';
        
        // 清理URL
        url = url.trim();
        
        // 验证URL格式
        if (!this.isValidUrl(url)) {
            this.log('warn', '无效的图片URL', { url });
            return '';
        }
        
        // 检查是否为图片格式
        const imageExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'];
        const hasImageExtension = imageExtensions.some(ext => 
            url.toLowerCase().includes(ext)
        );
        
        if (!hasImageExtension && !url.includes('image') && !url.includes('photo')) {
            this.log('warn', '可能不是图片URL', { url });
        }
        
        return url;
    }

    /**
     * 验证和清洗普通URL
     */
    validateAndCleanUrl(url) {
        if (!url) return '';
        
        url = url.trim();
        
        if (!this.isValidUrl(url)) {
            this.log('warn', '无效的URL', { url });
            return '';
        }
        
        return url;
    }

    /**
     * 格式化发布时间
     */
    formatPublishDate(dateInput) {
        if (!dateInput) {
            return Math.floor(Date.now() / 1000); // 当前时间戳
        }
        
        let timestamp;
        
        if (typeof dateInput === 'number') {
            // 已经是时间戳
            timestamp = dateInput > 1000000000000 ? Math.floor(dateInput / 1000) : dateInput;
        } else if (typeof dateInput === 'string') {
            // 字符串日期
            const date = new Date(dateInput);
            if (isNaN(date.getTime())) {
                this.log('warn', '无效的日期格式', { dateInput });
                return Math.floor(Date.now() / 1000);
            }
            timestamp = Math.floor(date.getTime() / 1000);
        } else {
            return Math.floor(Date.now() / 1000);
        }
        
        // 确保时间戳合理（不能是未来时间）
        const now = Math.floor(Date.now() / 1000);
        if (timestamp > now) {
            this.log('warn', '发布时间不能是未来时间', { timestamp, now });
            return now;
        }
        
        return timestamp;
    }

    /**
     * 分类映射
     */
    mapCategory(category) {
        if (!category) return 1;
        
        // 直接数字
        if (typeof category === 'number') {
            return category > 0 ? category : 1;
        }

        // 字符串数字
        if (typeof category === 'string' && /^\d+$/.test(category)) {
            const num = parseInt(category);
            return num > 0 ? num : 1;
        }

        // 标准化分类名称
        const normalizedCategory = this.normalizeCategory(category);
        
        // 精确匹配
        const exactMatch = this.categoryMapping.get(normalizedCategory) || 
                          this.categoryMapping.get(category.toLowerCase()) || 
                          this.categoryMapping.get(category);
        if (exactMatch) {
            this.log('debug', '分类精确匹配', { original: category, normalized: normalizedCategory, mapped: exactMatch });
            return exactMatch;
        }
        
        // 模糊匹配
        const fuzzyMatch = this.findFuzzyCategory(normalizedCategory);
        if (fuzzyMatch) {
            this.log('debug', '分类模糊匹配', { original: category, normalized: normalizedCategory, mapped: fuzzyMatch });
            return fuzzyMatch;
        }
        
        // 关键词匹配
        const keywordMatch = this.findCategoryByKeywords(normalizedCategory);
        if (keywordMatch) {
            this.log('debug', '分类关键词匹配', { original: category, normalized: normalizedCategory, mapped: keywordMatch });
            return keywordMatch;
        }
        
        this.log('warn', '未找到匹配的分类，使用默认分类', { original: category, normalized: normalizedCategory });
        return 1; // 默认分类
    }
    
    /**
     * 标准化分类名称
     */
    normalizeCategory(category) {
        if (!category) return '';
        
        return category.toString()
            .trim()
            .toLowerCase()
            .replace(/[\s\-_]+/g, '') // 移除空格、横线、下划线
            .replace(/[^\u4e00-\u9fa5a-z0-9]/g, ''); // 只保留中文、英文、数字
    }
    
    /**
     * 模糊匹配分类
     */
    findFuzzyCategory(normalizedCategory) {
        for (const [key, value] of this.categoryMapping) {
            if (normalizedCategory.includes(key) || key.includes(normalizedCategory)) {
                return value;
            }
        }
        return null;
    }
    
    /**
     * 通过关键词匹配分类
     */
    findCategoryByKeywords(normalizedCategory) {
        const keywordMap = {
            1: ['科技', 'tech', 'technology', 'ai', '人工智能', '互联网', 'it', '数码', '电子', '软件', '硬件', '编程', '开发'],
            2: ['新闻', 'news', '资讯', '时事', '热点', '头条', '快讯', '报道'],
            3: ['娱乐', 'entertainment', '明星', '电影', '音乐', '综艺', '八卦', '影视', '游戏'],
            4: ['体育', 'sports', '足球', '篮球', '运动', '健身', '比赛', '赛事', '奥运'],
            5: ['财经', 'finance', '经济', '金融', '股票', '投资', '理财', '商业', '创业', '市场'],
            6: ['汽车', 'auto', 'car', '车辆', '驾驶', '交通', '新车', '评测'],
            7: ['房产', 'real estate', '房屋', '楼市', '装修', '家居', '建筑'],
            8: ['教育', 'education', '学习', '培训', '考试', '学校', '知识', '课程'],
            9: ['健康', 'health', '医疗', '养生', '保健', '疾病', '医学', '药品'],
            10: ['旅游', 'travel', '旅行', '景点', '度假', '酒店', '攻略', '出行'],
            11: ['美食', 'food', '餐饮', '菜谱', '烹饪', '小吃', '饮食'],
            12: ['时尚', 'fashion', '服装', '美容', '化妆', '穿搭', '潮流'],
            13: ['文化', 'culture', '艺术', '历史', '传统', '文学', '书籍'],
            14: ['社会', 'society', '民生', '公益', '法律', '政策', '环保']
        };
        
        for (const [categoryId, keywords] of Object.entries(keywordMap)) {
            for (const keyword of keywords) {
                if (normalizedCategory.includes(keyword.toLowerCase()) || 
                    normalizedCategory.includes(this.normalizeCategory(keyword))) {
                    return parseInt(categoryId);
                }
            }
        }
        
        return null;
    }

    /**
     * 清理文本
     */
    cleanText(text) {
        if (!text) return '';
        return text.replace(/<[^>]*>/g, '')
                  .replace(/[\r\n\t]/g, ' ')
                  .replace(/\s+/g, ' ')
                  .trim();
    }

    /**
     * 清理HTML内容
     */
    cleanHtmlContent(html) {
        if (!html) return '';
        
        // 允许的HTML标签白名单
        const allowedTags = ['p', 'br', 'strong', 'b', 'em', 'i', 'u', 'a', 'img', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'];
        const allowedAttrs = ['href', 'src', 'alt', 'title'];
        
        // 简单的HTML清理（生产环境建议使用专业的HTML清理库）
        let cleaned = html;
        
        // 移除script和style标签
        cleaned = cleaned.replace(/<(script|style)[^>]*>.*?<\/\1>/gis, '');
        
        // 移除危险属性
        cleaned = cleaned.replace(/\s(on\w+|javascript:|data:)=[^>\s]*/gi, '');
        
        return cleaned;
    }

    /**
     * 生成关键词
     */
    generateKeywords(title, existingKeywords) {
        if (existingKeywords) {
            return existingKeywords;
        }
        
        if (!title) return '';
        
        // 简单的关键词提取
        const keywords = title.split(/[\s,，。！？；：]/)
                             .filter(word => word.length > 1)
                             .slice(0, 5)
                             .join(',');
        
        return keywords;
    }

    /**
     * 限流检查
     */
    async checkRateLimit(clientId) {
        const now = Date.now();
        const windowMs = 60000; // 1分钟窗口
        
        if (!this.rateLimitCounter.has(clientId)) {
            this.rateLimitCounter.set(clientId, {
                count: 0,
                timestamp: now,
                resetTime: now + windowMs
            });
        }

        const counter = this.rateLimitCounter.get(clientId);
        
        // 重置计数器
        if (now >= counter.resetTime) {
            counter.count = 0;
            counter.timestamp = now;
            counter.resetTime = now + windowMs;
        }

        // 检查限流
        if (counter.count >= this.config.rateLimit) {
            const waitTime = counter.resetTime - now;
            throw new Error(`请求频率过高，请等待 ${Math.ceil(waitTime / 1000)} 秒后重试`);
        }

        counter.count++;
    }

    /**
     * 签名验证
     */
    verifySignature(headers) {
        const signature = headers['x-signature'];
        const timestamp = headers['x-timestamp'];
        const nonce = headers['x-nonce'];
        
        if (!signature || !timestamp || !nonce) {
            return false;
        }

        // 检查时间戳（5分钟内有效）
        const now = Date.now();
        if (Math.abs(now - parseInt(timestamp)) > 300000) {
            return false;
        }

        // 验证签名
        const data = `${timestamp}${nonce}${this.config.secretKey}`;
        const expectedSignature = crypto.createHash('sha256').update(data).digest('hex');
        
        return signature === expectedSignature;
    }

    /**
     * 确保会话有效
     */
    async ensureValidSession() {
        const now = Date.now();
        
        // 检查会话是否过期（提前5分钟刷新）
        if (!this.sessionId || !this.sessionExpiry || now >= this.sessionExpiry - 300000) {
            await this.refreshSession();
        }
        
        // 验证会话有效性
        if (!await this.validateSession()) {
            this.log('warn', '会话验证失败，尝试重新获取');
            await this.refreshSession();
        }
    }

    /**
     * 验证会话有效性
     */
    async validateSession() {
        if (!this.sessionId) return false;
        
        try {
            // 通过获取基础配置来验证会话
            const response = await this.makeRequest({
                service: 'article',
                action: 'config'
            });
            
            return response && response.state === 100;
        } catch (error) {
            this.log('warn', '会话验证请求失败', { error: error.message });
            return false;
        }
    }

    /**
     * 刷新会话
     */
    async refreshSession() {
        try {
            // 优先级：环境变量 > 配置文件 > Cookie文件 > 默认值
            let sessionId = this.getSessionFromMultipleSources();
            
            if (!sessionId) {
                throw new Error('无法获取有效的会话ID');
            }
            
            this.sessionId = sessionId;
            this.sessionExpiry = Date.now() + 3600000; // 1小时后过期
            
            // 验证新会话是否有效
            const isValid = await this.validateSession();
            if (!isValid) {
                throw new Error('获取的会话ID无效');
            }
            
            this.log('info', '会话刷新成功', { 
                sessionId: sessionId.substring(0, 8) + '...',
                expiry: new Date(this.sessionExpiry).toISOString()
            });
        } catch (error) {
            this.log('error', '会话刷新失败', { error: error.message });
            throw new Error('会话管理失败: ' + error.message);
        }
    }

    /**
     * 从多个来源获取会话ID
     */
    getSessionFromMultipleSources() {
        // 1. 环境变量
        if (process.env.HUONIAO_PHPSESSID) {
            this.log('info', '从环境变量获取会话ID');
            return process.env.HUONIAO_PHPSESSID;
        }
        
        // 2. 配置对象
        if (this.config.sessionId) {
            this.log('info', '从配置对象获取会话ID');
            return this.config.sessionId;
        }
        
        // 3. 尝试从Cookie文件读取
        try {
            const cookieData = this.readCookieFile();
            if (cookieData && cookieData.PHPSESSID) {
                this.log('info', '从Cookie文件获取会话ID');
                return cookieData.PHPSESSID;
            }
        } catch (error) {
            this.log('warn', '读取Cookie文件失败', { error: error.message });
        }
        
        // 4. 默认会话ID（用于测试）
        this.log('warn', '使用默认会话ID，建议配置有效的会话');
        return 'e0rit6uelaapo8eqsgb7asmq83';
    }

    /**
     * 读取Cookie文件
     */
    readCookieFile() {
        try {
            const fs = require('fs');
            const path = require('path');
            
            // 查找Cookie文件
            const cookieFiles = [
                'BestCookier20250818-141527-hawaiihub.net.json',
                'cookies.json',
                'hawaiihub_cookies.json'
            ];
            
            for (const filename of cookieFiles) {
                const filepath = path.join(process.cwd(), filename);
                if (fs.existsSync(filepath)) {
                    const content = fs.readFileSync(filepath, 'utf8');
                    const cookies = JSON.parse(content);
                    
                    // 查找PHPSESSID
                    for (const cookie of cookies) {
                        if (cookie.name === 'PHPSESSID') {
                            return { PHPSESSID: cookie.value };
                        }
                    }
                }
            }
        } catch (error) {
            this.log('debug', 'Cookie文件读取异常', { error: error.message });
        }
        
        return null;
    }

    /**
     * 自动会话维护
     */
    startSessionMaintenance() {
        // 每30分钟检查一次会话状态
        setInterval(async () => {
            try {
                await this.ensureValidSession();
            } catch (error) {
                this.log('error', '自动会话维护失败', { error: error.message });
            }
        }, 1800000); // 30分钟
        
        this.log('info', '自动会话维护已启动');
    }

    /**
     * 发布文章到火鸟系统
     */
    async publishArticle(data) {
        const response = await this.makeRequest({
            service: 'article',
            action: 'put',
            ...data
        });

        if (response.state === 100) {
            this.log('info', '文章发布成功', { 
                title: data.title,
                articleId: response.info?.id 
            });
            
            return {
                success: true,
                data: { id: response.info?.id },
                message: '文章发布成功'
            };
        } else {
            throw new Error(response.msg || '文章发布失败');
        }
    }

    /**
     * 修改文章
     */
    async modifyArticle(id, data) {
        const response = await this.makeRequest({
            service: 'article',
            action: 'edit',
            id: id,
            ...data
        });

        if (response.state === 100) {
            return {
                success: true,
                data: { id },
                message: '文章更新成功'
            };
        } else {
            throw new Error(response.msg || '文章更新失败');
        }
    }

    /**
     * 删除文章
     */
    async removeArticle(id) {
        const response = await this.makeRequest({
            service: 'article',
            action: 'del',
            id: id
        });

        if (response.state === 100) {
            return {
                success: true,
                data: { id },
                message: '文章删除成功'
            };
        } else {
            throw new Error(response.msg || '文章删除失败');
        }
    }

    /**
     * 检查限流状态
     */
    async checkRateLimit() {
        const now = Date.now();
        const windowStart = now - (this.config.rateLimitWindow || 60000); // 默认1分钟窗口
        
        // 初始化限流计数器
        if (!this.rateLimitCounter) {
            this.rateLimitCounter = [];
        }
        
        // 清理过期的请求记录
        this.rateLimitCounter = this.rateLimitCounter.filter(timestamp => timestamp > windowStart);
        
        // 检查是否超过限制
        const maxRequests = this.config.rateLimitMax || 10;
        if (this.rateLimitCounter.length >= maxRequests) {
            const oldestRequest = Math.min(...this.rateLimitCounter);
            const waitTime = oldestRequest + (this.config.rateLimitWindow || 60000) - now;
            
            if (waitTime > 0) {
                this.log('warn', '触发限流，等待中', { 
                    currentRequests: this.rateLimitCounter.length,
                    maxRequests: maxRequests,
                    waitTime 
                });
                await this.delay(waitTime);
                return this.checkRateLimit(); // 递归检查
            }
        }
        
        // 记录当前请求
        this.rateLimitCounter.push(now);
        return true;
    }

    /**
     * 发起HTTP请求
     */
    async makeRequest(params, retryCount = 0) {
        // 限流检查
        await this.checkRateLimit();
        
        try {
            const url = `${this.config.baseUrl}${this.config.apiPath}`;
            const headers = {
                'Cookie': `PHPSESSID=${this.sessionId}`,
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'HuoNiao-Gateway/2.0.0'
            };

            const response = await axios.post(url, new URLSearchParams(params), {
                headers,
                timeout: this.config.timeout
            });

            if (response.data && typeof response.data === 'object') {
                return response.data;
            } else {
                throw new Error('响应格式错误');
            }
        } catch (error) {
            // 重试机制
            if (retryCount < this.config.maxRetries) {
                // 指数退避策略
                const baseDelay = this.config.retryDelay || 1000;
                const maxDelay = this.config.retryMaxDelay || 30000;
                const delay = Math.min(baseDelay * Math.pow(2, retryCount), maxDelay);
                
                this.log('warn', `请求失败，${delay}ms后重试`, { 
                    retryCount: retryCount + 1,
                    error: error.message 
                });
                
                await this.delay(delay);
                return this.makeRequest(params, retryCount + 1);
            }

            this.log('error', '请求最终失败', { 
                params,
                retryCount,
                error: error.message 
            });
            
            throw error;
        }
    }

    /**
     * 延迟函数
     */
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * 格式化错误
     */
    formatError(error) {
        const errorMap = {
            '签名验证失败': { code: 'AUTH_FAILED', message: '身份验证失败' },
            '请求频率过高': { code: 'RATE_LIMIT_EXCEEDED', message: '请求过于频繁，请稍后重试' },
            '数据验证失败': { code: 'VALIDATION_ERROR', message: '提交的数据格式不正确' },
            '会话管理失败': { code: 'SESSION_ERROR', message: '会话已过期，请重新认证' }
        };

        const mapped = errorMap[error.message] || {
            code: 'UNKNOWN_ERROR',
            message: error.message || '未知错误'
        };

        return {
            success: false,
            error: {
                code: mapped.code,
                message: mapped.message,
                timestamp: new Date().toISOString()
            }
        };
    }

    /**
     * 日志记录
     */
    log(level, message, data = {}) {
        if (!this.config.enableLogging) return;

        const logEntry = {
            timestamp: new Date().toISOString(),
            level,
            message,
            data,
            gateway: 'HuoNiao-Gateway'
        };

        console.log(JSON.stringify(logEntry));
    }
}

// 导出类和实例
module.exports = {
    HuoNiaoAPIGateway,
    HuoNiaoAPIClient // 保持向后兼容
};

// n8n使用示例
if (typeof $input !== 'undefined') {
    // n8n环境中的使用示例
    const gateway = new HuoNiaoAPIGateway({
        baseUrl: 'https://hawaiihub.net',
        secretKey: process.env.HUONIAO_SECRET_KEY || 'huoniao_gateway_secret_2025',
        enableSecurity: true,
        enableLogging: true
    });

    // 示例：创建文章
    const articleData = $input.first().json;
    const result = await gateway.handleRequest('POST', '/v1/articles', articleData, {
        'x-signature': 'your_signature',
        'x-timestamp': Date.now().toString(),
        'x-nonce': Math.random().toString(36),
        'x-client-id': 'n8n_workflow'
    });

    return result;
}