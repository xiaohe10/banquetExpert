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
| password      | 密码            |         yes    |
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
	"password":"pass",
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
| password      | 密码            |         yes    |

请求示例：

```
{
	"phone":"18813101211",
	"password":"pass",
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
URL：webApp/staff/profile/ <br>
请求方式：GET <br>
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
URL：webApp/staff/profile/ <br>
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


# 订单接口

## 提交订单
URL：webApp/order/submit <br>
请求方式：POST <br>

| 参数名称       | 含义             | 是否必选       |
|:------------- |:---------------| :-------------:|
| token         | 登录口令          |         yes  |
| staff_id         | 员工账户ID          |         yes  |
| dinner_time | 订单日期 | yes |
| dinner_period | 订餐时段(0, '午餐'), (1, '晚餐'), (2, '夜宵') | yes |
| name | 联系人 | yes |
| contact | 联系电话 | yes |
| guest_number | 客人数量 | yes |
| desk | 桌位 | yes |
| user_description | 用户备注 | no |
| staff_description | 员工备注 | no |
|以下是私人订制的字段|
| water_card | 水牌 | no |
| door_card | 门牌 | no |
| sand_table | 沙盘 | no |
| welcom_screen | 欢迎屏 | no |
| welcom_fruit | 迎宾水果的价格 | no |
| welcom_card | 欢迎卡 | no |
| pictures | 用户上传的图片（最多5张) | no |
| background_music | 背景音乐 | no |
| has_candle | 是否有蜡烛 | no |
| has_flower | 是否有鲜花 | no |
| has_balloon | 是否有气球 | no |
| group_photo | 合照？ | no |
| user | 顾客 | no |
| internal_channel | 内部获客渠道 | no |
| external_channel | 外部获客渠道 | no |


请求示例:


```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"staff_id":1,
	"dinner_time":"2014-02-01",
	"dinner_period":0,
	"name":"李四",
	"contact":"18813101211",
	"guest_number":10,
	"desk":[1,3,5],
	"user_description":"生日宴，准备蜡烛",
	"staff_description":"客户年级大，做好防滑",
	"water_card":"水牌内容",
	"door_card":"门牌内容",
	"sand_table":"沙盘内容",
	"welcome_screen":"欢迎xx领导",
	"welcome_fruit": 128,
	"welcome_card":"欢迎你",
	"pictures":[file1,file2...],
	"background_music":"我爱你中国",
	"has_candle":true,
	"has_flower":false,
	"has_balloon":false,
	"group_photo":"合照名称",
	"user":"userid_001",
	"internal_channel":"channel_id_001",
	"external_channel":"channel_id_001"
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
		"order_id":"001"
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
| staff_id         | 员工账户ID          |         yes  |
| order_date    | 下单日期  |   no |
| dinner_period | 餐段    |   no |
| dinner_time   | 用餐时间  |   no  |
| state | 订单状态（默认缺省表示所有未完成订单列表，没有限制，finished 表示未完成，processing 表示进行中）  | no |
| search_key | 搜索关键词（如姓名、手机等进行模糊搜索） | no |


请求示例:


```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"staff_id":1,
	"state":"finished",
	"search_key":"张总",
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| order_id| 订单ID |
| create_time | 创建日期 |
| cancel_time | 撤销日期 |
| finish_time | 完成日期 | 
| state | 状态((0, '已订'), (1, '客到'), (2, '已完成'), (3, '已撤单'))|
| dinner_time | 订单日期 | yes |
| dinner_period | 订餐时段(0, '午餐'), (1, '晚餐'), (2, '夜宵') | yes |
| name | 联系人 | yes |
| contact | 联系电话 | yes |
| guest_number | 客人数量 | yes |
| desk | 桌位 | yes |



返回示例：

注意：返回的订单列表以数组来表示

```
{
	"status":"true",
	"data":[
		{
			"order_id":"001",
			"create_time":"2014-02-01 10:00:00",
			"cancel_time":"2014-02-01 10:00:00",
			"finish_time":"2014-02-01 10:00:00",
			"state":0,
			"order_id":"001",
			"dinner_time":"2014-02-01",
			"dinner_period":0,
			"name":"李四",
			"contact":"18813101211",
			"guest_number":10,
			"desk":[1,3,5]
		},
		...	
	]
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
| staff_id         | 员工账户ID          |         yes  |
| order_id | 订单ID | yes |


请求示例:


```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"staff_id":1,
	"order_id":"order_id",
}
```

返回参数：

| 参数名称       | 含义             |
|:------------- |:---------------|
| order_id| 订单ID |
| create_time | 创建日期 |
| cancel_time | 撤销日期 |
| finish_time | 完成日期 | 
| state | 状态((0, '已订'), (1, '客到'), (2, '已完成'), (3, '已撤单'))|
| dinner_time | 订单日期 | yes |
| dinner_period | 订餐时段(0, '午餐'), (1, '晚餐'), (2, '夜宵') | yes |
| name | 联系人 | yes |
| contact | 联系电话 | yes |
| guest_number | 客人数量 | yes |
| desk | 桌位 | yes |
| user_description | 用户备注 | no |
| staff_description | 员工备注 | no |
|以下是私人订制的字段|
| water_card | 水牌 | no |
| door_card | 门牌 | no |
| sand_table | 沙盘 | no |
| welcom_screen | 欢迎屏 | no |
| welcom_fruit | 迎宾水果的价格 | no |
| welcom_card | 欢迎卡 | no |
| pictures | 用户上传的图片（最多5张) | no |
| background_music | 背景音乐 | no |
| has_candle | 是否有蜡烛 | no |
| has_flower | 是否有鲜花 | no |
| has_balloon | 是否有气球 | no |
| group_photo | 合照？ | no |
| user | 顾客 | no |
| internal_channel | 内部获客渠道 | no |
| external_channel | 外部获客渠道 | no |


