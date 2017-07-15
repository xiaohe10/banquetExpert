import hashlib

from django.db import models
from django.utils import timezone

__all__ = ['Admin', 'Hotel', 'HotelBranch', 'Desk', 'Staff', 'ExternalChannel',
           'User', 'Order', 'OrderScore', 'Course', 'CoursePurchaseRecord',
           'LiveSubscribe']


class EnabledManager(models.Manager):
    """自定义管理器"""
    def get_queryset(self):
        return super().get_queryset().filter(is_enabled=True)


class Admin(models.Model):
    """管理员模型"""

    # 用户名
    username = models.CharField(
        max_length=20, default=None, null=True, unique=True)
    # 密码
    password = models.CharField(max_length=32)
    # 令牌
    token = models.CharField(max_length=32)
    # 类型
    type = models.IntegerField(choices=((0, '管理员'), (1, '超级管理员')),
                               default=0)
    # 权限
    authority = models.CharField(max_length=20, default='', db_index=True)
    # 是否有效
    is_enabled = models.BooleanField(default=True, db_index=True)

    # 创建时间
    create_time = models.DateTimeField(default=timezone.now, db_index=True)

    # 所属酒店(超级管理员不属于任何酒店)
    hotel = models.ForeignKey('Hotel', models.CASCADE, 'admins', default=None,
                              null=True)

    # 管理器
    objects = models.Manager()
    enabled_objects = EnabledManager()

    class Meta:
        ordering = ['-create_time']

    def update_token(self):
        """更新令牌"""

        random_content = self.username + timezone.now().isoformat()
        hasher = hashlib.md5()
        hasher.update(random_content.encode())
        self.token = hasher.hexdigest()[:32]


class Hotel(models.Model):
    """酒店模型"""

    # 名称
    name = models.CharField(max_length=20)
    # 头像
    icon = models.CharField(max_length=100, default='')
    # 法人代表
    owner_name = models.CharField(max_length=20)
    # 会员价值分类的最小区间值(根据最小区间与最大区间将客户分为:活跃会员、沉睡会员和流失会员)
    min_vip_category = models.IntegerField(default=60)
    # 会员价值分类的最大区间值
    max_vip_category = models.IntegerField(default=120)
    # 门店数量上限
    branch_number = models.IntegerField(default=10)
    # 开通的服务
    service = models.CharField(max_length=50, default='')
    # 职位列表
    positions = models.CharField(max_length=1000, default='')
    # 是否有效
    is_enabled = models.BooleanField(default=True, db_index=True)

    # 创建时间
    create_time = models.DateTimeField(default=timezone.now, db_index=True)

    # 管理器
    objects = models.Manager()
    enabled_objects = EnabledManager()

    class Meta:
        ordering = ['-create_time']


class HotelBranch(models.Model):
    """门店模型"""

    # 名称
    name = models.CharField(max_length=20)
    # 头像
    icon = models.CharField(max_length=100, default='')
    # 酒店门店介绍图片，最多5张
    pictures = models.CharField(max_length=300, default='')
    # 所属省
    province = models.CharField(max_length=20, default='')
    # 所属市
    city = models.CharField(max_length=20, default='')
    # 所属县/区
    county = models.CharField(max_length=20, default='')
    # 详细地址
    address = models.CharField(max_length=50, default='')
    # 餐段
    meal_period = models.CharField(max_length=5000, default='')
    # 设施
    facility = models.CharField(max_length=640, default='')
    # 可以刷哪些卡
    pay_card = models.CharField(max_length=120, default='')
    # 电话(最多3个)
    phone = models.CharField(max_length=50, default='')
    # 菜系
    cuisine = models.CharField(max_length=1000, default='')
    # 私人订制项
    personal_tailor = models.CharField(max_length=2000, default='')
    # 是否有效
    is_enabled = models.BooleanField(default=True, db_index=True)

    # 创建时间
    create_time = models.DateTimeField(default=timezone.now, db_index=True)

    # 所属酒店
    hotel = models.ForeignKey('Hotel', models.CASCADE, 'branches')
    # 店长
    manager = models.ForeignKey('Staff', models.CASCADE, 'branches')

    # 管理器
    objects = models.Manager()
    enabled_objects = EnabledManager()

    class Meta:
        ordering = ['-create_time']


