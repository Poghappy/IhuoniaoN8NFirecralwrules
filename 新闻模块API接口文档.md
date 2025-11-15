火鸟门户
火鸟门户API接口使用文档 （新闻模块）
[ Huoniao. API. OpenAPI. article]
l 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 http://www.ikuman.cn

火鸟门户
修订记录：
版本 修订记录 修订人 修订时间
v1.0.0 1.文档创建 郭永顺 2014-3-22
V1.0.1 2.信息列表增加多个筛选参数 郭永顺 2014-5-6
V1.0.2 3.信息内容增加移动端字段：mbody 郭永顺 2014-6-11
V1.0.3 4.修改评论返回内容，增加多级评论格式以及更详细的会员数据 郭永顺 2015-3-9
V1.0.4 5.新增【发布投稿】6.新增【修改投稿】7.新增【删除信息】 郭永顺 2015-7-1
2 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 http://www.ikuman.cn

火鸟门户
目录：
一、 接口说明：…………………………………………………………………………………………………………………………………………………………………………………………………4
1.1 . 新闻管理…………………………………………………………………… 4
1.1 .1 新闻基本参数…………………………………………… .4
1.1 .2 新闻分类……………………………………………………… .5
1.1 .3新闻分类详细信息………………………………… ……………7
1.1 .4 新闻列表…………………………………………………………… …………8
1.1 .5 新闻详细信息…………………………………………… ……11
1.1 .6 新闻评论……………………………………………………… …12
1.1 .7 发表新闻评论……………………………………………… ……………………………………………………………………………………14
1.1 .8 发布投稿………………………………………………………………………………………………………………………………………………………………………………15
1.1 .9 修改投稿……………………………………………………… ………………………………………………………………………………………16
1.1 .10 删除投稿…………………………………………………… ……………………………………………………………………………………………………17
3 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 http://www.ikuman.cn

火鸟门户
一、 接口说明：
服务名：article
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
1.1 .新闻管理
1.1 .1 新闻基本参数
动作名：config
其 它：param（这个值为元素名，如果传入此值则只返回此元素的值，支持传入多个值，不传则返回所有）
参数 是否必传 类型 说明
param 否 string 多个值由“，”分隔
4 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 http://www.ikuman.cn

火鸟门户
返回参数信息：
参数名 描述 类型 说明
channelName 模块名称 string
logoUrl logo地址 string
subDomain 访问方式 int 0：主域名 1：子域名 2：子目录
channelDomain 绑定的域名 string
channelSwitch 模块开关 int 0：启用 1：禁用
closeCause 模块禁用说明 string
title seo标题 string
keywords seo关键字 string
description seo描述 string
hotline 咨询热线 string
atlasMax 图集数量限制 int
template 风格模板 string
softSize 附件上传限制大小 int
softType 附件上传类型限制 string
thumbSize 缩略图上传限制大小 int
thumbType 缩略图上传类型限制 string
atlasSize 图集上传限制大小 int
atlasType 图集上传类型限制 string
1.1 .2 新闻分类
动作名：type
其 它：param
param 参数 是否必传 类型 说明
type 否 int 分类ID
5 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 http://www.ikuman.cn

火鸟门户
page 否 int 页码
pageSize 否 int 每页显示数量
返回信息：
[
{
" id": "1",
" parentid": "0",
" typename": "国内新闻“，
" url": " http://m.menhu168.com/ news/ article-list-1-1.html",
" lower": [
{
" id": "2",
" parentid": "1",
" typename": "苏州新闻“，
" url": " http://m.menhu168.com/ news/ article-list-2-1.html",
" lower": []
},
……
]
},
…
]
返回参数说明：
参数名 描述 类型 说明
id 分类ID int
parentid 上级ID int
typename 分类名称 string
url 分类访问地址 string
lower 下级分类 array 结构与上级相同
6 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 http://www.ikuman.cn

