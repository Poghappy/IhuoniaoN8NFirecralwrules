<?php
/**
 * NewsAPI 服务类
 * 用于对接 NewsAPI.org 获取新闻数据
 *
 * @version        2025-07-21
 * @package        HuoNiao.Plugins.NewsAPI
 * @copyright      Copyright (c) 2025, HuoNiao, Inc.
 */

if(!defined('HUONIAOINC')) exit('Request Error!');

class NewsAPIService {
    
    private $apiKey;
    private $baseUrl = 'https://newsapi.org/v2/';
    private $dsql;
    
    public function __construct($apiKey, $dsql) {
        $this->apiKey = $apiKey;
        $this->dsql = $dsql;
    }
    
    /**
     * 获取头条新闻
     * @param array $params 参数数组
     * @return array
     */
    public function getTopHeadlines($params = []) {
        $defaultParams = [
            'country' => 'us',
            'pageSize' => 20,
            'page' => 1
        ];
        
        $params = array_merge($defaultParams, $params);
        $params['apiKey'] = $this->apiKey;
        
        $url = $this->baseUrl . 'top-headlines?' . http_build_query($params);
        return $this->makeRequest($url);
    }
    
    /**
     * 搜索新闻
     * @param string $query 搜索关键词
     * @param array $params 额外参数
     * @return array
     */
    public function searchNews($query, $params = []) {
        $defaultParams = [
            'q' => $query,
            'sortBy' => 'publishedAt',
            'pageSize' => 20,
            'page' => 1,
            'language' => 'en'
        ];
        
        $params = array_merge($defaultParams, $params);
        $params['apiKey'] = $this->apiKey;
        
        $url = $this->baseUrl . 'everything?' . http_build_query($params);
        return $this->makeRequest($url);
    }
    
    /**
     * 获取新闻源列表
     * @param array $params 参数
     * @return array
     */
    public function getSources($params = []) {
        $params['apiKey'] = $this->apiKey;
        $url = $this->baseUrl . 'sources?' . http_build_query($params);
        return $this->makeRequest($url);
    }
    
    /**
     * 发起HTTP请求
     * @param string $url
     * @return array
     */
    private function makeRequest($url) {
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 30);
        curl_setopt($ch, CURLOPT_USERAGENT, 'HuoNiao NewsAPI Client/1.0');
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
        
        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        
        if ($httpCode !== 200) {
            return ['status' => 'error', 'message' => 'HTTP Error: ' . $httpCode];
        }
        
        $data = json_decode($response, true);
        if (json_last_error() !== JSON_ERROR_NONE) {
            return ['status' => 'error', 'message' => 'JSON解析错误'];
        }
        
        return $data;
    }
    
    /**
     * 将NewsAPI数据转换为系统格式并保存
     * @param array $articles NewsAPI文章数组
     * @param int $nodeId 采集节点ID
     * @return int 保存的文章数量
     */
    public function saveArticlesToSystem($articles, $nodeId) {
        $savedCount = 0;
        
        foreach ($articles as $article) {
            // 检查是否已存在
            $checkSql = $this->dsql->SetQuery("SELECT id FROM `#@__site_plugins_spider_content` WHERE url = '" . addslashes($article['url']) . "'");
            $exists = $this->dsql->dsqlOper($checkSql, "results");
            
            if (!empty($exists)) {
                continue; // 跳过已存在的文章
            }
            
            // 处理图片URL
            $imageUrl = $article['urlToImage'] ? $article['urlToImage'] : '';
            
            // 处理发布时间
            $publishedAt = $article['publishedAt'] ? strtotime($article['publishedAt']) : time();
            
            // 构建内容数据
            $contentData = [
                'node_id' => $nodeId,
                'title' => addslashes($article['title']),
                'content' => addslashes($article['content'] ?: $article['description']),
                'description' => addslashes($article['description']),
                'url' => addslashes($article['url']),
                'image_url' => addslashes($imageUrl),
                'source' => addslashes($article['source']['name']),
                'author' => addslashes($article['author'] ?: ''),
                'published_at' => date('Y-m-d H:i:s', $publishedAt),
                'created_at' => date('Y-m-d H:i:s'),
                'status' => 1
            ];
            
            // 插入数据库
            $insertSql = $this->dsql->SetQuery("INSERT INTO `#@__site_plugins_spider_content` 
                (`node_id`, `title`, `content`, `description`, `url`, `image_url`, `source`, `author`, `published_at`, `created_at`, `status`) 
                VALUES 
                ('{$contentData['node_id']}', '{$contentData['title']}', '{$contentData['content']}', '{$contentData['description']}', 
                '{$contentData['url']}', '{$contentData['image_url']}', '{$contentData['source']}', '{$contentData['author']}', 
                '{$contentData['published_at']}', '{$contentData['created_at']}', '{$contentData['status']}')");
            
            $result = $this->dsql->dsqlOper($insertSql, "lastid");
            if ($result) {
                $savedCount++;
            }
        }
        
        return $savedCount;
    }
    
    /**
     * 创建NewsAPI采集任务
     * @param array $config 配置参数
     * @return int 节点ID
     */
    public function createNewsAPINode($config) {
        $nodeData = [
            'name' => addslashes($config['name']),
            'type' => 'newsapi',
            'config' => addslashes(json_encode($config)),
            'status' => 1,
            'created_at' => date('Y-m-d H:i:s')
        ];
        
        $sql = $this->dsql->SetQuery("INSERT INTO `#@__site_plugins_spider_nodes` 
            (`name`, `type`, `config`, `status`, `created_at`) 
            VALUES 
            ('{$nodeData['name']}', '{$nodeData['type']}', '{$nodeData['config']}', '{$nodeData['status']}', '{$nodeData['created_at']}')");
        
        return $this->dsql->dsqlOper($sql, "lastid");
    }
    
    /**
     * 执行NewsAPI采集任务
     * @param int $nodeId 节点ID
     * @param array $params 采集参数
     * @return array 采集结果
     */
    public function executeNewsAPICollection($nodeId, $params = []) {
        // 获取节点配置
        $sql = $this->dsql->SetQuery("SELECT * FROM `#@__site_plugins_spider_nodes` WHERE id = $nodeId");
        $node = $this->dsql->dsqlOper($sql, "results");
        
        if (empty($node)) {
            return ['status' => 'error', 'message' => '节点不存在'];
        }
        
        $config = json_decode($node[0]['config'], true);
        
        // 根据配置类型执行不同的采集
        switch ($config['api_type']) {
            case 'top-headlines':
                $result = $this->getTopHeadlines($params);
                break;
            case 'everything':
                $result = $this->searchNews($config['query'], $params);
                break;
            default:
                return ['status' => 'error', 'message' => '未知的API类型'];
        }
        
        if ($result['status'] === 'ok' && !empty($result['articles'])) {
            $savedCount = $this->saveArticlesToSystem($result['articles'], $nodeId);
            return [
                'status' => 'success',
                'message' => "成功采集 {$savedCount} 篇文章",
                'total' => $result['totalResults'],
                'saved' => $savedCount
            ];
        } else {
            return [
                'status' => 'error',
                'message' => $result['message'] ?? '采集失败'
            ];
        }
    }
}
?>
