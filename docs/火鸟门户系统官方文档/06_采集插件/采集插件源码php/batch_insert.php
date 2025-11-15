<?php
/**
 * 批量写入采集URL脚本
 */
define('HUONIAOADMIN', ".");
require_once 'common.php';

$dsql = new dsql($dbo);

// 配置参数
$node_id = 1; // 节点ID
$urls = [
    'http://example1.com/news/1',
    'http://example1.com/news/2',
    'http://example1.com/news/3',
    // 添加更多URL...
];

// 批量插入URL
$success_count = 0;
$error_count = 0;

foreach ($urls as $url) {
    // 检查是否已存在
    $sql_check = $dsql->SetQuery("SELECT id FROM `#@__site_plugins_spider_urls` WHERE node_id = $node_id AND url = '$url'");
    $exists = $dsql->dsqlOper($sql_check, "results");
    
    if (empty($exists)) {
        $sql_insert = $dsql->SetQuery("INSERT INTO `#@__site_plugins_spider_urls` (node_id, url, is_get) VALUES ($node_id, '$url', 1)");
        $result = $dsql->dsqlOper($sql_insert, "lastid");
        
        if ($result) {
            $success_count++;
            echo "✅ 插入成功: $url\n";
        } else {
            $error_count++;
            echo "❌ 插入失败: $url\n";
        }
    } else {
        echo "⚠️  已存在: $url\n";
    }
}

echo "\n📊 批量插入完成:\n";
echo "成功: $success_count 条\n";
echo "失败: $error_count 条\n";
echo "总计: " . count($urls) . " 条\n";
?> 