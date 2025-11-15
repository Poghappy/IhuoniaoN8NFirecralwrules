<?php
require_once('../../common.inc.php');
require_once 'service/HttpDownService.php';

function autoget($type, $body ){

    if(!empty($type) && !empty($body)){

        $title = $keywords = $description = "";
        $return = AnalyseHtmlBody($body, $description, $keywords);

        if($type == "keywords"){
            return $keywords;
        }else{
            return $description;
        }

    }
}


/**
 * 下载页面
 * @param $dourl
 * @return string
 */
function downOnePage($dourl)
{
    $http = new HttpDownService();
    $http->OpenUrl($dourl);
    $html = $http->GetHtml();
    $html = strToUtf8($html);
    return $html;
}


/**
 * 判断当前域名是否为https
 */
function is_https() {
    if ( !empty($_SERVER['HTTPS']) && strtolower($_SERVER['HTTPS']) !== 'off') {
        return true;
    } elseif ( isset($_SERVER['HTTP_X_FORWARDED_PROTO']) && $_SERVER['HTTP_X_FORWARDED_PROTO'] === 'https' ) {
        return true;
    } elseif ( !empty($_SERVER['HTTP_FRONT_END_HTTPS']) && strtolower($_SERVER['HTTP_FRONT_END_HTTPS']) !== 'off') {
        return true;
    }
    return false;
}

/**
 * 判断是否为post
 */
if(!function_exists('is_post')){
    function is_post()
    {
        return isset($_SERVER['REQUEST_METHOD']) && strtoupper($_SERVER['REQUEST_METHOD'])=='POST';
    }
}

/**
 * 判断是否为get
 */
if(!function_exists('is_get')){
    function is_get()
    {
        return isset($_SERVER['REQUEST_METHOD']) && strtoupper($_SERVER['REQUEST_METHOD'])=='GET';
    }
}

/**
 * 判断是否为ajax
 */
if(!function_exists('is_ajax')){
    function is_ajax()
    {
        return isset($_SERVER['HTTP_X_REQUESTED_WITH']) && strtoupper($_SERVER['HTTP_X_REQUESTED_WITH'])=='XMLHTTPREQUEST';
    }
}

/**
 * 判断是否为命令行模式
 */
if(!function_exists('is_cli')){
    function is_cli()
    {
        return (PHP_SAPI === 'cli' OR defined('STDIN'));
    }
}

/**
 * 解析多维数组中的json
 * @param $arrs
 * @return array
 */
function changeJsonToArr($arrs)
{
    static $tmp = [];
    foreach ($arrs as $arr){
        if(is_array($arr)){
            foreach ($arr as $v){
                $_arr = json_decode($v, true);
                if(is_array($_arr)){
                    $tmp[] = $_arr;
                }
            }
        }else{
            $_arr = json_decode($arr, true);
            $tmp[] = $_arr;
        }
    }
    return $tmp;
}


/**
 * 将多维数组转换成一维数组
 * @param $arr
 * @return array
 */
function changeArr($arr) {
    static $tmp = array();

    foreach ($arr as $val )
    {
        if (is_array ($val))
        {
            changeArr ($val);
        }
        else
        {
            $tmp[]=$val;
        }
    }

    return $tmp;
}


/**
 * 正则匹配json
 * @param $str
 * @return mixed
 */
function json_reg($str) {
    echo '<xmp>';

    //基础元素
    $r_int   = '-?\d+'; //整数: 100, -23
    $r_blank = '\s*'; //空白
    $r_obj_l = '\\{'.$r_blank; // {
    $r_obj_r = $r_blank.'\\}'; // }
    $r_arr_l = '\\['.$r_blank; // [
    $r_arr_r = $r_blank.'\\]'; // [
    $r_comma = $r_blank.','.$r_blank; //逗号
    $r_colon = $r_blank.':'.$r_blank; //冒号

    //基础数据类型
    $r_str   = '"(?:\\\\"|[^"])+"';  //双引号字符串
    $r_num   = "{$r_int}(?:\\.{$r_int})?(?:[eE]{$r_int})?"; //数字(整数,小数,科学计数): 100,-23; 12.12,-2.3; 2e9,1.2E-8
    $r_bool  = '(?:true|false)'; //bool值
    $r_null  = 'null'; //null

    //衍生类型
    $r_key = $r_str; //json中的key
    $r_val = "(?:(?P>json)|{$r_str}|{$r_num}|{$r_bool}|{$r_null})"; //json中val: 可能为 json对象,字符串,num, bool,null
    $r_kv  = "{$r_key}{$r_colon}{$r_val}"; //json中的一个kv结构

    $r_arr = "{$r_arr_l}{$r_val}(?:{$r_comma}{$r_val})*{$r_arr_r}"; //数组: 由val列表组成
    $r_obj = "{$r_obj_l}{$r_kv}(?:{$r_comma}{$r_kv})*{$r_obj_r}";   //对象: 有kv结构组成

    $reg = "/(?<json>(?:{$r_obj}|{$r_arr}))/is";  //数组或对象
    // echo $reg, "\n"; //最终正则表达式

    preg_match_all($reg, $str, $arr);
    return $arr;
}

/**
 * 返回json(结束脚本)
 * @param $arr
 */
function returnJson($arr)
{
    if(!array_key_exists('code', $arr) || !array_key_exists('msg', $arr))
        die('returnJson error');
    $data = array_key_exists('data', $arr) ? $arr['data'] : '';
    header('Content-Type: application/json');
    die(json_encode([ 'code' => $arr['code'], 'msg' => $arr['msg'], 'data' => $data ], JSON_UNESCAPED_UNICODE));
}