class CallRecord(models.Model):
    """餐厅来电记录"""
    # 电话
    phone = models.CharField(max_length=11)
    # 创建时间
    create_time = models.DateTimeField(default=timezone.now, db_index=True)

    # 处理人
    staff = models.ForeignKey('Staff', models.CASCADE, 'dealt_call_records')

    class Meta:
        ordering = ['-create_time']


class Area(models.Model):
    """餐厅区域模型"""

    # 名称
    name = models.CharField(max_length=10, unique=True)
    # 排序
    order = models.IntegerField(default=0, db_index=True)
    # 是否有效
    is_enabled = models.BooleanField(default=True, db_index=True)

    # 创建时间
    create_time = models.DateTimeField(default=timezone.now, db_index=True)

    # 所属门店
    branch = models.ForeignKey('HotelBranch', models.CASCADE, 'areas')

    # 管理器
    objects = models.Manager()
    enabled_objects = EnabledManager()

    class Meta:
        ordering = ['-create_time']


class Desk(models.Model):
    """桌位模型"""

    # 桌位号
    number = models.CharField(max_length=10)
    # 排序
    order = models.IntegerField(default=0, db_index=True)
    # 费用说明
    expense = models.CharField(max_length=500, default='')
    # 房间类型
    type = models.CharField(max_length=10, default='', db_index=True)
    # 设施
    facility = models.CharField(max_length=120, default='')
    # 照片
    picture = models.CharField(max_length=100, default='')
    # 是否靠窗
    is_beside_window = models.BooleanField(default=False)
    # 最小可容纳人数
    min_guest_num = models.IntegerField(default=None, null=True)
    # 最大可容纳人数
    max_guest_num = models.IntegerField(default=None, null=True)
    # 备注
    description = models.CharField(max_length=200, default='')
    # 是否有效
    is_enabled = models.BooleanField(default=True, db_index=True)

    # 创建时间
    create_time = models.DateTimeField(default=timezone.now, db_index=True)

    # 所属区域
    area = models.ForeignKey('Area', models.CASCADE, 'desks')

    # 管理器
    objects = models.Manager()
    enabled_objects = EnabledManager()

    class Meta:
        ordering = ['-create_time']


class Staff(models.Model):
    """员工模型"""

    # 员工编号
    staff_number = models.CharField(max_length=20, default=None, null=True)
    # 手机
    phone = models.CharField(max_length=11, unique=True)
    # 密码
    password = models.CharField(max_length=32)
    # 令牌
    token = models.CharField(max_length=32)
    # 姓名
    name = models.CharField(max_length=20)
    # 身份证号
    id_number = models.CharField(max_length=18, default='', unique=True)
    # 头像
    icon = models.CharField(max_length=100, default='')
    # 性别
    gender = models.IntegerField(choices=((0, '保密'), (1, '男'), (2, '女')),
                                 default=0, db_index=True)
    # 职位
    position = models.CharField(max_length=20, default='')
    # 所属获客渠道
    guest_channel = models.IntegerField(
        choices=((0, '无'), (1, '高层管理'), (2, '预定员和迎宾'), (3, '客户经理')),
        default=0, db_index=True)
    # 状态
    status = models.IntegerField(
        choices=((0, '待审核'), (1, '审核通过')), default=0, db_index=True)
    # 备注
    description = models.CharField(max_length=200, default='')
    # 权限
    authority = models.CharField(max_length=20, default='', db_index=True)
    # 电话隐私
    phone_private = models.BooleanField(default=False)
    # 销售职能
    sale_enabled = models.BooleanField(default=True)
    # 订单短信
    order_sms_inform = models.BooleanField(default=True)
    # 短信附加
    order_sms_attach = models.BooleanField(default=True)
    # 提成结算/接单提成 消费额百分比，按订单数量，按消费人数
    order_bonus = models.CharField(max_length=60, default='')
    # 提成结算/开新客提成 消费额百分比，按订单数量，按消费人数
    new_customer_bonus = models.CharField(max_length=60, default='')
    # 管辖桌位
    manage_desks = models.CharField(max_length=1000, default='')
    # 管辖区域
    manage_areas = models.CharField(max_length=500, default='')
    # 管理渠道客户
    manage_channel = models.CharField(max_length=1000, default='')
    # 沟通渠道
    communicate = models.CharField(max_length=800, default='')
    # 是否有效
    is_enabled = models.BooleanField(default=True, db_index=True)

    # 创建时间
    create_time = models.DateTimeField(default=timezone.now, db_index=True)

    # 所属酒店
    hotel = models.ForeignKey('Hotel', models.CASCADE, 'staffs')

    # 管理器
    objects = models.Manager()
    enabled_objects = EnabledManager()

    class Meta:
        ordering = ['-create_time']

    def update_token(self):
        """更新令牌"""

        random_content = self.phone + timezone.now().isoformat()
        hasher = hashlib.md5()
        hasher.update(random_content.encode())
        self.token = hasher.hexdigest()


