<?php
/**
 * 信息资讯采集插件
 *
 * @version        2021-02-18 上午10:17:21 $
 * @package        HuoNiao.Plugins
 * @copyright      Copyright (c) 2013 - 2021, HuoNiao, Inc.
 * @link           https://www.ihuoniao.cn/
 */
define('HUONIAOADMIN', ".");
require_once 'common.php';

$dsql                     = new dsql($dbo);
$userLogin                = new userLogin($dbo);
$tpl                      = dirname(__FILE__) . "/tpl";
$huoniaoTag->template_dir = $tpl; //设置后台模板目录
$templates                = "index.html";

if($userLogin->getUserID()==-1){
  header("location:" . $cfg_secureAccess.$cfg_basehost);
  exit();
}

$mod = $mod ? $mod : 'article';

$userLogin = new userLogin($dbo);

$err = '';
if (isset($_GET['err']) && $_GET['err'] !== '') $err = $_GET['err'];


$sql = $dsql->SetQuery("SELECT * FROM `#@__site_plugins_spider_nodes`");
$ret = $dsql->dsqlOper($sql, "results");


if (isset($_GET['delete'])) {
    if (!$_GET['delete'] !== '') {
        //删除该节点下所有内容
        $id   = intval($_GET['delete']);
        $sql1 = $dsql->SetQuery("delete from `#@__site_plugins_spider_nodes` where id = $id");
        $dsql->dsqlOper($sql1, "lastid");
        $sql2 = $dsql->SetQuery("delete from `#@__site_plugins_spider_node_rules` where node_id = $id");
        $dsql->dsqlOper($sql2, "lastid");
        $sql3 = $dsql->SetQuery("delete from `#@__site_plugins_spider_urls` where node_id = $id");
        $dsql->dsqlOper($sql3, "lastid");
        $sql4 = $dsql->SetQuery("delete  from `#@__site_plugins_spider_content` where node_id = $id");
        $dsql->dsqlOper($sql4, "lastid");
        returnJson(['code' => 200, 'msg' => '删除成功']);
    }
} else if (isset($_GET['getNewsList'])) {
    if (is_ajax()) {
        //删除指定新闻
        $id  = $_GET['del'];
        $sql = $dsql->SetQuery("delete from `#@__site_plugins_spider_content` where id = $id");
        $dsql->dsqlOper($sql, "lastid");
        returnJson(['code' => 200, 'msg' => '删除成功']);
    }
    //获取已采集
    $id   = intval($_GET['getNewsList']);
    $sql1 = $dsql->SetQuery("select * from `#@__site_plugins_spider_content` where node_id = $id");
    $res  = $dsql->dsqlOper($sql1, "results");
    $res  = changeHtmlSpec($res);
    $huoniaoTag->assign('cfg_staticPath', $cfg_staticPath);
    $huoniaoTag->assign('list', $res);
    $huoniaoTag->assign('node_id', $id);
    $huoniaoTag->display('./newsList.html');
    exit;

} else if (isset($_GET['changeNode'])) {
    $id                      = intval($_GET['changeNode']);
    $sql                     = $dsql->SetQuery("select * from `#@__site_plugins_spider_nodes` where id = $id");
    $res                     = $dsql->dsqlOper($sql, "results");
    $sql2                    = $dsql->SetQuery("select * from `#@__site_plugins_spider_node_rules` where node_id = $id");
    $res2                    = $dsql->dsqlOper($sql2, "results");
    $res[0]['list_page_url'] = unserialize($res[0]['list_page_url']);
    $arr                     = changeHtmlSpec($res);

    $arr2 = changeHtmlSpec($res2);


    $huoniaoTag->assign('errmsg', $err);
    $huoniaoTag->assign('nodes', $arr[0]);
    $huoniaoTag->assign('node_rules', $arr2[0]);
    $huoniaoTag->assign('cfg_staticPath', $cfg_staticPath);
    $huoniaoTag->display('./changeNodes.html');
    exit;
} else if (isset($_GET['export'])) {
    //导出新闻
    $id = intval($_GET['export']);

    $sql      = $dsql->SetQuery("select * from `#@__site_plugins_spider_content` where node_id = $id");
    $resCount = $dsql->dsqlOper($sql, "totalCount");

    if (is_ajax()) {
        $post = $_GET;

        if ($post['typeid'] == 0 || $post['cityid'] == '') {
            $err = '请选择城市和分类';
            returnJson(['code' => 201, 'msg' => '请选择城市和分类']);
        }
        $totle = $post['totle'];
        $sql   = $dsql->SetQuery("select * from `#@__site_plugins_spider_content` where node_id = $id and is_export = 1 limit $totle");

        //获取该节点内容
        //查询该节点是否已经导出
        $sql_isexp = $dsql->SetQuery("select * from `#@__site_plugins_spider_nodes` where id = $id");
        $isExp     = $dsql->dsqlOper($sql_isexp, "results");
        if ($isExp[0]['is_export'] == 2) {
            returnJson(['code' => 201, 'msg' => '该节点已经导出']);
        } else {
            $content = $dsql->dsqlOper($sql, "results");
            if (count($content) == 0) {
                $sqlUpdate = $dsql->SetQuery("update `#@__site_plugins_spider_nodes` set `is_export` = 2 where id = {$id}");
                $dsql->dsqlOper($sqlUpdate, "update");
                returnJson(['code' => 201, 'msg' => '导出完成']);
            }

            $time = time();
            foreach ($content as $item) {

            	if($mod == 'article'){
	                $archives = $dsql->SetQuery("INSERT INTO `#@__articlelist` (`cityid`, `title`, `subtitle`, `flag`, `redirecturl`, `weight`, `litpic`,
	`source`, `sourceurl`, `writer`, `typeid`, `keywords`, `description`, `mbody`, `notpost`, `click`, `color`, `arcrank`, `pubdate`, `admin`,
	`reward_switch`, `audit_log`, `audit_edit`) VALUES ('{$post['cityid']}', '{$item['title']}', '', '', '', 1, '{$item['thumb']}', '{$item['source']}',
	 '', '{$item['author']}', '{$post['typeid']}', '{$item['keywords']}', '{$item['description']}', '', '0', '1', '', '1', {$time}, '1',
	 '', '', '' )");
	                $aid      = $dsql->dsqlOper($archives, "lastid");

	                $art = $dsql->SetQuery("INSERT INTO `#@__article` (`aid`, `body`) VALUES ('$aid', '{$item['content']}')");
	                $dsql->dsqlOper($art, "update");
	            }else{
	            	$art = $dsql->SetQuery("INSERT INTO `#@__house_news` (`cityid`, `title`, `typeid`, `litpic`, `click`, `weight`, `source`, `writer`, `keyword`, `description`, `body`, `arcrank`, `pubdate`) VALUES ('$cityid', '{$item['title']}', '{$post['typeid']}', '{$item['thumb']}', 0, 1, '{$item['source']}', '{$item['author']}', '{$item['keywords']}', '{$item['description']}', '{$item['content']}', 0, '{$time}')");
	                $dsql->dsqlOper($art, "update");
	            }

                $sql_up = $dsql->SetQuery("update `#@__site_plugins_spider_content` set is_export = 2 where id = {$item['id']} ");
                $dsql->dsqlOper($sql_up, "update");
            }

            returnJson(['code' => 200, 'msg' => '导出成功']);
        }
    }

    $adminCityArr = $userLogin->getAdminCity();
    $adminCityArr = empty($adminCityArr) ? array() : $adminCityArr;
    $domain       = '//' . $_SERVER['HTTP_HOST'];

    if($mod == 'article'){
	    $huoniaoTag->assign('typeListArr', json_encode($dsql->getTypeList(0, 'articletype')));
	}else{
	    $huoniaoTag->assign('typeListArr', json_encode($dsql->getTypeList(0, 'house_newstype')));
	}
    $huoniaoTag->assign('count', $resCount);

    $huoniaoTag->assign('cityList', json_encode($adminCityArr));
    $huoniaoTag->assign('node_id', $id);
    $huoniaoTag->assign('cfg_staticPath', $cfg_staticPath);
    $huoniaoTag->assign('domain', $domain);
	$huoniaoTag->assign('mod', $mod);
    $huoniaoTag->display('./export.html');
    exit;
} else if (isset($_GET['getView'])) {
    $id   = intval($_GET['getView']);
    $type = intval($_GET['type']);

    $sql                     = $dsql->SetQuery("select * from `#@__site_plugins_spider_nodes` where id = $id");
    $res                     = $dsql->dsqlOper($sql, "results");
    $res[0]['list_page_url'] = unserialize($res[0]['list_page_url']);
    $arr                     = changeHtmlSpec($res);
    $huoniaoTag->assign('nodes', $arr[0]);
    $huoniaoTag->assign('node_id', $id);
    $huoniaoTag->assign('type', $type);
    $huoniaoTag->assign('errmsg', $err);
    $huoniaoTag->assign('cfg_staticPath', $cfg_staticPath);

    $huoniaoTag->display('./getView.html');
    exit;
} else if (isset($_GET['start'])) {
    //匹配列表页测试
    $start    = intval($_GET['start']);
    $end      = intval($_GET['end']);
    $node     = intval($_GET['node']);
    $nodeInfo = getNode($node);
    $listUrl  = $nodeInfo['list_page_url_rule'];
    $sign     = '(*)';
    $arr      = [];
    for ($i = $start; $i <= $end; $i++) {
        $listUrl1 = str_replace($sign, $i, $listUrl);
        $html     = strToUtf8(curl_get($listUrl1));
        if (!$html) $html = strToUtf8(file_get_contents($listUrl1));
        $arr[] = $listUrl1;
    }
    returnJson(['code' => 200, 'msg' => 'success', 'data' => $arr]);

} else if (isset($_GET['resUrls'])) {
    $node_id = $_GET['node_id'];
    $url = file_get_contents('./cache/' . $node_id . '.txt');
    $urls = unserialize($url);
    $sql_del = $dsql->SetQuery("delete from `#@__site_plugins_spider_urls` where node_id = $node_id");
    $dsql->dsqlOper($sql_del, "lastid");
    foreach ($urls as $url) {

        $sql2  = "insert into #@__site_plugins_spider_urls (node_id, url) values ($node_id, '{$url}')";
        $sql2s = $dsql->SetQuery($sql2);
        $res   = $dsql->dsqlOper($sql2s, "lastid");
    }
    returnJson(['code' => 200, 'msg' => 'success', 'data' => '']);

}


$huoniaoTag->assign('nodes', $ret);
$huoniaoTag->assign('cfg_staticPath', $cfg_staticPath);
$huoniaoTag->display($templates);


/**
 * 转义数组中的html(htmlspecialchars)
 * @param $res
 * @return array
 */
function changeHtmlSpec($res)
{
    $arrs = [];
    foreach ($res as $re) {
        $arr = [];
        foreach ($re as $k => $v) {
            if ($k == 'list_page_url') {
                $arr[$k] = $v;
                continue;
            }
            $arr[$k] = htmlspecialchars($v);
        }
        array_push($arrs, $arr);
    }
    return $arrs;
}

/**
 * 获取节点信息
 * @param $id
 * @return array
 */
function getNode($id)
{
    global $dsql;
    $sql  = "select * from `#@__site_plugins_spider_nodes` where id = $id";
    $sqls = $dsql->SetQuery($sql);
    $res  = $dsql->dsqlOper($sqls, "results");
    return isset($res[0]) ? $res[0] : '';
}
