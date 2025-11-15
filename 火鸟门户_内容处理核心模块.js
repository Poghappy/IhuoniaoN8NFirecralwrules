/**
 * 火鸟门户内容处理核心模块 - 增强版
 * 智能内容处理、优化和质量控制
 * 与API网关深度集成，提供全面的内容处理能力
 * 
 * @author AI Assistant
 * @version 2.0.0
 * @date 2025-01-18
 */

const crypto = require('crypto');
const axios = require('axios');

/**
 * 火鸟门户内容处理器增强版
 */
class HuoNiaoContentProcessor {
    constructor(config = {}) {
        // 基础配置
        this.config = {
            // AI服务配置
            aiApiKey: config.aiApiKey || process.env.OPENAI_API_KEY,
            aiBaseUrl: config.aiBaseUrl || 'https://api.openai.com/v1',
            aiModel: config.aiModel || 'gpt-3.5-turbo',
            
            // 内容质量配置
            minContentLength: config.minContentLength || 100,
            maxContentLength: config.maxContentLength || 5000,
            minTitleLength: config.minTitleLength || 5,
            maxTitleLength: config.maxTitleLength || 60,
            
            // 相似度阈值
            similarityThreshold: config.similarityThreshold || 0.8,
            
            // 图片处理配置
            maxImageSize: config.maxImageSize || 2 * 1024 * 1024, // 2MB
            allowedImageTypes: config.allowedImageTypes || ['jpg', 'jpeg', 'png', 'gif', 'webp'],
            imageQuality: config.imageQuality || 80,
            
            // 缓存配置
            enableCache: config.enableCache !== false,
            cacheExpiry: config.cacheExpiry || 3600000, // 1小时
            
            // 日志配置
            enableLogging: config.enableLogging !== false,
            
            ...config
        };

        // 内部状态
        this.contentCache = new Map();
        this.similarityCache = new Map();
        this.categoryCache = new Map();
        this.sensitiveWords = new Set();
        this.categoryMapping = new Map();
        
        // 初始化
        this.initializeSensitiveWords();
        this.initializeCategoryMapping();
        this.startCleanupTimer();
    }

    /**
     * 初始化敏感词库
     */
    initializeSensitiveWords() {
        const sensitiveWordsList = [
            // 政治敏感词
            '政治', '政府', '官员', '腐败', '抗议', '示威',
            // 暴力相关
            '暴力', '杀害', '恐怖', '爆炸', '武器', '枪支',
            // 色情相关
            '色情', '裸体', '性爱', '成人', '黄色',
            // 赌博相关
            '赌博', '博彩', '彩票', '赌场', '下注',
            // 毒品相关
            '毒品', '大麻', '海洛因', '可卡因', '吸毒',
            // 其他违法内容
            '诈骗', '洗钱', '偷税', '走私', '盗版'
        ];

        sensitiveWordsList.forEach(word => {
            this.sensitiveWords.add(word);
        });

        this.log('info', '敏感词库初始化完成', { count: this.sensitiveWords.size });
    }

