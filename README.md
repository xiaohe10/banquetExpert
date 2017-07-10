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

## 获取验证码（有效时间10分钟，访问频率1分钟）
URL：webApp/staff/validation_code/
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| phone         | 手机号          |         yes    |

请求示例：

```
{
	"phone":"18813101211",
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
| err_2 | 接口访问频率限制 |


## 注册
URL：webApp/staff/register/ <br>
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
URL：webApp/staff/login/ <br>
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
URL：webApp/staff/pass_modify/ <br>
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

URL：webApp/staff/hotel/ <br>
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


## 搜索我的订单列表
URL：webApp/staff/order/search/ <br>
请求方式：POST <br>

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 登录口令          |         yes  |
| order_date    | 下单日期  |   no |
| dinner_period | 餐段，0：午餐，1：晚餐，2：夜宵    |   no |
| dinner_date   | 预定用餐日期  |   no  |
| dinner_time   | 预定用餐时间  |   no  |
| status | 订单状态（0: 进行中，1: 已完成，2: 已删除，默认为0）  | no |
| search_key | 搜索关键词（如姓名、手机等进行模糊搜索） | no |
| offset | 起始值（默认0） | no |
| limit | 偏移量（默认10） | no |
| order | 排序方式（0: 注册时间升序，1: 注册时间降序，默认1） | no |


请求示例:


```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"status":0,
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
| consumption   | 消费金额  |
| status | 状态((0, '已订'), (1, '客到'), (2, '已完成'), (3, '已撤单'))|
| dinner_date | 预定用餐日期 |
| dinner_time   | 预定用餐时间  |
| dinner_period | 订餐时段(0, '午餐'), (1, '晚餐'), (2, '夜宵') |
| name | 联系人 |
| contact | 联系电话 |
| guest_type | 顾客身份 |
| guest_number | 客人数量 |
| desks | 桌位ID数组 |
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
            "consumption":1000,
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


# 酒店接口

## 获取所有酒店列表

URL：webApp/hotel/list/ <br>
请求方式：POST <br>

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| offset | 起始值（默认0） | no |
| limit | 偏移量（默认10） | no |
| order | 排序方式（0: 注册时间升序，1: 注册时间降序，2: 名称升序，3: 名称降序，默认1） | no |

请求示例:


```
{

}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| count | 酒店总数  |
| list  |   酒店列表    |
| 以下为list中的数据   |
| hotel_id | 酒店 ID |
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
	    "count":100,
	    "list":{[
            "hotel_id":1,
            "name":"北京宴",
            "icon":"http://oss.aliyun/banquet/avatar/1.jpg",
            "branches_count":3,
            "owner_name":"杨秀荣",
            "create_time":"创建时间"
            ],
            ...
		}
	}
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |


## 获取酒店的门店列表
URL：webApp/hotel/hotel_branch/list/ <br>
请求方式：POST <br>

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| offset | 起始值（默认0） | no |
| limit | 偏移量（默认10） | no |
| order | 排序方式（0: 注册时间升序，1: 注册时间降序，2: 名称升序，3: 名称降序，默认1） | no |

请求示例:


```
{

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
| pictures | 介绍图片（最多5张，数组） |
| province | 省 |
| city | 城市 |
| county | 区/县 |
| address | 详细地址 |
| meal_period | 餐段设置（键值对） |
| facility | 设施（数组） |
| pay_card | 可以刷哪些卡（数组） |
| personal_tailor   | 私人订制项(最多10个，数组) |
| phone | 联系电话（最多3个，数组） |
| cuisine | 菜系（键值对） |
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
		"meal_period":{
            "Monday":{
                "lunch":{"from": "8:30","to": "12:00"},
                "dinner":{"from":"12:00","to":"18:00"},
                "supper":{"from":"18:00","to":"24:00"}
            },
            "TuesDay":{
                "lunch":{"from": "8:30","to": "12:00"},
                "dinner":{"from":"12:00","to":"18:00"},
                "supper":{"from":"18:00","to":"24:00"}
            },
            ...
        },
		"facility":["停车场","吸烟区"],
		"pay_card":["银联", "支付宝"],
		"personal_tailor":[
            {
                "name": "门牌",
                "labels": ["a", "b"],
                "order":1
            },
            {
                "name": "沙盘",
                "labels": ["a", "b"],
                "order":2
            },
            ...
        ]
		"phone":["13011111111", "13100000000"],
		"cuisine":{
		    "北京菜":["烤鸭","京酱肉丝"],
		    "浙江菜":["鸡"]
		},
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


## 获取门店的区域列表（根据order逆序排列）
URL：webApp/hotel_branch/area/list/ <br>
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
| count | 区域总数 |
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
		    "order":10,
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


## 获取门店某一天某餐段的桌位使用情况列表（根据order逆序排列）
URL：webApp/hotel_branch/desk/list/ <br>
请求方式：POST <br>

| 请求参数      | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 登录口令          |         yes  |
| branch_id | 门店 ID | yes |
| date  | 日期 | yes |
| dinner_period | 餐段（0:午餐, 1:晚餐, 2:夜宵）  | yes   |
| area_id   | 区域 ID | no    |

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
| count | 桌位总数 |
| list | 桌位列表 |
|以下为list中的数据|
| desk_id | 桌位 ID |
| number | 桌位编号 |
| status    | 桌位状态0: 空闲, 1: 预定中, 2: 用餐中  |
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
	        "number":"202",
	        "status":0,
		    "area_name":"一楼",
		    "order":1,
		    "min_guest_num":10,
		    "max_guest_num":15,
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

## 提交订单（今天及以后的订单）
URL：webApp/order/submit/ <br>
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
| desks | 桌位ID的数组 | yes |
| banquet   | 宴会类型，来自36宴  | no    |
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
	"banquet":"满月宴",
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
| err_3 | 桌位不存在 |
| err_4 | 桌位已被预定    |
| err_5 | 补录订单日期不能大于当前日期    |
| err_6 | 服务器创建订单错误 |


## 搜索订单列表
URL：webApp/order/search/ <br>
请求方式：POST <br>

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 登录口令          |         yes  |
| order_date    | 下单日期  |   no |
| dinner_period | 餐段，0：午餐，1：晚餐，2：夜宵    |   no |
| dinner_date   | 预定用餐日期  |   no  |
| dinner_time   | 预定用餐时间  |   no  |
| status | 订单状态（0: 进行中，1: 已完成，2: 已删除，默认为0）  | no |
| search_key | 搜索关键词（如姓名、手机等进行模糊搜索） | no |
| offset | 起始值（默认0） | no |
| limit | 偏移量（默认10） | no |
| order | 排序方式（0: 注册时间升序，1: 注册时间降序，默认1） | no |


请求示例:


```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"status":0,
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
| consumption   | 消费金额  |
| status | 状态((0, '已订'), (1, '客到'), (2, '已完成'), (3, '已撤单'))|
| dinner_date | 预定用餐日期 |
| dinner_time   | 预定用餐时间  |
| dinner_period | 订餐时段(0, '午餐'), (1, '晚餐'), (2, '夜宵') |
| name | 联系人 |
| contact | 联系电话 |
| guest_type | 顾客身份 |
| guest_number | 客人数量 |
| desks | 桌位ID数组 |
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
            "consumption":1000,
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
URL：webApp/order/profile/ <br>
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
| consumption   | 消费金额  |
| status | 状态((0, '已订'), (1, '客到'), (2, '已完成'), (3, '已撤单'))|
| dinner_date | 预定用餐日期 | yes |
| dinner_time   | 预定用餐时间  |   yes  |
| dinner_period | 订餐时段(0, '午餐'), (1, '晚餐'), (2, '夜宵') | yes |
| name | 联系人 |
| guest_type | 顾客身份 |
| contact | 联系电话 |
| guest_number | 客人数量 |
| banquet   | 宴会类型  |
| desks | 桌位ID和编号 |
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
		"consumption":1000,
		"status":0,
		"order_id":"001",
		"dinner_date":"2014-02-01",
		"dinner_time":"12:00",
		"dinner_period":0,
		"name":"李四",
		"guest_type":"vip",
		"contact":"18813101211",
		"guest_number":10,
		"banquet":"满月宴",
		"desks":[{"desk_id":1,"number":"309"},{"desk_id":2,"number":"312"},{"desk_id":3,"number":"311"}],
		"user_description":"生日宴，准备蜡烛",
		"staff_description":"客户年纪大，做好防滑",
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
| status | 订单状态, 0: 已订, 1: 客到, 2: 已完成, 3: 已撤单   | no    |
| banquet   | 宴会类型，来自36宴    | no    |
| name | 联系人 | no |
| contact | 联系电话 | no |
| guest_number | 客人数量 | no |
| desks | 桌位ID数组 | no |
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
	"status":2,
	"banquet":"满月宴",
	"name":"李四",
	"contact":"18813101211",
	"guest_number":10,
	"desk":[1,3,5],
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

URL：webApp/order/month_list/ <br>
请求方式：POST <br>

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 登录口令          |         yes  |
| year          | 年份，默认为当前年份 |          no  |

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| month | 月份
order_number | 单数
desk_number | 桌子个数
guest_number | 人数
consumption | 总消费
person_consumption | 人均消费
desk_consumption | 桌均消费

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
			"consumption":100000,
			"person_consumption":1000,
			"desk_consumption":99
		},
		...
	]
}
```


## 日订单列表

URL：webApp/order/day_list/ <br>
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
consumption | 总消费
person_consumption | 人均消费
desk_consumption | 桌均消费

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
			"consumption":100000,
			"person_consumption":1000,
			"desk_consumption":99
		},
		{
			"date":"2015-10-25",
			"order_number":10,
			"guest_number":100,
			"desk_number":100,
			"consumption":100000,
			"person_consumption":1000,
			"desk_consumption":99
		},
		...
	]
}
```

## 搜索员工自己的订单列表
URL：webApp/staff/order/search/ <br>
请求方式：POST <br>

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 登录口令          |         yes  |
| order_date    | 下单日期  |   no |
| date_start    | 起始日期  | no    |
| date_end  | 终止日期  | no    |
| desk_id   | 桌位ID  | no    |
| dinner_period | 餐段，0：午餐，1：晚餐，2：夜宵    |   no |
| dinner_date   | 预定用餐日期  |   no  |
| dinner_time   | 预定用餐时间  |   no  |
| status | 订单状态（0: 进行中，1: 已完成，2: 已删除，默认为0）  | no |
| search_key | 搜索关键词（如姓名、手机等进行模糊搜索） | no |
| offset | 起始值（默认0） | no |
| limit | 偏移量（默认10） | no |
| order | 排序方式（0: 注册时间升序，1: 注册时间降序，默认1） | no |


请求示例:


```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"status":0,
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
| consumption   | 消费金额  |
| status | 状态((0, '已订'), (1, '客到'), (2, '已完成'), (3, '已撤单'))|
| dinner_date | 预定用餐日期 |
| dinner_time   | 预定用餐时间  |
| dinner_period | 订餐时段(0, '午餐'), (1, '晚餐'), (2, '夜宵') |
| name | 联系人 |
| contact | 联系电话 |
| guest_type | 顾客身份 |
| guest_number | 客人数量 |
| desks | 桌位ID数组 |
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
            "consumption":1000,
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


