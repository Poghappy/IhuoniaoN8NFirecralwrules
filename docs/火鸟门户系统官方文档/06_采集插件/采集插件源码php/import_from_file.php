<?php
/**
 * 从文件批量导入URL
 */
define('HUONIAOADMIN', ".");
require_once 'common.php';

$dsql = new dsql($dbo);

// 配置参数
$node_id = 1; // 节点ID
$file_path = './urls.txt'; // URL文件路径

// 读取URL文件
if (!file_exists($file_path)) {
    die("❌ 文件不存在: $file_path\n");
}

$urls = file($file_path, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
if (empty($urls)) {
    die("❌ 文件为空或格式错误\n");
}

echo "📁 读取文件: $file_path\n";
echo "📊 总URL数量: " . count($urls) . "\n\n";

// 批量插入
$success_count = 0;
$error_count = 0;
$exists_count = 0;

// 使用事务提高性能
$dsql->dsqlOper("START TRANSACTION", "update");

try {
    foreach ($urls as $index => $url) {
        $url = trim($url);
        if (empty($url)) continue;
        
        // 检查是否已存在
        $sql_check = $dsql->SetQuery("SELECT id FROM `#@__site_plugins_spider_urls` WHERE node_id = $node_id AND url = '$url'");
        $exists = $dsql->dsqlOper($sql_check, "results");
        
        if (empty($exists)) {
            $sql_insert = $dsql->SetQuery("INSERT INTO `#@__site_plugins_spider_urls` (node_id, url, is_get) VALUES ($node_id, '$url', 1)");
            $result = $dsql->dsqlOper($sql_insert, "lastid");
            
            if ($result) {
                $success_count++;
                if ($index % 100 == 0) {
                    echo "✅ 已处理: $index / " . count($urls) . "\n";
                }
            } else {
                $error_count++;
            }
        } else {
            $exists_count++;
        }
    }
    
    // 提交事务
    $dsql->dsqlOper("COMMIT", "update");
    
} catch (Exception $e) {
    // 回滚事务
    $dsql->dsqlOper("ROLLBACK", "update");
    die("❌ 批量插入失败: " . $e->getMessage() . "\n");
}

echo "\n📊 批量导入完成:\n";
echo "✅ 成功插入: $success_count 条\n";
echo "⚠️  已存在: $exists_count 条\n";
echo "❌ 插入失败: $error_count 条\n";
echo "📁 总计处理: " . count($urls) . " 条\n";
?> 