返回示例：

```
{
	"status":"true",
	data:{
		"order_id":"001",
		"create_time":"2014-02-01 10:00:00",
		"cancel_time":"2014-02-01 10:00:00",
		"finish_time":"2014-02-01 10:00:00",
		"state":0,
		"order_id":"001",
		"dinner_time":"2014-02-01",
		"dinner_period":0,
		"name":"李四",
		"contact":"18813101211",
		"guest_number":10,
		"desk":[1,3,5]
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
		"user":"userid_001",
		"internal_channel":"channel_id_001",
		"external_channel":"channel_id_002"
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
| staff_id         | 员工账户ID          |         yes  |
| order_id| 订单 ID | yes|
| dinner_time | 订单日期 | no |
| dinner_period | 订餐时段(0, '午餐'), (1, '晚餐'), (2, '夜宵') | no |
| name | 联系人 | no |
| contact | 联系电话 | no |
| guest_number | 客人数量 | no |
| desk | 桌位 | no |
| user_description | 用户备注 | no |
| staff_description | 员工备注 | no |
|以下是私人订制的字段|
| water_card | 水牌 | no |
| door_card | 门牌 | no |
| sand_table | 沙盘 | no |
| welcom_screen | 欢迎屏 | no |
| welcom_fruit | 迎宾水果的价格 | no |
| welcom_card | 欢迎卡 | no |
| pictures | 用户上传的图片（最多5张) | no |
| background_music | 背景音乐 | no |
| has_candle | 是否有蜡烛 | no |
| has_flower | 是否有鲜花 | no |
| has_balloon | 是否有气球 | no |
| group_photo | 合照？ | no |
| user | 顾客 | no |
| internal_channel | 内部获客渠道 | no |
| external_channel | 外部获客渠道 | no |

请求示例:


```
{
	"token":"129ASDFIOJIO3RN23U12934INASDF",
	"staff_id":1,
	"order_id":"001",
	"dinner_time":"2014-02-01",
	"dinner_period":0,
	"name":"李四",
	"contact":"18813101211",
	"guest_number":10,
	"desk":[1,3,5],
	"user_description":"生日宴，准备蜡烛",
	"staff_description":"客户年级大，做好防滑",
	"water_card":"水牌内容",
	"door_card":"门牌内容",
	"sand_table":"沙盘内容",
	"welcome_screen":"欢迎xx领导",
	"welcome_fruit": 128,
	"welcome_card":"欢迎你",
	"pictures":[file1,file2...],
	"background_music":"我爱你中国",
	"has_candle":true,
	"has_flower":false,
	"has_balloon":false,
	"group_photo":"合照名称",
	"user":"userid_001",
	"internal_channel":"channel_id_001",
	"external_channel":"channel_id_001"
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


## 订单推送
客户端给服务端推送，以json表示数据


| 参数名称       | 含义             |
|:------------- |:---------------| :-------------:|
| push_id        | 推送事件ID         |         yes  |
| push_type | 推送事件类型（订单提醒、客户服务等，待定）| yes |
| message        | 消息文字通知         |         yes  |


推送示例:


```
{
	"push_id":"129ASDFIOJIO3RN23U12934INASDF",
	"push_type":"order notify",
	"message":"xx订单即将开始，请准备"
}
```





##环境配置
1. 安装 conda<br>
下载：https://conda.io/miniconda.html<br>
运行：bash Miniconda3-latest-MacOSX-x86_64.sh<br>
验证：conda info

2. 使用 conda 新建虚拟环境（把snakes换成自己起的名称）
> conda create --name snakes python=3
3. 激活虚拟环境<br>
> source activate snakes
4. 安装django 1.11和必要的程序<br>
> pip install django<br>
> pip install mysqlclient


## mysql 数据库
数据库 <br>
host: 114.215.220.241<br>
name: banquetExpert<br>
username: root<br>
password: beijingyan
