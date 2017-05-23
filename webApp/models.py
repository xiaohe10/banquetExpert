import hashlib

from django.db import models
from django.utils import timezone


class Admin(models.Model):
    """管理员模型"""

    username = models.CharField(
        max_length=20, default=None, null=True, unique=True)
    password = models.CharField(max_length=128)
    token = models.CharField(max_length=32)
    authority = models.CharField(max_length=20, default='', db_index=True)
    is_enabled = models.BooleanField(default=True, db_index=True)

    create_time = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ['-create_time']


class Hotel(models.Model):
    """酒店模型"""

    name = models.CharField(max_length=20)
    owner_name = models.CharField(max_length=20)
    is_enabled = models.BooleanField(default=True, db_index=True)

    create_time = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ['-create_time']


class HotelBranch(models.Model):
    """门店模型"""

    name = models.CharField(max_length=20)
    icon = models.CharField(max_length=100, default='')
    # 酒店门店介绍图片，最多5张
    picture = models.CharField(max_length=300, default='')
    province = models.CharField(max_length=20, default='')
    city = models.CharField(max_length=20, default='')
    county = models.CharField(max_length=20, default='')
    address = models.CharField(max_length=50, default='')
    phone = models.CharField(max_length=11, unique=True)
    is_enabled = models.BooleanField(default=True, db_index=True)

    create_time = models.DateTimeField(default=timezone.now, db_index=True)

    hotel = models.ForeignKey('Hotel', models.CASCADE, 'branches')
    manager = models.ForeignKey('Staff', models.CASCADE, 'branches')

    class Meta:
        ordering = ['-create_time']


class Room(models.Model):
    """房间模型"""

    number = models.CharField(max_length=10)
    position = models.CharField(max_length=10)
    state = models.IntegerField(
        choices=((0, '空闲'), (1, '预定中'), (2, '用餐中')),
        default=0, db_index=True)
    people_number_range = models.CharField(max_length=20, default='')
    is_enabled = models.BooleanField(default=True, db_index=True)

    create_time = models.DateTimeField(default=timezone.now, db_index=True)

    branch = models.ForeignKey('HotelBranch', models.CASCADE, 'rooms')
    staff = models.ManyToManyField('Staff', 'rooms')

    class Meta:
        ordering = ['-create_time']


class Staff(models.Model):
    """员工模型"""

    username = models.CharField(
        max_length=20, default=None, null=True, unique=True)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=11, unique=True)
    token = models.CharField(max_length=32)
    name = models.CharField(max_length=20)
    icon = models.CharField(max_length=100, default='')
    gender = models.IntegerField(choices=((0, '保密'), (1, '男'), (2, '女')),
                                 default=0, db_index=True)
    position = models.CharField(max_length=20, default='')
    birthday = models.DateField(default=None, null=True, db_index=True)
    description = models.CharField(max_length=100, default='')
    authority = models.CharField(max_length=20, default='', db_index=True)
    is_enabled = models.BooleanField(default=True, db_index=True)

    create_time = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ['-create_time']

    def set_password(self, password):
        """设置密码(MD5加密方式)"""

        hasher = hashlib.md5(password.encode(encoding='utf-8'))
        self.password = hasher.hexdigest()

    def check_password(self, password):
        """检查密码(MD5验证方式)"""

        hasher = hashlib.md5(password.encode(encoding='utf-8'))
        password1 = hasher.hexdigest()
        return password1 == self.password

    def update_token(self):
        """更新令牌"""

        random_content = self.phone_number + timezone.now().isoformat()
        hasher = hashlib.md5()
        hasher.update(random_content.encode())
        self.token = hasher.hexdigest()


class User(models.Model):
    """用户模型"""

    username = models.CharField(
        max_length=20, default=None, null=True, unique=True)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=11, unique=True)
    token = models.CharField(max_length=32)
    nike_name = models.CharField(max_length=20, default='')
    name = models.CharField(max_length=20, default='')
    id_number = models.CharField(max_length=18, default='')
    icon = models.CharField(max_length=100, default='')
    gender = models.IntegerField(choices=((0, '保密'), (1, '男'), (2, '女')),
                                 default=0, db_index=True)
    qq = models.CharField(max_length=20, default='')
    wechat = models.CharField(max_length=20, default='')
    birthday = models.DateField(default=None, null=True, db_index=True)
    province = models.CharField(max_length=20, default='')
    city = models.CharField(max_length=20, default='')
    county = models.CharField(max_length=20, default='')
    address = models.CharField(max_length=50, default='')
    hobby = models.CharField(max_length=100, default='')
    taboo = models.CharField(max_length=100, default='')
    Individualization = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=100, default='')
    is_enabled = models.BooleanField(default=True, db_index=True)

    create_time = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ['-create_time']

    def set_password(self, password):
        """设置密码(MD5加密方式)"""

        hasher = hashlib.md5(password.encode(encoding='utf-8'))
        self.password = hasher.hexdigest()

    def check_password(self, password):
        """检查密码(MD5验证方式)"""

        hasher = hashlib.md5(password.encode(encoding='utf-8'))
        password1 = hasher.hexdigest()
        return password1 == self.password

    def update_token(self):
        """更新令牌"""

        random_content = self.phone_number + timezone.now().isoformat()
        hasher = hashlib.md5()
        hasher.update(random_content.encode())
        self.token = hasher.hexdigest()

    def save_and_generate_name(self):
        """生成序列用户昵称并保存当前实例"""

        self.nike_name = '宴专家用户 #{}'.format(self.id)
        self.save()