class ExternalChannel(models.Model):
    """外部接单渠道"""

    # 名称
    name = models.CharField(max_length=20)
    # 折扣
    discount = models.FloatField(default=0)
    # 头像
    icon = models.CharField(max_length=100, default='')
    # 合作起始时间
    begin_cooperate_time = models.DateField(default=None, null=True)
    # 合作结束时间
    end_cooperate_time = models.DateField(default=None, null=True)
    # 佣金核算方式
    commission_type = models.IntegerField(
        choices=((0, '无'),
                 (1, '按消费额百分百比'),
                 (2, '按订单数量'),
                 (3, '按消费人数')),
        default=0)
    # 佣金核算数值
    commission_value = models.IntegerField(default=0)
    # 是否有效
    is_enabled = models.BooleanField(default=True, db_index=True)

    # 创建时间
    create_time = models.DateTimeField(default=timezone.now, db_index=True)

    # 直属上级
    staff = models.ForeignKey('Staff', models.CASCADE, 'external_channels')

    # 管理器
    objects = models.Manager()
    enabled_objects = EnabledManager()


class User(models.Model):
    """用户模型"""

    # 用户名
    username = models.CharField(
        max_length=20, default=None, null=True, unique=True)
    # 密码
    password = models.CharField(max_length=32)
    # 手机
    phone = models.CharField(max_length=11, unique=True)
    # 令牌
    token = models.CharField(max_length=32)
    # 昵称
    nike_name = models.CharField(max_length=20, default='')
    # 真实姓名
    name = models.CharField(max_length=20, default='')
    # 身份证号
    id_number = models.CharField(max_length=18, default='')
    # 头像
    icon = models.CharField(max_length=100, default='')
    # 性别
    gender = models.IntegerField(choices=((0, '保密'), (1, '男'), (2, '女')),
                                 default=0, db_index=True)
    # QQ
    qq = models.CharField(max_length=20, default='')
    # 微信
    wechat = models.CharField(max_length=20, default='')
    # 生日
    birthday = models.DateField(default=None, null=True)
    # 生日类型
    birthday_type = models.IntegerField(
        choices=((0, '阳历'), (1, '农历')), default=0)
    # 所在省
    province = models.CharField(max_length=20, default='')
    # 所在市
    city = models.CharField(max_length=20, default='')
    # 所在区/县
    county = models.CharField(max_length=20, default='')
    # 详细地址
    address = models.CharField(max_length=50, default='')
    # 备注
    description = models.CharField(max_length=200, default='')
    # 是否有效
    is_enabled = models.BooleanField(default=True, db_index=True)

    # 创建时间
    create_time = models.DateTimeField(default=timezone.now, db_index=True)

    # 管理器
    objects = models.Manager()
    enabled_objects = EnabledManager()

    class Meta:
        ordering = ['-create_time']

    def update_token(self):
        """更新令牌"""

        random_content = self.phone + timezone.now().isoformat()
        hasher = hashlib.md5()
        hasher.update(random_content.encode())
        self.token = hasher.hexdigest()

    def save_and_generate_name(self):
        """生成序列用户昵称并保存当前实例"""

        self.nike_name = '宴专家用户 #{}'.format(self.id)
        self.save()