火鸟门户
1.1 .3新闻分类详细信息
动作名：typeDetail
其 它：param
参数 是否必传 类型 说明
param 是 int 分类ID
返回信息：
[
{
" id": "5",
" typename": "苏州新闻“，
" seotitle": " seo标题“，
" keywords": " seo关键字“，
" description": " seo描述“，
" url": " http://m.menhu168.com/ news/ article-list-5-1.html"},
…
]
返回参数说明：
参数名 描述 类型 说明
id 分类ID int
typename 分类名称 string
seotitle SEO标题 string
keywords SEO关键字 string
description SEO描述 string
url 分类访问地址 string
7 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 http://www.ikuman.cn

火鸟门户
1.1 .4 新闻列表
动作名 : alist
其 它：param（支持以下参数）
param 参数 是否必传 类型 说明
typeid 否 int 分类ID
title 否 string 信息标题（支持模糊查询）
flag 否 string 自定义属性空：不限 h：头条 r：推荐b : 加粗 t：跳转
thumb 否 int 缩略图选项0：不包含 1：包含
orderby 否 int 排序： 0：默认排序1：发布时间 2：浏览量3：随机 4：评论2.1：今日浏览量 4.1：今日评论量2.2：昨日浏览量 4.2：昨日评论量2.3：本周浏览量 4.3：本周评论量2.4：本月浏览量 4.4：本月评论量
u 否 int 为1时表示只列出当前登录会员的所有信息
state 否 int 空：全部 0：未审核1：已审核 2：审核拒绝
page 否 int 页码
8 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 http://www.ikuman.cn

火鸟门户
pageSize 否 int 每页显示数量
返回信息：
"pageInfo": {
" page":1,
"pageSize":10,
"totalPage":1,
"totalCount":2,
" gray":3,
" audit":25,
" refuse":1
},
" list": [
{
" id": "2",
" title": "信息标题“，
" subtitle": "信息短标题“，
" typeid": "9",
"typeName": "经济-公司“，
" flag": "r,b,p",
" keywords": "关键字“，
" description": "描述“，
" source": "来源“，
" redirecturl": "",
" litpic": "VWowR1kxVXk=",
" color": "#ff0000",
" click": "892",
" arcrank": "1",
" pubdate": "1395485308",
" common": "5168",
" url": " http://m.menhu168.com/ news/ article-detail-126.html",
" group img": [
{
" path": " http://m.menhu168.com/ include/ attachment.php?f=QldsY01c9",
" info": "图片说明“
},
……
]
},
……
]
9 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 http://www.ikuman.cn

火鸟门户
返回参数说明：
参数名 描述 类型 说明
pageInfo 页码参数 array
page 当前页码 int
pageSize 每页显示数 int
totalPage 总页数 int
totalCount 总记录数 int
gray 未审核 int 这三项只有在会员中心处显示
audit 已审核 int
refuse 审核拒绝 int
list 信息列表 array
id 信息ID int
title 信息标题 string
subtitle 信息短标题 string
typeid 信息分类ID int
typeName 分类名称 string 子级由“-”分隔
flag 信息属性 string 多个由“，”分隔h：头条 r：推荐b：加粗 p：图文t：跳转
keywords 关键词 string
description 描述 string
source 来源 string
redirecturl 跳转URL string
litpic 缩略图 string
color 标题颜色 string
click 浏览次数 int
arcrank 状态 int 0未审核 1已审核 2审核拒绝
10 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 http://www.ikuman.cn

火鸟门户
pubdate 发布时间 int Linux时间戳
common 评论数量 int
url 访问链接 string
group img 图集 array
path 图片地址 string
info 图片说明 string
1.1 .5 新闻详细信息
动作名：detail
其 它：param
参数 是否必传 类型 说明
param 是 int 信息ID
返回参数信息：
参数名 描述 类型 说明
id 信息ID int
title 信息标题 string
subtitle 短标题 string
flag 信息属性 string 多个由“，”分隔h：头条 r：推荐b：加粗 p：图文t：跳转
redirecturl 跳转URL string
litpic 缩略图 string
litpicSource 缩略图加密信息 string
source 来源 string
11 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 http://www.ikuman.cn

