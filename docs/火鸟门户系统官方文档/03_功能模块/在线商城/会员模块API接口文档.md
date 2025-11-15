火鸟门户
火鸟门户API接口使用文档
（会员模块）
[Huoniao. API. OpenAPI. member]
1 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
修订记录：
版本 修订记录 修订人 修订时间
v1.0.0 1.文档创建 郭永顺 2015-7-8
2 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
目录：
一、 接口说明：………………………………………………………………………………………………………………………………………………………………………………………………4
1.1 会员模块………………………………………………………………………………………………………………………………………………………………………………………………………4
1.1 .1 基本参数……………………………………………………………………………………………………………………………………………………………………… .4
1.1 .2 会员详细信息……………………………………………………………………………………………………………………………… .5
1.1 .3当前登录会员的登录记录……………………………………………………………………………………………………………………………………6
1.1 .4 信息收藏………………………………………………………………………………………………………………………………………………………………………………………7
3 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

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
1.1 会员模块
服务名：member
1.1 .1 基本参数
动作名：config
其 它：param（这个值为元素名，如果传入此值则只返回此元素的值，支持传入多个值，不传则返回所有）
参数 是否必传 类型 说明
param 否 string 多个值由“，”分隔
4 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
返回参数信息：
参数名 描述 类型 说明
userDomain 个人会员域名 string
busiDomain 企业会员域名 string
1.1 .2 会员详细信息
动作名：detail
其 它：param（这个值为元素名，如果传入此值则只返回此元素的值，支持传入多个值，不传则返回所有）
参数 是否必传 类型 说明
param 否 int 为空自动获取当前登录的会员
返回参数信息：
参数名 描述 类型 说明
userid 会员ID int
userType 会员类型 int 1个人 2企业
username 用户名 string
nickname 昵称 string
certifyState 实名认证 int 0：未认证 1已认证
paypwdCheck 支付密码 int 0：未设置 1已设置
email 邮箱 string
emailCheck 邮箱验证 int 0：未认证 1已认证
phone 手机号码 string
phoneCheck 手机验证 int 0：未认证 1已认证
qq 联系QQ int
photo 头像 string
5 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
sex 性别 int 0女 1男
message 消息数量 int
money 余额 int
freeze 冻结金额 int
point 积分 int
lastlogintime 最后登录时间 time
lastloginip 最后登录IP string
lastloginipaddr 最后登录IP详细地址 string
addr 所在区域ID ID
addrName 所在区域 ID
company 公司名称 string
address 详细地址 sting
licenseState 企业认证状态 int
1.1 .3当前登录会员的登录记录
动作名：loginrecord
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
6 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
list": [
{
" time": "2015-07-08 16:47:32",
" ip": "180.108.246.180",
" addr": "江苏省苏州市 电信“
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
list 数据列表 array
time 登录时间 time
ip 登录IP string
addr IP归属地 string
1.1 .4 信息收藏
动作名：collect
其 它：param
param 参数 是否必传 类型 说明
module 是 string 信息所属模块
temp 是 string 模块子级
id 是 string 信息id
7 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>

火鸟门户
type 是 int add增加 del删除
check 否 int 为1时验证是否已经收藏
返回参数说明：
参数名 描述
无
当type值为add时：如果还没有收藏则【返回“ok”,如果check为1时返回“no”】,已经收藏返回“has”;
如果type值为del时：直接返回“ok”
8 苏州酷曼软件技术有限公司 地址：苏州工业园区九华路18号华景花园39幢1206室 电话:0512-65071790 <http://www.ikuman.cn>
