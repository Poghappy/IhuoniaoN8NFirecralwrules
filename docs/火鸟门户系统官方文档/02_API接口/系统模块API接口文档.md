火鸟门户
火鸟门户API接口使用文档
（系统模块）
[Huoniao. API. OpenAPI. siteConfig]
1 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
修订记录：
版本 修订记录 修订人 修订时间
v1.0.0 1.文档创建 郭永顺 2014-3-20
V1.0.1 2.增加【城市地铁】 郭永顺 2015-1-14
V1.0.2 3.增加【热门关键词】 郭永顺 2015-2-10
V1.0.3 4.增加【判断验证码是否输入正确】 郭永顺 2015-6-7
2 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
目录：
一、 接口说明：……………………………………………………………………………………………………………………………………………………………………………………………………5
1.1 系统模块…………………………………………………………………………… 5
1.1 .1 系统基本参数……………………………………………… 5
1.1 .2 安全配置参数……………………………………………… .7
1.1 .3 支付方式…………………………………………………………… 8
1.1 .4 网站地区…………………………………………………………… ..8
1.1 .5 城市地铁………………………………………………………… …9
1.1 .6 已安装模块信息………………………………………… ……………10
1.1 .7 热门关键词………………………………………………… … …………11
1.1 .8 单页文档……………………………………………………… ……………………………………………………………………………………………………12
1.1 .9单页文档详细信息…………………………………… ………………12
1.1 .10 网站公告………………………………………………………… ………16
1.1 .11 网站公告详细信息………………………………… ……………14
1.1 .12 帮助信息……………………………………………………… ………………14
1.1 .13 帮助信息详细信息…………………………………… …………13
1.1 .14 帮助信息分类……………………………………………… ……………16
1.1 .15 网站协议…………………………………………………………… …………………17
1.1 .16 网站广告…………………………………………………………… …………18
1.1 .17 友情链接分类……………………………………………… ……………………………………20
1.1 .18 友情链接………………………………………………………… ………………………………………21
3 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
1.1 .19 发送邮件……………………………………………………………………………………………………………………………………………………………………………22
1.1 .20 发送短信……………………………………………………………………………………………………………………………………………………………………22
1.1 .21 判断验证码是否正确……………………………………………………………………………………………………………………………………………22
4 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
一、 接口说明：
使用方法：
$ handels = new handlers($ service, $ action);
$ handels->getHandle($ param);
参数： 参数名称 描述 是否必传 类型 取值说明
service 服务名 是 string 即模块名
action 动作名 是 string 具体要做什么操作
param 其它参数 否 array 更细化的操作
返回： 类型 参数 类型 说明
array state int 状态码：100（成功）101（错误）200（失败）
info array 内容
1.1 系统模块
服务名：siteConfig
1.1 .1 系统基本参数
动作名：config
其 它：param（这个值为元素名，如果传入此值则只返回此元素的值，支持传入多个值，不传则返回所有）
参数 是否必传 类型 说明
param 否 string 多个值由“，”分隔
5 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
返回参数信息：
参数名 描述 类型 说明
baseHost 网站域名 string
webName 网站名称 string
fileUrl 默认附件地址 string
webLogo 网站logo地址 string
keywords 网站关键字 string
description 网站描述 string
beian 网站ICP备案号 string
hotline 咨询热线 string
powerby 网站版权信息 string
statisticscode 统计代码 string
visitState 网站运营状态 int 0：启用 1：禁用
visitMessage 禁用时的说明信息 string
timeZone 网站默认时区 int
mapCity 地图默认城市 string 城市中文名称
softSize 附件上传限制大小 int
softType 附件上传类型限制 string
thumbSize 缩略图上传限制大小 int
thumbType 缩略图上传类型限制 string
atlasSize 图集上传限制大小 int
atlasType 图集上传类型限制 string
photoSize 头像上传限制大小 int
photoType 头像上传类型限制 string
6 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
1.1 .2 安全配置参数
动作名：safe
其 它：param（这个值为元素名，如果传入此值则只返回此元素的值，支持传入多个值，不传则返回所有）
参数 是否必传 类型 说明
param 否 string 多个值由“，”分隔
返回参数信息：
参数名 描述 类型 说明
regstatus 会员注册开关 int 0：开启 1：关闭
regclosemessage 会员注册关闭原因 string
replacestr 敏感词过滤 string 多个会以“|”分隔
seccodestatus 启用验证码的功能 string 多个会以“，”分隔
secqaastatus 启用验证问题的功能 string 多个会以“，”分隔
safeqa 验证问题数据 array 见下表
验证问题数量格式：
参数 类型 说明
safeqa array [ { " id": "1"," question": "1+1=?"," answer": "2"},…]
7 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
1.1 .3 支付方式
动作名 : payment
返回信息：
[
{
" id": "1",
" pay code": " alipay",
" pay name": "支付宝在线支付“，
" pay desc": "支付宝在线支付说明“
},
…
]
返回参数说明：
参数名 描述 类型 说明
id 支付方式ID int
pay code 支付方式代表CODE string
pay name 支付方式名称 string
pay desc 支付方式说明 string
1.1 .4 网站地区
动作名：addr
其 它：param
参数 是否必传 类型 说明
param 否 int 分类ID（传入此值则只返回此ID的下级分类）
返回信息：
[
{
8 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 http://www.ikuman.cn

火鸟门户
" id": "1",
" parentid": "0",
" typename": "吴中区“，
" lower": [
{
" id": "2",
" parentid": "1",
" typename": "东山镇“，
" lower": []
},
…
]
},
…
]
返回参数说明：
参数名 描述 类型 说明
id 分类ID int
parentid 上级ID int
typename 分类名称 string
lower 下级分类 array 结构与上级相同
1.1 .5 城市地铁
动作名：subway
其 它：param
参数 是否必传 类型 说明
param 否 int 站点ID（传入此值则只返回此ID的下级分类）
返回信息：
[
{
" id": "1",
9 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 http://www.ikuman.cn

火鸟门户
" parentid": "0",
" typename": "1号线“，
" lower": [
{
" id": "2",
" parentid": "1",
" typename": "木渎“
},
…
]
},
…
]
返回参数说明：
参数名 描述 类型 说明
id 分类ID int
parentid 上级ID int
typename 站点名称 string
lower 下级分类 array 结构与上级相同
1.1 .6 已安装模块信息
动作名：module
返回信息：
[
{
" id": "1",
" icon": " article. png",
" title": "新闻“，，
" name": " article"
},
…
]
10 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
返回信息说明：
参数名 描述 类型 说明
id 模块ID int
icon 模块图标 string 所在目录：/ static/ images/ admin/ nav/
title 模块名称 string
name 模块英文名 string
1.1 .7 热门关键词
动作名 : hotkeywords
其 它：param（支持以下参数）
param 参数 是否必传 类型 说明
module 是 string 模块标识
返回信息：
[
{
" href": " http://m.menhu168.com/ info/ search-最美农家乐.html",
" target": "0",
" keyword": "< font color="#92d050">< strong>最美农家乐"},
…
]
返回信息说明：
参数名 描述 类型 说明
href 访问链接 string
target 打开方式 int 0：新窗口 1：本窗口
keyword 关键词 string 包含html代码【颜色、加粗】
11 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
1.1 .8 单页文档
动作名：singel
返回信息：
[
{
" id": "1",
" title": "公司简介“
},
…
]
返回信息说明：
参数名 描述 类型 说明
id 文档ID int
title 文档标题 string
1.1 .9单页文档详细信息
动作名：singelDetail
其 它：param
参数 是否必传 类型 说明
param 是 int 文档ID
返回参数信息：
参数名 描述 类型 说明
title 文档名称 string
body 文档内容 string
pubdate 发布时间 int Linux时间截
12 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
1.1 .10 网站公告
动作名：notice
其 它：param（支持以下参数）
param 参数 是否必传 类型 说明
page 否 int 页码
pageSize 否 int 每页显示数量
返回信息：
"pageInfo": {
" page":1,
"pageSize":10,
"totalPage":1,
"totalCount":2
},
" list": [
{
" id": "12",
" title": "公告标题“，
" color": "#ff0000",
" redirect": " http:// www.baidu.com",
" pubdate": "1395384998"
},
…
]
返回信息说明：
参数名 描述 类型 说明
pageInfo 页码参数 array
page 当前页码 int
pageSize 每页显示数 int
13 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
totalPage 总页数 int
totalCount 总记录数 int
list 公告列表 array
id 公告ID int
title 公告标题 string
color 标题颜色 string
redirect 跳转地址 string
pubdate 发布时间 int Linux时间戳
1.1 .11 网站公告详细信息
动作名：noticeDetail
其 它：param
参数 是否必传 类型 说明
param 是 int 公告ID
返回参数信息：
参数名 描述 类型 说明
title 公告标题 string
color 标题颜色 string #ff0000
redirecturl 跳转地址 string http:// <www.xxx.com>
body 文档内容 string
pubdate 发布时间 int Linux时间截
1.1 .12 帮助信息
动作名 : helps
14 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
其 它:param（支持以下参数）
param 参数 是否必传 类型 说明
typeid 否 int 分类ID
page 否 int 页码
pageSize 否 int 每页显示数量
返回信息：
"pageInfo": {
" page":1,
"pageSize":10,
"totalPage":1,
"totalCount":1
},
" list": [
{
" id": "20",
" title": " aaaaa",
" pubdate": "1395386401"
},
…
]
返回信息说明：
参数名 描述 类型 说明
pageInfo 页码参数 array
page 当前页码 int
pageSize 每页显示数 int
totalPage 总页数 int
totalCount 总记录数 int
list 信息列表 array
id 信息ID int
15 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
title 信息标题 string
pubdate 发布时间 int Linux时间戳
1.1 .13 帮助信息详细信息
动作名 : helpsDetail
其 它：param
参数 是否必传 类型 说明
param 是 int 公告ID
返回参数信息：
参数名 描述 类型 说明
title 信息标题 string
typeid 所属分类 int
body 信息内容 string
pubdate 发布时间 string Linux时间截
1.1 .14 帮助信息分类
动作名：helpsType
其 它：param
参数 是否必传 类型 说明
param 否 int 分类ID（传入此值则只返回此ID的下级分类）
返回信息：
[
{
16 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 http://www.ikuman.cn

火鸟门户
" id": "1",
" parentid": "0",
" typename": "新手帮助“，
" lower": [
{
" id": "2",
" parentid": "1",
" typename": "会员中心帮助“，
" lower": []
},
…
]
},
…
]
返回信息说明：
参数名 描述 类型 说明
id 分类ID int
parentid 上级ID int
typename 分类名称 string
lower 下级分类 array 结构与上级相同
1.1 .15 网站协议
动作名：agree
其 它：param
参数 是否必传 类型 说明
param 是 int 协议ID
返回参数信息：
参数名 描述 类型 说明
17 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
title 协议名称 string
body 协议内容 string
1.1 .16 网站广告
动作名：adv
其 它：param
参数 是否必传 类型 说明
param 是 int 广告ID
返回参数信息：
普通广告：
参数名 描述 类型 说明
class 广告类型 int 固定值：1
type 类型 string code text pic flash
代码类型【code】
body 代码内容 string
文字类型【text】
title 文字内容 string
color 文字颜色 string
link 文字链接 string
size 文字大小 int
图片类型【pic】
src 图片地址 string
href 图片链接 string
title 图片名称 string
width 图片宽度 int
18 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
height 图片高度 int
动画类型【flash】
src Flash地址 string
width Flash宽度 int
height Flash高度 int
多图广告：
参数名 描述 类型 说明
class 广告类型 int 固定值：2
width 宽度 int
height 高度 int
list 图片列表 array
src 图片地址 string
title 图片名称 string
link 图片链接 string
desc 图片说明 string
伸缩广告：
参数名 描述 类型 说明
class 广告类型 int 固定值：3
time 显示时间 int
width 广告宽度 int
link 链接地址 string
large 大图地址 string
largeHeight 大图高度 int
small 小图地址 string
smallHeight 小图高度 int
对联广告：
19 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
参数名 描述 类型 说明
class 广告类型 int 固定值：4
width 页面宽度 int
adwidth 广告宽度 int
adheight 广告高度 int
topheight 距离顶部 int
left 左边
src 附件地址 string
link 链接地址 string
title 替换文字 string
right 右边
src 附件地址 string
link 链接地址 string
title 替换文字 string
1.1 .17 友情链接分类
动作名：friendLinkType
其 它：param
参数 类型 说明
module string 所属模块
返回信息：
[
{
" id": "1",
" typename": "合作伙伴“
},
…
20 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 http://www.ikuman.cn

火鸟门户
]
返回参数说明：
参数名 描述 类型 说明
id 分类ID int
typename 分类名称 string
1.1 .18 友情链接
动作名：friendLink
其 它：param
param 参数 类型 说明
module string 所属模块
type int 可选，默认返回所有，否则返回分类下所有信息
返回信息：
[
{
" id": "1",
" sitename": "链接名称“，
" sitelink": "链接地址“，
" litpic": "网站LOGO"
},
…
]
返回参数说明：
参数名 描述 类型 说明
id 链接ID int
sitename 链接名称 string
21 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
sitelink 链接地址 string
litpic IOGO地址 string
1.1 .19 发送邮件
动作名：sendMail
其 它：param
param 参数 类型 说明
email string 收件人，多个用“，”分隔
mailtitle string 邮件标题
mailbody string 邮件内容
返回参数信息：
参数名 描述
无 成功直接返回“发送成功！”字样。
1.1 .20 发送短信
动作名：sendSMS
1.1 .21 判断验证码是否正确
动作名：checkVdimgck
其 它：param
22 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
param 参数 类型 说明
code string 需要验证的字符
返回参数信息：
参数名 描述
无 error:输入错误 ok：输入正确
23 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>
