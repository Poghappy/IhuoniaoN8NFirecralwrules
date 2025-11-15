<?php
/**
 * 添加采集节点
 */
define('HUONIAOADMIN', ".");
require_once './common.php';

$dsql                     = new dsql($dbo);
$userLogin                = new userLogin($dbo);
$tpl                      = dirname(__FILE__) . "/tpl";
$huoniaoTag->template_dir = $tpl; //设置后台模板目录
$templates                = "insertNode.html";

$err = '';
if (isset($_GET['err']) && $_GET['err'] !== '') $err = $_GET['err'];

if (is_post()) {

    $data = $_POST;
    $err  = false;

    if (!array_key_exists('type', $data) || !array_key_exists('must_include', $data) || !array_key_exists('nodename', $data) || !array_key_exists('list_start_sign', $data) || !array_key_exists('list_end_sign', $data)) {
        header("Location: ./insertNode.php?err=参数不正确");
        exit;
    }
    //整理字段
    $type            = $data['type'] ? $data['type'] : $err = true;
    $nodename        = $data['nodename'] ? $data['nodename'] : $err = true;

    $list_start_sign = array_key_exists('list_start_sign', $data) ? $data['list_start_sign'] : '';
    $list_start_sign = rtrim($list_start_sign);
    $list_start_sign = preg_replace('/\'/', '"', $list_start_sign);

    $list_end_sign   = array_key_exists('list_end_sign', $data) ? $data['list_end_sign'] : '';
    $list_end_sign = rtrim($list_end_sign);
    $list_end_sign = preg_replace('/\'/', '"', $list_end_sign);

    $must_include    = $data['must_include'] ? $data['must_include'] : '';
    $must_include =  rtrim($must_include);
    $not_include     = array_key_exists('not_include', $data) ? $data['not_include'] : '';
    $not_include = rtrim($not_include);

    $list_page_url   = array_key_exists('list_page_url', $data) ? $data['list_page_url'] : '';


    $node_id            = array_key_exists('node_id', $data) ? $data['node_id'] : '';
    $list_page_url_rule = array_key_exists('list_page_url_rule', $data) ? $data['list_page_url_rule'] : '';
    $list_page_url_rule = rtrim($list_page_url_rule);


    if ($err) {
        header("Location: ./insertNode.php?err=添加失败~请核对输入");
        exit;
    }

    $list_pages = serialize($list_page_url);

    //存入node表
    $time = time();
    if ($node_id) {
        $sql = "UPDATE `#@__site_plugins_spider_nodes` SET type = '{$type}', nodename = '{$nodename}', list_page_url = '{$list_pages}',
list_start_sign = '{$list_start_sign}', list_end_sign = '{$list_end_sign}', category = '', must_include = '{$must_include}',
not_include = '{$not_include}', updated_at = {$time} , list_page_url_rule = '{$list_page_url_rule}' where id = {$node_id}";
    } else {
        $sql = "INSERT INTO `#@__site_plugins_spider_nodes`
(type, nodename, list_page_url, list_start_sign, list_end_sign, category, must_include, not_include, created_at, updated_at, list_page_url_rule)
        VALUES ('{$type}', '{$nodename}', '{$list_pages}', '{$list_start_sign}', '{$list_end_sign}', '',
        '{$must_include}', '{$not_include}', {$time}, {$time}, '{$list_page_url_rule}')";
    }


    $sqls = $dsql->SetQuery($sql);
    if ($node_id) {
        //编辑
        $aid = $dsql->dsqlOper($sqls, "update");
        if ($aid) {
            header("Location: ./index.php?changeNode={$node_id}&err=添加成功");
            exit;
        } else {
            header("Location: ./insertNode.php?err=添加失败~请稍后再试");
            exit;
        }
    } else {
        //添加
        $aid = $dsql->dsqlOper($sqls, "lastid");
        if ($aid) {
            header("Location: ./insertBodyRules.php?node=$aid");
            exit;
        } else {
            header("Location: ./insertNode.php?err=添加失败~请稍后再试");
            exit;
        }
    }


}

$huoniaoTag->assign('cfg_staticPath', $cfg_staticPath);

$huoniaoTag->assign('errmsg', $err);
$huoniaoTag->display($templates);
