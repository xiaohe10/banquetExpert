# banquetExpert

#员工接口（移动客户端）
##综述：
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

#员工账号

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
	"hotel_id":"12",
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
		"staff_id":"001"
	}
}
```

错误代码：

| 错误代码      | 含义             |
|:------------- |:---------------|
| err_1 | 参数不正确（缺少参数或者不符合格式） |
| err_2 | 该手机号已经注册过 |


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
		"staff_id":"001",
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
		"staff_id":"001"
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
	"staff_id":"101",
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
		"staff_id":"001",
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
| staff_id         | 员工账户ID          |         yes  |
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
	"staff_id":"001",
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
| err_3 | 不存在该员工 |


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