火鸟门户
sourceurl 来源网址 string
writer 作者 string
typeid 分类ID int
typeName 分类名称 string 多级分类中间由“>”分隔
body 信息内容 text
mbody 移动端信息内容 text
imglist 信息图集 array [ { "pathSource": "加密地址", " path": "图片地址“，” info”：”图片说明“}，…]
keywords 关键字 string
description 描述 string
notpost 评论开关 int 0：开启 1：关闭
click 阅读次数 int
color 标题颜色 string
pubdate 发布时间 int Linux时间戳
1.1 .6 新闻评论
动作名：common
其 它：param（支持以下参数）
param 参数 是否必传 类型 说明
newsid 是 int 信息ID
page 否 int 页码
12 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 http://www.ikuman.cn

火鸟门户
pageSize 否 int 每页显示数量
返回参数信息：
"pageInfo": {
" page":1,
"pageSize":10,
"totalPage":1,
"totalCount":2
},
" list": [
{
" id": "6",
" userinfo": [
{
" userid":7,
" username": "a414644502",
"userType":1,
" nickname": "郭子“，
" photo": "头像地址“，
" message":10
}
],
" content": "测试评论内容！！！！“，
" dtime": "1395507206",
" ftime": "2分钟前“，
" ip": "192.168.1.108",
" ipaddr": "局域网“，
" good": "0",
" bad": "0",
" lower": [
{
评论子级列表，格式同父级一致！
}
]
},
……
]
返回参数说明：
参数名 描述 类型 说明
13 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 http://www.ikuman.cn

火鸟门户
pageInfo 页码参数 array
page 当前页码 int
pageSize 每页显示数 int
totalPage 总页数 int
totalCount 总记录数 int
list 评论列表 array
id 评论ID int
content 评论内容 string
dtime 评论时间 int Linux时间戳
ip 评论者IP string
ipaddr IP详细地址 string
good 顶 int
bad 踩 int
userinfo 评论用户信息 array
userid 用户 ID int
username 用户名 string
usertype 用户类型 int 1:个人2:企业
nickname 昵称 string
photo 头像 string
message 信息中心条数 int
lower 子级评论 array
数所格式与父级相同
1.1 .7 发表新闻评论
动作名:sendCommon
其 它：param
14 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 http://www.ikuman.cn

火鸟门户
param 参数 类型 说明
aid int 文章信息ID
id int 所评信息ID
content string 评论内容
返回参数信息：
参数名 描述
无 成功直接返回评语的详细数据，格式参考评论列表。
1.1 .8 发布投稿
动作名：put
其 它：param
param 参数 类型 说明
title string 信息标题
typeid int 类型ID
litpic string 缩略图
body text 投稿内容
imglist string 图集列表格式：图片加密ID|说明，图片加密ID|说明…
writer string 作者
source string 来源
keywords string 关键词
15 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 http://www.ikuman.cn

火鸟门户
description string 描述
vdimgck string 验证码
返回参数信息：
参数名 描述
无 成功直接返回发布成功的信息ID.
1.1 .9 修改投稿
动作名：edit
其 它：param
param 参数 类型 说明
id int 需要修改的信息ID
title string 信息标题
typeid int 类型ID
litpic string 缩略图
body text 投稿内容
imglist string 图集列表格式：图片加密ID|说明，图片加密ID|说明…
writer string 作者
source string 来源
keywords string 关键词
description string 描述
16 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 http://www.ikuman.cn

火鸟门户
vdimgck string 验证码
返回参数信息：
参数名 描述
无 成功直接返回【修改成功】字样。
1.1 .10 删除投稿
动作名：del
其 它：param
param 参数 类型 说明
id int 需要删除的信息ID
返回参数信息：
参数名 描述
无 成功直接返回删除成功。
17 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 http://www.ikuman.cn