## 补录订单（今天及以前的订单）
URL：webApp/order/supply/ <br>
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
| desks | 桌位ID的数组 | yes |
| banquet   | 宴会类型，来自36宴  | no    |
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
	"banquet":"满月宴",
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
| err_3 | 桌位不存在 |
| err_4 | 补录订单日期不能大于当前日期    |
| err_5 | 服务器创建订单错误 |

# 我的客户

## 获取员工的客户列表（搜索）

URL：webApp/staff/guest/list/ <br>
请求方式：POST

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------|
| token         | 登录口令          |         yes  |
| search_key | 客户手机号或者姓名 | no |
| status | 客户状态，0：全部，1：活跃，2：沉睡，3：流失，4：无订单，默认0 | no |
| offset | 起始值（默认0） | no |
| limit | 偏移量（默认10） | no |

请求示例

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"search_key":"18813101211"
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| count | 顾客总数 |
| list  | 顾客列表 |
| 以下为list中的数据 |
| guest_id  | 顾客 ID |
| phone | 电话    |
| name | 姓名 |
| gender    | 性别，0:保密，1:男，2:女    |
| birthday | 生日 |
| birthday_type | 生日类型，0:阳历，1:农历 |
| guest_type  | 顾客类别  |
| like | 喜好 |
| dislike | 忌讳 |
| special_day | 纪念日 |
| personal_need | 个性化需求 |
| status | 客户状态：1：活跃，2：沉睡，3：流失，4：无订单 |
| desk_number   | 消费总桌数 |
| person_consumption    | 人均消费  |
| order_per_month    | 消费频度, 单/月 |
| last_consumption  | 上次消费日期    |


返回示例

```
{
	"status":"true",
	"data":
	{
	    "count":100,
	    "list":[
	    {
	        "guest_id":1,
	        "phone":"13111111111",
			"name":"习某某",
			"gender":1,
			"guest_type":"vip",
			"birthday":"1992-02-15",
			"birthday_type":0,
			"like":"吃辣",
			"dislike":"不吃香菜",
			"special_day":"",
			"personal_need":"",
			"status":1,
			"desk_number":10,
			"person_consumption":400,
			"order_per_month":3.11,
			"last_consumption":"1993-02-25"
		},
		...
		]
	}
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 不存在该条件的用户 |


## 获取员工的客户统计
URL：webApp/staff/guest/statistic/ <br>
请求方式：POST

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------|
| token         | 登录口令          |         yes  |

请求示例

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF"
}
```

返回参数


| 参数名称       | 含义    |
|:------------- |:---------------|
| all_guest\_number | 所有客户
active_guest\_number | 活跃客户数量
sleep_guest\_number | 沉睡客户数量
lost_guest\_number | 流失客户数量

返回示例


```
{
	"status":"true",
	"data":{
		"all_guest_number":1000,
		"active_guest_number": 1000,
		"sleep_guest_number": 1000,
		"lost_guest_number": 1000
	}
}
```


# 客户管理

## 获取客户概况
URL：webApp/guest/profile/general/ <br>
请求方式：POST

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------|
| token         | 登录口令          |         yes  |

请求示例

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF"
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

## 获取客户来源（内部销售和外部销售）
URL：webApp/guest/channel/list/ <br>
请求方式：POST

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------|
| token         | 登录口令          |         yes  |

