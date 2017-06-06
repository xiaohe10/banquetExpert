import hashlib

from django.db import models
from django.utils import timezone

__all__ = ['Admin', 'Hotel', 'HotelBranch', 'Desk', 'Staff', 'ExternalChannel',
           'User', 'Order', 'OrderScore', 'Course', 'CoursePurchaseRecord']


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
    picture = models.CharField(max_length=300, default='')
    # 所属省
    province = models.CharField(max_length=20, default='')
    # 所属市
    city = models.CharField(max_length=20, default='')
    # 所属县/区
    county = models.CharField(max_length=20, default='')
    # 详细地址
    address = models.CharField(max_length=50, default='')
    # 设施
    facility = models.CharField(max_length=100, default='')
    # 可以刷哪些卡
    pay_card = models.CharField(max_length=20, default='')
    # 电话(最多3个)
    phone = models.CharField(max_length=50, default='')
    # 菜系
    cuisine = models.CharField(max_length=100, default='')
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


class Desk(models.Model):
    """桌位模型"""

    # 桌位号
    number = models.CharField(max_length=10)
    # 位置
    position = models.CharField(max_length=10)
    # 状态
    state = models.IntegerField(
        choices=((0, '空闲'), (1, '预定中'), (2, '用餐中')),
        default=0, db_index=True)
    # 排序
    order = models.IntegerField(db_index=True)
    # 费用说明
    expense = models.IntegerField(default=None, null=True)
    # 房间类型
    type = models.CharField(max_length=10, default='', db_index=True)
    # 设施
    facility = models.CharField(max_length=100, default='')
    # 照片
    picture = models.CharField(max_length=100, default='')
    # 是否靠窗
    is_beside_window = models.BooleanField(default=False)
    # 最小可容纳人数
    min_people_number = models.IntegerField(default=None, null=True)
    # 最大可容纳人数
    max_people_number = models.IntegerField(default=None, null=True)
    # 是否有效
    is_enabled = models.BooleanField(default=True, db_index=True)

    # 创建时间
    create_time = models.DateTimeField(default=timezone.now, db_index=True)

    # 所属门店
    branch = models.ForeignKey('HotelBranch', models.CASCADE, 'desks')
    # 员工
    staff = models.ManyToManyField('Staff', 'desks')

    # 管理器
    objects = models.Manager()
    enabled_objects = EnabledManager()

    class Meta:
        ordering = ['-create_time']


class Staff(models.Model):
    """员工模型"""

    # 员工编号
    staff_number = models.CharField(
        max_length=20, default=None, null=True, unique=True)
    # 手机
    phone = models.CharField(max_length=11, unique=True)
    # 密码
    password = models.CharField(max_length=32)
    # 令牌
    token = models.CharField(max_length=32)
    # 姓名
    name = models.CharField(max_length=20)
    # 身份证号
    id_number = models.CharField(max_length=18, default='')
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
    description = models.CharField(max_length=100, default='')
    # 权限
    authority = models.CharField(max_length=20, default='', db_index=True)
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
    discount = models.IntegerField(default=0)
    # 头像
    icon = models.CharField(max_length=100, default='')
    # 合作起始时间
    begin_cooperate_time = models.DateField()
    # 合作结束时间
    end_cooperate_time = models.DateField()
    # 佣金核算方式
    commission_type = models.IntegerField(
        choices=((0, '无'),
                 (1, '按消费额百分百比'),
                 (2, '按订单数量'),
                 (3, '按消费人数')),
        default=0)
    # 佣金核算数值
    commission_value = models.IntegerField()
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
    # 所在省
    province = models.CharField(max_length=20, default='')
    # 所在市
    city = models.CharField(max_length=20, default='')
    # 所在区/县
    county = models.CharField(max_length=20, default='')
    # 详细地址
    address = models.CharField(max_length=50, default='')
    # 爱好
    hobby = models.CharField(max_length=100, default='')
    # 忌讳
    taboo = models.CharField(max_length=100, default='')
    # 个性化需求
    Individualization = models.CharField(max_length=100, default='')
    # 备注
    description = models.CharField(max_length=100, default='')
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


class Order(models.Model):
    """订单模型"""

    # 订单状态
    state = models.IntegerField(
        choices=((0, '已订'), (1, '客到'), (2, '已完成'), (3, '已撤单')),
        default=0, db_index=True)
    # 联系人
    name = models.CharField(max_length=20, db_index=True)
    # 联系电话
    people_number = models.IntegerField(db_index=True)
    # 支付金额
    pay_number = models.IntegerField(default=None, db_index=True)
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
    picture = models.CharField(max_length=300, default='')
    # 背景音乐
    background_music = models.CharField(max_length=20, default='')
    # 是否有蜡烛
    has_candle = models.BooleanField(default=False)
    # 是否有鲜花
    has_flower = models.BooleanField(default=False)
    # 是否有气球
    has_balloon = models.BooleanField(default=False)
    # 合照
    group_photo = models.CharField(max_length=100, default='')
    # 顾客备注
    user_description = models.CharField(max_length=100, default='')
    # 员工备注
    staff_description = models.CharField(max_length=100, default='')

    # 餐段
    dinner_period = models.IntegerField(
        choices=((0, '午餐'), (1, '晚餐'), (2, '夜宵')), default=0, db_index=True)
    # 就餐时间
    dinner_time = models.DateTimeField(db_index=True)
    # 创建时间
    create_time = models.DateTimeField(default=timezone.now, db_index=True)
    # 完成时间
    finish_time = models.DateTimeField(default=None, db_index=True)
    # 撤销时间
    reverse_time = models.DateTimeField(default=None, db_index=True)

    # 预定桌位
    desk = models.ForeignKey('Desk', models.CASCADE, 'orders')
    # 顾客(可能是散客)
    user = models.ForeignKey(
        'User', models.CASCADE, 'orders', default=None, null=True)
    # 内部获客渠道
    internal_channel = models.ForeignKey(
        'Staff', models.CASCADE, 'orders', default=None, null=True)
    # 外部获客渠道
    external_channel = models.ForeignKey(
        'ExternalChannel', models.CASCADE, 'orders', default=None, null=True)

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


class Course(models):
    """微课堂模型"""

    # 对应cc视频ID
    videoID = models.CharField(max_length=20, unique=True)
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
    description = models.CharField(max_length=100, default='')

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


class CoursePurchaseRecord(models):
    """课程购买模型"""

    # 其他支付信息
    # todo

    # 花费
    cost = models.IntegerField()
    # 创建时间
    create_time = models.DateTimeField(default=timezone.now, db_index=True)

    # 课程
    course = models.ForeignKey('Course', models.CASCADE, 'purchase_records')
    # 购买者
    hotel = models.ForeignKey('Hotel', models.CASCADE, 'purchase_records')

    class Meta:
        ordering = ['-create_time']