class Guest(models.Model):
    """顾客模型"""

    # 手机
    phone = models.CharField(max_length=11)
    # 姓名
    name = models.CharField(max_length=20, default='')
    # 用户会员类别
    type = models.CharField(max_length=10, default='')
    # 性别
    gender = models.IntegerField(choices=((0, '保密'), (1, '男'), (2, '女')),
                                 default=0, db_index=True)
    # 单位
    unit = models.CharField(max_length=60, default='')
    # 职位
    position = models.CharField(max_length=20, default='')
    # 生日
    birthday = models.DateField(default=None, null=True)
    # 生日类型
    birthday_type = models.IntegerField(
        choices=((0, '阳历'), (1, '农历')), default=0)
    # 爱好
    like = models.CharField(max_length=100, default='')
    # 忌讳
    dislike = models.CharField(max_length=100, default='')
    # 纪念日
    special_day = models.CharField(max_length=20, default='')
    # 个性化需求
    personal_need = models.CharField(max_length=100, default='')

    # 总预定桌数(通过每天定时任务来更新数据)
    desk_number = models.IntegerField(default=0, db_index=True)
    # 总消费(通过每天定时任务来更新数据)
    consumption = models.IntegerField(default=0, db_index=True)
    # 人均消费(通过每天定时任务来更新数据)
    person_consumption = models.FloatField(default=0.0, db_index=True)
    # 桌均消费(通过每天定时任务来更新数据)
    desk_consumption = models.FloatField(default=0.0, db_index=True)
    # 消费频度, 每月平均多少单(通过每天定时任务来更新数据)
    order_per_month = models.FloatField(default=0.0, db_index=True)
    # 最后消费时间戳, 排序用(通过每天定时任务来更新数据)
    last_consumption = models.IntegerField(default=0, db_index=True)

    # 创建时间
    create_time = models.DateTimeField(default=timezone.now, db_index=True)

    # 所属酒店
    hotel = models.ForeignKey('Hotel', models.CASCADE, 'guests')
    # 内部销售
    internal_channel = models.ForeignKey(
        'Staff', models.CASCADE, 'guests', default=None, null=True)
    # 外部销售
    external_channel = models.ForeignKey(
        'ExternalChannel', models.CASCADE, 'guests', default=None, null=True)

    class Meta:
        ordering = ['-create_time']


class Order(models.Model):
    """订单模型"""

    # 订单状态
    status = models.IntegerField(
        choices=((0, '已订'), (1, '客到'), (2, '已完成'), (3, '已撤单')),
        default=0, db_index=True)
    # 联系人
    name = models.CharField(max_length=20, db_index=True)
    # 性别
    gender = models.IntegerField(choices=((0, '保密'), (1, '男'), (2, '女')),
                                 default=0, db_index=True)
    # 联系电话
    contact = models.CharField(max_length=11, default='')
    # 到店人数
    guest_number = models.IntegerField(default=0, db_index=True)
    # 预定桌位, 可能多桌
    desks = models.CharField(max_length=200, default='')
    # 餐桌数
    table_count = models.IntegerField(default=1, db_index=True)
    # 支付金额
    consumption = models.IntegerField(default=0, db_index=True)
    # 宴会类型
    banquet = models.CharField(max_length=200, default='')
    # 水牌
    water_card = models.CharField(max_length=10, default='')
    # 门牌
    door_card = models.CharField(max_length=10, default='')
    # 沙盘
    sand_table = models.CharField(max_length=10, default='')
    # 欢迎屏
    welcome_screen = models.CharField(max_length=10, default='')
    # 迎宾水果的价格
    welcome_fruit = models.IntegerField(default=None, null=True)
    # 欢迎卡
    welcome_card = models.CharField(max_length=10, default='')
    # 用户上传的图片，最多5张
    pictures = models.CharField(max_length=300, default='')
    # 背景音乐
    background_music = models.CharField(max_length=20, default='')
    # 是否有蜡烛
    has_candle = models.BooleanField(default=False)
    # 是否有鲜花
    has_flower = models.BooleanField(default=False)
    # 是否有气球
    has_balloon = models.BooleanField(default=False)
    # 用户上传的合照
    group_photo = models.CharField(max_length=100, default='')
    # 顾客备注
    user_description = models.CharField(max_length=200, default='')
    # 员工备注
    staff_description = models.CharField(max_length=200, default='')

    # 餐段
    dinner_period = models.IntegerField(
        choices=((0, '午餐'), (1, '晚餐'), (2, '夜宵')), default=0, db_index=True)
    # 预定用餐日期
    dinner_date = models.DateField(db_index=True)
    # 预定用餐时间
    dinner_time = models.TimeField()
    # 创建时间
    create_time = models.DateTimeField(default=timezone.now, db_index=True)
    # 客到时间
    arrival_time = models.DateTimeField(default=None, null=True, db_index=True)
    # 完成时间
    finish_time = models.DateTimeField(default=None, null=True, db_index=True)
    # 撤销时间
    cancel_time = models.DateTimeField(default=None, null=True, db_index=True)

    # 顾客(顾客端订餐关联)
    user = models.ForeignKey(
        'User', models.CASCADE, 'orders', default=None, null=True)
    # 内部获客渠道
    internal_channel = models.ForeignKey(
        'Staff', models.CASCADE, 'orders', default=None, null=True)
    # 外部获客渠道
    external_channel = models.ForeignKey(
        'ExternalChannel', models.CASCADE, 'orders', default=None, null=True)

    # 所属门店
    branch = models.ForeignKey('HotelBranch', models.CASCADE, 'orders')

    class Meta:
        ordering = ['-create_time']


