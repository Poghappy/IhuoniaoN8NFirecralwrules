火鸟门户
火鸟门户API接口使用文档 （招聘模块）
[ Huoniao. API. OpenAPI. job]
1 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
修订记录：
版本 修订记录 修订人 修订时间
v1.0.0 1.文档创建 郭永顺 2014-04-04
V1.0.1 2.增加伯乐、工资、招聘会模块 郭永顺 2015-03-17
V1.0.2 3.职位信息增加伯乐数据 郭永顺 2015-03-17
V1.0.3 4.增加【招聘会】 郭永顺 2015-04-07
2

火鸟门户
目录：
一、 接口说明：…………………………………………………………………………………………………………………………………………………………………………………………………………5
1.1 . 招聘模块………………………………………………………………………… 5
1.1 .1 基本参数………………………………………………………… 5
1.1 .2 招聘地区………………………………………………………… 6
1.1 .3 职位类别………………………………………………………… ..8
1.1 .4 行业类别………………………………………………………… …9
1.1 .5 招聘分类………………………………………………………… ....10
1.1 .6 企业列表………………………………………………………… .....11
1.1 .7 企业详细信息……………………………………………… ……………………………………………………13
1.1 .8 伯乐…………………………………………………………………………………………………………………………………………………………………………………………………14
1.1 .9 伯乐详细信息………………………………………………… …………………………………………………………………………………………………………16
1.1 .10 招聘职位………………………………………………………… ………………………………………………………………17
1.1 .11 职位详细信息……………………………………………… …………………………………………………………20
1.1 .12 简历………………………………………………………………… ……………………………………………………………21
1.1 .13 简历详细信息……………………………………………… ……………………………………………………………………………23
1.1 .14 工资统计列表……………………………………………… ……………………………………………………25
1.1 .15 企业评论……………………………………………… ………………………………………………………………27
1.1 .16 伯乐评论………………………………………………………… …………………………………………………………………………29
1.1 .17 一句话求职/招聘……………………………………… ………………………………30
1.1 .18 发布一句话求职/招聘……………………………… ……………………………………………32
3 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
1.1 .19 招聘会场………………………………………………………………………………………………………………………………………………………………………32
1.1 .20 会场详细信息……………………………………………………………………………………………………………………………………………………………34
1.1 .21 招聘会……………………………………………………………………………………………………………………………………………………………………………35
1.1 .22 招聘会详细信息………………………………………………………………………………………………………………………………………………………37
1.1 .23 招聘资讯………………………………………………………………………………………………………………………………………………………………………37
1.1 .24 招聘资讯详细信息…………………………………………………………………………………………………………………………………………………39
1.1 .25 招聘资讯分类……………………………………………………………………………………………………………………………………………………………39
4 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
一、 接口说明：
服务名：job
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
1.1 .招聘模块
1.1 .1 基本参数
动作名：config
其 它：param（这个值为元素名，如果传入此值则只返回此元素的值，支持传入多个值，不传则返回所有）
参数 是否必传 类型 说明
param 否 string 多个值由“，”分隔
5 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

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
gs atlasMax 公司图集数量限制 int
fair atlasMax 会场图集数量限制 int
template 风格模板 string
map 地图配置 int 0：系统默认 1：谷歌2：百度 3：腾迅
softSize 附件上传限制大小 int
softType 附件上传类型限制 string
thumbSize 缩略图上传限制大小 int
thumbType 缩略图上传类型限制 string
atlasSize 图集上传限制大小 int
atlasType 图集上传类型限制 string
1.1 .2 招聘地区
动作名：addr
6 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
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
7 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
1.1 .3 职位类别
动作名：type
其 它：param
参数 是否必传 类型 说明
param 否 int 分类ID（传入此值则只返回此ID的下级分类）
返回信息：
[
{
" id": "1",
" parentid": "0",
" typename": "计算机/互联网/通信/电子“，
" lower": [
{
" id": "2",
" parentid": "1",
" typename": "计算机硬件“，
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
8 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
1.1 .4 行业类别
动作名：industry
其 它：param
参数 是否必传 类型 说明
param 否 int 分类ID（传入此值则只返回此ID的下级分类）
返回信息：
[
{
" id": "1",
" parentid": "0",
" typename": "计算机/互联网/通信/电子“，
" lower": [
{
" id": "2",
" parentid": "1",
" typename": "计算机软件“，
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
9 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
1.1 .5 招聘分类
动作名：item
其 它：param
参数 是否必传 类型 说明
param 否 int 分类ID（传入此值则只返回此ID的下级分类）
返回信息：
[
{
" id": "1",
" parentid": "0",
" typename": "工作经验“，
" lower": [
{
" id": "2",
" parentid": "1",
" typename": "不限“，
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
10 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
1.1 .6 企业列表
动作名：company
其 它：param（支持以下参数）
param 参数 类型 是否必传 说明
typeid int 否 性质
scale int 否 规模
industry int 否 行业
addrid int 否 区域ID
title string 否 关键字
property string 否 r：推荐 m：名企 u：紧急
orderby string 否 0：默认 1：点评数 2：职位数3：工资统计数 4:星级
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
" id": "3",
" title":"迈可行通信股份有限公司“，
" domain": " http:// maike.f.jsmeixin.com",
11 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 http://www.ikuman.cn

火鸟门户
" nature": "国内上市公司“，
" scale": "500-999人“，
" industry": "通信/电信运营、增值服务“，
" logo": " http:// jsmeixin.com/ include/ attachment.php?f=WHpSVU9sODRBVFE9",
" addrid": "239",
" addr": "北桥“，
" address": "吴中区工业园区星海街168号“，
" Inglat": "120.67168235778809,31.313241616101102",
" score": "4",
" rcount": "25",
" pcount": "101",
" wcount": "50",
" url": " <http://f.jsmeixin.com/> company-24.html"
},
…
]
返回参数说明：
参数名 描述 类型 说明
id 信息ID int
title 公司名称 string
domain 访问地址 string
nature 公司性质 string
scale 公司规模 string
industry 所属行业 string
logo 公司LOGO string
addrid 区域ID int
addr 区域名称 string
address 详细地址 string
Inglat 地图坐标 string
score 综合评分 int
rcount 评论数量 int
pcount 职位数量 int
wcount 工资统计数量 int
12 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
url 访问地址 string
1.1 .7 企业详细信息
动作名：companyDetail
其 它：param
参数 是否必传 类型 说明
param 是 int 公司ID
返回参数信息：
参数名 描述 类型 说明
id 公司ID int
title 公司名称 string
domain 绑定域名 string
nature 公司性质 string
scale 公司规模 string
industry 经营行业 string
logo LOGO string
userid 对应会员ID int
people 联系人 string
contact 联系电话 string
address 公司地址 string
Inglat 地图坐标 string
postcode 邮编 int
email 联系邮箱 string
site 公司网址 string
body 公司介绍 string
13 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
seotitle SEO标题 string
keywords 关键字 string
description 描述 string
pubdate 入驻时间 int Linux时间戳
1.1 .8 伯乐
动作名：bole
其 它：param（支持以下参数）
param 参数 是否必传 类型 说明
cid 否 int 公司ID
type 否 int 身份类型1: HR 2：猎头3：高管
addr 否 int 所在区域
status 否 int 招聘状态1：正在招聘2：有好的人才可以考虑3：暂不招聘
industry 否 int 招聘行业
zhineng 否 int 招聘职能
title 否 string 模糊匹配【支持：姓名、职位、公司】
orderby 否 int 0:默认 1:点评数 2:职位数 3:粉丝数
page 否 int 页码
14 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
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
" id": "1",
" cid": "2",
" company": "蓝图房地产代理有限公司“，
" userid": "2",
" mid": "13",
" realname": "赵龙龙“，
" photo": " http:// jsmeixin.com/ include/ attachment.php?f=WHpRQmJnUm9CajQ9",
" work": "招聘经理·主管“，
" type": "1",
" addr": "元和“，
" status": "1",
" rcount":0,
" pcount":1,
" fcount":0,
" industry":"计算机服务（系统、数据服务、维修），互联网/电子商务“，
" zhineng"："网站营运专员，网站策划，网站维护工程师“，
" url": " http://f.jsmeixin.com/ bole-21.html"
},
…
]
返回信息说明：
参数名 描述 类型 说明
pageInfo 页码参数 array
page 当前页码 int
pageSize 每页显示数 int
totalPage 总页数 int
15 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
totalCount 总记录数 int
list 伯乐列表 array
id 职位ID int
cid 公司ID int
company 公司名称 string
userid 简历ID int
mid 会员ID int
realname 真实姓名 string
photo 照片 string
work 职位 string
type 身份类型 int 1:HR 2:猎头 3:高管
addr 区域 string
status 招聘状态 int 1：正在招聘2：有好的人才可以考虑3：暂不招聘
industry 招聘行业 string
zhineng 招聘职能 string
rcount 评论数量 int
pcount 职位数量 int
fcount 粉丝数量 int
url 访问地址 string
1.1 .9 伯乐详细信息
动作名：boleDetail
其 它：param
参数 是否必传 类型 说明
16 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
param 是 int 伯乐ID
返回参数信息：
参数名 描述 类型 说明
id 伯乐ID int
cid 公司ID int
userid 简历ID int
work 职位 string
type 身份类型 int 1:HR 2:猎头 3:高管
addr 区域 string
status 招聘状态 int 1：正在招聘2：有好的人才可以考虑3：暂不招聘
industry 招聘行业 string
zhineng 招聘职能 string
note 招聘简介 string
1.1 .10 招聘职位
动作名：post
其 它：param（支持以下参数）
param 参数 是否必传 类型 说明
addr 否 int 工作地点
type 否 int 职位类别
experience 否 int 工作经验
educational 否 int 学历要求
17 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
sex 否 int 性别 0:不限 1:男 2:女
nature 否 int 职位性质0:全职 1:兼职 2:临时 3:实习
salary 否 int 薪资范围
company 否 int 公司ID
bole 否 int 伯乐ID
title 否 string 职位模糊匹配【支持：职位名、公司名】
property string 否 h：热门u:紧急 r:推荐
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
" id": "3",
" title": "业务员“，
" type": "销售人员“，
" company": [
{
格式参考【公司详细信息】
}
],
" bole":[
{
格式参考【伯乐详细信息】
}
18 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 http://www.ikuman.cn

火鸟门户
],
" nature": "0",
" number": "3",
" addr": "元和“，
" experience": "1-2年“，
" educational": "中专/职高“，
" salary": "1000以下“，
" click": "1",
" property": "h",
" pubdate": "1396574511",
" url": " <http://f.jsmeixin.com/> post-47.html"
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
list 职位列表 array
id 职位ID int
title 职位名称 string
type 职位类别 string
company 公司详细信息 array
格式参考【公司详细信息】
bole 伯乐详细信息 array
格式参考【伯乐详细信息】
nature 性质 int 0：全职 1：兼职2:临时 3：实习
19 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
addr 工作地点 string
number 招聘人数 int
addr 工作区域 string
experience 工作经验 string
educational 学历要求 string
salary 薪资范围 string
click 浏览次数 int
property 属性 string h:热门 u:紧急 r:推荐
pubdate 更新时间 int Linux时间戳
url 访问地址 string
1.1 .11 职位详细信息
动作名：detail
其 它：param
参数 是否必传 类型 说明
param 是 int 职位ID
返回参数信息：
参数名 描述 类型 说明
id 职位ID int
title 职位名称 string
type 职位类别 string
company 公司详细信息 array
格式参考【公司详细信息】
bole 伯乐详细信息 array
20 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
格式参考【伯乐详细信息】
sex 性别要求 int 0：不限 1:男 2:女
nature 职位性质 int 0:全职 1:兼职 2:临时 3:实习
number 招聘人数 int
addr 工作地点 string
experience 工作经验 string
educational 学历要求 string
language 语言能力 string
salary 薪资范围 string
note 职位描述 string
claim 职位要求 string
tel 联系电话 string
email 联系邮箱 string
click 浏览量 int
property 属性 string h:热门u :紧急
pubdate 更新时间 int Linux时间戳
1.1 .12 简历
动作名：resume
其 它：param（支持以下参数）
param 参数 是否必传 类型 说明
addr 否 int 所在区域
type 否 int 职位类别
sex 否 int 性别 0:男 1:女
21 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
nature 否 int 性质0:全职 1:兼职 2:临时 3:实习
workyear 否 int 工作经验
educational 否 int 学历要求
orderby 否 int 0：默认 1：粉丝
title 否 string 简历模糊搜索【支持：姓名、学校、专业】
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
" id": "1",
" userid": "12",
" name": "张小华“，
" sex": "0",
" nature": "0",
" type": "计算机软件“，
" addr": "浒墅关“，
" photo": " http:// jsmeixin.com/ include/ attachment.php?f=QUdOU1BWYzdEelk9",
" salary": "8000",
" workyear": "4",
" educational": "中专/职高“，
" college": "杭州大学“，
" professional": "电子商务“
},
…
]
22 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
返回信息说明：
参数名 描述 类型 说明
pageInfo 页码参数 array
page 当前页码 int
pageSize 每页显示数 int
totalPage 总页数 int
totalCount 总记录数 int
list 简历列表 array
id 简历ID int
userid 会员ID int
name 名称 string
sex 性别 int 0:男 1:女
nature 性质 int 0：全职 1：兼职2：临时 3：实习
type 职位类别 string
addr 期望工作地点 int Linux时间戳
photo 照片 string
salary 期望薪资 int
workyear 工作年限 int
educational 学历 string
college 毕业学院 string
professional 所学专业 string
1.1 .13 简历详细信息
动作名：resumeDetail
其 它：param
23 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
参数 是否必传 类型 说明
param 是 int 简历ID
返回参数信息：
参数名 描述 类型 说明
id 简历ID int
userid 会员ID int
name 姓名 string
sex 性别 int 0：不限 1:男 2:女
nature 职位性质 int 0：全职 1：兼职2：临时 3：实习
type 职位类别 string
addr 期望工作地点 string
birth 出生日期 int Linux时间戳
photo 头像 string
home 故乡 string
address 现居地 string
phone 联系电话 string
email 联系邮箱 string
salary 期望薪资 int
startwork 到岗时间 string
evaluation 自我评价 string
objective 职业目标 string
workyear 工作年限 int
experience 工作经验 string
educational 最高学历 string
college 毕业学院 string
graduation 毕业时间 int Linux时间戳
24 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
professional 所学专业 string
language 外语水平 string
computer 计算机水平 string
education 教育经历 string
click 浏览量 int
gz 关注数量 int
guanzhu 关注的会员 array
id 简历ID int
name 会员名称 string
photo 头像 string
fs 粉丝数量 int
guanzhu 关注的会员 array
id 简历ID int
name 会员名称 string
photo 头像 string
1.1 .14 工资统计列表
动作名：wage
其 它：param（支持以下参数）
param 参数 是否必传 类型 说明
addr 否 int 区域ID
industry 否 int 行业ID
company 否 int 公司ID
title 否 string 模糊查询【支持：职位名、公司名】
orderby 否 int 0：默认
25 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
1：平均值正序 2：平均值倒序3：最低值正序 4：最低值倒序5：最大值正序 6：最大值倒序
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
" id": "5",
" cid": "2",
" addr": "胥江“，
" work": "网页设计师“，
" avg":3500,
" min": "2100",
" max": "6000"
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
26 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
list 工资统计列表 array
id ID int
cid 公司ID int
addr 所在区域 tring
work 职位名称 string
avg 平均工资 int
min 最低 int
max 最高 int
1.1 .15 企业评论
动作名：companyReview
其 它：param（支持以下参数）
param 参数 是否必传 类型 说明
company 是 int 企业ID
userid 否 int 会员ID
page 否 int 页码
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
" id": "3",
27 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 http://www.ikuman.cn

火鸟门户
" score": "3",
" content": " ccccccc:",
" gx": "3",
" dtime": "1234567890",
" ftime": "6天前“，
" ip": "127.0.0.1",
" ipaddr": "本机地址“，
" lower": [
{
" id": "4",
" content": " dfasdfasdfsd",
" dtime": "1234567890",
" ftime": "6天前“，
" ip": "127.0.0.1",
" ipaddr": "本机地址“，
" lower": null
}
]
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
list 评论列表 array
id 评论ID int
score 评分 int
content 评论内容 string
gx 评论者关系 int
dtime 评论时间 int Linux时间戳
ftime 个性化时间 string
28 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
ip 评论者IP string
ipaddr IP详细地址 string
lower 子级评论 array
数所格式【除没有score、gx这两个字段外】与父级相同
1.1 .16 伯乐评论
动作名：boleReview
其 它：param（支持以下参数）
param 参数 是否必传 类型 说明
bole 是 int 伯乐ID
userid 否 int 会员ID
page 否 int 页码
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
" id": "2",
" content": " dsfasdfasdf",
" gx": "1",
" dtime": "1234567890",
" ftime": "6天前“，
" ip": "127.0.0.1",
" ipaddr": "本机地址“
29 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 http://www.ikuman.cn

火鸟门户
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
list 评论列表 array
id 评论ID int
content 评论内容 string
gx 评论者关系 int
dtime 评论时间 int Linux时间戳
ftime 个性化时间 string
ip 评论者IP string
ipaddr IP详细地址 string
1.1 .17 一句话求职/招聘
动作名：sentence
其 它：param（支持以下参数）
param 参数 是否必传 类型 说明
type 否 int 0：招聘 1：求职
id 否 int 信息ID
page 否 int 页码
30 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
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
" type": "0",
" title": "招聘信息测试“，
" people": "韩明明“，
" contact": "18913541613",
" password": "b0baee9d279d34fa1dfd71aadb908c3f",
" note": "招聘信息测试内容！！！！！“，
" pubdate": "1234567890"
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
id ID int
type 类型 int 0：招聘 1：求职
title 标题 string
31 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
people 联系人 string
contact 联系方式 int
password 管理密码 string
note 说明 string
pubdate 发布时间 int Linux时间戳
1.1 .18 发布一句话求职/招聘
动作名：sendSentence
其 它：param
param 参数 是否必传 类型 说明
type 是 int 0：招聘 1：求职
title 是 string 标题
people 是 string 联系人
contact 是 string 联系方式
password 是 string 管理密码
note 是 string 说明
返回参数信息：
参数名 描述
无 成功直接返回“发布成功！”字样。
1.1 .19 招聘会场
动作名 : fairsCenter
32 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
其 它：param（支持以下参数）
param 参数 是否必传 类型 说明
addr 否 int 区域ID
title 否 string 模糊匹配【标题、地址】
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
" title": "河西万达广场E座“，
" people": "祁经理“，
" addr": "梅李“，
" address": "河西万达广场E座503",
" lnglat": "121.51345544047547,31.3000763387588",
" traffic": "7路、37路、39路、57路、186路江东万达广场站下“，
" url": " http://f.jsmeixin.com/fairsCenter-5.html"
},
…
]
返回信息说明：
参数名 描述 类型 说明
pageInfo 页码参数 array
page 当前页码 int
pageSize 每页显示数 int
33 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
totalPage 总页数 int
totalCount 总记录数 int
list 信息列表 array
id ID int
title 会场名称 string
people 联系人 string
addr 所在区域 string
address 详细地址 string
Inglat 地图坐标 string
traffic 公交线路 string
url 访问地址 string
1.1 .20 会场详细信息
动作名：fairsCenterDetail
其 它：param
参数 是否必传 类型 说明
param 是 int 信息ID
返回参数信息：
参数名 描述 类型 说明
id 信息ID int
title 会场名称 string
people 联系人 string
mobile 联系手机 string
tel 电话 string
fax 传真 string
34 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
addr 所在区域 string
address 详细地址 string
Inglat 地图坐标 string
email 联系邮箱 string
qq 联系QQ string
note 会场介绍 string
traffic 公交线路 string
pics 会场图集 string
1.1 .21 招聘会
动作名：fairs
其 它：param（支持以下参数）
param 参数 是否必传 类型 说明
time 否 date 举办时间，格式:2015-02-03
addr 否 int 区域ID
center 否 int 所在会场ID
title 否 string 模糊匹配【标题、地址】
page 否 int 页码
pageSize 否 int 每页显示数量
返回信息：
"pageInfo": {
" page":1,
"pageSize":10,
"totalPage":1,
"totalCount":1
35 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
},
" list": [
{
" id": "1",
" fid": "4",
" fairs":【Array，格式参考[招聘会详细信息]】，
" title":"4月17日济南大学2015年春季大型校园双选招聘会“，
" date": "2015-04-17",
" click": "501",
" url": " http://f.jsmeixin.com/ fairs-1.html"
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
id ID int
fid 会场ID int
fairs 会场信息 array
格式参考【会场详细信息】
title 招聘会名称 string
date 举办时间 date
click 浏览次数 int
url 访问地址 string
36 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
1.1 .22 招聘会详细信息
动作名 : fairsDetail
其 它：param
参数 是否必传 类型 说明
param 是 int 信息ID
返回参数信息：
参数名 描述 类型 说明
id 信息ID int
fid 会场ID int
fairs 会场信息 array
格式参考【会场详细信息】
title 招聘会名称 string
date 举办时间 date
began 开始时间段 string 格式:09:08
end 结束时间段 string 格式:11:40
click 浏览次数 int
note 招聘会介绍 string
1.1 .23 招聘资讯
动作名：news
其 它：param（支持以下参数）
param 参数 是否必传 类型 说明
37 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
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
" title"："居家彩绘设计 艺术让房子灵动起来“，
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
title 信息标题 string
typeid 分类ID int
click 浏览 int
38 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
writer 编辑 string
pubdate 发布时间 int Linux时间戳
1.1 .24 招聘资讯详细信息
动作名：newsDetail
其 它：param
参数 是否必传 类型 说明
param 是 int 信息ID
返回参数信息：
参数名 描述 类型 说明
title 信息标题 string
typeid 所属分类 int
click 浏览 int
source 来源 string
sourceUrl 来源网址 string
writer 作者 string
keyword 关键字 string
description 描述 string
body 信息内容 string
pubdate 发布时间 string Linux时间截
1.1 .25 招聘资讯分类
动作名：newsType
39 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
其 它：param
参数 是否必传 类型 说明
param 否 int 分类ID（传入此值则只返回此ID的下级分类）
返回信息：
[
{
" id": "1",
" parentid": "0",
" typename": "面试宝典“，
" lower": [
{
" id": "2",
" parentid": "1",
" typename": "职业规划“，
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
40 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
41 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>