/**
 * print_r
 * @param $str
 */
function ddArr($str)
{
    echo '<pre>';
    print_r($str);
}


/**
 * 验证是否是url
 * @param  string  $url   url
 * @return boolean        是否是url
 */
function is_url($url){
    if(filter_var($url,FILTER_VALIDATE_URL)){
        return true;
    }else{
        return false;
    }
}

/**
 * 转换utf8
 * @param $str
 * @return string
 */
function strToUtf8($str)
{
    $encode = mb_detect_encoding($str, array('GB2312','GBK','UTF-8', 'BIG5')); //得到字符串编码
    $str = iconv($encode, 'UTF-8', $str);
    return $str;
}

/**
 * 获取汉字
 * @param $str
 * @return string
 */
function getChinese($str){
    $tmp = '';
    if($str == '') return $tmp;
    preg_match_all("/[\x{4e00}-\x{9fa5}]+/u", $str, $title);
    if(is_array($title)){
        if(array_key_exists('0', $title)){
                foreach ($title[0] as $s){
                    $tmp .= $s;
                }
        }
    }else{
        $tmp = $title;
    }
    return $tmp;
}

/**
 * 删除html
 * @param $str
 * @return string
 */
function deleteHtml($str)
{
    if($str == '') return '';
    $str = trim($str); //清除字符串两边的空格
    $str = strip_tags($str,""); //利用php自带的函数清除html格式
    $str = preg_replace("/\t/","",$str); //使用正则表达式替换内容，如：空格，换行，并将替换为空。
    $str = preg_replace("/\r\n/","",$str);
    $str = preg_replace("/\r/","",$str);
    $str = preg_replace("/\n/","",$str);
    $str = preg_replace("/ /","",$str);
    $str = preg_replace("/  /","",$str);  //匹配html中的空格
    return trim($str); //返回字符串
}

/**
 * curl get
 * @param string $url
 * @return mixed
 */
function curl_get($url = '')
{
    $curl = curl_init();
    curl_setopt($curl, CURLOPT_URL, $url);
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1); //成功只将结果返回，不自动输出任何内容 失败返回FALSE
    curl_setopt($curl, CURLOPT_HEADER, false);

    if(strstr($url, "https")){
        curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
    }
    $str = curl_exec($curl);
    curl_close($curl);
    return $str;
}

function curl_get_copy($url = '')
{
    $ip = mt_rand(11, 191).".".mt_rand(0, 240).".".mt_rand(1, 240).".".mt_rand(1, 240);   //随机ip
    $agentarry = [
        //PC端的UserAgent
        "safari 5.1 – MAC"=>"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "safari 5.1 – Windows"=>"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Firefox 38esr"=>"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
        "IE 11"=>"Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
        "IE 9.0"=>"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0",
        "IE 8.0"=>"Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
        "IE 7.0"=>"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "IE 6.0"=>"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
        "Firefox 4.0.1 – MAC"=>"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Firefox 4.0.1 – Windows"=>"Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera 11.11 – MAC"=>"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera 11.11 – Windows"=>"Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Chrome 17.0 – MAC"=>"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "360浏览器"=>"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
        "搜狗浏览器 1.x"=>"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
        "Avant"=>"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
        "Green Browser"=>"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        //移动端口
        "safari iOS 4.33 – iPhone"=>"Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "safari iOS 4.33 – iPod Touch"=>"Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "safari iOS 4.33 – iPad"=>"Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Android N1"=>"Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Android QQ浏览器 For android"=>"MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Android Opera Mobile"=>"Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
        "Android Pad Moto Xoom"=>"Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
        "BlackBerry"=>"Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
        "WebOS HP Touchpad"=>"Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
        "UC标准"=>"NOKIA5700/ UCWEB7.0.2.37/28/999",
        "UCOpenwave"=>"Openwave/ UCWEB7.0.2.37/28/999",
        "UC Opera"=>"Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
        "微信内置浏览器"=>"Mozilla/5.0 (Linux; Android 6.0; 1503-M02 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/37.0.0.0 Mobile MQQBrowser/6.2 TBS/036558 Safari/537.36 MicroMessenger/6.3.25.861 NetType/WIFI Language/zh_CN",
    ];
    $useragent = $agentarry[array_rand($agentarry,1)];
    $header = array(
        'CLIENT-IP:'.$ip,
        'X-FORWARDED-FOR:'.$ip,
    );    //构造ip
    $referurl = parse_url($url);
    $referurl = $referurl['host'];

    $curl = curl_init();
    curl_setopt($curl, CURLOPT_URL, $url);
    curl_setopt($curl, CURLOPT_HTTPHEADER, $header);
    curl_setopt($curl, CURLOPT_USERAGENT, $useragent);  //模拟常用浏览器的useragent
    curl_setopt($curl, CURLOPT_REFERER, $referurl);  //模拟来源网址
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, 1); //成功只将结果返回，不自动输出任何内容 失败返回FALSE
    curl_setopt($curl, CURLOPT_HEADER, false);

    if(strstr($url, "https")){
        curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
    }
    $str = curl_exec($curl);
    curl_close($curl);
    return $str;
}
/**
 * 去除script标签
 * @param $string
 * @return null|string|string[]
 */
function delScript($string){
    if($string == '') return '';
    $string = preg_replace('/<script[^>]*?>.*?<\/script>/is',"",$string);
    return $string;
}