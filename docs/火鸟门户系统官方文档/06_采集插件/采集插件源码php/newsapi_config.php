<?php
/**
 * NewsAPI 配置管理页面
 *
 * @version        2025-07-21
 * @package        HuoNiao.Plugins.NewsAPI
 */

define('HUONIAOADMIN', ".");
require_once 'common.php';
require_once 'newsapi_service.php';

$dsql = new dsql($dbo);
$userLogin = new userLogin($dbo);
$tpl = dirname(__FILE__) . "/tpl";
$huoniaoTag->template_dir = $tpl;

if($userLogin->getUserID() == -1){
    header("location:" . $cfg_secureAccess.$cfg_basehost);
    exit();
}

// 处理表单提交
if ($_POST) {
    $action = $_POST['action'];
    
    switch ($action) {
        case 'save_config':
            // 保存NewsAPI配置
            $apiKey = trim($_POST['api_key']);
            $defaultCountry = trim($_POST['default_country']);
            $defaultLanguage = trim($_POST['default_language']);
            
            $config = [
                'api_key' => $apiKey,
                'default_country' => $defaultCountry,
                'default_language' => $defaultLanguage,
                'updated_at' => date('Y-m-d H:i:s')
            ];
            
            // 保存到配置表
            $configJson = json_encode($config);
            $sql = $dsql->SetQuery("REPLACE INTO `#@__site_plugins_config` (`plugin_id`, `config_key`, `config_value`) VALUES (4, 'newsapi', '" . addslashes($configJson) . "')");
            $dsql->dsqlOper($sql, "lastid");
            
            $message = "NewsAPI配置保存成功！";
            break;
            
        case 'create_node':
            // 创建NewsAPI采集节点
            $nodeName = trim($_POST['node_name']);
            $apiType = $_POST['api_type'];
            $query = trim($_POST['query']);
            $country = $_POST['country'];
            $language = $_POST['language'];
            $category = $_POST['category'];
            $sources = $_POST['sources'];
            
            $nodeConfig = [
                'api_type' => $apiType,
                'query' => $query,
                'country' => $country,
                'language' => $language,
                'category' => $category,
                'sources' => $sources
            ];
            
            // 获取API Key
            $configSql = $dsql->SetQuery("SELECT config_value FROM `#@__site_plugins_config` WHERE plugin_id = 4 AND config_key = 'newsapi'");
            $configResult = $dsql->dsqlOper($configSql, "results");
            
            if (empty($configResult)) {
                $error = "请先配置NewsAPI密钥！";
                break;
            }
            
            $apiConfig = json_decode($configResult[0]['config_value'], true);
            $newsAPI = new NewsAPIService($apiConfig['api_key'], $dsql);
            
            $nodeId = $newsAPI->createNewsAPINode([
                'name' => $nodeName,
                'api_type' => $apiType,
                'query' => $query,
                'country' => $country,
                'language' => $language,
                'category' => $category,
                'sources' => $sources
            ]);
            
            if ($nodeId) {
                $message = "NewsAPI采集节点创建成功！节点ID: $nodeId";
            } else {
                $error = "创建节点失败！";
            }
            break;
            
        case 'test_api':
            // 测试API连接
            $apiKey = trim($_POST['test_api_key']);
            $newsAPI = new NewsAPIService($apiKey, $dsql);
            
            $result = $newsAPI->getTopHeadlines(['pageSize' => 1]);
            
            if ($result['status'] === 'ok') {
                $message = "API连接测试成功！可用请求数: " . $result['totalResults'];
            } else {
                $error = "API连接测试失败: " . ($result['message'] ?? '未知错误');
            }
            break;
    }
}

// 获取当前配置
$configSql = $dsql->SetQuery("SELECT config_value FROM `#@__site_plugins_config` WHERE plugin_id = 4 AND config_key = 'newsapi'");
$configResult = $dsql->dsqlOper($configSql, "results");
$currentConfig = [];

if (!empty($configResult)) {
    $currentConfig = json_decode($configResult[0]['config_value'], true);
}

// 获取NewsAPI节点列表
$nodesSql = $dsql->SetQuery("SELECT * FROM `#@__site_plugins_spider_nodes` WHERE type = 'newsapi' ORDER BY id DESC");
$newsApiNodes = $dsql->dsqlOper($nodesSql, "results");

// 国家代码选项
$countries = [
    'us' => '美国',
    'cn' => '中国',
    'gb' => '英国',
    'ca' => '加拿大',
    'au' => '澳大利亚',
    'jp' => '日本',
    'kr' => '韩国',
    'de' => '德国',
    'fr' => '法国',
    'it' => '意大利'
];

// 语言选项
$languages = [
    'en' => 'English',
    'zh' => '中文',
    'ja' => '日语',
    'ko' => '韩语',
    'de' => 'Deutsch',
    'fr' => 'Français',
    'es' => 'Español',
    'it' => 'Italiano'
];

// 分类选项
$categories = [
    '' => '全部',
    'business' => '商业',
    'entertainment' => '娱乐',
    'general' => '综合',
    'health' => '健康',
    'science' => '科学',
    'sports' => '体育',
    'technology' => '科技'
];

$huoniaoTag->assign('currentConfig', $currentConfig);
$huoniaoTag->assign('newsApiNodes', $newsApiNodes);
$huoniaoTag->assign('countries', $countries);
$huoniaoTag->assign('languages', $languages);
$huoniaoTag->assign('categories', $categories);
$huoniaoTag->assign('message', $message ?? '');
$huoniaoTag->assign('error', $error ?? '');
$huoniaoTag->assign('cfg_staticPath', $cfg_staticPath);

$huoniaoTag->display('./newsapi_config.html');
?>
