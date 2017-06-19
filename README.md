# banquetExpert

# 员工接口（移动客户端）
## 综述：
接口的URL前缀均为：http://114.215.220.241:8000/（可能会改变，建议用变量表示）<br>
支持格式均为：json

返回状态：

1. 返回成功：

```
{
	"status":"true",
	"data":{
		...
	}
}
```

2. 返回失败：

```
{
	"status":"false",
	"err_code":"err_1",
	"description":"错误描述：密码错误"
}
```

# 员工账号

## 注册
URL：webApp/staff/register <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| phone         | 手机号          |         yes    |
| password      | 密码（MD5加密后结果，32位）  |         yes    |
| validation_code   | 验证码   |   yes |
| hotel_id      | 酒店ID          |         yes    |
| staff_number  | 员工编号        |         yes    |
| name          | 姓名            |         yes    |
| gender        | 性别，0: 保密, 1: 男, 2: 女, 默认为0   | yes |
| position      | 职位            |         yes    |
| id_number     | 身份证号         | yes           |

请求示例：

```
{
	"phone":"18813101211",
	"password":"f344e6af76dba76214024c7b327eff78",
	"validation_code":"123456",
	"hotel_id":12,
	"staff_number":"2017213464",
	"name":"小张",
	"gender":1,
	"position":"前台",
	"id_number":"101213413431234",
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| staff_id | 员工账号ID |

返回示例：

```
{
	"status":"true",
	"data":{
		"staff_id":1
	}
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 该手机号已经注册过 |
| err_3 | 该酒店不存在 |
| err_4 | 服务器发生错误 |


## 登录
URL：webApp/staff/login <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| phone         | 手机号          |         yes    |
| password      | 密码（MD5加密后结果，32位）  |         yes    |

请求示例：

```
{
	"phone":"18813101211",
	"password":"f344e6af76dba76214024c7b327eff78",
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| staff_id | 员工账号ID |
| token | 验证口令 |

返回示例：

```
{
	"status":"true",
	"data":{
		"staff_id":1,
		"token":"129ASDFIOJIO3RN23U12934INASDF"
	}
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 不存在该用户 |
| err_3 | 密码错误 |


## 修改密码
URL：webApp/staff/pass_modify <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| phone         | 手机号          |         yes    |
| old_password      | 密码            |         yes    |
| new_password      | 密码            |         yes    |

请求示例：

```
{
	"phone":"18813101211",
	"old_password":"pass",
	"new_password":"pass",
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| staff_id | 员工账号ID |

返回示例：

```
{
	"status":"true",
	"data":{
		"staff_id":1
	}
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 不存在该用户 |
| err_3 | 旧密码错误 |


## 获取员工信息
URL：webApp/staff/profile/get/ <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 登录口令          |         yes    |
| staff_id      | 目标员工的ID （默认为自己）|         no   |

请求示例：

```
{
	"staff_id":101,
	"token":"129ASDFIOJIO3RN23U12934INASDF",
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| staff_id | 员工账号ID |
| staff_number| 员工编号 |
| name| 员工姓名 |
| icon| 头像    |
| gender| 性别   |
| position| 职位   |
| guest_channel | 所属获客渠道, 0:无, 1:高层管理, 2:预定员和迎宾, 3:客户经理 |
| description| 备注   |
| authority| 权限等级 |
| icon | 头像 |
| create_time| 创建时间|

返回示例：

```
{
	"status":"true",
	"data":{
		"staff_id":1,
		"staff_number":"2017013434",
		"name":"小张",
		"gender":1,
		"position":"前台",
		"guest_channel":0,
		"description":"备注",
		"authority":"权限等级",
		"icon":"http://oss.aliyun/banquet/avatar/1.jpg"
		"create_time":"创建时间",
	}
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 不存在该员工 |

## 修改员工信息
URL：webApp/staff/profile/modify/ <br>
请求方式：POST <br>

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 登录口令          |         yes  |
| staff_number      | 员工编号     |         no   |
| gender      | 性别    |         no   |
| position      | 职位     |         no   |
| guest_channel      | 所属获客渠道, 0:无, 1:高层管理, 2:预定员和迎宾, 3:客户经理   |         no   |
| description      | 备注，最多100字符   |         no   |
| authority      | 权限    |         no   |
| icon      | 头像（文件）    |         no   |

请求示例:


```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"staff_number":"2017013434",
	"name":"小张",
	"gender":1,
	"position":"前台",
	"guest_channel":0,
	"description":"备注",
	"authority":"权限等级",
	"icon":[FILE]
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|


返回示例：

```
{
	"status":"true"
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |


## 获取员工所在酒店信息
URL：webApp/staff/hotel <br>
请求方式：POST <br>
| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 登录口令          |         yes  |

请求示例:


```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| hotel_id | 酒店 ID |
| branch_id | 分店 ID |
| name | 酒店名称 |
| icon | 头像 |
| branches_count | 门店数 |
| owner_name | 法人代表 |
| create_time | 创建时间 |


返回示例：

```
{
	"status":"true",
	"data":{
		"hotel_id":1,
		"branch_id":2,
		"name":"北京宴",
		"icon":"http://oss.aliyun/banquet/avatar/1.jpg",
		"branches_count":3,
		"owner_name":"杨秀荣",
		"create_time":"创建时间"
	}
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_3 | 不存在该员工 |


## 获取员工所在酒店的门店列表
URL：webApp/staff/hotel_branch/list/ <br>
请求方式：POST <br>

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 登录口令          |         yes  |
| offset | 起始值（默认0） | no |
| limit | 偏移量（默认10） | no |
| order | 排序方式（0: 注册时间升序，1: 注册时间降序，2: 名称升序，3: 名称降序，默认1） | no |

请求示例:


```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| count | 门店数   |
| list  | 门店列表  |
|以下为list中的数据|
| branch_id | 门店 ID |
| name | 名称 |
| icon | 头像 |
| province | 省 |
| city | 城市 |
| county | 区/县 |
| address | 详细地址 |
| hotel_name | 所属酒店名 |
| manager_name | 店长名 |
| create_time | 创建时间 |

返回示例：

```
{
	"status":"true",
	"data":{
	    "count":3,
	    "list":[
            "branch_id":1,
            "name":"北京宴总店",
            "icon":"http://oss.aliyun/banquet/avatar/1.jpg",
            "province":"北京市",
            "city":"北京市",
            "county":"丰台区",
            "address":"北京市丰台区靛厂路333号",
            "branches_count":3,
            "hotel_name":"北京宴",
            "manager_name":"陈奎义",
            "create_time":"创建时间"
            ],
            ...
	    }
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_3 | 不存在该员工 |

# 门店接口

## 获取门店的详情
URL：webApp/hotel_branch/profile/ <br>
请求方式：POST <br>

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 登录口令          |         yes  |
| branch_id | 门店 ID | yes |

请求示例:


```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"branch_id":1,
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| name | 名称 |
| icon | 头像 |
| pictures | 介绍图片（json字符串，最多5张） |
| province | 省 |
| city | 城市 |
| county | 区/县 |
| address | 详细地址 |
| meal_period | 餐段设置（json字符串） |
| facility | 设施（json字符串） |
| pay_card | 可以刷哪些卡（json字符串） |
| phone | 联系电话（json字符串，最多3个） |
| cuisine | 菜系（json字符串） |
| hotel_name | 所属酒店名 |
| manager_name | 店长名 |
| create_time | 创建时间 |

返回示例：

```
{
	"status":"true",
	"data":{
		"name":"北京宴总店",
		"icon":"http://oss.aliyun/banquet/avatar/1.jpg",
		"pictures":"[picture1, picture2, ...]",
		"province":"北京市",
		"city":"北京市",
		"county":"丰台区",
		"address":"北京市丰台区靛厂路333号",
		"meal_period":"{"Monday":{"lunch":[08:00,08:30], "dinner":[14:00,14:30], "supper":[20:00,20:30]},"Tuesday":{},...}",
		"facility":"["停车场","吸烟区"]",
		"pay_card":"["银联", "支付宝"]",
		"phone":"["13011111111", "13100000000"]",
		"cuisine":"菜系",
		"hotel_name":"北京宴",
		"manager_name":"陈奎义",
		"create_time":"创建时间"
	}
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 不存在该员工 |
| err_4 | 门店不存在 |


## 获取门店的区域列表
URL：webApp/hotel_branch/area/list/ <br>
请求方式：POST <br>

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 登录口令          |         yes  |
| branch_id | 门店 ID | yes |
| order | 排序方式（0: 注册时间升序，1: 注册时间降序，2: 名称升序，3: 名称降序，默认1） | no |

请求示例:


```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"branch_id":1,
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| count | 区域数 |
| list | 区域列表 |
|以下为list中的数据|
| area_id | 区域 ID |
| name | 名称 |
| order | 排序 |
| create_time | 创建时间 |

返回示例：

```
{
	"status":"true",
	"data":{
	    "count":33,
	    "list":[
	        "area_id":1,
		    "name":"一楼",
		    "order":1,
		    "create_time":"创建时间"
		    ],
		    ...
	    }
}
```

错误代码：<br>

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 不存在该员工 |
| err_4 | 门店不存在 |
| err_5 | 餐厅区域不存在 |


## 获取门店某一天某餐段的桌位使用情况列表
URL：webApp/hotel_branch/area/list/ <br>
请求方式：POST <br>

| 请求参数      | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 登录口令          |         yes  |
| branch_id | 门店 ID | yes |
| date  | 日期 | yes |
| dinner_period | 餐段（0:午餐, 1:晚餐, 2:夜宵）  | yes   |
| area_id   | 区域 ID | no    |
| order | 排序方式（0: 注册时间升序，1: 注册时间降序，2: 名称升序，3: 名称降序，默认1） | no |

请求示例:

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"branch_id":1,
	"date":"2017-6-12",
	"dinner_period":0,
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| count | 区域数 |
| list | 区域列表 |
|以下为list中的数据|
| desk_id | 桌位 ID |
| name | 名称 |
| order | 排序 |
| area_name | 所在区域名   |
| min_guest_num | 最小容纳人数    |
| max_guest_num | 最大容纳人数    |
| create_time | 创建时间 |

返回示例：

```
{
	"status":"true",
	"data":{
	    "count":33,
	    "list":[
	        "desk_id":1,
		    "area_name":"一楼",
		    "order":1,
		    "create_time":"创建时间"
		    ],
		    ...
	    }
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 不存在该员工 |
| err_4 | 门店不存在 |


# 订单接口

## 提交订单
URL：webApp/order/submit <br>
请求方式：POST <br>

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 登录口令          |         yes  |
| dinner_date | 预定用餐日期 | yes |
| dinner_time | 预定用餐时间 | yes |
| dinner_period | 订餐时段(0, '午餐'), (1, '晚餐'), (2, '夜宵') | yes |
| name | 联系人 | yes |
| contact | 联系电话 | yes |
| guest_number | 客人数量 | yes |
| desks | 桌位 | yes |
| staff_description | 员工备注 | no |
|以下是私人订制的字段|
| water_card | 水牌 | no |
| door_card | 门牌 | no |
| sand_table | 沙盘 | no |
| welcome_screen | 欢迎屏 | no |
| welcome_fruit | 迎宾水果的价格 | no |
| welcome_card | 欢迎卡 | no |
| background_music | 背景音乐 | no |
| has_candle | 是否有蜡烛 | no |
| has_flower | 是否有鲜花 | no |
| has_balloon | 是否有气球 | no |


请求示例:


```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"dinner_date":"2014-02-01",
	"dinner_time":"12:00"
	"dinner_period":0,
	"name":"李四",
	"contact":"18813101211",
	"guest_number":10,
	"desks":[1,3,5],
	"staff_description":"客户年纪大，做好防滑",
	"water_card":"水牌内容",
	"door_card":"门牌内容",
	"sand_table":"沙盘内容",
	"welcome_screen":"欢迎xx领导",
	"welcome_fruit": 128,
	"welcome_card":"欢迎你",
	"background_music":"我爱你中国",
	"has_candle":true,
	"has_flower":false,
	"has_balloon":false,
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| order_id | 订单 ID |


返回示例：

```
{
	"status":"true",
	"data":{
		"order_id":1
	}
}
```



错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |


## 搜索订单列表
URL：webApp/order/search/ <br>
请求方式：POST <br>

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 登录口令          |         yes  |
| order_date    | 下单日期  |   no |
| dinner_period | 餐段    |   no |
| dinner_date   | 预定用餐日期  |   no  |
| dinner_time   | 预定用餐时间  |   no  |
| state | 订单状态（0: 进行中，1: 已完成，默认为0）  | no |
| search_key | 搜索关键词（如姓名、手机等进行模糊搜索） | no |
| offset | 起始值（默认0） | no |
| limit | 偏移量（默认10） | no |
| order | 排序方式（0: 注册时间升序，1: 注册时间降序，默认1） | no |


请求示例:


```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"state":0,
	"search_key":"张总",
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| count | 订单数量 |
| list | 订单列表 |
| 以下为list中的数据 |
| order_id| 订单ID |
| create_time | 创建日期 |
| cancel_time | 撤销日期 |
| arrival_time  | 客到日期 |
| finish_time | 完成日期 | 
| status | 状态((0, '已订'), (1, '客到'), (2, '已完成'), (3, '已撤单'))|
| dinner_date | 预定用餐日期 |
| dinner_time   | 预定用餐时间  |
| dinner_period | 订餐时段(0, '午餐'), (1, '晚餐'), (2, '夜宵') |
| name | 联系人 |
| contact | 联系电话 |
| guest_type | 顾客身份 |
| guest_number | 客人数量 |
| desks | 桌位 |
| internal_channel | 内部获客渠道, 即接单人名字, 如果存在 |
| external_channel | 外部获客渠道, 即外部渠道名称, 如果存在 |


返回示例：

注意：返回的订单列表以数组来表示

```
{
	"status":"true",
	"data":{
	    "count":100,
	    "list":[
            "order_id":1,
            "create_time":"2014-02-01 10:00:00",
            "cancel_time":"2014-02-01 10:00:00",
            "arrival_time":"2014-02-01 10:00:00",
            "finish_time":"2014-02-01 10:00:00",
            "status":0,
            "order_id":"001",
            "dinner_date":"2014-02-01",
            "dinner_time":"12:00",
            "dinner_period":0,
            "name":"李四",
            "guest_type":"vip",
            "contact":"18813101211",
            "guest_number":10,
            "desks":[1,3,5],
            "internal_channel":"刘光艳",
            "external_channel":"美团"
            ],
			...
	    }
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |

## 获取订单详情
URL：webApp/order/detail/ <br>
请求方式：POST

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------|
| token         | 登录口令          |         yes  |
| order_id | 订单ID | yes |


请求示例:


```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"order_id":"order_id",
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| order_id| 订单ID |
| create_time | 创建日期 |
| cancel_time | 撤销日期 |
| arrival_time  | 客到日期 |
| finish_time | 完成日期 |
| status | 状态((0, '已订'), (1, '客到'), (2, '已完成'), (3, '已撤单'))|
| dinner_date | 预定用餐日期 | yes |
| dinner_time   | 预定用餐时间  |   yes  |
| dinner_period | 订餐时段(0, '午餐'), (1, '晚餐'), (2, '夜宵') | yes |
| name | 联系人 |
| guest_type | 顾客身份 |
| contact | 联系电话 |
| guest_number | 客人数量 |
| desks | 桌位ID和名称 |
| user_description | 用户备注 |
| staff_description | 员工备注 |
|以下是私人订制的字段|
| water_card | 水牌 |
| door_card | 门牌 |
| sand_table | 沙盘 |
| welcome_screen | 欢迎屏 |
| welcome_fruit | 迎宾水果的价格 |
| welcome_card | 欢迎卡 |
| pictures | 用户上传的图片（最多5张) |
| background_music | 背景音乐 |
| has_candle | 是否有蜡烛 |
| has_flower | 是否有鲜花 |
| has_balloon | 是否有气球 |
| group_photo | 用户上传的合照 |
| internal_channel | 内部获客渠道, 即接单人名字, 如果存在 |
| external_channel | 外部获客渠道, 即外部渠道名称, 如果存在 |


返回示例：

```
{
	"status":"true",
	data:{
		"order_id":1,
		"staff_name":"小二",
		"create_time":"2014-02-01 10:00:00",
		"cancel_time":"2014-02-01 10:00:00",
		"arrival_time":"2014-02-01 10:00:00",
		"finish_time":"2014-02-01 10:00:00",
		"status":0,
		"order_id":"001",
		"dinner_date":"2014-02-01",
		"dinner_time":"12:00",
		"dinner_period":0,
		"name":"李四",
		"guest_type":"vip",
		"contact":"18813101211",
		"guest_number":10,
		"desks":[{"id":1,"name":"309"},{"id":2,"name":"312"},{"id":3,"name":"311"}],
		"user_description":"生日宴，准备蜡烛",
		"staff_description":"客户年级大，做好防滑",
		"water_card":"水牌内容",
		"door_card":"门牌内容",
		"sand_table":"沙盘内容",
		"welcome_screen":"欢迎xx领导",
		"welcome_fruit": 128,
		"welcome_card":"欢迎你",
		"pictures":["http://demo.com/1.jpg","http://demo.com/2.jpg", ...],
		"background_music":"我爱你中国",
		"has_candle":true,
		"has_flower":false,
		"has_balloon":false,
		"group_photo":"合照名称",
		"internal_channel":"刘光艳",
		"external_channel":"美团"
	}
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 该订单不存在 |


##编辑订单
URL：webApp/order/update/ <br>
请求方式：POST <br>

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 登录口令          |         yes  |
| order_id| 订单 ID | yes|
| dinner_date | 预定用餐日期 | no |
| dinner_time   | 预定用餐时间  |   no  |
| dinner_period | 订餐时段(0, '午餐'), (1, '晚餐'), (2, '夜宵') | no |
| name | 联系人 | no |
| contact | 联系电话 | no |
| guest_number | 客人数量 | no |
| desks | 桌位 | no |
| staff_description | 员工备注 | no |
|以下是私人订制的字段|
| water_card | 水牌 | no |
| door_card | 门牌 | no |
| sand_table | 沙盘 | no |
| welcome_screen | 欢迎屏 | no |
| welcome_fruit | 迎宾水果的价格 | no |
| welcome_card | 欢迎卡 | no |
| background_music | 背景音乐 | no |
| has_candle | 是否有蜡烛 | no |
| has_flower | 是否有鲜花 | no |
| has_balloon | 是否有气球 | no |

请求示例:


```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"order_id":1,
	"dinner_time":"2014-02-01",
	"dinner_period":0,
	"name":"李四",
	"contact":"18813101211",
	"guest_number":10,
	"desk":[1,3,5],
	"staff_description":"客户年级大，做好防滑",
	"water_card":"水牌内容",
	"door_card":"门牌内容",
	"sand_table":"沙盘内容",
	"welcome_screen":"欢迎xx领导",
	"welcome_fruit": 128,
	"welcome_card":"欢迎你",
	"background_music":"我爱你中国",
	"has_candle":true,
	"has_flower":false,
	"has_balloon":false,
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|


返回示例：

```
{
	"status":"true"
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 不存在该订单 |



## 月订单列表（员工服务的订单，不是填写的预订单）

URL：webApp/order/monthlist/ <br>
请求方式：POST <br>

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 登录口令          |         yes  |

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| month | 月份
order_number | 单数
desk_number | 桌子个数
guest_number | 人数
comsuption | 总消费
person_comsuption | 人均消费
desk_comsuption | 桌均消费

返回示例：

```
{
	"status":"true",
	data:[
		{
			"month":"2017-05",
			"order_number":10,
			"guest_number":100,
			"desk_number":100,
			"comsuption":100000,
			"person_comsuption":1000,
			"desk_comsuption":99
		}
	]
}
```


## 日订单列表

URL：webApp/order/daylist/ <br>
请求方式：POST <br>

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 登录口令          |         yes  |
| month         | 月份          |         yes |


返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| date | 日期
order_number | 单数
desk_number | 桌子个数
guest_number | 人数
comsuption | 总消费
person_comsuption | 人均消费
desk_comsuption | 桌均消费

返回示例

```
{
	"status":"true",
	data:[
		{
			"date":"2015-10-25",
			"order_number":10,
			"guest_number":100,
			"desk_number":100,
			"comsuption":100000,
			"person_comsuption":1000,
			"desk_comsuption":99
		},
		{
			"date":"2015-10-25",
			"order_number":10,
			"guest_number":100,
			"desk_number":100,
			"comsuption":100000,
			"person_comsuption":1000,
			"desk_comsuption":99
		},
		...
	]
}
```
# 客户管理
## 获取客户概况
URL：webApp/guest/profile/general <br>
请求方式：POST

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------|
| token         | 登录口令          |         yes  |

请求示例

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"phone_number":"18813101211"
}
```

返回参数


| 参数名称       | 含义    | 
|:------------- |:---------------| 
| all_guest\_number | 所有客户
active_guest\_number | 活跃客户数量
sleep_guest\_number | 沉睡客户数量
lost_guest\_number | 流失客户数量
blank_guest\_number | 无订单客户数量
guest_from\_manager | 客户来源：客户经理
guest_from\_order | 客户来源：预订台
guest_from\_outer | 客户来源：外部渠道

返回示例


```
{
	"status":"true",
	"data":{
		"all_guest_number":1000,
		"active_guest_number": 1000,
		"sleep_guest_number": 1000,
		"lost_guest_number": 1000,
		"blank_guest_number": 1000,
		"guest_from_manager": 1000,
		"guest_from_order": 1000,
		"guest_from_outer": 1000,
	}
}
```

## 获取客户列表（搜索）

URL：webApp/guest/list/ <br>
请求方式：POST

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------|
| token         | 登录口令          |         yes  |
| search_key | 客户手机号或者姓名 | no |
| guest_type | 客户类型 | no |
| guest_from | 获客渠道| no |

请求示例

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"search_key":"18813101211",
	"guest_type":"vip",
	"guest_from":"客户经理"
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| name | 姓名 |
| birthday | 生日 |
| like | 喜好 |
| dislike | 忌讳 |
| special_day | 纪念日 |
| personal_need | 个性化需求 |
| state | 客户状态：活跃（active），沉睡（sleep），流失（lost）等 |


返回示例

```
{
	"status":"true",
	"data":[
		{
			"name":"习某某",
			"birthday":"1992-02-15",
			"like":"吃辣",
			"dislike":"不吃香菜",
			"special_day":"",
			"personal_need":"",
			"state":"avtive"
		}
	]
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 不存在该条件的用户


## 获取客户档案

URL：webApp/guest/profile/ <br>
请求方式：POST

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------|
| token         | 登录口令          |         yes  |

请求示例

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"phone_number":"18813101211"
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| name | 姓名 |
| birthday | 生日 |
| like | 喜好 |
| dislike | 忌讳 |
| special_day | 纪念日 |
| personal_need | 个性化需求 |
| all_order_number | 历史所有有效订单数 |
| day60_order_number | 最近60天订单数 |
| all_consumption | 所有有效消费 |
| day60_consumption | 最近60天消费金额 |


返回示例

```
{
	"status":"true",
	"data":{
		"name":"习某某",
		"birthday":"1992-02-15",
		"like":"吃辣",
		"dislike":"不吃香菜",
		"special_day":"",
		"personal_need":"",
		"all_order_number":22,
		"day60_order_number":9,
		"all_consumption":10000,
		"day60_consumption:800
	}
}
```

错误代码

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 不存在该手机号码的用户 |


## 客户历史订单列表

URL：webApp/guest/history_orders/ <br>
请求方式：POST

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------|
| token         | 登录口令          |         yes  |
| phone_number | 客户手机号（作为查找的依据） | yes |
| offset | 分页获取的地方（默认为0) | no
| limit | 获取的个数 (默认为20）| no

请求示例

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"phone_number":"18813101211",
	"offset":40,
	"limit":20
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| time | 日期时间 |
| status | 状态((0, '已订'), (1, '客到'), (2, '已完成'), (3, '已撤单'))|
guest_number | 人数
consumption | 消费
desks | 桌位
description | 备注


返回示例

```
{
	"status":"true",
	"data":[
		{
			"time":"2014-05-12 10:00:00",
			"state":0,
			"guest_number":10,
			"consumption":1000,
			"desks":["一楼101"],
			"description":"生日宴 水牌 门牌 沙盘 欢迎屏 背景音乐 气球 欢迎卡 花瓣 蜡烛 手语操作"
		}
	]
}
```

错误代码


| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 不存在该手机号码的用户 |

## 添加客户档案（现场添加客户）
URL：webApp/guest/profile/add <br>
请求方式：POST

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------|
| token         | 登录口令          |         yes  |
| phone_number | 客户手机号（作为查找的依据） | yes |
| name | 姓名 | yes
| birthday | 生日 | yes
| like | 喜好 | yes
| dislike | 忌讳 | yes
| special_day | 纪念日 | yes 
| personal_need | 个性化需求 | yes

请求示例

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"phone_number":"18813101211"
	"name":"习某某",
	"birthday":"1992-02-15",
	"like":"吃辣",
	"dislike":"不吃香菜",
	"special_day":"10-25",
	"personal_need":"生日宴"
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|


返回示例

```
{
	"status":"true"
}
```

错误代码

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 该用户已经注册过 |


## 修改客户档案

URL：webApp/guest/profile/modify <br>
请求方式：POST

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------|
| token         | 登录口令          |         yes  |
| phone_number | 客户手机号（作为查找的依据） | yes |
| name | 姓名 | no
| birthday | 生日 | no
| like | 喜好 | no
| dislike | 忌讳 | no
| special_day | 纪念日 | no 
| personal_need | 个性化需求 | no

请求示例

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"phone_number":"18813101211"
	"name":"习某某",
	"birthday":"1992-02-15",
	"like":"吃辣",
	"dislike":"不吃香菜",
	"special_day":"10-25",
	"personal_need":"生日宴"
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|


返回示例

```
{
	"status":"true"
}
```

错误代码

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 不存在该手机号码的用户 |


# 评分管理
## 获取评分项目
URL：webApp/score/matrix/ <br>
请求方式：POST

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------|
| token         | 登录口令(根据口令判断此员工所属酒店的评分标准）|         yes  |

请求示例：

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF"
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| hotel_name | 酒店名称 |
| branch_name | 店名|
item_key | 项目关键词 （即英文字段名称）
item_name | 项目名称
item_need_picture | 是否需要上传图片(0代表不上传，1代表上传)

返回示例

```
{
	"status":"true",
	"data":[
		{
			"item_key":"door_card",
			"item_name":"门牌",
			"item_need_picture":1
		},
		{
			"item_key":"sand_table",
			"item_name":"沙盘",
			"item_need_picture":1
		},
		....
	]
}
```



## 提交（修改）评分
URL：webApp/score/submit/ <br>
请求方式：POST

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------|
| token         | 登录口令          |         yes  |
| [item_key]\_picture | 项目图片 | no |
| [item_key]\_score | 项目打分 | no |


请求示例

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"door_card_picture":[FILE],
	"door_card_score":10,
	"sand_table_picture":[FILE],
	"sand_table_score":9,
	...
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| score_id | 评分ID |


返回示例

```
{
	"status":"true",
	"data":[
		{
			"score_id":"001"
		}
	]
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |


## 评分排名（酒店）
URL：webApp/score/ranking/hotel <br>
请求方式：POST

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------|
| token         | 登录口令          |         yes  |

请求示例

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| ranking_number | 排名 |
hotel_name | 品牌名称
branch_name | 店名
branch_id | 门店ID
| all_score | 总分 | 
satisfaction_score | 顾客满意度 
transform_score | 转换度
position | 地址
manager | 店总




返回示例

```
{
	"status":"true",
	"data":[
		{
			"ranking_number":3,
			"hotel_name":"北京宴",
			"branch_name":"总店",
			"branch_id":"001",
			"all_score":89,
			"satisfaction_score":9,
			"transform_score":8,
			"position":"北京市蓝靛路",
			"manager":"张某某"
		}
	]
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |


## 评分排名（房间）
URL：webApp/score/ranking/room <br>
请求方式：POST

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------|
| token         | 登录口令          |         yes  |
| hotel_name | 品牌 | no 
branch_name | 门店 | no

请求示例

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"hotel_name":"俏江南",
	"branch_name":"五道口店"
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| ranking_number | 排名 |
hotel_name | 品牌名称
branch_name | 店名
branch_id | 门店ID
| all_score | 总分 | 
satisfaction_score | 顾客满意度 
transform_score | 转换度
position | 地址
manager | 店总



返回示例

```
{
	"status":"true",
	"data":[
		{
			"ranking_number":3,
			"hotel_name":"北京宴",
			"branch_name":"总店",
			"branch_id":"001",
			"all_score":89,
			"satisfaction_score":9,
			"transform_score":8,
			"position":"北京市蓝靛路",
			"manager":"张某某"
		}
	]
}
```

错误代码

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |


## 评分排名（宴会）
URL：webApp/score/ranking/dinner <br>
请求方式：POST

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------|
| token         | 登录口令          |         yes  |
| hotel_name | 品牌 | no 
branch_name | 门店 |  no
type | 宴会类型 | no


```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"hotel_name":"俏江南",
	"branch_name":"五道口店",
	"type":"生日宴"
}
```


返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| ranking_number | 排名 |
hotel_name | 品牌名称
branch_name | 店名
branch_id | 门店ID
| all_score | 总分 | 
satisfaction_score | 顾客满意度 
transform_score | 转换度
position | 地址
manager | 店总

返回示例

```
{
	"status":"true",
	"data":[
		{
			"ranking_number":3,
			"hotel_name":"北京宴",
			"branch_name":"总店",
			"branch_id":"001",
			"all_score":89,
			"satisfaction_score":9,
			"transform_score":8,
			"position":"北京市蓝靛路",
			"manager":"张某某"
		}
	]
}
```
错误代码

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |


## 评分详情

URL：webApp/score/ranking/dinner <br>
请求方式：POST

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------|
| token         | 登录口令          |         yes  |
| ranking_id | 排名ID | yes |



返回参数：

| 参数名称       | 二级参数   |    含义   |
|:------------- |:---------------|:---|
| ranking_number | 排名 |
| all_score | | 总分 | 
hotel_name | | 品牌名称
branch_id | | 门店ID
branch_name| | 店名
position || 地址
manageer || 店总
items |  所有的评分项
||item_key | 评分关键词
||item_name | 评分名称
||item_score | 评分
||item_check\_score | 复查分数


返回示例

```
{
	"status":"true",
	"data":[
		{
			"ranking_number":3,
			"all_score":89,
			"hotel_name":"俏江南",
			"branch_id":"001",
			"branch_name":"三里屯店",
			"position":"北京市蓝靛路",
			"manager":"张某某",
			"items":[
				{
					"item_key":"door_card",
					"item_name":"门牌",
					"item_score":100,
					"item_check_score":9
				},
				{
					"item_key":"door_card",
					"item_name":"门牌",
					"item_score":100,
					"item_check_score":9
				}
				
			]
		}
	]
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 不存在该排名 |


#消息推送
客户端给服务端推送，以json表示数据:

| 参数名称       | 含义             |
|:------------- |:---------------| :-------------:|
| push_id        | 推送事件ID         |         yes  |
| push_type | 推送事件类型（订单提醒、客户服务等，待定）| yes |
| push_data | 事件处理需要的信息（如订单ID等） | yes |
| message        | 消息文字通知         |         yes  |

推送示例:


```
{
	"push_id":"129ASDFIOJIO3RN23U12934INASDF",
	"push_type":"order notify",
	"push_data":"19u390joasdifoasf",
	"message":"xx订单即将开始，请准备"
}
```
