<?php
/**
 * 添加节点对应的内容页面的规则
 */
define('HUONIAOADMIN', ".");
require_once 'common.php';
require_once 'service/ImagesService.php';

$dsql                     = new dsql($dbo);
$userLogin                = new userLogin($dbo);
$tpl                      = dirname(__FILE__) . "/tpl";
$huoniaoTag->template_dir = $tpl; //设置后台模板目录
$templates                = "insertBodyRules.html";

$err = '';
if (isset($_GET['err']) && $_GET['err'] !== '') $err = $_GET['err'];

$nodeId = isset($_GET['node']) && $_GET['node'] !== '' ? $_GET['node'] : '';

if (is_post()) {
    $data = $_POST;
    $err  = false;

    if (!array_key_exists('title_start', $data) || !array_key_exists('title_end', $data) || !array_key_exists('body_start', $data) || !array_key_exists('body_end', $data)) {
        header("Location: ./insertBodyRules.php?err=参数不正确");
        exit;
    }
    $title_start  = $title_start ? $title_start : $err = true;
    $title_start = rtrim($title_start);
    // $title_start = preg_replace('/\'/', '"', $title_start);

    $title_end    = $title_end ? $title_end : $err = true;
    $title_end = rtrim($title_end);
    // $title_end = preg_replace('/\'/', '"', $title_end);


    $time_start   = array_key_exists("time_start", $data) ? $time_start : '';
    $time_start = rtrim($time_start);
    // $time_start = preg_replace('/\'/', '"', $time_start);


    $time_end     = array_key_exists("time_end", $data) ? $time_end : '';
    $time_end =  rtrim($time_end);
    // $time_end = preg_replace('/\'/', '"', $time_end);


    $body_start   = $body_start ? $body_start : $err = true;
    $body_start = rtrim($body_start);
    // $body_start = preg_replace('/\'/', '"', $body_start);


    $body_end     = $body_end ? $body_end : $err = true;
    $body_end = rtrim($body_end);
    // $body_end = preg_replace('/\'/', '"', $body_end);


    $source_start = array_key_exists('source_start', $data) ? $source_start : '';
    $source_start = rtrim($source_start);
    // $source_start = preg_replace('/\'/', '"', $source_start);


    $source_end   = array_key_exists('source_end', $data) ? $source_end : '';
    $source_end = rtrim($source_end);
    // $source_end = preg_replace('/\'/', '"', $source_end);


    $author_start = array_key_exists('author_start', $data) ? $author_start : '';
    $author_start = rtrim($author_start);
    // $author_start = preg_replace('/\'/', '"', $author_start);


    $author_end   = array_key_exists('author_end', $data) ? $author_end : '';
    $author_end = rtrim($author_end);
    // $author_end = preg_replace('/\'/', '"', $author_end);


    $update_id    = array_key_exists('update_id', $data) ? $update_id : '';

    $nodeId       = $node ? $node : $err = true;
    if ($nodeId == '') $err = true;
    if ($err) {
        header("Location: ./insertBodyRules.php?err=参数不正确");
        exit;
    }
    if ($update_id) {
        $sql = "update `#@__site_plugins_spider_node_rules` set title_start = '{$title_start}', title_end = '{$title_end}',
time_start =  '{$time_start}', time_end = '{$time_end}', source_start = '{$source_start}', source_end = '{$source_end}',
author_start = '{$author_start}', author_end = '{$author_end}', body_start = '{$body_start}', body_end = '{$body_end}' where id = $update_id";
        $sql = $dsql->SetQuery($sql);
        $res = $dsql->dsqlOper($sql, "update");
        if ($res) {
            header("Location: ./index.php?changeNode={$nodeId}&err=添加成功");
            exit;
        } else {
            header("Location: ./index.php?changeNode={$nodeId}&err=添加失败~请稍后再试");
            exit;
        }
    } else {
        $sql = "insert into `#@__site_plugins_spider_node_rules` (node_id,title_start,title_end,time_start,time_end,source_start,source_end,author_start,author_end,body_start,body_end) values
($nodeId,'{$title_start}','{$title_end}', '{$time_start}','{$time_end}','{$source_start}','{$source_end}','{$author_start}','{$author_end}','{$body_start}','{$body_end}')";
        $sql = $dsql->SetQuery($sql);
        $res = $dsql->dsqlOper($sql, "lastid");
        if ($res) {
            header("Location: ./index.php");
        } else {
            header("Location: ./insertBodyRules.php?err=添加失败~请稍后再试");
            exit;
        }
    }

}

$huoniaoTag->assign('cfg_staticPath', $cfg_staticPath);

$huoniaoTag->assign('errmsg', $err);

$huoniaoTag->assign('nodeId', $nodeId);
$huoniaoTag->display($templates);
