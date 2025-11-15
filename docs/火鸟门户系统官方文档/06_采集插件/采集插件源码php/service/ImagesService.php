<?php
require_once 'HttpDownService.php';

/**
 * html文本图片处理
 * Class ImagesService
 */
class ImagesService
{

    public $body;
    public $node;
    public $urlId;

    public function __construct($body, $node, $urlId)
    {
        $this->body  = $body;
        $this->node  = $node;
        $this->urlId = $urlId;
    }

    /**
     * @return bool|mixed|string
     */
    public function getNewsContent()
    {
        $imgs = $this->htmlImgs($this->body);
        if (empty($imgs)) return false;
        $imgNewPath = $this->downloadImg($imgs);
        $newBody    = $this->repBodyImg($imgNewPath, $imgs);
        return $newBody;
    }

    /**
     * 获取指定html中的图片
     * @param $html
     * @return array
     */
    public function htmlImgs($html = '')
    {
        $imgs = array();
        if (empty($html)) return $imgs;
        preg_match_all("/<img[^>]+>/i", $html, $img);
        if (empty($img)) return $imgs;
        $img = $img[0];
        foreach ($img as $g) {
            $g = preg_replace("/^<img|>$/i", '', $g);    //移除二头字符
            //空格 src 可能空格 = 可能空格 "非"" 或 '非'' 或 非空白 这几种可能,下同
            preg_match("/\ssrc\s*\=\s*\"([^\"]+)|\ssrc\s*\=\s*'([^']+)|\ssrc\s*\=\s*([^\"'\s]+)/i", $g, $src);
            $src = empty($src) ? '' : $src[count($src) - 1];  //匹配到,总会放在最后
            if (empty($src)) { //空的src 没用,跳过
                continue;
            }
            $imgs[] = $src;
        }
        return $imgs;
    }

    /**
     * 下载图片到本地并且按顺序返回新的路径
     * @param $file_url
     * @return array
     */
    public function downloadImg($file_url)
    {
        $arr = [];
        $save_path =  HUONIAOROOT . '/uploads/plugins/'. date("Y") .'/'. date("m") . '/' . date("d") . '/' . 'node_' . $this->node . '/' . 'url_' . $this->urlId . '/';

        foreach ($file_url as $k => $item) {
            $file_name     = $k . '.png';

            $save_img_path =  $save_path;
            $path          = $this->curlDownFile($item, $save_img_path, $file_name);
            $arr[]         = $path;
        }


        return $arr;
    }



    /**
     * @param string $img_url 下载文件地址
     * @param string $save_path 下载文件保存目录
     * @param string $filename 下载文件保存名称
     * @return bool
     */
    public function curlDownFile($img_url, $save_path = '', $filename = '')
    {
      	global $cfg_secureAccess;
      	global $cfg_basehost;
      
        if (trim($img_url) == '') {
            return false;
        }
        if (trim($save_path) == '') {
            $save_path = './';
        }
        //创建保存目录
        if (!file_exists($save_path) && !mkdir($save_path, 0777, true)) {
            return false;
        }
//        // curl下载文件
//        $ch      = curl_init();
//        $timeout = 5;
//        curl_setopt($ch, CURLOPT_URL, $img_url);
//        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
//        curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, $timeout);
//        curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
//        $img = curl_exec($ch);
//        curl_close($ch);
        /* 下载文件 */

        $path = $save_path . $filename;

        $httpdown = new HttpDownService();
        $httpdown->OpenUrl($img_url); # 远程文件地址
        $httpdown->SaveToBin($path); # 保存路径及文件名

        // 保存文件到制定路径
//        if (!file_exists($path)) {
//            file_put_contents($path, $img);
//        }
        //http://cg.215000.com/include/plugins/3/img/
        $newsPath = '/include/attachment.php?f=/plugins/'. date("Y") .'/'. date("m") . '/' . date("d") . '/node_' . $this->node . '/url_' . $this->urlId .'/'. $filename;

        unset($img, $url);
        return $newsPath;
    }

    /**
     * 替换html中的图片链接为本地的链接  返回最后经过处理的body
     * @param $newSrc
     * @param $oldSrc
     * @return mixed|string
     */
    public function repBodyImg($newSrc, $oldSrc)
    {
        $newBody = '';
        foreach ($oldSrc as $k => $old) {
            if ($k == 0) {
                $newBody = str_replace($old, $newSrc[$k+1], $this->body);
            } else {
                $newBody = str_replace($old, $newSrc[$k+1], $newBody);
            }
        }
        return $newBody . '||' . $newSrc[0];
    }
}