class OrderLog(models.Model):
    """订单操作日志"""

    # 创建时间
    create_time = models.DateTimeField(default=timezone.now)
    # 操作类型
    type = models.IntegerField(
        choices=((0, '预定'), (1, '客到'), (2, '翻台'), (3, '调桌'), (4, '撤单'),
                 (5, '补录')),
        default=0, db_index=True)
    # 内容
    content = models.CharField(max_length=200, default='')

    # 订单
    order = models.ForeignKey('Order', models.CASCADE, 'logs')
    # 操作员工
    staff = models.ForeignKey('Staff', models.CASCADE, 'order_logs')

    class Meta:
        ordering = ['-create_time']


class HotelDayConsumption(models.Model):
    """酒店的日消费统计模型"""

    # 总订单数
    order_number = models.IntegerField(default=0)
    # 总人数
    guest_number = models.IntegerField(default=0)
    # 总消费
    consumption = models.IntegerField(default=0)
    # 总桌数
    desk_number = models.IntegerField(default=0)
    # 人均消费
    person_consumption = models.FloatField(default=0.00)
    # 桌均消费
    desk_consumption = models.FloatField(default=0.00)

    # 日期
    date = models.DateField(db_index=True)
    # 创建时间
    create_time = models.DateTimeField(default=timezone.now)

    # 酒店
    hotel = models.ForeignKey('Hotel', models.CASCADE, 'day_consumptions')

    class Meta:
        ordering = ['-create_time']


class HotelMonthConsumption(models.Model):
    """酒店的月消费统计模型"""

    # 总订单数
    order_number = models.IntegerField(default=0)
    # 总人数
    guest_number = models.IntegerField(default=0)
    # 总消费
    consumption = models.IntegerField(default=0)
    # 总桌数
    desk_number = models.IntegerField(default=0)
    # 人均消费
    person_consumption = models.FloatField(default=0.0)
    # 桌均消费
    desk_consumption = models.FloatField(default=0.0)

    # 年月(例, 2017-06)
    month = models.CharField(max_length=10, db_index=True)
    # 创建时间
    create_time = models.DateTimeField(default=timezone.now)

    # 酒店
    hotel = models.ForeignKey('Hotel', models.CASCADE, 'month_consumptions')

    class Meta:
        ordering = ['-create_time']


