<?php
/**
 * 批量采集脚本 - 优化版本
 */
define('HUONIAOADMIN', ".");
require_once 'common.php';

$dsql = new dsql($dbo);

// 配置参数
$node_id = isset($_GET['node']) ? intval($_GET['node']) : 1;
$batch_size = isset($_GET['batch']) ? intval($_GET['batch']) : 50; // 每批处理数量
$max_pages = isset($_GET['pages']) ? intval($_GET['pages']) : 10; // 最大页数

echo "🚀 开始批量采集 - 节点ID: $node_id\n";
echo "📊 批次大小: $batch_size\n";
echo "📄 最大页数: $max_pages\n\n";

// 获取节点信息
$nodeInfo = getNode($node_id);
if (empty($nodeInfo)) {
    die("❌ 节点不存在: $node_id\n");
}

$total_collected = 0;
$total_urls = 0;

// 批量处理页面
for ($page = 1; $page <= $max_pages; $page++) {
    echo "📄 处理第 $page 页...\n";
    
    // 获取当前页的URL
    $urls = getPageUrls($nodeInfo, $page);
    if (empty($urls)) {
        echo "⚠️  第 $page 页无URL，跳过\n";
        continue;
    }
    
    $page_urls = count($urls);
    $total_urls += $page_urls;
    echo "🔗 发现 $page_urls 个URL\n";
    
    // 批量插入URL
    $inserted = batchInsertUrls($node_id, $urls);
    $total_collected += $inserted;
    
    echo "✅ 第 $page 页完成，插入 $inserted 个URL\n\n";
    
    // 检查是否达到限制
    if ($total_collected >= $batch_size) {
        echo "🎯 达到批次限制，停止采集\n";
        break;
    }
    
    // 避免请求过快
    sleep(1);
}

echo "🎉 批量采集完成!\n";
echo "📊 统计信息:\n";
echo "   - 总URL数量: $total_urls\n";
echo "   - 成功插入: $total_collected\n";
echo "   - 处理页数: " . min($page - 1, $max_pages) . "\n";

/**
 * 获取页面URL
 */
function getPageUrls($nodeInfo, $page) {
    $rule_url = $nodeInfo['list_page_url_rule'];
    $sign = '(*)';
    $listUrl = str_replace($sign, $page, $rule_url);
    
    $html = downOnePage($listUrl);
    if (!$html) {
        $html = strToUtf8(file_get_contents($listUrl));
    }
    
    if (!$html) {
        return [];
    }
    
    // 获取正文
    $body = getBody($html);
    if (!$body) {
        return [];
    }
    
    // 提取URL
    $urls = getUrls($body);
    return $urls ?: [];
}

/**
 * 批量插入URL
 */
function batchInsertUrls($node_id, $urls) {
    global $dsql;
    
    $inserted = 0;
    $existing = 0;
    
    foreach ($urls as $url) {
        // 检查是否已存在
        $sql_check = $dsql->SetQuery("SELECT id FROM `#@__site_plugins_spider_urls` WHERE node_id = $node_id AND url = '$url'");
        $exists = $dsql->dsqlOper($sql_check, "results");
        
        if (empty($exists)) {
            $sql_insert = $dsql->SetQuery("INSERT INTO `#@__site_plugins_spider_urls` (node_id, url, is_get) VALUES ($node_id, '$url', 1)");
            $result = $dsql->dsqlOper($sql_insert, "lastid");
            
            if ($result) {
                $inserted++;
            }
        } else {
            $existing++;
        }
    }
    
    if ($existing > 0) {
        echo "   ⚠️  跳过 $existing 个已存在的URL\n";
    }
    
    return $inserted;
}

/**
 * 获取节点信息
 */
function getNode($id) {
    global $dsql;
    $sql = "select * from `#@__site_plugins_spider_nodes` where id = $id";
    $sqls = $dsql->SetQuery($sql);
    $res = $dsql->dsqlOper($sqls, "results");
    return isset($res[0]) ? $res[0] : '';
}

/**
 * 获取正文
 */
function getBody($html) {
    // 简化版本，实际使用时需要根据节点规则
    return $html;
}

/**
 * 获取URL列表
 */
function getUrls($html) {
    $pattern = '/<a(?:.*?)href="(((?:http(?:s?):\/\/)?([^\"\/]+))?(?:[^\"]*))"(?:[^>]*?)>([^<]*?)<\/a>/i';
    preg_match_all($pattern, $html, $mat);
    unset($mat[0], $mat[3], $mat[2], $mat[4]);
    $urls = $mat[1];
    
    // 过滤无效URL
    $urls = array_filter($urls, function($url) {
        return is_url($url);
    });
    
    return array_unique($urls);
}
?> 