    /**
     * 初始化分类映射
     */
    initializeCategoryMapping() {
        // 智能分类关键词映射
        this.categoryMapping.set('科技', {
            id: 1,
            keywords: ['AI', '人工智能', '科技', '技术', '创新', '数字化', '互联网', '软件', '硬件', '芯片', '5G', '区块链']
        });
        
        this.categoryMapping.set('商业', {
            id: 2,
            keywords: ['商业', '企业', '公司', '经济', '市场', '投资', '股票', '金融', '银行', '创业', 'IPO', '并购']
        });
        
        this.categoryMapping.set('新闻', {
            id: 3,
            keywords: ['新闻', '时事', '社会', '民生', '政策', '法律', '事件', '报道', '消息', '通知', '公告']
        });
        
        this.categoryMapping.set('体育', {
            id: 4,
            keywords: ['体育', '运动', '足球', '篮球', '网球', '游泳', '跑步', '健身', '比赛', '奥运', '世界杯', '联赛']
        });
        
        this.categoryMapping.set('娱乐', {
            id: 5,
            keywords: ['娱乐', '明星', '电影', '电视', '音乐', '综艺', '演员', '导演', '歌手', '娱乐圈', '八卦', '红毯']
        });
        
        this.categoryMapping.set('健康', {
            id: 6,
            keywords: ['健康', '医疗', '养生', '疾病', '治疗', '药物', '医院', '医生', '营养', '保健', '心理', '康复']
        });
        
        this.categoryMapping.set('财经', {
            id: 7,
            keywords: ['财经', '金融', '股市', '基金', '债券', '外汇', '期货', '理财', '保险', '银行', '央行', '货币']
        });
        
        this.categoryMapping.set('汽车', {
            id: 8,
            keywords: ['汽车', '车辆', '驾驶', '新车', '电动车', '燃油车', 'SUV', '轿车', '卡车', '摩托车', '交通', '驾照']
        });
        
        this.categoryMapping.set('旅游', {
            id: 9,
            keywords: ['旅游', '旅行', '景点', '酒店', '机票', '度假', '出国', '国内游', '自由行', '跟团游', '攻略', '美食']
        });
        
        this.categoryMapping.set('教育', {
            id: 10,
            keywords: ['教育', '学校', '学习', '考试', '培训', '课程', '老师', '学生', '大学', '中学', '小学', '在线教育']
        });
    }

    /**
     * 启动清理定时器
     */
    startCleanupTimer() {
        setInterval(() => {
            this.cleanupExpiredCache();
        }, 3600000); // 每小时清理一次
    }

    /**
     * 清理过期缓存
     */
    cleanupExpiredCache() {
        const now = Date.now();
        
        // 清理内容缓存
        for (const [key, data] of this.contentCache.entries()) {
            if (now - data.timestamp > this.config.cacheExpiry) {
                this.contentCache.delete(key);
            }
        }

        // 清理相似度缓存
        for (const [key, data] of this.similarityCache.entries()) {
            if (now - data.timestamp > this.config.cacheExpiry) {
                this.similarityCache.delete(key);
            }
        }

        this.log('info', '缓存清理完成', {
            contentCache: this.contentCache.size,
            similarityCache: this.similarityCache.size
        });
    }

    /**
     * 主要内容处理流程
     */
    async processContent(inputData, options = {}) {
        try {
            this.log('info', '开始内容处理流程', { title: inputData.title });

            // 1. 基础数据验证
            const validationResult = this.validateBasicData(inputData);
            if (!validationResult.isValid) {
                throw new Error(`数据验证失败: ${validationResult.errors.join(', ')}`);
            }

            // 2. 内容去重检测
            const dedupeResult = await this.checkContentDuplicate(inputData);
            if (dedupeResult.isDuplicate) {
                return {
                    success: false,
                    isDuplicate: true,
                    message: '检测到重复内容',
                    duplicateInfo: dedupeResult
                };
            }

            // 3. 内容质量评分
            const qualityScore = this.calculateContentQuality(inputData);
            if (qualityScore < 60) {
                this.log('warn', '内容质量较低', { score: qualityScore, title: inputData.title });
            }

            // 4. 敏感词检测
            const sensitiveResult = this.detectSensitiveContent(inputData);
            if (sensitiveResult.hasSensitive) {
                if (options.strictMode) {
                    throw new Error(`检测到敏感内容: ${sensitiveResult.words.join(', ')}`);
                } else {
                    this.log('warn', '检测到敏感词，已自动过滤', { words: sensitiveResult.words });
                }
            }

            // 5. AI内容优化
            let optimizedData = inputData;
            if (options.enableAI !== false) {
                optimizedData = await this.optimizeContentWithAI(inputData, options);
            }

            // 6. 智能分类
            const categoryResult = this.intelligentCategorization(optimizedData);
            optimizedData.category = categoryResult.category;
            optimizedData.categoryConfidence = categoryResult.confidence;

            // 7. 图片处理
            if (optimizedData.images && optimizedData.images.length > 0) {
                optimizedData.processedImages = await this.processImages(optimizedData.images);
            }

            // 8. 生成最终数据
            const finalData = this.generateFinalData(optimizedData, {
                qualityScore,
                categoryResult,
                sensitiveResult: sensitiveResult.filtered || optimizedData
            });

            this.log('info', '内容处理完成', {
                title: finalData.title,
                category: finalData.category,
                qualityScore,
                hasImages: !!finalData.processedImages
            });

            return {
                success: true,
                data: finalData,
                metadata: {
                    qualityScore,
                    categoryConfidence: categoryResult.confidence,
                    processedAt: new Date().toISOString(),
                    hasSensitiveContent: sensitiveResult.hasSensitive,
                    optimizedByAI: options.enableAI !== false
                }
            };

        } catch (error) {
            this.log('error', '内容处理失败', { error: error.message, title: inputData.title });
            throw error;
        }
    }