class OrderScore(models.Model):
    """评分模型"""

    # 门牌拍照
    door_card_picture = models.CharField(max_length=100, default='')
    door_card_score = models.IntegerField(default=None, null=True)
    check_door_card_score = models.IntegerField(default=None, null=True)
    # 沙盘
    sand_table_picture = models.CharField(max_length=100, default='')
    sand_table_score = models.IntegerField(default=None, null=True)
    check_sand_table_score = models.IntegerField(default=None, null=True)
    # 欢迎屏
    welcome_screen_picture = models.CharField(max_length=100, default='')
    welcome_screen_score = models.IntegerField(default=None, null=True)
    check_welcome_screen_score = models.IntegerField(default=None, null=True)
    # 氛围
    atmosphere_picture = models.CharField(max_length=100, default='')
    atmosphere_score = models.IntegerField(default=None, null=True)
    check_atmosphere_score = models.IntegerField(default=None, null=True)
    # 拍照
    group_photo_picture = models.CharField(max_length=100, default='')
    group_photo_score = models.IntegerField(default=None, null=True)
    check_group_photo_score = models.IntegerField(default=None, null=True)
    # 烤瓷杯
    cup_picture = models.CharField(max_length=100, default='')
    cup_score = models.IntegerField(default=None, null=True)
    check_cup_score = models.IntegerField(default=None, null=True)
    # 小册子
    brochure_picture = models.CharField(max_length=100, default='')
    brochure_score = models.IntegerField(default=None, null=True)
    check_brochure_score = models.IntegerField(default=None, null=True)
    # 台历
    calendar_picture = models.CharField(max_length=100, default='')
    calendar_score = models.IntegerField(default=None, null=True)
    check_calendar_score = models.IntegerField(default=None, null=True)
    # 荣誉证书
    honor_certificate_picture = models.CharField(max_length=100, default='')
    honor_certificate_score = models.IntegerField(default=None, null=True)
    check_honor_certificate_score = models.IntegerField(default=None, null=True)
    # 用心工作
    work_in_heart_picture = models.CharField(max_length=100, default='')
    work_in_heart_score = models.IntegerField(default=None, null=True)
    check_work_in_heart_score = models.IntegerField(default=None, null=True)
    # 私人订制创新
    innovation_picture = models.CharField(max_length=100, default='')
    innovation_score = models.IntegerField(default=None, null=True)
    check_innovation_score = models.IntegerField(default=None, null=True)
    # 表扬信顾客满意度
    praise_letter_picture = models.CharField(max_length=100, default='')
    praise_letter_score = models.IntegerField(default=None, null=True)
    check_praise_letter_score = models.IntegerField(default=None, null=True)
    # 朋友圈顾客满意度
    friend_circle_picture = models.CharField(max_length=100, default='')
    friend_circle_score = models.IntegerField(default=None, null=True)
    check_friend_circle_score = models.IntegerField(default=None, null=True)
    # 网评顾客满意度
    network_comment_picture = models.CharField(max_length=100, default='')
    network_comment_score = models.IntegerField(default=None, null=True)
    check_network_comment_score = models.IntegerField(default=None, null=True)
    # 单桌当餐转化率
    single_table_transform_score = models.IntegerField(default=None, null=True)
    check_single_table_transform_score = models.IntegerField(
        default=None, null=True)
    # 多桌当餐转化率
    multi_table_transform_score = models.IntegerField(default=None, null=True)
    check_multi_table_transform_score = models.IntegerField(
        default=None, null=True)
    # 总分
    score = models.FloatField(default=0.00)

    # 创建时间
    create_time = models.DateTimeField(default=timezone.now, db_index=True)
    # 检查人最后打分时间
    modify_time = models.DateTimeField(default=None, null=True, db_index=True)

    # 对应订单
    order = models.ForeignKey('Order', models.CASCADE, 'order_score')
    # 打分员工
    staff = models.ForeignKey('Staff', models.CASCADE, 'order_scores')
    # 检查员工
    check_staff = models.ForeignKey('Staff', models.CASCADE,
                                    'check_order_scores', default=None,
                                    null=True)

    class Meta:
        ordering = ['-create_time']


