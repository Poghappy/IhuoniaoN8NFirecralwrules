<?php
/**
 * node =
 * 根据节点id获取新闻内页
 */
define('HUONIAOADMIN', "." );
require_once 'common.php';
require_once 'service/ImagesService.php';

$dsql = new dsql($dbo);
$userLogin = new userLogin($dbo);
$tpl = dirname(__FILE__)."/tpl";
$huoniaoTag->template_dir = $tpl; //设置后台模板目录
$templates = "";


$err = false;
$nodeId = isset($_GET['node']) ? $_GET['node'] : $err = true;
$page = isset($_GET['page']) ? $_GET['page'] : $err = true;

if($err) returnJson(['code' => 201 , 'msg' => '参数错误']);
$nodeInfo = getBodyRules(intval($nodeId));

if(empty($nodeInfo)) returnJson( ['code' => 201, 'msg' => '内容节点规则不存在' ]);

//所有新闻url
$ids_err = [];

$newsUrls = getUrl($nodeId, $page);
if(empty($newsUrls)) returnJson( ['code' => 201, 'msg' => '已完成' ]);
    foreach ($newsUrls as $k => $url){
        $html = downOnePage($url['url']);
        if(!$html) $html = strToUtf8(curl_get($url['url']));
//        if(!$html) $html = strToUtf8(curl_get_copy($url['url']));
//        if(!$html) $html = strToUtf8(file_get_contents($url['url']));
        if(!$html) {
            $ids_err[] = $url['id'];
            continue;
        }
        //新闻内容
        $newsHtmlNew = useRuleGetBodys($html, 'body', $url['id']);
        if(!$newsHtmlNew) {
            $ids_err[] = $url['id'];
            continue;
        }
        //截取出来之前拼的缩略图地址
        $exp = explode("||", $newsHtmlNew);
        if(count($exp) > 1){
            $thumb = $exp[count($exp)-1];
            $newsHtmlNew = str_replace($thumb, "", $newsHtmlNew);
            $newsHtmlNew = str_replace("||", "", $newsHtmlNew);
        }
        $newsBody = preg_replace('/\'/', '"', $newsHtmlNew);
        //获取新闻标题
        $title = useRuleGetBodys($html, 'title');
        if(!$title) {
            $ids_err[] = $url['id'];
            continue;
        }
        //关键词和描述
        $keywords = autoget('keywords' , $html);
        $desc = autoget('desc' , $html);
        //获取来源
        $source = useRuleGetBodys($html, 'source');
        //获取作者
        $author = useRuleGetBodys($html, 'author');
        //获取时间
        $times  = useRuleGetBodys($html, 'time');
        if($times == false) $times = 1;

        $sql = "insert into #@__site_plugins_spider_content (node_id, url_id, content, times, title, source, author, thumb, keywords, description) values
                ( {$nodeId}, {$url['id']}, '{$newsBody}', {$times}, '{$title}', '{$source}', '{$author}', '{$thumb}', '{$keywords}', '{$desc}' )";
        if($newsBody !== ''){
            $sqls = $dsql->SetQuery($sql);
            $id = $dsql->dsqlOper($sqls, "lastid");
            //标记$url['id']为已采集
            if(is_numeric($id)){
                $sql3 = "update #@__site_plugins_spider_urls set is_get = 2 where id = {$url['id']}";
                $sql3 = $dsql->SetQuery($sql3);
                $dsql->dsqlOper($sql3, "lastid");
                //$ids_err 抓取不到内容的id
                foreach ($ids_err as $v){
                    $sql4 = "update #@__site_plugins_spider_urls set is_get = 3 where id = $v";
                    $sql4 = $dsql->SetQuery($sql4);
                    $dsql->dsqlOper($sql4, "update");
                }

                //百分比
                $sum = getUrlSum($nodeId); //总共
                $isGet = getUrlSum2($nodeId); //已采集
                $per = sprintf("%.4f",($isGet / $sum));
                $per = $per * 100;
                $per = ceil($per) . '%';
                if(!$per){
                    $per = '100%';
                }
                returnJson(['code' => 200 , 'msg' => 'success！', 'data' => $per]);
            }else{
                returnJson(['code' => 201 , 'msg' => '操作失败！']);
            }
        }

    }

//$ids_err 抓取不到内容的id
foreach ($ids_err as $v){
    $sql4 = "update #@__site_plugins_spider_urls set is_get = 3 where id = $v";
    $sql4 = $dsql->SetQuery($sql4);
    $dsql->dsqlOper($sql4, "update");
}
//百分比
$sum = getUrlSum($nodeId); //总共
$isGet = getUrlSum2($nodeId); //已采集
$per = sprintf("%.4f",($isGet / $sum));
$per = $per * 100;
$per = ceil($per) . '%';
if(!$per){
    $per = '100%';
}

returnJson(['code' => 200 , 'msg' => 'success!', 'data' => $per]);


/**
 *
 * @param $html
 * @param $type
 * @param string $url_id
 * @return bool|false|int|mixed|string
 */
