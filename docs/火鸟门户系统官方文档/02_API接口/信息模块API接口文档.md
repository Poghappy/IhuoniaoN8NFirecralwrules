火鸟门户
火鸟门户API接口使用文档 （信息模块）
[Huoniao. API. OpenAPI. info ]
1 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
修订记录：
版本 修订记录 修订人 修订时间
v1.0.0 1.文档创建 郭永顺 2014-3-23
V1.0.1 2.信息内容增加移动端字段：mbody 郭永顺 2014-6-11
V1.0.2 3.新增【发布信息】4.新增【修改信息】5.新增【删除信息】 郭永顺 2015-6-7
2 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
目录：
一、 接口说明：…………………………………………………………………………………………………………………………………………………………………………………………………4
1.1 . 信息模块………………………………………………………………………… 4
1.1 .1 基本参数…………………………………………………………… 4
1.1 .2 信息分类…………………………………………………………… 5
1.1 .3信息分类详细信息…………………………………… .6
1.1 .4 信息地区…………………………………………………………… 8
1.1 .5 信息列表…………………………………………………………… .9
1.1 .6 详细信息…………………………………………………………… …14
1.1 .7 信息评论…………………………………………………………… ……………………………………………16
1.1 .8 发表评论…………………………………………………………………………………………………………………………………………………………………………18
1.1 .9 发布信息………………………………………………………… ……………………………………………………………………19
1.1 .10 修改信息………………………………………………………… …………………………………………………………………20
1.1 .11 删除信息…………………………………………………………… ……………………………………………………………………………21
3 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
一、 接口说明：
服务名：info
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
1.1 .信息模块
1.1 .1 基本参数
动作名：config
其 它：param（这个值为元素名，如果传入此值则只返回此元素的值，支持传入多个值，不传则返回所有）
参数 是否必传 类型 说明
param 否 string 多个值由“，”分隔
4 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

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
1.1 .2 信息分类
动作名：type
其 它：param
param 参数 是否必传 类型 说明
type 否 int 分类ID
5 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
page 否 int 页码
pageSize 否 int 每页显示数量
返回信息：
[
{
" id": "1",
" parentid": "0",
" typename": "生活服务“，
" lower": [
{
" id": "2",
" parentid": "1",
" typename": "搬家“，
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
1.1 .3信息分类详细信息
动作名：typeDetail
6 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
其 它:param（支持以下参数）
参数 是否必传 类型 说明
param 是 int 分类ID
返回信息：
[
{
" id": "104",
" typename": "搬家“，
" seotitle": "",
" keywords": "",
" description": "",
" item": [
{
" id": "182",
" field": " type",
" title": "类别“，
" formtype": " checkbox",
" required": "1",
" options": "转让|求购“，
" default": "转让“
},
…
]
}
]
返回参数说明：
参数名 描述 类型 说明
id 分类ID int
typename 分类名称 string
seotitle 分类SEO标题 string
keywords 分类SEO关键字 string
description 分类SEO描述 string
item 分类字段 array 分类有下属字段时才会返回
7 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
id 字段ID int
field 字段名 string
title 字段名称 string
fromtype 字段类型 string text:文本checkbox:多选radio:单选
options 字段内容 string 多个值由“|”分隔
default 初始值 string
1.1 .4 信息地区
动作名：addr
其 它：param
param 参数 是否必传 类型 说明
type 否 int 分类ID
page 否 int 页码
pageSize 否 int 每页显示数量
返回信息：
[
{
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
8 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 http://www.ikuman.cn

火鸟门户
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
1.1 .5 信息列表
动作名：ilist
其 它：param（支持以下参数）
param 参数 是否必传 类型 说明
nature 否 int 0：全部 1：个人 2：商家
typeid 否 int 分类ID
addrid 否 int 地区ID
valid 否 int 过 期 时 间3 : 三 天 后 过 期7 : 七 天 后 过 期30 : 一 个 月 后 过 期90：三个月后过期
9 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
title 否 string 信息标题（支持模糊查询）
item 否 array 所属分类字段，格式如下：[ { " id": "182"," value": "转让“}…]
rec 否 int 0：默认 1：推荐
fire 否 int 0：默认 1：火急
top 否 int 0：默认 1：置顶
pic 否 int 0：全部 1：必须有图
orderby 否 int 排序： 0：默认排序1：发布时间 2：浏览量3：随机 4：评论2.1：今日浏览量 4.1：今日评论量2.2：昨日浏览量 4.2：昨日评论量2.3：本周浏览量 4.3：本周评论量2.4：本月浏览量 4.4：本月评论量
u 否 int 为 1 时表示只列出当前登录会员的所有信息
state 否 int 空：全部 0：未审核
10 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
1：已审核 2：审核拒绝3：取消显示 4：已过期
userid 否 int 会员ID
page 否 int 页码
pageSize 否 int 每页显示数量
返回信息：
"pageInfo": {
" page":1,
"pageSize":10,
"totalPage":1,
"totalCount":2,
" gray":3,
" audit":25,
" refuse":1,
" expire":10
},
" list": [
{
" id": "2",
" title": "信息标题“，
" color": "#ff0000",
" collect":1,
"fabuCount": "15",
" address": "吴中区“，
" typeid": "109",
" typename": "货运物流“，
" pubdate": "1395485308",
" tel": "15006212131",
" teladdr": "江苏 苏州市“，
" click": "568",
" rec": "1",
" fire": "0",
" top": "1",
" pcount": "8",
" arcrank": "2",
" desc"："苏州昌尔胜货运有限公司成立于1998年，其总公司设在江苏省苏州市虎丘风景
11 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 http://www.ikuman.cn

火鸟门户
区，意为“沙漠中的骆驼”。“昌尔胜”通过全体员工的不懈努力，现已成为组织健全，设施完善，经验丰富“，
" common": "15",
" typeurl": " <http://m.menhu168.com/> info/ info-list-11.html",
" url": " <http://m.menhu168.com/> info/ info-detail-213.html",
" litpic": " <http://m.menhu168.com/> include/ attachment.php?f=WGpNQmIxRTdEajA9",
" member": {
" mtype": "1",
" username": "414644502",
" nickname": "郭子“，
" email": "414644502@ qq.com",
"emailCheck": "1",
" phone": "15363215365",
"phoneCheck": "1",
" qq": "",
" photo": " <http://menhu168.com/> uploads/siteConfig/.../7845176.jpg",
" sex": "1",
" addr": "238",
" addrs": "元和“，
" company": "苏州酷曼软件技术有限公司“，
" address": "东环路378号1-503",
"licenseState": "1"
}
},
…
]
返回参数说明：
参数名 描述 类型 说明
pageInfo 页码参数 array
page 当前页码 int
pageSize 每页显示数 int
totalPage 总页数 int
totalCount 总记录数 int
gray 未审核 int 这四项只有在会员中心处显示
audit 已审核 int
refuse 审核拒绝 int
expire 已过期 int
12 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
list 信息列表 array
id 信息ID int
title 信息标题 string
fabuCount 此会员共发布信息数量 int
color 标题颜色 string
collect 是否已经收藏 int 1已收藏 0未收藏
address 区域名称 string
typeid 分类ID int
typename 分类名称 string
tel 联系电话 string
teladdr 电话归属地 string
click 浏览量 int
pubdate 发布时间 int Linux时间戳
rec 推荐 int 1为推荐
fire 火急 int 1为火急
top 置顶 int 1为置顶
pcount 图片数量 int
desc 信息介绍 string
common 评论数量 int
typeurl 分类访问地址 string
url 信息访问地址 string
litpic 信息缩略图 string
arcrank 状态 int 0未审核 1已审核 2审核拒绝3取消显示 4已过期
member 会员信息 array
id 会员ID int
mtype 会员类型 int 1:个人2:企业
username 会员名 string
13 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
nickname 昵称 string
email 邮箱 string
emailCheck 邮箱验证 int 0：未验证1：已验证
phone 手机 string
phoneCheck 手机验证 int 0：未验证1：已验证
qq QQ号码 string
photo 头像 string
sex 性别 int 1:男 0:女
addr 区域ID int
addrs 所在区域 string
company 公司名称 string
address 公司地址 string
licenseState 企业认证 int 0未认证 1 已认证 2认证失败
1.1 .6 详细信息
动作名：detail
其 它：param
参数 是否必传 类型 说明
param 是 int 信息ID
返回参数信息：
参数名 描述 类型 说明
id 信息ID int
typeid 分类ID int
title 信息标题 string
color 标题颜色 string
14 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
validVal 有效期值 int 0长期有效 3三天后过期7一周后过期 30一个月后过期90三个月后过期
valid 有效期 string 长期有效 已过期 **天后过期
addrid 区域ID int
address 区域名称 string
item 字段内容 array [ { " iid": "204"," type": "供求“，” value”：”转让“}，…]
body 信息内容 text
mbody 移动端信息内容 text
person 联系人 string
tel 联系电话 string 此处返回加密过的字符串/ include/ json. php? action= phoneimage&num=AG9SO14wUWAANIU1UmQDNAAyVTVUZg==
teINum 未加密的电话号码 string
teladdr 电话归属地 string
qq 联系QQ string
click 浏览次数 int
ip 发布者IP string
ipaddr IP详细地址 string
userid 会员ID int
member 会员信息 array 格式参考【信息列表】返回结果
rec 推荐 int 1推荐 0不推荐
fire 火急 int 1火急 0不火急
15 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
top 置顶 int 1置顶 0不置顶
fabuCount 会员发布信息统计 int
collect 是否已经收藏 int 0没收藏 1已经收藏
telCount 手机号码信息统计 int
pubdate 发布时间 int Linux时间戳
imglist 信息图集 array [ { "pathSource": "图片加密地址“， " path": "图片地址“，” info”：”图片说明“}，…]
common 评论数量 int
1.1 .7 信息评论
动作名：common
其 它：param（支持以下参数）
param 参数 是否必传 类型 说明
newsid 是 int 信息ID
page 否 int 页码
pageSize 否 int 每页显示数量
返回参数信息：
"pageInfo": {
" page":1,
"pageSize":10,
"totalPage":1,
"totalCount":2
16 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
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
pageInfo 页码参数 array
page 当前页码 int
pageSize 每页显示数 int
totalPage 总页数 int
totalCount 总记录数 int
list 评论列表 array
id 评论ID int
17 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
content 评论内容 string
dtime 评论时间 int Linux时间戳
ip 评论者IP string
ipaddr IP详细地址 string
good 顶 int
bad 踩 int
userinfo 评论用户信息 array
userid 用户ID int
username 用户名 string
usertype 用户类型 int 1:个人2:企业
nickname 昵称 string
photo 头像 string
message 信息中心条数 int
lower 子级评论 array
数所格式与父级相同
1.1 .8 发表评论
动作名：sendCommon
其 它：param
param 参数 类型 说明
aid int 信息ID
id int 所评信息ID
content string 评论内容
返回参数信息：
18 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
参数名 描述
无 成功直接返回评语的详细数据，格式参考评论列表。
1.1 .9 发布信息
动作名：put
其 它：param
param 参数 类型 说明
typeid int 类型ID
title string 信息标题
addr int 所在区域
person string 联系人
qq string QQ
tel string 联系手机
valid int 有效期
body text 信息内容
imglist string 图集列表格式：图片加密ID|说明，图片加密ID|说明…
vdimgck string 验证码
还有其它自定义字段的参数，这里不做介绍。
返回参数信息：
参数名 描述
无 成功直接返回发布成功的信息ID.
19 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
1.1 .10 修改信息
动作名：edit
其 它：param
param 参数 类型 说明
id int 要修改的信息ID
typeid int 类型ID
title string 信息标题
addr int 所在区域
person string 联系人
qq string QQ
tel string 联系手机
valid int 有效期
body text 信息内容
imglist string 图集列表格式：图片加密ID|说明，图片加密ID|说明…
vdimgck string 验证码
还有其它自定义字段的参数，这里不做介绍。
返回参数信息：
参数名 描述
无 成功直接返回【修改成功】字样。
20 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
1.1 .11 删除信息
动作名：del
其 它：param
param 参数 类型 说明
id int 需要删除的信息ID
返回参数信息：
参数名 描述
无 成功直接返回删除成功。
21 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>