请求示例

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF"
}
```

返回参数


| 参数名称       | 含义    |
|:------------- |:---------------|
| internal_channel | 内部销售  |
| external_channel | 外部销售  |
| id    | 对应销售的ID   |
| name  | 对应销售的名称   |

返回示例


```
{
	"status":"true",
	"data":
	{
	    "internal_channel":
	    [
            {
                "id":1,
                "name":"刘光艳"
            },
            ...
	    ]
		"external_channel":
		[
            {
                "id":1,
                "name":"美团"
            },
            ...
		]
	}
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_3 | 不存在该条件的用户

## 获取客户列表（搜索）

URL：webApp/guest/list/ <br>
请求方式：POST

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------|
| token         | 登录口令          |         yes  |
| search_key | 客户手机号或者姓名 | no |
| status | 客户状态：0：全部，1：活跃，2：沉睡，3：流失，4：无订单，默认0 | no |
| internal_channel | 内部销售ID | no |
| external_channel | 外部销售ID | no |
| offset | 起始值（默认0） | no |
| limit | 偏移量（默认10） | no |
| order | 排序方式（0: 最近就餐，1: 总预定桌数，2: 人均消费，3: 消费频度，默认0） | no |

请求示例

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"search_key":"18813101211",
	"status":0,
	"internal_channel":1
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| count | 顾客总数 |
| list  | 顾客列表 |
| 以下为list中的数据 |
| guest_id  | 顾客 ID |
| phone | 电话    |
| name | 姓名 |
| gender    | 性别，0:保密，1:男，2:女    |
| birthday | 生日 |
| birthday_type | 生日类型，0:阳历，1:农历 |
| guest_type  | 顾客类别  |
| like | 喜好 |
| dislike | 忌讳 |
| special_day | 纪念日 |
| personal_need | 个性化需求 |
| status | 客户状态：1：活跃，2：沉睡，3：流失，4：无订单 |
| desk_number   | 消费总桌数 |
| person_consumption    | 人均消费  |
| order_per_month    | 消费频度, 单/月 |
| last_consumption  | 上次消费日期    |


返回示例

```
{
	"status":"true",
	"data":
	{
	    "count":100,
	    "list":[
	    {
	        "guest_id":1,
	        "phone":"13111111111",
			"name":"习某某",
			"gender":1,
			"guest_type":"vip",
			"birthday":"1992-02-15",
			"birthday_type":0,
			"like":"吃辣",
			"dislike":"不吃香菜",
			"special_day":"",
			"personal_need":"",
			"status":1,
			"desk_number":10,
			"person_consumption":400,
			"order_per_month":3.11,
			"last_consumption":"1993-02-25"
		},
		...
		]
	}
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 不存在该条件的用户 |
| err_4 | 内部销售渠道不存在 |
| err_5 | 外部销售渠道不存在 |


## 获取客户档案（根据顾客ID或手机）

URL：webApp/guest/profile/ <br>
请求方式：POST

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------|
| token         | 登录口令          |         yes  |
| guest_id      | 顾客 ID          |         no   |
| phone         | 手机             |         no  |

请求示例

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"phone":"18813101211"
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| name | 姓名 |
| gender    | 性别，0:保密，1:男，2:女   |
| phone | 电话    |
| guest_type  | 顾客类别  |
| birthday | 生日 |
| birthday_type | 生日类型，0:阳历，1:农历 |
| like | 喜好 |
| dislike | 忌讳 |
| special_day | 纪念日 |
| personal_need | 个性化需求 |
| status    | 客户状态, 1: 活跃, 2: 沉睡, 3: 流失, 4: 无订单 |
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
		"gender":1,
		"phone":"13111111111",
		"guest_type":"vip",
		"birthday":"1992-02-15",
		"birthday_type":0,
		"like":"吃辣",
		"dislike":"不吃香菜",
		"special_day":"",
		"personal_need":"",
		"status":1,
		"all_order_number":22,
		"day60_order_number":9,
		"all_consumption":10000,
		"day60_consumption:800
	}
}
```

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
| phone | 客户手机号（作为查找的依据） | yes |
| offset | 分页获取的地方（默认为0) | no
| limit | 获取的个数 (默认为20）| no

请求示例

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"phone":"18813101211",
	"offset":40,
	"limit":20
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| count | 数量    |
| list  | 列表    |
| 以下为list中的数据   |
| time | 日期时间 |
| status | 状态((0, '已订'), (1, '客到'), (2, '已完成'), (3, '已撤单'))|
guest_number | 人数
consumption | 消费
area    | 区域
desks | 桌位
description | 备注


返回示例

```
{
	"status":"true",
	"data":
	{
        "count":10,
        "list":{
        [
            "time":"2014-05-12 10:00:00",
            "status":0,
            "guest_number":10,
            "consumption":1000,
            "area":"一楼",
            "desks":["101"],
            "description":"生日宴 水牌 门牌 沙盘 欢迎屏 背景音乐 气球 欢迎卡 花瓣 蜡烛 手语操作"
	    ]
	    ...
	    }
	}
}
```

错误代码


| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 不存在该手机号码的用户 |

## 添加客户档案（现场添加客户）
URL：webApp/guest/profile/add/ <br>
请求方式：POST

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------|
| token         | 登录口令          |         yes  |
| phone | 客户手机号（作为查找的依据） | yes |
| name | 姓名 | yes |
| gender    | 性别，0:保密，1:男，2:女   | no    |
| guest_type | 客户类别 | no    |
| birthday | 生日 | no    |
| birthday_type | 生日类型，0:阳历，1:农历 | no   |
| like | 喜好 | no    |
| dislike | 忌讳 | no |
| special_day | 纪念日 | no    |
| personal_need | 个性化需求 | no    |

请求示例

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"phone":"18813101211"
	"name":"习某某",
	"gender":1,
	"guest_type":"vip",
	"birthday":"1992-02-15",
	"birthday_type":0,
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

URL：webApp/guest/profile/modify/ <br>
请求方式：POST

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------|
| token         | 登录口令          |         yes  |
| phone | 客户手机号（作为查找的依据） | yes |
| name | 姓名 | no
| gender    | 性别，0:保密，1:男，2:女   | no
| guest_type | 客户类型 | no
| birthday | 生日 | no
| birthday_type | 生日类型，0:阳历，1:农历 | no
| like | 喜好 | no
| dislike | 忌讳 | no
| special_day | 纪念日 | no 
| personal_need | 个性化需求 | no

请求示例

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"phone":"18813101211"
	"name":"习某某",
	"gender":1,
	"birthday":"1992-02-15",
	"birthday_type":0,
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

## 获取评分列表
URL：webApp/score/list/ <br>
请求方式：POST <br>

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 登录口令          |         yes  |
| order_date    | 下单日期  |   no |
| dinner_period | 餐段    |   no |
| dinner_date   | 预定用餐日期  |   no  |
| dinner_time   | 预定用餐时间  |   no  |
| search_key | 搜索关键词（如姓名、手机等进行模糊搜索） | no |
| offset | 起始值（默认0） | no |
| limit | 偏移量（默认10） | no |
| order | 排序方式（0: 注册时间升序，1: 注册时间降序，默认1） | no |


请求示例:


```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"search_key":"张总",
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| count | 订单数量 |
| list | 订单列表 |
| 以下为list中的数据 |
| score_id  | 评分记录ID    |
| order_id  | 订单ID |
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
| desks | 桌位ID数组 |
| internal_channel | 内部获客渠道, 即接单人名字, 如果存在 |
| external_channel | 外部获客渠道, 即外部渠道名称, 如果存在 |
| score | 总分    |


返回示例：

注意：返回的订单列表以数组来表示

```
{
	"status":"true",
	"data":{
	    "count":100,
	    "list":[
	        "score_id":1,
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
            "external_channel":"美团",
            "score":200
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


## 获取评分详情
URL：webApp/score/matrix/ <br>
请求方式：POST

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------|
| token         | 登录口令(根据口令判断此员工所属酒店的评分标准）|         yes  |
| score_id  | 评分记录 ID   | yes   |

请求示例：

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"score_id":1
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| item_type | 项目类型  |
| total_score   | 总分    |
| list  |   评分列表    |
| 以下为list中的数据   |
| item_key | 项目关键词 （即英文字段名称）    |
| item_name | 项目名称  |
| item_need_picture | 是否需要上传图片(0代表不上传，1代表上传)    |
| item_picture  | 图片地址  |
| item_score    | 评分    |

返回示例

```
{
	"status":"true",
	"data":[
	{
        "item_type":"私人订制",
        "total_score":20,
        "list":[
        {
            "item_key":"door_card",
            "item_name":"门牌",
            "item_need_picture":1,
            "item_picture":"图片地址",
            "item_score":9
        },
        {
            "item_key":"sand_table",
            "item_name":"沙盘",
            "item_need_picture":1,
            "item_picture":"图片地址",
            "item_score":9
        },
        ....
        ]
    }
    {
        "item_type":"顾客满意度",
        "total_score":20,
        "list":[
        {
            "item_key":"praise_letter",
            "item_name":"表扬信",
            "item_need_picture":1,
            "item_picture":"图片地址",
            "item_score":9
        },
        {
            "item_key":"friend_circle",
            "item_name":"朋友圈",
            "item_need_picture":1,
            "item_picture":"图片地址",
            "item_score":9
        },
        ....
        ]
    }
    ...
	]
}
```

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
| item_type | 项目类型  |
| item_key | 项目关键词 （即英文字段名称）    |
| item_name | 项目名称  |
| item_need_picture | 是否需要上传图片(0代表不上传，1代表上传)    |

返回示例

```
{
	"status":"true",
	"data":[
	{
        "item_type":"私人订制",
        "list":[
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
    {
        "item_type":"顾客满意度",
        "list":[
        {
            "item_key":"praise_letter",
            "item_name":"表扬信",
            "item_need_picture":1
        },
        {
            "item_key":"friend_circle",
            "item_name":"朋友圈",
            "item_need_picture":1
        },
        ....
        ]
    }
    ...
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
URL：webApp/score/ranking/hotel/ <br>
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
URL：webApp/score/ranking/room/ <br>
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
URL：webApp/score/ranking/dinner/ <br>
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

URL：webApp/score/ranking/dinner/ <br>
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
|:------------- |:---------------| 
| push_id        | 推送事件ID         |
| push_type | 推送事件类型（订单提醒、客户服务等，待定）|
| push_data | 事件处理需要的信息（如订单ID等） |
| message        | 消息文字通知         | 

推送示例:


```
{
	"push_id":"129ASDFIOJIO3RN23U12934INASDF",
	"push_type":"order notify",
	"push_data":"19u390joasdifoasf",
	"message":"xx订单即将开始，请准备"
}
```

# 超级管理员接口（web端）


## 注册
URL：webApp/super_admin/register/ <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 令牌          |         yes    |
| username  | 用户名，最多20位          |         yes    |
| password      | 密码（MD5加密后结果，32位）  |         yes    |
| type   | 类型，0: 管理员，1: 超级管理员，默认1   |   no |
| hotel_id      | 管理员所属酒店ID，超管不传          |         no    |

请求示例：

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"username":"admin",
	"password":"f344e6af76dba76214024c7b327eff78",
	"type":0,
	"hotel_id":1
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| admin_id | 管理员账号ID |

返回示例：

```
{
	"status":"true",
	"data":{
		"admin_id":1
	}
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误  |
| err_3 | 该酒店不存在 |
| err_4 | 该用户名已经注册 |
| err_5 | 服务器创建管理员失败 |


## 登录
URL：webApp/super_admin/login/ <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| username         | 用户名          |         yes    |
| password      | 密码（MD5加密后结果，32位）  |         yes    |

请求示例：

```
{
	"username":"admin",
	"password":"f344e6af76dba76214024c7b327eff78"
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| token | 令牌 |

返回示例：

```
{
	"status":"true",
	"data":{
		"token":"129ASDFIOJIO3RN23U12934INASDF"
	}
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 管理员不存在 |
| err_3 | 密码错误 |


## 获取管理员列表
URL：webApp/super_admin/list/ <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 令牌          |         yes    |
| is_enabled    | 是否有效管理员，默认是   |   no  |
| offset | 起始值（默认0） | no |
| limit | 偏移量（默认10） | no |
| order | 排序方式（0: 注册时间升序，1: 注册时间降序，2: 名称升序，3: 名称降序，默认1） | no |

请求示例：

```
{
    "token":"129ASDFIOJIO3RN23U12934INASDF"
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| count | 管理员数  |
| list | 管理员列表 |
| 以下为list中的数据    |
| admin_id  | 管理员 ID    |
| username  | 用户名   |
| type  | 类别, 0: 管理员, 1: 超级管理员  |
| hotel_name    | 所属酒店名，超级管理员不属于任何酒店，返回''   |
| authority | 权限    |
| is_enabled    | 是否有效  |
| create_time   | 创建时间  |

返回示例：

```
{
	"status":"true",
	"data":{
	    "count":20,
	    "list":{[
		    "admin_id":1,
		    "username":"admin",
		    "type":1,
		    "hotel_name":"",
		    "authority":"权限",
		    "is_enabled":"True",
		    "create_time":"创建时间"
		    ],
		    ...
		}
	}
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 管理员不存在 |


## 修改管理员
URL：webApp/super_admin/delete/ <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 令牌          |         yes    |
| admin_id      | 管理员ID          |         yes    |
| username  | 用户名   | no    |
| password  | 密码    | no    |
| is_enabled    | 是否有效  | no    |

请求示例：

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"admin_id":1
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
| err_2 | 权限错误  |
| err_3 | 管理员不存在  |
| err_4 | 操作错误 |


## 获取酒店列表
URL：webApp/super_admin/hotel/list/ <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 令牌          |         yes    |
| is_enabled    | 是否有效，默认是   |   no  |
| offset | 起始值（默认0） | no |
| limit | 偏移量（默认10） | no |
| order | 排序方式（0: 注册时间升序，1: 注册时间降序，2: 名称升序，3: 名称降序，默认1） | no |

请求示例：

```
{
    "token":"129ASDFIOJIO3RN23U12934INASDF"
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| count | 酒店数  |
| list | 酒店列表 |
| 以下为list中的数据    |
| hotel_id  | 酒店 ID    |
| name  | 名称   |
| icon  | 头像  |
| branches_count  | 门店数   |
| owner_name    | 法人代表   |
| branch_number | 门店数量上限    |
| service   | 开通的服务 |
| is_enabled    | 是否有效  |
| create_time   | 创建时间  |

返回示例：

```
{
	"status":"true",
	"data":{
	    "count":20,
	    "list":{[
		    "hotel_id":1,
		    "name":"北京宴",
		    "icon":"头像地址",
		    "branches_count":10,
		    "owner_name":"杨秀荣",
		    "branch_number":3,
            "service":{
                "order_analyze":True,
                "source_statistic":True
            },
		    "is_enabled":"True",
		    "create_time":"创建时间"
		    ],
		    ...
		}
	}
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 管理员不存在 |


## 注册酒店
URL：webApp/super_admin/hotel/register/ <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 令牌          |         yes    |
| name  | 用户名，最多20位          |         yes    |
| owner_name      | 公司法人  |         yes    |
| branch_number | 门店数量上限    | no    |

请求示例：

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"name":"北京宴",
	"owner_name":"杨秀荣",
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| hotel_id | 酒店 ID |

返回示例：

```
{
	"status":"true",
	"data":{
		"hotel_id":1
	}
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误  |
| err_3 | 管理员不存在 |
| err_4 | 酒店名已注册 |
| err_5 | 服务器创建酒店失败 |


## 删除酒店
URL：webApp/super_admin/hotel/delete/ <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 令牌          |         yes    |
| hotel_id      | 酒店ID          |         yes    |

请求示例：

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"hotel_id":1
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
| err_2 | 权限错误  |
| err_3 | 管理员不存在  |
| err_4 | 该酒店不存在 |


## 获取酒店信息
URL：webApp/super_admin/hotel/profile/get/ <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 令牌          |         yes    |
| hotel_id      | 酒店ID          |         yes    |

请求示例：

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"hotel_id":1
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| hotel_id  | 酒店 ID |
| name  | 酒店名   |
| icon  | 头像    |
| branches_count    | 门店数   |
| owner_name    | 法人    |
| branch_number | 门店数量上限    |
| service   | 开通的服务 |
| is_enabled    | 是否有效  |
| create_time   | 创建时间  |

返回示例：

```
{
	"status":"true"
	"data":{
	    "hotel_id":1,
	    "name":"北京宴",
	    "icon":"头像地址",
	    "branches_count":10,
	    "owner_name":"杨秀荣",
	    "branch_number":10,
	    "service":{
	        "order_analyze":True,
	        "source_statistic":True
	    },
	    "is_enabled":"True",
	    "create_time":"创建时间"
	}
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误  |
| err_3 | 管理员不存在  |
| err_4 | 酒店不存在 |


## 删除酒店
URL：webApp/super_admin/hotel/delete/ <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 令牌          |         yes    |
| hotel_id      | 酒店ID          |         yes    |

请求示例：

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"hotel_id":1
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
| err_2 | 权限错误  |
| err_3 | 管理员不存在  |
| err_4 | 该酒店不存在 |


## 修改酒店信息
URL：webApp/super_admin/hotel/profile/modify/ <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 令牌          |         yes    |
| hotel_id      | 酒店ID          |         yes    |
| name  | 酒店名   | no  |
| owner_name    | 法人    | no    |
| branch_number | 门店数量上限    | no    |
| service   | 开通的服务 |   no  |
| icon  | 头像，file格式    | no    |

请求示例：

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"hotel_id":1,
	"name":"珍珠大饭店",
	"owner":"梅本山",
	"branch_number":10,
	"service":{
	        "order_analyze":True,
	        "source_statistic":True
	    },
	"icon":"[file]"
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
| err_2 | 权限错误  |
| err_3 | 管理员不存在  |
| err_4 | 酒店不存在 |
| err_5 | 酒店名已注册 |
| err_6 | 图片为空或图片格式错误 |


# 管理员接口

## 登录
URL：webApp/admin/login/ <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| username         | 用户名          |         yes    |
| password      | 密码（MD5加密后结果，32位）  |         yes    |

请求示例：

```
{
	"username":"admin",
	"password":"f344e6af76dba76214024c7b327eff78"
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| token | 令牌 |

返回示例：

```
{
	"status":"true",
	"data":{
		"token":"129ASDFIOJIO3RN23U12934INASDF"
	}
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 管理员不存在 |
| err_3 | 密码错误 |


## 获取自己酒店信息
URL：webApp/admin/hotel/profile/get/ <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 令牌          |         yes    |

请求示例：

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF"
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| hotel_id  | 酒店 ID |
| name  | 酒店名   |
| icon  | 头像    |
| branches_count    | 门店数   |
| owner_name    | 法人    |
| branch_number | 门店数量上限    |
| service   | 开通的服务 |
| create_time   | 创建时间  |

返回示例：

```
{
	"status":"true"
	"data":{
	    "hotel_id":1,
	    "name":"北京宴",
	    "icon":"头像地址",
	    "branches_count":10,
	    "owner_name":"杨秀荣",
	    "branch_number":3,
	    "service":{
	        "order_analyze":True,
	        "source_statistic":True
	    },
	    "create_time":"创建时间"
	}
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误  |
| err_3 | 管理员不存在  |
| err_4 | 酒店不存在 |


## 修改酒店信息
URL：webApp/admin/hotel/profile/modify/ <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 令牌          |         yes    |
| hotel_id      | 酒店ID          |         yes    |
| name  | 酒店名   | no  |
| owner_name    | 法人    | no    |
| icon  | 头像，file格式    | no    |

请求示例：

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"hotel_id":1,
	"name":"珍珠大饭店",
	"owner":"梅本山",
	"icon":"[file]"
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
| err_2 | 权限错误  |
| err_3 | 管理员不存在  |
| err_4 | 酒店不存在 |
| err_5 | 酒店名已注册 |
| err_6 | 图片为空或图片格式错误 |


## 获取酒店门店列表
URL：webApp/admin/hotel_branch/list/ <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 令牌          |         yes    |
| hotel_id  | 酒店 ID | yes   |
| is_enabled    | 是否有效，默认是   |   no  |
| offset | 起始值（默认0） | no |
| limit | 偏移量（默认10） | no |
| order | 排序方式（0: 注册时间升序，1: 注册时间降序，2: 名称升序，3: 名称降序，默认1） | no |

请求示例：

```
{
    "token":"129ASDFIOJIO3RN23U12934INASDF",
    "hotel_id":1
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| count | 门店数  |
| list | 门店列表 |
| 以下为list中的数据    |
| branch_id  | 门店 ID    |
| name  | 名称   |
| icon  | 头像  |
| pictures  | 介绍图片（最多5张，数组） |
| province  | 省 |
| city  | 市 |
| county    | 区/县   |
| address   | 详细地址  |
| facility  | 设施（数组）    |
| pay_card  | 可以哪些支付（数组） |
| phone | 电话（最多3个，数组）   |
| hotel_name    | 所属酒店名   |
| manager_name    | 店长名  |
| create_time   | 创建时间  |

返回示例：

```
{
	"status":"true",
	"data":{
	    "count":20,
	    "list":{[
		    "branch_id":1,
		    "name":"北京宴总店",
		    "icon":"头像地址",
		    "pictures":["picture1","picture2"],
		    "province":"北京市",
		    "city":"北京市",
		    "county":"丰台区",
		    "address":"靛厂路333号",
		    "facility":["停车场","吸烟区"],
		    "pay_card":["支付宝","微信"],
		    "phone":["13051391335", "13188888888"],
		    "cuisine":{},
		    "hotel_name":"北京宴",
		    "manager_name":"陈总",
		    "create_time":"创建时间"
		    ],
		    ...
		}
	}
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 管理员不存在 |
| err_4 | 酒店不存在 |


## 注册酒店门店
URL：webApp/admin/hotel_branch/register/ <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 令牌          |         yes    |
| hotel_id  | 酒店 ID | yes   |
| staff_id  | 店长 ID | yes   |
| name  | 名称   | yes   |
| province  | 省 | yes   |
| city  | 市 | yes   |
| county    | 区/县   | yes   |
| address | 详细地址    | yes    |
| phone | 电话（最多3个，数组）  | no   |
| facility | 设施（数组）   | no    |
| pay_card  | 可以哪些支付（数组）    | no    |
| cuisine   | 菜系（键值对）  | no    |

请求示例：

```
{
    "token":"129ASDFIOJIO3RN23U12934INASDF",
    "hotel_id":1,
    "staff_id":1,
    "name":"北京宴总店",
    "province":"北京市",
    "city":"北京市",
    "county":"丰台区",
    "address":"靛厂路333号",
    "phone":["13051391335","13000000000"],
    "facility":["停车场","吸烟区"],
    "pay_card":["支付宝","微信"],
    "cuisine":{}
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| branch_id | 门店 ID |

返回示例：

```
{
	"status":"true",
	"data":{
	    "branch_id":1,
	}
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 管理员不存在 |
| err_4 | 酒店不存在 |
| err_5 | 员工不存在 |
| err_6 | 门店数量已达上限  |
| err_7 | 服务器创建门店失败 |


## 停用门店
URL：webApp/admin/hotel_branch/delete/ <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 令牌          |         yes    |
| branch_id      | 门店 ID          |         yes    |

请求示例：

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"branch_id":1
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
| err_2 | 权限错误  |
| err_3 | 管理员不存在  |
| err_4 | 门店不存在 |


## 获取门店详情
URL：webApp/admin/hotel_branch/profile/get/ <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 令牌          |         yes    |
| branch_id  | 门店 ID | yes   |

请求示例：

```
{
    "token":"129ASDFIOJIO3RN23U12934INASDF",
    "branch_id":1
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| name  | 名称   |
| icon  | 头像  |
| pictures  | 介绍图片 |
| province  | 省 |
| city  | 市 |
| county    | 区/县   |
| address   | 详细地址  |
| facility  | 设施    |
| meal_period   | 餐段    |
| pay_card  | 可以哪些支付 |
| personal_tailor   | 私人订制项设置   |
| phone | 电话   |
| cuisine   | 菜系    |
| hotel_name    | 所属酒店名   |
| manager_name    | 店长名  |
| create_time   | 创建时间  |

返回示例：

```
{
	"status":"true",
	"data":{
        "name":"北京宴总店",
        "icon":"头像地址",
        "pictures":["picture1","picture2"],
        "province":"北京市",
        "city":"北京市",
        "county":"丰台区",
        "address":"靛厂路333号",
        "meal_period":{
            "Monday":{
                "lunch":{"from": "8:30","to": "12:00"},
                "dinner":{"from":"12:00","to":"18:00"},
                "supper":{"from":"18:00","to":"24:00"}
            },
            "TuesDay":{
                "lunch":{"from": "8:30","to": "12:00"},
                "dinner":{"from":"12:00","to":"18:00"},
                "supper":{"from":"18:00","to":"24:00"}
            },
            ...
        },
        "facility":["停车场","吸烟区"],
        "pay_card":["支付宝","微信"],
        "personal_tailor":[
            {
                "name": "门牌",
                "labels": ["a", "b"],
                "order":1
            },
            {
                "name": "沙盘",
                "labels": ["a", "b"],
                "order":2
            },
            ...
        ]
        "phone":["13051391335", "13188888888"],
        "cuisine":{},
        "hotel_name":"北京宴",
        "manager_name":"陈总",
        "create_time":"创建时间"
		}
	}
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 管理员不存在 |
| err_4 | 酒店不存在 |


## 修改门店信息
URL：webApp/admin/hotel_branch/profile/modify/ <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 令牌          |         yes    |
| hotel_id  | 酒店 ID | yes   |
| staff_id  | 店长 ID | no   |
| name  | 名称   | yes   |
| province  | 省 | yes   |
| city  | 市 | yes   |
| county    | 区/县   | yes   |
| address | 详细地址    | yes    |
| phone | 电话（最多5个，数组）  | no   |
| facility | 设施（数组）   | no    |
| pay_card  | 可以哪些支付（数组）    | no    |
| cuisine   | 菜系（键值对）  | no    |

请求示例：

```
{
    "token":"129ASDFIOJIO3RN23U12934INASDF",
    "hotel_id":1,
    "staff_id":1,
    "name":"北京宴总店",
    "province":"北京市",
    "city":"北京市",
    "county":"丰台区",
    "address":"靛厂路333号",
    "phone":["13051391335","13000000000"],
    "facility":["停车场","吸烟区"],
    "pay_card":["支付宝","微信"],
    "cuisine":{}
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| branch_id | 门店 ID |

返回示例：

```
{
	"status":"true",
	"data":{
	    "branch_id":1,
	}
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 管理员不存在 |
| err_4 | 酒店不存在 |
| err_5 | 员工不存在 |
| err_6 | 图片为空或图片格式错误 |


## 修改门店餐段信息
URL：webApp/admin/hotel_branch/meal_period/modify/ <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 令牌          |         yes    |
| branch_id  | 门店 ID | yes   |
| meal_period  | 餐段 | yes   |

请求示例：

```
{
    "token":"129ASDFIOJIO3RN23U12934INASDF",
    "branch_id":1,
    "meal_period":{
            "Monday":{
                "lunch":{"from": "8:30","to": "12:00"},
                "dinner":{"from":"12:00","to":"18:00"},
                "supper":{"from":"18:00","to":"24:00"}
            },
            "TuesDay":{
                "lunch":{"from": "8:30","to": "12:00"},
                "dinner":{"from":"12:00","to":"18:00"},
                "supper":{"from":"18:00","to":"24:00"}
            },
            ...
        },
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|

返回示例：

```
{
	"status":"true",
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 管理员不存在 |
| err_4 | 酒店不存在 |


## 修改门店私人订制项设置
URL：webApp/admin/hotel_branch/personal_tailor/modify/ <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 令牌          |         yes    |
| branch_id  | 门店 ID | yes   |
| personal_tailor  | 私人订制项 | yes   |

请求示例：

```
{
    "token":"129ASDFIOJIO3RN23U12934INASDF",
    "branch_id":1,
    "personal_tailor":[
        {
            "name": "门牌",
            "labels": ["a", "b"],
            "order":1
        },
        {
            "name": "沙盘",
            "labels": ["a", "b"],
            "order":2
        },
        ...
    ]
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|

返回示例：

```
{
	"status":"true",
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 管理员不存在 |
| err_4 | 酒店不存在 |


## 增加门店介绍图片
URL：webApp/admin/hotel_branch/picture/add/ <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 令牌          |         yes    |
| branch_id  | 门店 ID | yes   |
| picture   | 图片，[file]格式    | yes   |

请求示例：

```
{
    "token":"129ASDFIOJIO3RN23U12934INASDF",
    "branch_id":1,
    "picture":"[file]文件",
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|

返回示例：

```
{
	"status":"true",
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 管理员不存在 |
| err_4 | 酒店不存在 |
| err_5 | 图片数量已超过限制 |
| err_6 | 图片为空或图片格式错误   |


## 删除酒店门店介绍图片
URL：webApp/admin/hotel_branch/picture/delete/ <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 令牌          |         yes    |
| branch_id  | 门店 ID | yes   |
| pictures   | 需要删除的图片地址（可以多张，数组）    | yes   |

请求示例：

```
{
    "token":"129ASDFIOJIO3RN23U12934INASDF",
    "branch_id":1,
    "picture":["picture1","picture2"],
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|

返回示例：

```
{
	"status":"true",
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 管理员不存在 |
| err_4 | 酒店不存在 |
| err_5 | 图片不存在 |


## 获取门店的餐厅区域列表
URL：webApp/admin/hotel_branch/area/list/ <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 令牌          |         yes    |
| branch_id  | 门店 ID | yes   |

请求示例：

```
{
    "token":"129ASDFIOJIO3RN23U12934INASDF",
    "branch_id":1
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| count | 门店数  |
| list | 门店列表 |
| 以下为list中的数据    |
| area_id  | 区域 ID    |
| name  | 名称   |
| order  | 排序  |
| is_enabled    | 是否有效  |
| create_time   | 创建时间  |

返回示例：

```
{
	"status":"true",
	"data":{
	    "count":20,
	    "list":{[
		    "area_id":1,
		    "name":"一楼",
		    "order":1,
		    "is_enabled":"True",
		    "create_time":"创建时间"
		    ],
		    ...
		}
	}
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 管理员不存在 |
| err_4 | 门店不存在 |


## 批量增加门店的餐厅区域
URL：webApp/admin/hotel_branch/area/add/ <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 令牌          |         yes    |
| branch_id  | 门店 ID | yes   |
| list  | 门店数组  | yes   |
| 以下为list中的数据  |
| name  | 名称    |   yes |
| order | 排序 | yes |

请求示例：

```
{
    "token":"129ASDFIOJIO3RN23U12934INASDF",
    "branch_id":1,
    "list":[
        {
            "name":"一楼",
            "order":1
        },
        ...
    ]
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|


返回示例：

```
{
	"status":"true",
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 管理员不存在 |
| err_4 | 门店不存在 |
| err_5 | 区域已存在    |
| err_6 | 服务器添加餐厅区域失败   |


## 批量修改门店的餐厅区域
URL：webApp/admin/hotel_branch/area/modify/ <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 令牌          |         yes    |
| list  | 门店数组  | yes   |
| 以下为list中的数据  |
| area_id  | 区域 ID | yes   |
| name  | 名称    |   yes |
| order | 排序 | yes |
| is_enabled    | 是否有效  | yes    |

请求示例：

```
{
    "token":"129ASDFIOJIO3RN23U12934INASDF",
    "list":[
        {
            "area_id":1,
            "name":"一楼",
            "order":1
        },
    ...
    ]
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|


返回示例：

```
{
	"status":"true",
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 管理员不存在 |
| err_4 | 门店不存在 |
| err_5 | 区域名已存在    |


## 获取门店的桌位列表
URL：webApp/admin/hotel_branch/desk/list/ <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 令牌          |         yes    |
| area_id  | 区域 ID | yes   |
| offset | 起始值（默认0） | no |
| limit | 偏移量（默认10） | no |

请求示例：

```
{
    "token":"129ASDFIOJIO3RN23U12934INASDF",
    "area_id":1
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| count | 桌位数  |
| list | 桌位列表 |
| 以下为list中的数据    |
| desk_id  | 桌位 ID    |
| number  | 编号   |
| order  | 排序  |
| min_guest_num | 最小容纳人数    |
| max_guest_num | 最大容纳人数    |
| expense  | 费用说明  |
| type  | 类型    |
| facility  | 设施（数组）    |
| picture   | 照片    |
| is_beside_window    | 是否靠窗  |
| description   | 备注    |
| create_time   | 创建时间  |

返回示例：

```
{
	"status":"true",
	"data":{
	    "count":20,
	    "list":{[
		    "desk_id":1,
		    "number":"201",
		    "order":1,
		    "min_guest_num":10,
		    "max_guest_num":15,
		    "expense":"收取15%服务费",
		    "type":"豪华包间",
		    "facility":["电脑","吸烟区"],
		    "picture":"图片地址",
		    "is_beside_window":"True",
		    "description":"",
		    "create_time":"创建时间"
		    ],
		    ...
		}
	}
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 管理员不存在 |
| err_4 | 该区域不存在 |


## 增加门店区域的桌位
URL：webApp/admin/hotel_branch/desk/add/ <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 令牌          |         yes    |
| area_id  | 区域 ID | yes   |
| number  | 编号    |   yes |
| order | 排序 | yes |
| min_guest_num | 最小容纳人数    | yes   |
| max_guest_num | 最大容纳人数    | yes   |
| expense  | 费用说明  | no |
| type  | 类型    |   no  |
| facility  | 设施（数组）    | no    |
| picture   | 房间介绍照片，[file]文件    | no    |
| is_beside_window    | 是否靠窗  | no  |
| description | 备注  | no    |

请求示例：

```
{
    "token":"129ASDFIOJIO3RN23U12934INASDF",
    "area_id":1,
    "number":"201",
    "order":1,
    "min_guest_num":10,
    "max_guest_num":15,
    "expense":["收取15%服务费"],
    "type":"豪华包间",
    "facility":["电脑","吸烟区"],
    "picture":"图片地址",
    "is_beside_window":"True",
    "description":"",
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|


返回示例：

```
{
	"status":"true",
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 管理员不存在 |
| err_4 | 地区不存在 |
| err_5 | 区域名已存在    |
| err_6 | 图片为空或图片格式错误   |
| err_7 | 服务器创建桌位失败 |


## 修改门店区域的桌位
URL：webApp/admin/hotel_branch/area/modify/ <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 令牌          |         yes    |
| desk_id  | 桌位 ID | yes   |
| number  | 编号    |   no |
| order | 排序 | no |
| min_guest_num | 最小容纳人数    | no   |
| max_guest_num | 最大容纳人数    | no   |
| expense  | 费用说明(数组)  | no |
| type  | 类型    |   no  |
| facility  | 设施（数组）    | no    |
| picture   | 房间介绍照片，[file]文件    | no    |
| is_beside_window    | 是否靠窗  | no  |
| description | 备注  | no    |

请求示例：

```
{
    "token":"129ASDFIOJIO3RN23U12934INASDF",
    "desk_id":1,
    "number":"301",
    "order":3
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|


返回示例：

```
{
	"status":"true",
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 管理员不存在 |
| err_4 | 桌位不存在 |
| err_5 | 桌位编号已存在   |
| err_6 | 图片为空或图片格式错误   |


## 自动推荐桌位列表
URL：webApp/admin/hotel_branch/desk/recommend/ <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 令牌          |         yes    |
| branch_id  | 门店 ID | yes   |
| guest_number  | 顾客人数  | yes   |
| offset | 起始值（默认0） | no |
| limit | 偏移量（默认10） | no |

请求示例：

```
{
    "token":"129ASDFIOJIO3RN23U12934INASDF",
    "branch_id":1,
    "guest_number":10
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| count | 桌位数  |
| list | 桌位列表 |
| 以下为list中的数据    |
| desk_id  | 桌位 ID    |
| number  | 编号   |
| order  | 排序  |
| min_guest_num | 最小容纳人数    |
| max_guest_num | 最大容纳人数    |
| expense  | 费用说明(数组)  |
| type  | 类型    |
| facility  | 设施（数组）    |
| picture   | 照片    |
| is_beside_window    | 是否靠窗  |
| description   | 备注    |
| create_time   | 创建时间  |

返回示例：

```
{
	"status":"true",
	"data":{
	    "count":20,
	    "list":{[
		    "desk_id":1,
		    "number":"201",
		    "order":1,
		    "min_guest_num":10,
		    "max_guest_num":15,
		    "expense":["收取15%服务费"],
		    "type":"豪华包间",
		    "facility":["电脑","吸烟区"],
		    "picture":"图片地址",
		    "is_beside_window":"True",
		    "description":"",
		    "create_time":"创建时间"
		    ],
		    ...
		}
	}
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 管理员不存在 |
| err_4 | 该区域不存在 |


## 批量修改门店的桌位
URL：webApp/admin/hotel_branch/desks/modify/ <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 令牌          |         yes    |
| list  | 门店数组  | yes   |
| 以下为list中的数据  |
| desk_id  | 桌位 ID | yes   |
| number  | 桌位编号    |   yes |
| order | 排序 | yes |
| is_enabled    | 是否有效  | yes    |

请求示例：

```
{
    "token":"129ASDFIOJIO3RN23U12934INASDF",
    "list":[
        {
            "area_id":1,
            "number":"110",
            "order":1,
            "is_enabled":True
        },
    ...
    ]
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|


返回示例：

```
{
	"status":"true",
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 管理员不存在 |
| err_4 | 门店不存在 |
| err_5 | 桌位名已存在    |


## 获取酒店的员工列表
URL：webApp/admin/hotel/staff/list/ <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 令牌          |         yes    |
| hotel_id  | 酒店 ID | yes   |
| order | 排序方式（0: 注册时间升序，1: 注册时间降序，2: 昵称升序，3: 昵称降序，默认1） | no |

请求示例：

```
{
    "token":"129ASDFIOJIO3RN23U12934INASDF",
    "hotel_id":1
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| count | 员工数  |
| list | 员工列表 |
| 以下为list中的数据    |
| staff_id  | 员工 ID    |
| staff_number    | 员工编号    |
| name  | 员工姓名  |
| icon  | 员工头像  |
| status    | 员工状态，0：待审核，1：审核通过 |
| gender    | 性别，0:保密，1:男，2:女    |
| hotel_name    | 员工所属酒店    |
| position  | 职位    |
| guest_channel | 所属获客渠道, 0:无, 1:高层管理, 2:预定员和迎宾, 3:客户经理 |
| authority | 权限    |
| is_enabled    | 是否有效  |
| create_time   | 创建时间  |

返回示例：

```
{
	"status":"true",
	"data":{
	    "count":20,
	    "list":{[
		    "staff_id":1,
		    "staff_number":"12345",
		    "name":"张三",
		    "icon":"头像地址",
		    "status":1,
		    "gender":0,
		    "hotel_name":"北京宴",
		    "position":"经理",
		    "guest_channel":1,
		    "authority":"权限",
		    "is_enabled":True,
		    "create_time":"创建时间"
		    ],
		    ...
		}
	}
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 管理员不存在 |
| err_4 | 酒店不存在 |


## 增加酒店的员工
URL：webApp/admin/hotel/staff/add/ <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 令牌          |         yes    |
| hotel_id  | 酒店 ID | yes   |
| phone |   手机号 | yes   |
| password  | 密码    | yes   |
| name  | 员工姓名  | yes   |
| id_number | 身份证号  | yes   |
| position  | 职位    | yes   |
| staff_number    | 员工编号    | no |
| icon  | 头像，[file]格式  | no   |
| gender    | 性别，0:保密，1:男，2:女    | no   |
| guest_channel | 所属获客渠道, 0:无, 1:高层管理, 2:预定员和迎宾, 3:客户经理 | no   |
| description   | 备注    |   no  |
| authority | 权限    | no   |

请求示例：

```
{
    "token":"129ASDFIOJIO3RN23U12934INASDF",
    "hotel_id":1,
    "phone":"13000000000",
    "name":"张三",
    "id_number":"430723111111111111",
    "password":"098f6bcd4621d373cade4e832627b4f6",
    "position":"经理",
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|


返回示例：

```
{
	"status":"true",
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 管理员不存在 |
| err_4 | 酒店不存在 |
| err_5 | 该手机号已注册   |
| err_6 | 图片为空或图片格式错误   |
| err_7 | 服务器创建员工失败   |


## 删除员工
URL：webApp/admin/hotel/staff/delete/ <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 令牌          |         yes    |
| staff_id  | 门店 ID | yes   |

请求示例：

```
{
    "token":"129ASDFIOJIO3RN23U12934INASDF",
    "staff_id":1,
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|

返回示例：

```
{
	"status":"true",
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 管理员不存在 |
| err_4 | 员工不存在 |


## 获取员工信息
URL：webApp/admin/hotel/staff/profile/get/ <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 登录口令          |         yes    |
| staff_id      | 目标员工的ID   |         yes   |

请求示例：

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"staff_id":1
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| staff_id  | 员工账号ID |
| staff_number  | 员工编号 |
| name  | 员工姓名 |
| status    | 员工状态，0: 待审核，1: 审核通过   |
| icon  | 头像    |
| gender    | 性别   |
| position  | 职位   |
| guest_channel | 所属获客渠道, 0:无, 1:高层管理, 2:预定员和迎宾, 3:客户经理 |
| description   | 备注   |
| authority | 权限等级 |
| phone_private | 电话隐私  |
| sale_enabled  | 销售职能  |
| order_sms_inform  | 订单短信  |
| order_sms_attach  | 短信附加  |
| order_bonus   | 提成结算/接单提成（消费额百分比, 按订单数量, 按消费人数）  |
| new_customer_bonus    | 提成结算/开新客提成（消费额百分比, 按订单数量, 按消费人数）   |
| manage_desks  | 管辖桌位  |
| manage_areas  | 管辖区域  |
| manage_channel    | 管理渠道客户    |
| communicate   | 沟通渠道  |
| create_time   | 创建时间|

返回示例：

```
{
	"status":"true",
	"data":{
		"staff_id":1,
		"staff_number":"2017013434",
		"name":"小张",
		"status":1,
		"gender":1,
		"position":"前台",
		"guest_channel":0,
		"description":"备注",
		"authority":[],
		"phone_private": false,
        "sale_enabled": true,
        "order_sms_inform": false,
        "order_sms_attach": false,
        "order_bonus": {
            enabled: true,
            method: 1,
            value: 0.8
        },
        "new_customer_bonus": {
            enabled: false,
            value: 0.8
        },
        "manage_desks": [],
        "manage_areas": [0, 2, 3],
        "manage_channel": [1, 2, 3],
        "communicate": {
            channel: "tel_box",
            tel_box: [
                "(来电盒子)线路1", "(来电盒子)线路2", "(来电盒子)线路3", "(来电盒子)线路4",
                "(来电盒子)线路5", "(来电盒子)线路6", "(来电盒子)线路7", "(来电盒子)线路8"
            ],
            smart_tel: [
                "(智能电话)线路1", "(智能电话)线路2", "(智能电话)线路3", "(智能电话)线路4",
                "(智能电话)线路5", "(智能电话)线路6", "(智能电话)线路7"
            ]
            },
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
| err_3 | 管理员不存在 |
| err_4 | 员工不存在 |


## 修改员工信息，包括账号审核
URL：webApp/admin/hotel/staff/profile/modify/ <br>
请求方式：POST <br>

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 登录口令          |         yes  |
| staff_id  | 员工 ID | yes   |
| status    | 员工状态，0: 待审核，1: 审核通过   | no    |
| staff_number      | 员工编号     |         no   |
| gender      | 性别    |         no   |
| position      | 职位     |         no   |
| guest_channel      | 所属获客渠道, 0:无, 1:高层管理, 2:预定员和迎宾, 3:客户经理   |         no   |
| description      | 备注，最多100字符   |         no   |
| authority      | 权限    |         no   |
| icon      | 头像（文件）    |         no   |
| phone_private | 电话隐私  | no    |
| sale_enabled  | 销售职能  | no    |
| order_sms_inform  | 订单短信  | no    |
| order_sms_attach  | 短信附加  | no    |
| order_bonus   | 提成结算/接单提成（消费额百分比, 按订单数量, 按消费人数）  | no |
| new_customer_bonus    | 提成结算/开新客提成（消费额百分比, 按订单数量, 按消费人数）   | no   |
| manage_desks  | 管辖桌位  | no    |
| manage_areas  | 管辖区域  | no    |
| manage_channel    | 管理渠道客户    | no    |
| communicate   | 沟通渠道  | no    |

请求示例:


```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"staff_number":"2017013434",
	"status":1,
	"gender":1,
	"position":"前台",
	"guest_channel":0,
	"description":"备注",
	"authority":[],
	"phone_private": false,
    "sale_enabled": true,
    "order_sms_inform": false,
    "order_sms_attach": false,
    "order_bonus": {
        enabled: true,
        method: 1,
        value: 0.8
    },
    "new_customer_bonus": {
        enabled: false,
        value: 0.8
    },
    "manage_desks": [],
    "manage_areas": [0, 2, 3],
    "manage_channel": [1, 2, 3],
    "communicate": {
        channel: "tel_box",
        tel_box: [
            "(来电盒子)线路1", "(来电盒子)线路2", "(来电盒子)线路3", "(来电盒子)线路4",
            "(来电盒子)线路5", "(来电盒子)线路6", "(来电盒子)线路7", "(来电盒子)线路8"
        ],
        smart_tel: [
            "(智能电话)线路1", "(智能电话)线路2", "(智能电话)线路3", "(智能电话)线路4",
            "(智能电话)线路5", "(智能电话)线路6", "(智能电话)线路7"
        ]
        },
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
| err_3 | 管理员不存在 |
| err_4 | 员工不存在 |
| err_5 | 图片为空或图片格式错误   |


## 获取获客渠道列表
URL：webApp/admin/hotel/channel/list/ <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 登录口令          |         yes    |

请求示例：

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF"
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| internal_channel  | 内部获客渠道    |
| 以下为internal_channel中的数据    |
| staff_id  | 员工账号ID |
| name  | 员工姓名 |
| staff_number  | 员工编号  |
| icon  | 头像    |
| gender    | 性别   |
| position  | 职位   |
| guest_channel | 所属获客渠道, 0:无, 1:高层管理, 2:预定员和迎宾, 3:客户经理 |
| authority | 权限    |
| phone_private | 电话隐私  |
| sale_enabled  | 销售职能  |
| order_sms_inform  | 订单短信  |
| order_sms_attach  | 短信附加  |
| order_bonus   | 提成结算/接单提成（消费额百分比, 按订单数量, 按消费人数）  |
| new_customer_bonus    | 提成结算/开新客提成（消费额百分比, 按订单数量, 按消费人数）   |
| manage_desks  | 管辖桌位  |
| manage_areas  | 管辖区域  |
| manage_channel    | 管理渠道客户    |
| communicate   | 沟通渠道  |
| create_time   | 创建时间|
| external_channel  | 外部获客渠道    |
| 以下为external_channel中的数据    |
| id    | ID    |
| name  | 名称    |
| discount  | 折扣    |
| icon  | 头像    |
| begin_cooperate_time | 合作起始时间 |
| end_cooperate_time | 合作结束时间   |
| staff_name | 直属上级名称   |
| is_enabled | 是否有效  |
| create_time | 创建时间 |

返回示例：

```
{
	"status":"true",
	"data":{
	    "internal_channel":[{
            "staff_id":1,
            "name":"小张",
            "staff_number":"007",
            "status":1,
            "gender":1,
            "position":"前台",
            "guest_channel":0,
            "icon":"http://oss.aliyun/banquet/avatar/1.jpg",
            "authority":[],
            "phone_private": false,
            "sale_enabled": true,
            "order_sms_inform": false,
            "order_sms_attach": false,
            "order_bonus": {
                enabled: true,
                method: 1,
                value: 0.8
            },
            "new_customer_bonus": {
                enabled: false,
                value: 0.8
            },
            "manage_desks": [],
            "manage_areas": [0, 2, 3],
            "manage_channel": [1, 2, 3],
            "communicate": {
                channel: "tel_box",
                tel_box: [
                    "(来电盒子)线路1", "(来电盒子)线路2", "(来电盒子)线路3", "(来电盒子)线路4",
                    "(来电盒子)线路5", "(来电盒子)线路6", "(来电盒子)线路7", "(来电盒子)线路8"
                ],
                smart_tel: [
                    "(智能电话)线路1", "(智能电话)线路2", "(智能电话)线路3", "(智能电话)线路4",
                    "(智能电话)线路5", "(智能电话)线路6", "(智能电话)线路7"
                ]
                },
            "create_time":"创建时间"
            },
            ...
        ]
        "external_channel"[{
            "id":1,
            "name":"美团",
            "discount":4,
            "icon":"头像",
            "begin_cooperate_time":"1993-02-12",
            "end_cooperate_time":"2020-02-12",
            "staff_name":"张三",
            "is_enabled":True,
            "create_time":"创建时间"
            },
            ...
        ]
	}
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 管理员不存在 |


## 添加外部获客渠道
URL：webApp/admin/external_channel/add/ <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 登录口令          |         yes    |
| name    | 名称  | yes   |
| discount | 折扣 | no    |
| begin_cooperate_time | 合作起始时间 | no    |
| end_cooperate_time | 合作结束时间   | no    |
| commission_type | 佣金核算方式, 0:无, 1:按消费额百分百比, 2:按订单数量, 3:按消费人数   | no    |
| commission_value | 佣金核算数值 | no    |
| icon | 头像[file]格式 | no    |

请求示例：

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"name":"美团",
	"discount":3.8,
	"begin_cooperate_time":"1993-02-12",
	"end_cooperate_time":"2020-02-12",
	"commission_type":1,
	"commission_value":100,
	"icon":[file]
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| channel_id    | 外部获客渠道ID    |

返回示例：

```
{
	"status":"true",
	"data":{
            "channel_id":1
	}
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 管理员不存在 |
| err_4 | 员工不存在 |
| err_5 | 图片为空或图片格式错误   |
| err_6 | 服务器创建外部渠道失败   |


## 修改外部获客渠道
URL：webApp/admin/external_channel/modify/ <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 登录口令          |         yes    |
| channel_id    | 外部获客渠道ID  | yes   |
| name    | 名称  | no   |
| discount | 折扣 | no    |
| begin_cooperate_time | 合作起始时间 | no    |
| end_cooperate_time | 合作结束时间   | no    |
| commission_type | 佣金核算方式, 0:无, 1:按消费额百分百比, 2:按订单数量, 3:按消费人数   | no    |
| commission_value | 佣金核算数值 | no    |
| is_enabled    | 是否有效  | no    |
| icon | 头像[file]格式 | no    |

请求示例：

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"channel_id":1,
	"name":"美团",
	"discount":3.8,
	"begin_cooperate_time":"1993-02-12",
	"end_cooperate_time":"2020-02-12",
	"commission_type":1,
	"commission_value":100,
	"is_enabled":True,
	"icon":[file]
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|

返回示例：

```
{
	"status":"true",
	"data":{
	}
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 管理员不存在 |
| err_4 | 外部渠道不存在 |
| err_5 | 外部渠道名称已存在 |
| err_6 | 员工不存在 |
| err_7 | 图片为空或图片格式错误   |


## 获取外部获客渠道详情
URL：webApp/admin/external_channel/profile/ <br>
请求方式：POST <br>
请求参数：

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 登录口令          |         yes    |
| channel_id    | 外部获客渠道ID  | yes   |

请求示例：

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"channel_id":1
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| id    | ID    |
| name  | 名称    |
| discount  | 折扣    |
| icon  | 头像    |
| begin_cooperate_time | 合作起始时间 |
| end_cooperate_time | 合作结束时间   |
| commission_type   | 佣金核算方式, 0:无,1:按消费额百分百比, 2:按订单数量, 3:按消费人数    |
| commission_value  | 佣金核算数值    |
| staff_id | 直属上级ID  |
| staff_name | 直属上级名称   |
| is_enabled | 是否有效  |
| create_time | 创建时间 |

返回示例：

```
{
	"status":"true",
	"data":{
            "id":1,
            "name":"美团",
            "discount":4,
            "icon":"头像",
            "begin_cooperate_time":"1993-02-12",
            "end_cooperate_time":"2020-02-12",
            "commission_type":0,
            "commission_value":100,
            "staff_id":1,
            "staff_name":"张三",
            "is_enabled":True,
            "create_time":"创建时间"
	}
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 管理员不存在 |
| err_4 | 渠道不存在 |


## 搜索订单列表
URL：webApp/admin/order/search/ <br>
请求方式：POST <br>

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 登录口令          |         yes  |
| dinner_date_begin   | 预定用餐日期开始  |   yes  |
| dinner_date_end   | 预定用餐日期终止  |   yes  |
| search_key | 搜索关键词（如姓名、手机等进行模糊搜索） | no |
| dinner_period | 餐段，0：午餐，1：晚餐，2：夜宵    |   no |
| status | 订单状态（0: 进行中，1: 已完成，2: 已删除，默认为0）  | no |
| is_FIT    | 是否散客，默认否  | no    |
| offset | 起始值（默认0） | no |
| limit | 偏移量（默认10） | no |
| order | 排序方式（0: 注册时间升序，1: 注册时间降序，默认1） | no |


请求示例:


```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"status":0,
	"search_key":"张总",
	"dinner_date_begin":"2017-2-2",
	"dinner_date_end":"2017-6-6"
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
| consumption   | 消费金额  |
| status | 状态((0, '已订'), (1, '客到'), (2, '已完成'), (3, '已撤单'))|
| dinner_date | 预定用餐日期 |
| dinner_time   | 预定用餐时间  |
| dinner_period | 订餐时段(0, '午餐'), (1, '晚餐'), (2, '夜宵') |
| name | 联系人 |
| contact | 联系电话 |
| guest_type | 顾客身份 |
| guest_number | 客人数量 |
| desks | 桌位ID数组 |
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
            "consumption":1000,
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
| err_3 | 管理员不存在    |

## 获取订单详情
URL：webApp/admin/order/profile/ <br>
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
| consumption   | 消费金额  |
| banquet   | 宴会类型  |
| status | 状态((0, '已订'), (1, '客到'), (2, '已完成'), (3, '已撤单'))|
| dinner_date | 预定用餐日期 | yes |
| dinner_time   | 预定用餐时间  |   yes  |
| dinner_period | 订餐时段(0, '午餐'), (1, '晚餐'), (2, '夜宵') | yes |
| name | 联系人 |
| guest_type | 顾客身份 |
| contact | 联系电话 |
| guest_number | 客人数量 |
| desks | 桌位ID和编号 |
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
		"consumption":1000,
		"banquet":"满月宴",
		"status":0,
		"order_id":"001",
		"dinner_date":"2014-02-01",
		"dinner_time":"12:00",
		"dinner_period":0,
		"name":"李四",
		"guest_type":"vip",
		"contact":"18813101211",
		"guest_number":10,
		"desks":[{"desk_id":1,"number":"309"},{"desk_id":2,"number":"312"},{"desk_id":3,"number":"311"}],
		"user_description":"生日宴，准备蜡烛",
		"staff_description":"客户年纪大，做好防滑",
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
| err_3 | 管理员不存在    |
| err_4 | 该订单不存在 |


## 提交订单
URL：webApp/admin/order/submit/ <br>
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
| desks | 桌位ID的数组 | yes |
| banquet   | 宴会类型  | no    |
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
	"banquet":"满月宴",
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
| err_3 | 管理员不存在    |
| err_4 | 桌位不存在 |
| err_5 | 桌位已被预定    |
| err_6 | 服务器创建订单错误 |


##编辑订单
URL：webApp/admin/order/modify/ <br>
请求方式：POST <br>

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 登录口令          |         yes  |
| order_id| 订单 ID | yes|
| dinner_date | 预定用餐日期 | no |
| dinner_time   | 预定用餐时间  |   no  |
| dinner_period | 订餐时段(0, '午餐'), (1, '晚餐'), (2, '夜宵') | no |
| consumption   | 消费金额  | no    |
| status | 订单状态, 0: 已订, 1: 客到, 2: 已完成, 3: 已撤单   | no    |
| banquet   | 宴会类型  | no    |
| name | 联系人 | no |
| contact | 联系电话 | no |
| guest_number | 客人数量 | no |
| desks | 桌位ID数组 | no |
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
	"consumption":1000,
	"status":2,
	"banquet":"满月宴",
	"name":"李四",
	"contact":"18813101211",
	"guest_number":10,
	"desk":[1,3,5],
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
| err_3 | 管理员不存在    |
| err_4 | 不存在该订单 |
| err_5 | 桌位不存在 |
| err_6 | 桌位已被预定    |


## 获取客户列表（搜索）

URL：webApp/admin/guest/list/ <br>
请求方式：POST

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------|
| token         | 登录口令          |         yes  |
| search_key | 客户手机号或者姓名 | no |
| status | 客户状态：0：全部，1：活跃，2：沉睡，3：流失，4：无订单，默认0 | no |
| internal_channel | 内部销售ID | no |
| external_channel | 外部销售ID | no |
| offset | 起始值（默认0） | no |
| limit | 偏移量（默认10） | no |
| order | 排序方式（0: 最近就餐，1: 总预定桌数，2: 人均消费，3: 消费频度，默认0） | no |

请求示例

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"search_key":"18813101211",
	"status":0,
	"internal_channel":1
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| count | 顾客总数 |
| list  | 顾客列表 |
| 以下为list中的数据 |
| guest_id  | 顾客 ID |
| phone | 电话    |
| name | 姓名 |
| gender    | 性别，0:保密，1:男，2:女    |
| birthday | 生日 |
| birthday_type | 生日类型，0:阳历，1:农历 |
| guest_type  | 顾客类别  |
| like | 喜好 |
| dislike | 忌讳 |
| special_day | 纪念日 |
| personal_need | 个性化需求 |
| status | 客户状态：1：活跃，2：沉睡，3：流失，4：无订单 |
| desk_number   | 消费总桌数 |
| person_consumption    | 人均消费  |
| order_per_month    | 消费频度, 单/月 |
| last_consumption  | 上次消费日期    |


返回示例

```
{
	"status":"true",
	"data":
	{
	    "count":100,
	    "list":[
	    {
	        "guest_id":1,
	        "phone":"13111111111",
			"name":"习某某",
			"gender":1,
			"guest_type":"vip",
			"birthday":"1992-02-15",
			"birthday_type":0,
			"like":"吃辣",
			"dislike":"不吃香菜",
			"special_day":"",
			"personal_need":"",
			"status":1,
			"desk_number":10,
			"person_consumption":400,
			"order_per_month":3.11,
			"last_consumption":"1993-02-25"
		},
		...
		]
	}
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 管理员不存在   |
| err_4 | 内部销售渠道不存在 |
| err_5 | 外部销售渠道不存在 |


## 获取客户档案详情（根据顾客ID或手机）

URL：webApp/admin/guest/profile/ <br>
请求方式：POST

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------|
| token         | 登录口令          |         yes  |
| guest_id      | 顾客 ID          |         no   |
| phone         | 手机             |         no  |

请求示例

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"phone":"18813101211"
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| name | 姓名 |
| gender    | 性别，0:保密，1:男，2:女   |
| phone | 电话    |
| guest_type  | 顾客类别  |
| birthday | 生日 |
| birthday_type | 生日类型，0:阳历，1:农历 |
| like | 喜好 |
| dislike | 忌讳 |
| special_day | 纪念日 |
| personal_need | 个性化需求 |
| status    | 客户状态, 1: 活跃, 2: 沉睡, 3: 流失, 4: 无订单 |
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
		"gender":1,
		"phone":"13111111111",
		"guest_type":"vip",
		"birthday":"1992-02-15",
		"birthday_type":0,
		"like":"吃辣",
		"dislike":"不吃香菜",
		"special_day":"",
		"personal_need":"",
		"status":1,
		"all_order_number":22,
		"day60_order_number":9,
		"all_consumption":10000,
		"day60_consumption:800
	}
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 权限错误 |
| err_3 | 管理员不存在    |
| err_4 | 客户不存在 |


## 添加客户档案
URL：webApp/guest/profile/add/ <br>
请求方式：POST

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------|
| token         | 登录口令          |         yes  |
| phone | 客户手机号（作为查找的依据） | yes |
| name | 姓名 | yes |
| gender    | 性别，0:保密，1:男，2:女   | no    |
| guest_type | 客户类别 | no    |
| birthday | 生日 | no    |
| birthday_type | 生日类型，0:阳历，1:农历 | no   |
| like | 喜好 | no    |
| dislike | 忌讳 | no |
| special_day | 纪念日 | no    |
| personal_need | 个性化需求 | no    |

请求示例

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"phone":"18813101211"
	"name":"习某某",
	"gender":1,
	"guest_type":"vip",
	"birthday":"1992-02-15",
	"birthday_type":0,
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
| err_3 | 管理员不存在    |
| err_4 | 该手机号已存在   |
| err_5 | 服务器创建员工错误 |


## 修改客户档案

URL：webApp/admin/guest/profile/modify/ <br>
请求方式：POST

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------|
| token         | 登录口令          |         yes  |
| phone | 客户手机号（作为查找的依据） | yes |
| name | 姓名 | no
| gender    | 性别，0:保密，1:男，2:女   | no
| guest_type | 客户类型 | no
| birthday | 生日 | no
| birthday_type | 生日类型，0:阳历，1:农历 | no
| like | 喜好 | no
| dislike | 忌讳 | no
| special_day | 纪念日 | no
| personal_need | 个性化需求 | no

请求示例

```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"phone":"18813101211"
	"name":"习某某",
	"gender":1,
	"birthday":"1992-02-15",
	"birthday_type":0,
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
| err_3 | 管理员不存在    |
| err_4 | 不存在该手机号码的客户 |