function useRuleGetBodys($html, $type, $url_id = '')
{
    global $nodeInfo;
    if(!$type || !$html) return '';
    switch ($type){
        //获取正文
        case 'body':
            $start = $nodeInfo['body_start'];
            $end = $nodeInfo['body_end'];
            $body = getNewHtml($start, $end, $html);
            $body    = delScript($body);
            //获取正文中的图片，下载到本地，替换正文中的链接
            $imgService = new ImagesService($body, $nodeInfo['node_id'], $url_id);
            $newsHtmlNew = $imgService->getNewsContent();
            if(!$newsHtmlNew) return $body;
            return $newsHtmlNew;
        case 'title':
            //获取标题
            $start = $nodeInfo['title_start'];
            $end = $nodeInfo['title_end'];
            if($start == '' || $end == '') return '';
            $body = getNewHtml($start, $end, $html);
            $body = deleteHtml($body);
            //提取中文
            $title = getChinese($body);
            return $title;
        case 'source':
            //获取来源
            $start = $nodeInfo['source_start'];
            $end = $nodeInfo['source_end'];
            if($start == '' || $end == '') return '';
            $body = getNewHtml($start, $end, $html);
            $source = deleteHtml($body);
//            $sources = getChinese($source);
            //可能会出现'年月日'日期'时间'
            if($source !== ''){
                if(mb_strstr($source,'年')){
                    $source = str_replace(mb_substr($sources,0,3,"UTF8"),"", $source);
                }
                if(mb_strstr($source, '日期')){
                    $source = str_replace(mb_substr($sources,0,2,"UTF8"),"", $source);
                }
                if(mb_strstr($source, '时间')){
                    $source = str_replace(mb_substr($sources,0,2,"UTF8"),"", $source);
                }
            }
            return $source;
        case 'time':
            //获取时间
            $start = $nodeInfo['time_start'];
            $end = $nodeInfo['time_end'];
            if($start == '' || $end == '') return '';
            $body = getNewHtml($start, $end, $html);
            $time = strip_tags($body);
            if(preg_match('/(\d+)年?(\d+)月(\d+)日\s+\d+\:\d+\:\d+/',$time,$m)){
                $timeArr = date_parse_from_format('Y年m月d日 H:i:s', $m[0]);
                $time = mktime(0,0,0,$timeArr['month'],$timeArr['day'],$timeArr['year']);
                return $time;
            }

            if(preg_match('/(\d+)年?(\d+)月(\d+)日\s+\d+\:\d+/',$time,$m)){
                $timeArr = date_parse_from_format('Y年m月d日 H:i', $m[0]);
                $time = mktime(0,0,0,$timeArr['month'],$timeArr['day'],$timeArr['year']);
                return $time;
            }
            $pat = '/\d+\W\d+\W\d+\s+\d+\:\d+\:\d+/';
            preg_match($pat, $time, $mat);
            if(!array_key_exists('0', $mat)){
                if(!$mat[0]){
                    $pat2 = '/\d+\W\d+\W\d+/';
                    preg_match($pat2, $time, $mat);
                }
            }
            return array_key_exists('0', $mat) ? strtotime($mat[0]) : '';
        case 'author':
            $start = $nodeInfo['author_start'];
            $end = $nodeInfo['author_end'];
            if($start == '' || $end == '') return '';
            $body = getNewHtml($start, $end, $html);
            $author = deleteHtml($body);
            preg_match("/\"/", $author, $mat_au);
            if(!$mat_au){
                return $author;
            }else{
                return getChinese($author);
            }
        default:
            return false;
    }
}

/**
 * 获取各个内容的公用方法
 * @param $start
 * @param $end
 * @param $html
 * @return bool|string
 */
function getNewHtml($start, $end, $html)
{
    $start = rtrim($start);
    $end = rtrim($end);
    if($start == '' || $end =='') return '';
    //删除开始标签之前的字符  包括开始标记本身
    $left_str_index = strpos($html, $start);
    if(!$left_str_index)  return '';
    $start_left_html = substr($html,0, $left_str_index+strlen($start));  //开始标签左边的html
    $start_right_html = str_replace($start_left_html, "", $html);  // 删掉左边 剩下右边

    $starts = strpos($start_right_html, $start);
    if(!$starts){
        $ends = strpos($start_right_html, $end);
        $bodys = substr($start_right_html, $starts, $ends);
    }else{
        $ends = strpos($start_right_html, $end);
        $bodys = substr($start_right_html, $starts, $ends-$starts);
    }

    return $bodys;
}


/**
 * 获取节点下面的url
 * @param $node_id
 * @return array
 */
function getUrl($node_id, $page){
    global $dsql;
    $sql = "select * from `#@__site_plugins_spider_urls` where node_id = $node_id AND is_get = 1 limit $page";
    $sqls = $dsql->SetQuery($sql);
    $res = $dsql->dsqlOper($sqls, "results");
    return $res;
}

function getUrlSum($node_id){
    global $dsql;
    $sql = "select * from `#@__site_plugins_spider_urls` where node_id = $node_id";
    $sqls = $dsql->SetQuery($sql);
    $res = $dsql->dsqlOper($sqls, "totalCount");
    return $res;
}
function getUrlSum2($node_id){
    global $dsql;
    $sql = "select * from `#@__site_plugins_spider_urls` where node_id = $node_id AND is_get in (2,3)";
    $sqls = $dsql->SetQuery($sql);
    $res = $dsql->dsqlOper($sqls, "totalCount");
    return $res;
}
/**
 * 获取节点body规则信息
 * @param $id
 * @return array
 */
function getBodyRules($id)
{
    global $dsql;
    $sql = "select * from `#@__site_plugins_spider_node_rules` where node_id = $id";
    $sqls = $dsql->SetQuery($sql);
    $res = $dsql->dsqlOper($sqls, "results");
    return isset($res[0]) ? $res[0] :'';
}