class Order(models.Model):
    """订单模型"""

    state = models.IntegerField(
        choices=((0, '进行中'), (1, '已完成'), (2, '已删除')),
        default=0, db_index=True)
    people_number = models.IntegerField(db_index=True)
    pay_number = models.IntegerField(default=None, db_index=True)
    water_card = models.CharField(max_length=10, default='')
    door_card = models.CharField(max_length=10, default='')
    sand_table = models.CharField(max_length=10, default='')
    welcome_screen = models.CharField(max_length=10, default='')
    welcome_fruit = models.CharField(max_length=10, default='')
    welcome_card = models.CharField(max_length=10, default='')
    # 用户上传的图片，最多5张
    picture = models.CharField(max_length=300, default='')
    background_music = models.CharField(max_length=20, default='')
    has_candle = models.BooleanField(default=False)
    has_flower = models.BooleanField(default=False)
    has_balloon = models.BooleanField(default=False)
    group_photo = models.CharField(max_length=100, default='')
    user_description = models.CharField(max_length=100, default='')
    staff_description = models.CharField(max_length=100, default='')

    create_time = models.DateTimeField(default=timezone.now, db_index=True)
    finish_time = models.DateTimeField(default=None, db_index=True)
    reverse_time = models.DateTimeField(default=None, db_index=True)

    room = models.ForeignKey('Room', models.CASCADE, 'orders')
    user = models.ForeignKey('User', models.CASCADE, 'orders')
    staff = models.ForeignKey('Staff', models.CASCADE, 'orders')

    class Meta:
        ordering = ['-create_time']


class OrderScore(models.Model):
    """评分模型"""

    # 门牌
    door_card_picture = models.CharField(max_length=100, default='')
    door_card_score = models.IntegerField(default=None)
    check_door_card_score = models.IntegerField(default=None)
    # 沙盘
    sand_table_picture = models.CharField(max_length=100, default='')
    sand_table_score = models.IntegerField(default=None)
    check_sand_table_score = models.IntegerField(default=None)
    # 欢迎屏
    welcome_screen_picture = models.CharField(max_length=100, default='')
    welcome_screen_score = models.IntegerField(default=None)
    check_welcome_screen_score = models.IntegerField(default=None)
    # 氛围
    atmosphere_picture = models.CharField(max_length=100, default='')
    atmosphere_score = models.IntegerField(default=None)
    check_atmosphere_score = models.IntegerField(default=None)
    # 拍照
    group_photo_picture = models.CharField(max_length=100, default='')
    group_photo_score = models.IntegerField(default=None)
    check_group_photo_score = models.IntegerField(default=None)
    # 烤瓷杯
    cup_picture = models.CharField(max_length=100, default='')
    cup_score = models.IntegerField(default=None)
    check_cup_score = models.IntegerField(default=None)
    # 小册子
    brochure_picture = models.CharField(max_length=100, default='')
    brochure_score = models.IntegerField(default=None)
    check_brochure_score = models.IntegerField(default=None)
    # 台历
    calendar_picture = models.CharField(max_length=100, default='')
    calendar_score = models.IntegerField(default=None)
    check_calendar_score = models.IntegerField(default=None)
    # 荣誉证书
    honor_certificate_picture = models.CharField(max_length=100, default='')
    honor_certificate_score = models.IntegerField(default=None)
    check_honor_certificate_score = models.IntegerField(default=None)
    # 用心工作
    work_in_heart_picture = models.CharField(max_length=100, default='')
    work_in_heart_score = models.IntegerField(default=None)
    check_work_in_heart_score = models.IntegerField(default=None)
    # 表扬信顾客满意度
    praise_letter_picture = models.CharField(max_length=100, default='')
    praise_letter_score = models.IntegerField(default=None)
    check_praise_letter_score = models.IntegerField(default=None)
    # 朋友圈顾客满意度
    friend_circle_picture = models.CharField(max_length=100, default='')
    friend_circle_score = models.IntegerField(default=None)
    check_friend_circle_score = models.IntegerField(default=None)
    # 网评顾客满意度
    network_comment_picture = models.CharField(max_length=100, default='')
    network_comment_score = models.IntegerField(default=None)
    check_network_comment_score = models.IntegerField(default=None)
    # 单桌当餐转化率
    single_table_transform_score = models.IntegerField(default=None)
    check_single_table_transform_score = models.IntegerField(default=None)
    # 多桌当餐转化率
    multi_table_transform_score = models.IntegerField(default=None)
    check_multi_table_transform_score = models.IntegerField(default=None)

    create_time = models.DateTimeField(default=timezone.now, db_index=True)
    modify_time = models.DateTimeField(default=None, db_index=True)

    order = models.ForeignKey('Order', models.CASCADE, 'order_score')
    staff = models.ForeignKey('Staff', models.CASCADE, 'order_scores')
    check_staff = models.ForeignKey('Staff', models.CASCADE,
                                    'check_order_scores')

    class Meta:
        ordering = ['-create_time']