class Course(models.Model):
    """微课堂模型"""

    # 对应CC视频ID
    cc_video_id = models.CharField(max_length=32, unique=True)
    # 状态
    status = models.IntegerField(
        choices=((0, '待审核'), (1, '审核通过'), (2, '审核未通过')),
        default=0, db_index=True)
    # 标题
    title = models.CharField(max_length=20)
    # 标签
    tags = models.CharField(max_length=20, db_index=True)
    # 价格
    price = models.IntegerField(default=0)
    # 描述
    description = models.CharField(max_length=200, default='')

    # 创建时间
    create_time = models.DateTimeField(default=timezone.now, db_index=True)
    # 检查人最后操作时间
    modify_time = models.DateTimeField(default=None, null=True, db_index=True)

    # 视频上传者
    staff = models.ForeignKey('Staff', models.CASCADE, 'courses')
    # 视频审核者
    check_staff = models.ForeignKey('Staff', models.CASCADE, 'check_courses',
                                    default=None, null=True)

    class Meta:
        ordering = ['-create_time']


class CoursePurchaseRecord(models.Model):
    """课程购买记录模型"""

    # 其他支付信息
    # todo

    # 花费
    cost = models.IntegerField()
    # 创建时间
    create_time = models.DateTimeField(default=timezone.now, db_index=True)

    # 课程
    course = models.ForeignKey('Course', models.CASCADE, 'purchase_records')
    # 购买者
    hotel = models.ForeignKey(
        'Hotel', models.CASCADE, 'course_purchase_records')

    class Meta:
        ordering = ['-create_time']


class Live(models.Model):
    """直播间模型"""

    # 对应CC直播间ID
    cc_room_id = models.CharField(max_length=32, unique=True)
    # 直播间名称
    name = models.CharField(max_length=20)
    # 描述
    description = models.CharField(max_length=200, default='')
    # 价格
    price = models.IntegerField(default=0)
    # 推流端密，即讲师密码
    publisher_password = models.CharField(max_length=6, default='')
    # 播放端密码
    play_password = models.CharField(max_length=6, default='')
    # 直播开始日期
    start_date = models.DateField(default=None, null=True)
    # 直播结束时间
    end_date = models.DateField(default=None, null=True)
    # 直播开始时间
    start_time = models.TimeField(default=None, null=True)
    # 直播结束时间
    end_time = models.TimeField(default=None, null=True)
    # 创建时间
    create_time = models.DateTimeField(default=timezone.now, db_index=True)

    # 直播的发布酒店
    hotel = models.ForeignKey('Hotel', models.CASCADE, 'lives')

    class Meta:
        ordering = ['-create_time']


class LivePurchaseRecord(models.Model):
    """直播购买记录模型"""

    # 其他支付信息
    # todo

    # 花费
    cost = models.IntegerField()
    # 创建时间
    create_time = models.DateTimeField(default=timezone.now, db_index=True)

    # 直播
    live = models.ForeignKey('Live', models.CASCADE, 'purchase_records')
    # 购买者
    hotel = models.ForeignKey('Hotel', models.CASCADE, 'live_purchase_records')

    class Meta:
        ordering = ['-create_time']


class LiveSubscribe(models.Model):
    """直播预约记录"""

    # 直播
    live = models.ForeignKey('Live', models.CASCADE, 'subscribes')
    # 预约者
    staff = models.ForeignKey('Staff', models.CASCADE, 'subscribe_lives')
    # 创建时间
    create_time = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ['-create_time']


class ValidationCode(models.Model):
    """验证码"""

    phone_number = models.CharField(max_length=11, primary_key=True)
    code = models.CharField(max_length=6, default=None)
    time_expired = models.DateTimeField()

    @classmethod
    def verify(cls, phone_number, code):
        """校验验证码"""

        try:
            now = timezone.now()
            r = cls.objects.get(phone_number=phone_number)
        except cls.DoesNotExist:
            return False
        else:
            return True if code == r.code and now <= r.time_expired else False

    @classmethod
    def generate(cls, phone_number, minutes=10):
        """为某个手机号生成验证码，有效时间为10分钟"""

        from datetime import timedelta
        from random import Random

        try:
            r = cls.objects.get(phone_number=phone_number)
            # 接口访问频率限制, 1分钟
            if r.time_expired >= timezone.now() + timedelta(minutes=9):
                return ''
        except cls.DoesNotExist:
            r = cls(phone_number)
        r.time_expired = timezone.now() + timedelta(minutes=minutes)
        random = Random()
        while True:
            code = ''
            for i in range(6):
                code += str(random.choice(range(0, 10)))
            if code != r.code:
                r.code = code
                break
        r.save()
        return r.code