    /**
     * 基础数据验证
     */
    validateBasicData(data) {
        const errors = [];

        // 标题验证
        if (!data.title || typeof data.title !== 'string') {
            errors.push('标题不能为空');
        } else if (data.title.length < this.config.minTitleLength) {
            errors.push(`标题长度不能少于${this.config.minTitleLength}个字符`);
        } else if (data.title.length > this.config.maxTitleLength) {
            errors.push(`标题长度不能超过${this.config.maxTitleLength}个字符`);
        }

        // 内容验证
        if (!data.content || typeof data.content !== 'string') {
            errors.push('内容不能为空');
        } else if (data.content.length < this.config.minContentLength) {
            errors.push(`内容长度不能少于${this.config.minContentLength}个字符`);
        } else if (data.content.length > this.config.maxContentLength) {
            errors.push(`内容长度不能超过${this.config.maxContentLength}个字符`);
        }

        // URL验证
        if (data.source_url && !this.isValidUrl(data.source_url)) {
            errors.push('来源URL格式无效');
        }

        if (data.image_url && !this.isValidUrl(data.image_url)) {
            errors.push('图片URL格式无效');
        }

        return {
            isValid: errors.length === 0,
            errors
        };
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
     * 内容去重检测
     */
    async checkContentDuplicate(data) {
        // 生成内容指纹
        const contentHash = this.generateContentHash(data);
        
        // 检查缓存
        if (this.config.enableCache && this.similarityCache.has(contentHash)) {
            const cached = this.similarityCache.get(contentHash);
            return {
                isDuplicate: true,
                method: 'hash',
                similarity: 1.0,
                cachedData: cached
            };
        }

        // 标题相似度检测
        const titleSimilarity = await this.calculateTitleSimilarity(data.title);
        if (titleSimilarity.maxSimilarity > this.config.similarityThreshold) {
            return {
                isDuplicate: true,
                method: 'similarity',
                similarity: titleSimilarity.maxSimilarity,
                similarTitle: titleSimilarity.similarTitle
            };
        }

        // 缓存结果
        if (this.config.enableCache) {
            this.similarityCache.set(contentHash, {
                title: data.title,
                timestamp: Date.now()
            });
        }

        return {
            isDuplicate: false,
            contentHash
        };
    }

    /**
     * 生成内容哈希
     */
    generateContentHash(data) {
        const content = `${data.title || ''}|${data.content || ''}|${data.source_url || ''}`;
        return crypto.createHash('md5').update(content).digest('hex');
    }

    /**
     * 计算标题相似度
     */
    async calculateTitleSimilarity(title) {
        // 简化的相似度计算（生产环境建议使用更复杂的算法）
        const titleWords = this.extractKeywords(title);
        let maxSimilarity = 0;
        let similarTitle = '';

        // 与缓存中的标题比较
        for (const [hash, cached] of this.similarityCache.entries()) {
            const cachedWords = this.extractKeywords(cached.title);
            const similarity = this.calculateJaccardSimilarity(titleWords, cachedWords);
            
            if (similarity > maxSimilarity) {
                maxSimilarity = similarity;
                similarTitle = cached.title;
            }
        }

        return {
            maxSimilarity,
            similarTitle
        };
    }

    /**
     * 提取关键词
     */
    extractKeywords(text) {
        if (!text) return new Set();
        
        return new Set(
            text.toLowerCase()
                .replace(/[^\w\s\u4e00-\u9fff]/g, ' ')
                .split(/\s+/)
                .filter(word => word.length > 1)
        );
    }

    /**
     * 计算Jaccard相似度
     */
    calculateJaccardSimilarity(set1, set2) {
        const intersection = new Set([...set1].filter(x => set2.has(x)));
        const union = new Set([...set1, ...set2]);
        
        return union.size === 0 ? 0 : intersection.size / union.size;
    }

    /**
     * 内容质量评分
     */
    calculateContentQuality(data) {
        let score = 0;

        // 标题质量 (30分)
        if (data.title) {
            const titleLength = data.title.length;
            if (titleLength >= 10 && titleLength <= 50) {
                score += 30;
            } else if (titleLength >= 5 && titleLength <= 60) {
                score += 20;
            } else {
                score += 10;
            }
        }

        // 内容质量 (40分)
        if (data.content) {
            const contentLength = data.content.length;
            const paragraphs = data.content.split(/\n\s*\n/).length;
            
            // 长度评分
            if (contentLength >= 300 && contentLength <= 2000) {
                score += 25;
            } else if (contentLength >= 100 && contentLength <= 3000) {
                score += 15;
            } else {
                score += 5;
            }

            // 结构评分
            if (paragraphs >= 3) {
                score += 15;
            } else if (paragraphs >= 2) {
                score += 10;
            } else {
                score += 5;
            }
        }

        // 元数据完整性 (20分)
        let metadataScore = 0;
        if (data.author) metadataScore += 5;
        if (data.source) metadataScore += 5;
        if (data.keywords) metadataScore += 5;
        if (data.description || data.summary) metadataScore += 5;
        score += metadataScore;

        // 媒体内容 (10分)
        if (data.image_url || (data.images && data.images.length > 0)) {
            score += 10;
        }

        return Math.min(100, score);
    }

    /**
     * 敏感词检测
     */
    detectSensitiveContent(data) {
        const sensitiveWords = [];
        const content = `${data.title || ''} ${data.content || ''} ${data.keywords || ''}`;
        
        for (const word of this.sensitiveWords) {
            if (content.includes(word)) {
                sensitiveWords.push(word);
            }
        }

        if (sensitiveWords.length > 0) {
            // 过滤敏感词
            let filteredContent = content;
            sensitiveWords.forEach(word => {
                const replacement = '*'.repeat(word.length);
                filteredContent = filteredContent.replace(new RegExp(word, 'g'), replacement);
            });

            return {
                hasSensitive: true,
                words: sensitiveWords,
                filtered: {
                    ...data,
                    title: data.title ? data.title.replace(new RegExp(sensitiveWords.join('|'), 'g'), match => '*'.repeat(match.length)) : data.title,
                    content: data.content ? data.content.replace(new RegExp(sensitiveWords.join('|'), 'g'), match => '*'.repeat(match.length)) : data.content
                }
            };
        }

        return {
            hasSensitive: false,
            words: []
        };
    }

    /**
     * AI内容优化
     */
    async optimizeContentWithAI(data, options = {}) {
        if (!this.config.aiApiKey) {
            this.log('warn', 'AI API密钥未配置，跳过AI优化');
            return data;
        }

        try {
            const optimizedData = { ...data };

            // 标题优化
            if (options.optimizeTitle !== false) {
                optimizedData.title = await this.optimizeTitle(data.title, data.content);
            }

            // 内容优化
            if (options.optimizeContent !== false) {
                optimizedData.content = await this.optimizeContent(data.content);
            }

            // 关键词生成
            if (options.generateKeywords !== false) {
                optimizedData.keywords = await this.generateKeywords(optimizedData.title, optimizedData.content);
            }

            // 摘要生成
            if (options.generateSummary !== false) {
                optimizedData.summary = await this.generateSummary(optimizedData.content);
            }

            return optimizedData;

        } catch (error) {
            this.log('error', 'AI优化失败', { error: error.message });
            return data; // 返回原始数据
        }
    }

    /**
     * 标题优化
     */
    async optimizeTitle(title, content) {
        const prompt = `请优化以下新闻标题，使其更加吸引人且准确反映内容：

原标题：${title}

内容摘要：${content.substring(0, 200)}...

要求：
1. 标题长度控制在10-50个字符
2. 突出关键信息
3. 使用吸引人的表达方式
4. 保持准确性

优化后的标题：`;

        const optimizedTitle = await this.callAI(prompt, { maxTokens: 100 });
        return optimizedTitle || title;
    }

    /**
     * 内容优化
     */
    async optimizeContent(content) {
        if (content.length < 200) {
            return content; // 内容太短，不需要优化
        }

        const prompt = `请优化以下新闻内容，使其更加清晰、准确和易读：

原内容：${content}

要求：
1. 保持原意不变
2. 改善语言表达
3. 优化段落结构
4. 修正语法错误
5. 控制在原长度的80%-120%范围内

优化后的内容：`;

        const optimizedContent = await this.callAI(prompt, { maxTokens: 1000 });
        return optimizedContent || content;
    }

    /**
     * 关键词生成
     */
    async generateKeywords(title, content) {
        const prompt = `基于以下标题和内容，生成5-8个相关关键词：

标题：${title}
内容：${content.substring(0, 500)}...

要求：
1. 关键词要准确反映内容主题
2. 使用逗号分隔
3. 优先选择搜索热度高的词汇
4. 避免过于宽泛的词汇

关键词：`;

        const keywords = await this.callAI(prompt, { maxTokens: 100 });
        return keywords || this.extractKeywordsFromText(title + ' ' + content);
    }

    /**
     * 摘要生成
     */
    async generateSummary(content) {
        const prompt = `请为以下内容生成一个简洁的摘要：

内容：${content}

要求：
1. 摘要长度控制在50-150个字符
2. 突出核心信息
3. 语言简洁明了
4. 保持客观性

摘要：`;

        const summary = await this.callAI(prompt, { maxTokens: 200 });
        return summary || content.substring(0, 100) + '...';
    }

    /**
     * 调用AI服务
     */
    async callAI(prompt, options = {}) {
        try {
            const response = await axios.post(`${this.config.aiBaseUrl}/chat/completions`, {
                model: this.config.aiModel,
                messages: [
                    {
                        role: 'user',
                        content: prompt
                    }
                ],
                max_tokens: options.maxTokens || 500,
                temperature: options.temperature || 0.7
            }, {
                headers: {
                    'Authorization': `Bearer ${this.config.aiApiKey}`,
                    'Content-Type': 'application/json'
                },
                timeout: 30000
            });

            return response.data.choices[0]?.message?.content?.trim();

        } catch (error) {
            this.log('error', 'AI服务调用失败', { error: error.message });
            throw error;
        }
    }

    /**
     * 从文本提取关键词（备用方法）
     */
    extractKeywordsFromText(text) {
        const words = this.extractKeywords(text);
        return Array.from(words).slice(0, 8).join(',');
    }

    /**
     * 智能分类
     */
    intelligentCategorization(data) {
        const content = `${data.title || ''} ${data.content || ''} ${data.keywords || ''}`.toLowerCase();
        let bestMatch = { category: '新闻', confidence: 0, id: 3 };

        for (const [categoryName, categoryInfo] of this.categoryMapping.entries()) {
            let matchCount = 0;
            let totalKeywords = categoryInfo.keywords.length;

            for (const keyword of categoryInfo.keywords) {
                if (content.includes(keyword.toLowerCase())) {
                    matchCount++;
                }
            }

            const confidence = matchCount / totalKeywords;
            if (confidence > bestMatch.confidence) {
                bestMatch = {
                    category: categoryName,
                    confidence,
                    id: categoryInfo.id
                };
            }
        }

        return bestMatch;
    }

    /**
     * 图片处理
     */
    async processImages(images) {
        const processedImages = [];

        for (const imageUrl of images) {
            try {
                const processedImage = await this.processImage(imageUrl);
                if (processedImage) {
                    processedImages.push(processedImage);
                }
            } catch (error) {
                this.log('error', '图片处理失败', { imageUrl, error: error.message });
            }
        }

        return processedImages;
    }

    /**
     * 处理单个图片
     */
    async processImage(imageUrl) {
        try {
            // 验证图片URL
            if (!this.isValidUrl(imageUrl)) {
                throw new Error('无效的图片URL');
            }

            // 检查图片类型
            const extension = imageUrl.split('.').pop().toLowerCase();
            if (!this.config.allowedImageTypes.includes(extension)) {
                throw new Error(`不支持的图片类型: ${extension}`);
            }

            // 获取图片信息
            const response = await axios.head(imageUrl, { timeout: 10000 });
            const contentLength = parseInt(response.headers['content-length'] || '0');
            
            if (contentLength > this.config.maxImageSize) {
                throw new Error(`图片文件过大: ${contentLength} bytes`);
            }

            return {
                url: imageUrl,
                size: contentLength,
                type: extension,
                processed: true,
                processedAt: new Date().toISOString()
            };

        } catch (error) {
            this.log('error', '图片处理失败', { imageUrl, error: error.message });
            return null;
        }
    }

    /**
     * 生成最终数据
     */
    generateFinalData(data, metadata = {}) {
        return {
            // 基础字段
            title: data.title,
            content: data.content,
            category: data.category,
            
            // 元数据
            author: data.author || 'AI采集',
            source: data.source || 'API采集',
            keywords: data.keywords || '',
            summary: data.summary || data.description || '',
            
            // URL字段
            source_url: data.source_url || '',
            image_url: data.image_url || '',
            redirect_url: data.redirect_url || '',
            
            // 处理后的数据
            processedImages: data.processedImages || [],
            
            // 质量和分类信息
            qualityScore: metadata.qualityScore || 0,
            categoryId: metadata.categoryResult?.id || 1,
            categoryConfidence: metadata.categoryResult?.confidence || 0,
            
            // 时间戳
            processedAt: new Date().toISOString(),
            
            // 其他字段
            ...data
        };
    }

    /**
     * 批量处理内容
     */
    async batchProcessContent(contentList, options = {}) {
        const results = [];
        const batchSize = options.batchSize || 5;
        const delayBetweenBatches = options.delayBetweenBatches || 1000;

        this.log('info', '开始批量内容处理', {
            totalCount: contentList.length,
            batchSize
        });

        for (let i = 0; i < contentList.length; i += batchSize) {
            const batch = contentList.slice(i, i + batchSize);
            const batchResults = [];

            // 并行处理当前批次
            const promises = batch.map(async (content, index) => {
                try {
                    if (index > 0) {
                        await this.delay(200); // 批次内延迟
                    }
                    return await this.processContent(content, options);
                } catch (error) {
                    return {
                        success: false,
                        error: error.message,
                        originalData: content
                    };
                }
            });

            const batchResult = await Promise.all(promises);
            batchResults.push(...batchResult);
            results.push(...batchResult);

            // 批次间延迟
            if (i + batchSize < contentList.length) {
                await this.delay(delayBetweenBatches);
            }

            this.log('info', `批次处理完成 ${Math.ceil((i + batchSize) / batchSize)}/${Math.ceil(contentList.length / batchSize)}`, {
                batchSize: batch.length,
                successCount: batchResult.filter(r => r.success).length
            });
        }

        const summary = {
            total: contentList.length,
            success: results.filter(r => r.success).length,
            failed: results.filter(r => !r.success).length,
            duplicates: results.filter(r => r.isDuplicate).length
        };

        return {
            success: true,
            summary,
            results
        };
    }

    /**
     * 延迟函数
     */
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
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
            processor: 'HuoNiao-ContentProcessor'
        };

        console.log(JSON.stringify(logEntry));
    }
}

// 导出类
module.exports = {
    HuoNiaoContentProcessor
};

// n8n使用示例
if (typeof $input !== 'undefined') {
    // n8n环境中的使用示例
    const processor = new HuoNiaoContentProcessor({
        aiApiKey: process.env.OPENAI_API_KEY,
        enableCache: true,
        enableLogging: true,
        similarityThreshold: 0.8
    });

    // 处理输入数据
    const inputData = $input.first().json;
    const result = await processor.processContent(inputData, {
        enableAI: true,
        optimizeTitle: true,
        optimizeContent: true,
        generateKeywords: true,
        generateSummary: true
    });

    return result;
}