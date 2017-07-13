import json
import time
import datetime

from datetime import timedelta
from django import forms
from django.db.models import Q, Sum
from django.utils import timezone
from django.db import IntegrityError, transaction
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator

from ..utils.decorator import validate_args, validate_staff_token, \
    validate_json_args
from ..utils.response import corr_response, err_response
from ..models import Desk, Order, Guest, OrderLog


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'order_date': forms.DateField(required=False),
    'dinner_date': forms.DateField(required=False),
    'date_from': forms.DateField(required=False),
    'date_to': forms.DateField(required=False),
    'dinner_time': forms.TimeField(required=False),
    'dinner_period': forms.IntegerField(
        min_value=0, max_value=2, required=False),
    'status': forms.IntegerField(min_value=0, max_value=2, required=False),
    'search_key': forms.CharField(min_length=1, max_length=20, required=False),
    'offset': forms.IntegerField(min_value=0, required=False),
    'limit': forms.IntegerField(min_value=0, required=False),
    'order': forms.IntegerField(min_value=0, max_value=3, required=False),
})
@validate_staff_token()
def search_orders(request, token, status=0, offset=0, limit=10, order=1,
                  **kwargs):
    """搜索订单列表

    :param token: 令牌(必传)
    :param status: 订单状态, 0: 进行中(默认), 1: 已完成, 2: 已撤单
    :param offset: 起始值
    :param limit: 偏移量
    :param order: 排序方式
        0: 注册时间升序
        1: 注册时间降序（默认值）
    :param kwargs:
        search_key: 关键字
        order_date: 下单日期
        dinner_date: 预定用餐日期
        date_from: 起始时间
        date_to: 终止时间
        dinner_time: 预定用餐时间
        dinner_period: 餐段, 0: 午餐, 1: 晚餐, 2: 夜宵
    :return:
        count: 订单总数
        consumption: 总消费
        guest_number: 就餐人数
        guest_consumption: 人均消费
        list: 订单列表
            order_id: 订单ID
            create_time: 创建日期
            cancel_time: 撤销日期
            arrival_time: 客到日期
            finish_time: 完成日期
            status: 状态, 0: 已订, 1: 进行中, 2: 已完成, 3: 已撤单
            dinner_date: 预定用餐日期
            dinner_time: 预定用餐时间
            dinner_period: 订餐时段, 0: 午餐, 1: 晚餐, 2: 夜宵
            consumption: 消费金额
            name: 联系人
            guest_type: 顾客身份
            contact: 联系电话
            guest_number: 客人数量
            table_count: 餐位数
            desks: 桌位, 数组
            staff_description: 员工备注
            internal_channel: 内部获客渠道, 即接单人名字, 如果存在
            external_channel: 外部获客渠道, 即外部渠道名称, 如果存在
    """
    ORDERS = ('create_time', '-create_time')

    hotel = request.staff.hotel

    if status == 0:
        rs = Order.objects.filter(Q(branch__hotel=hotel, status__in=[0, 1]))
    elif status == 1:
        rs = Order.objects.filter(Q(branch__hotel=hotel, status=2))
    else:
        rs = Order.objects.filter(Q(branch__hotel=hotel, status=3))

    if 'search_key' in kwargs:
        rs = rs.filter(Q(name__icontains=kwargs['search_key']) |
                       Q(contact__icontains=kwargs['search_key']))

    if 'date_from' in kwargs:
        date_from = kwargs['date_from']
        date_from = datetime.datetime.strptime(str(date_from), '%Y-%m-%d')
        rs = rs.filter(Q(create_time__gte=date_from))

    if 'date_to' in kwargs:
        date_to = kwargs['date_to'] + timedelta(days=1)
        date_to = datetime.datetime.strptime(str(date_to), '%Y-%m-%d')
        rs = rs.filter(Q(create_time__lt=date_to))

    if 'dinner_date' in kwargs:
        rs = rs.filter(Q(dinner_date=kwargs['dinner_date']))

    if 'dinner_time' in kwargs:
        rs = rs.filter(Q(dinner_time=kwargs['dinner_time']))

    if 'order_date' in kwargs:
        rs = rs.filter(Q(create_time__startswith=kwargs['order_date']))

    if 'dinner_period' in kwargs:
        rs = rs.filter(Q(dinner_period=kwargs['dinner_period']))

    # 就餐人数
    result = rs.values('branch_id').annotate(
        sum=Sum('guest_number')).order_by('branch_id')
    if result:
        guest_number = result[0]['sum']
    else:
        guest_number = 0

    # 总消费
    result = rs.values('branch_id').annotate(
        sum=Sum('consumption')).order_by('branch_id')
    if result:
        consumption = result[0]['sum']
    else:
        consumption = 0

    # 人均消费
    if guest_number > 0:
        # 结果保留2位小数
        guest_consumption = '%.2f' % (float(consumption) / guest_number)
    else:
        guest_consumption = 0.00

    c = rs.count()
    orders = rs.order_by(ORDERS[order])[offset:offset + limit]

    l = []
    for r in orders:
        d = {'order_id': r.id,
             'create_time': r.create_time,
             'cancel_time': r.cancel_time,
             'arrival_time': r.arrival_time,
             'finish_time': r.finish_time,
             'status': r.status,
             'dinner_date': r.dinner_date,
             'dinner_time': r.dinner_time,
             'dinner_period': r.dinner_period,
             'consumption': r.consumption,
             'name': r.name,
             'guest_type': Guest.objects.get(phone=r.contact).name
             if Guest.objects.filter(phone=r.contact).count() == 1 else '',
             'contact': r.contact,
             'guest_number': r.guest_number,
             'table_count': r.table_count,
             'staff_description': r.staff_description,
             'internal_channel': r.internal_channel.name if
             r.internal_channel else '',
             'external_channel': r.external_channel.name if
             r.external_channel else ''}

        desks_list = json.loads(r.desks)
        d['desks'] = []
        for desk in desks_list:
            desk_id = int(desk[1:-1])
            d['desks'].append(desk_id)

        l.append(d)

    return corr_response({'count': c,
                          'consumption': consumption,
                          'guest_number': guest_number,
                          'guest_consumption': guest_consumption,
                          'list': l})


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'order_id': forms.IntegerField(),
})
@validate_staff_token()
def get_profile(request, token, order_id):
    """获取订单详情

    :param token: 令牌(必传)
    :param order_id: 订单ID(必传)
    :return
        dinner_date: 预定就餐日期
        dinner_time: 预定就餐时间
        dinner_period: 餐段, 0: 午餐, 1: 晚餐, 2: 夜宵
        status: 状态, 0: 已订, 1: 客到, 2: 已完成, 3: 已撤单
        banquet: 宴会类型
        consumption: 消费金额
        name: 联系人
        guest_type: 顾客身份
        contact: 联系电话
        guest_number: 就餐人数
        desks: 预定桌位, 可以多桌, 数组, [{"desk_id":1,"number":"110"}, ...]
        table_count: 预定的餐桌数
        user_description: 用户备注
        staff_description: 员工备注
        water_card: 水牌
        door_card: 门牌
        sand_table: 沙盘
        welcome_screen: 欢迎屏
        welcome_fruit: 迎宾水果的价格
        welcome_card: 欢迎卡
        pictures: 用户上传的图片(最多5张)
        group_photo: 用户上传的合照
        background_music: 背景音乐
        has_candle: 是否有糖果
        has_flower: 是否有鲜花
        has_balloon: 是否有气球
        create_time: 创建时间
        cancel_time: 撤销时间
        arrival_time: 客到时间
        finish_time: 完成时间
        internal_channel: 内部获客渠道, 即接单人名字, 如果存在
        external_channel: 外部获客渠道, 即外部渠道名称, 如果存在
    """

    try:
        order = Order.objects.get(id=order_id)
    except ObjectDoesNotExist:
        return err_response('err_3', '订单不存在')

    if order.branch.hotel != request.staff.hotel:
        return err_response('err_2', '权限错误')

    d = {'dinner_date': order.dinner_date,
         'dinner_time': order.dinner_time,
         'dinner_period': order.dinner_period,
         'status': order.status,
         'banquet': order.banquet,
         'consumption': order.consumption,
         'name': order.name,
         'contact': order.contact,
         'guest_type': Guest.objects.get(phone=order.contact).name
         if Guest.objects.filter(
             phone=order.contact).count() == 1 else '',
         'guest_number': order.guest_number,
         'table_count': order.table_count,
         'user_description': order.user_description,
         'staff_description': order.staff_description,
         'water_card': order.water_card,
         'door_card': order.door_card,
         'sand_table': order.sand_table,
         'welcome_screen': order.welcome_screen,
         'welcome_fruit': order.welcome_fruit,
         'welcome_card': order.welcome_card,
         'pictures': json.loads(order.pictures) if order.pictures else [],
         'group_photo': order.group_photo,
         'background_music': order.background_music,
         'has_candle': order.has_candle,
         'has_flower': order.has_flower,
         'has_balloon': order.has_balloon,
         'create_time': order.create_time,
         'cancel_time': order.cancel_time,
         'arrival_time': order.arrival_time,
         'finish_time': order.finish_time,
         'internal_channel': order.internal_channel.name if
         order.internal_channel else '',
         'external_channel': order.external_channel.name if
         order.external_channel else '',
         'desks': []}

    desks_list = json.loads(order.desks)
    for desk in desks_list:
        desk_id = int(desk[1:-1])
        try:
            number = Desk.objects.get(id=desk_id).number
        except ObjectDoesNotExist:
            number = ''
        d['desks'].append({'desk_id': desk_id, 'number': number})

    return corr_response(d)


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'dinner_date': forms.DateField(),
    'dinner_time': forms.TimeField(),
    'dinner_period': forms.IntegerField(min_value=0, max_value=2),
    'name': forms.CharField(min_length=1, max_length=20),
    'contact': forms.CharField(max_length=11),
    'gender': forms.IntegerField(min_value=0, max_value=2, required=False),
    'guest_number': forms.IntegerField(),
    'table_count': forms.IntegerField(required=False),
    'banquet': forms.CharField(max_length=200, required=False),
    'staff_description': forms.CharField(max_length=200, required=False),
    'water_card': forms.CharField(max_length=10, required=False),
    'door_card': forms.CharField(max_length=10, required=False),
    'sand_table': forms.CharField(max_length=10, required=False),
    'welcome_screen': forms.CharField(max_length=10, required=False),
    'welcome_fruit': forms.IntegerField(required=False),
    'welcome_card': forms.CharField(max_length=10, required=False),
    'background_music': forms.CharField(max_length=20, required=False),
    'has_candle': forms.BooleanField(required=False),
    'has_flower': forms.BooleanField(required=False),
    'has_balloon': forms.BooleanField(required=False),
})
@validate_json_args({
    'desks': forms.CharField(max_length=200)
})
@validate_staff_token()
def submit_order(request, token, dinner_date, dinner_time, dinner_period,
                 **kwargs):
    """提交订单(今天及以后的订单)

    :param token: 令牌(必传)
    :param dinner_date: 预定就餐日期(必传)
    :param dinner_time: 预定就餐时间(必传)
    :param dinner_period: 餐段, 0: 午餐, 1: 晚餐, 2: 夜宵(必传)
    :param kwargs:
        name: 联系人(必传)
        contact: 联系电话(必传)
        gender: 性别(必传)
        guest_number: 就餐人数(必传)
        desks: 预定桌位, 可以多桌, 数组(必传)
        table_count: 餐桌数
        banquet: 宴会类型
        staff_description: 员工备注
        water_card: 水牌
        door_card: 门牌
        sand_table: 沙盘
        welcome_screen: 欢迎屏
        welcome_fruit: 迎宾水果的价格
        welcome_card: 欢迎卡
        background_music: 背景音乐
        has_candle: 是否有糖果
        has_flower: 是否有鲜花
        has_balloon: 是否有气球
    :return: order_id
    """

    # 下单日期校验
    if dinner_date < timezone.now().date():
        return err_response('err_5', '下单日期不能小于当前日期')

    branch_list = []
    branch = None
    # 验证桌位是否存在和是否被预定
    try:
        desk_list = kwargs['desks']
        for i in range(len(desk_list)):
            # 桌位号加首尾限定符
            desk_id = '$' + str(desk_list[i]) + '$'
            if not Desk.enabled_objects.filter(id=desk_list[i]).count() > 0:
                return err_response('err_3', '桌位不存在')

            # 查找订餐的门店
            branch = Desk.enabled_objects.get(id=desk_list[i]).area.branch
            if branch.id not in branch_list:
                branch_list.append(branch.id)

            if Order.objects.filter(dinner_date=dinner_date,
                                    dinner_time=dinner_time,
                                    dinner_period=dinner_period,
                                    status__in=[0, 1],
                                    desks__icontains=desk_id).count() > 0:
                return err_response('err_4', '桌位已被预定')
            desk_list[i] = desk_id
        desks = json.dumps(desk_list)
    except KeyError or ValueError:
        return err_response('err_1', '参数不正确（缺少参数或者不符合格式）')

    # 桌位验证
    if (len(branch_list) != 1) or (branch is None) or \
            (branch.hotel != request.staff.hotel):
        return err_response('err_3', '桌位不存在')

    # 验证门牌是否重复
    if 'door_card' in kwargs:
        door_card = kwargs['door_card']
        if Order.objects.filter(branch=branch,
                                dinner_date=dinner_date,
                                dinner_time=dinner_time,
                                dinner_period=dinner_period,
                                status__in=[0, 1],
                                door_card=door_card).count() > 0:
            return err_response('err_7', '门牌重复')

    order_keys = ('name', 'contact', 'guest_number', 'gender', 'table_count',
                  'water_card', 'door_card', 'sand_table', 'welcome_screen',
                  'welcome_fruit', 'welcome_card', 'background_music',
                  'has_candle', 'has_flower', 'has_balloon', 'banquet',
                  'staff_description')

    with transaction.atomic():
        try:
            order = Order(dinner_date=dinner_date, dinner_time=dinner_time,
                          dinner_period=dinner_period, desks=desks,
                          internal_channel=request.staff, branch=branch)
            for k in order_keys:
                if k in kwargs:
                    setattr(order, k, kwargs[k])
            order.save()
            # 记录订单的操作日志
            order.logs.create(staff=request.staff, status=0, content='创建订单')
            order.save()
            return corr_response({'order_id': order.id})
        except IntegrityError:
            return err_response('err_6', '服务器创建订单错误')


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'dinner_date': forms.DateField(),
    'dinner_time': forms.TimeField(),
    'dinner_period': forms.IntegerField(min_value=0, max_value=2),
    'name': forms.CharField(min_length=1, max_length=20),
    'contact': forms.CharField(max_length=11),
    'gender': forms.IntegerField(min_value=0, max_value=2, required=False),
    'guest_number': forms.IntegerField(),
    'table_count': forms.IntegerField(required=False),
    'banquet': forms.CharField(max_length=200, required=False),
    'staff_description': forms.CharField(max_length=200, required=False),
    'water_card': forms.CharField(max_length=10, required=False),
    'door_card': forms.CharField(max_length=10, required=False),
    'sand_table': forms.CharField(max_length=10, required=False),
    'welcome_screen': forms.CharField(max_length=10, required=False),
    'welcome_fruit': forms.IntegerField(required=False),
    'welcome_card': forms.CharField(max_length=10, required=False),
    'background_music': forms.CharField(max_length=20, required=False),
    'has_candle': forms.BooleanField(required=False),
    'has_flower': forms.BooleanField(required=False),
    'has_balloon': forms.BooleanField(required=False),
})
@validate_json_args({
    'desks': forms.CharField(max_length=200)
})
@validate_staff_token()
def supply_order(request, token, dinner_date, dinner_time, dinner_period,
                 **kwargs):
    """补录订单(今天及以前的订单)

    :param token: 令牌(必传)
    :param dinner_date: 预定就餐日期(必传)
    :param dinner_time: 预定就餐时间(必传)
    :param dinner_period: 餐段, 0: 午餐, 1: 晚餐, 2: 夜宵(必传)
    :param kwargs:
        name: 联系人(必传)
        contact: 联系电话(必传)
        gender: 性别(必传)
        guest_number: 就餐人数(必传)
        desks: 预定桌位, 可以多桌, 数组(必传)
        table_count: 餐位数
        banquet: 宴会类型
        staff_description: 员工备注
        water_card: 水牌
        door_card: 门牌
        sand_table: 沙盘
        welcome_screen: 欢迎屏
        welcome_fruit: 迎宾水果的价格
        welcome_card: 欢迎卡
        background_music: 背景音乐
        has_candle: 是否有糖果
        has_flower: 是否有鲜花
        has_balloon: 是否有气球
    :return: order_id
    """

    # 下单日期校验
    if dinner_date > timezone.now().date():
        return err_response('err_4', '补录订单日期不能大于当前日期')

    branch_list = []
    branch = None
    # 验证桌位是否存在
    try:
        desk_list = kwargs['desks']
        for i in range(len(desk_list)):
            # 桌位号加首尾限定符
            desk_id = '$' + str(desk_list[i]) + '$'
            if not Desk.enabled_objects.filter(id=desk_list[i]).count() > 0:
                return err_response('err_3', '桌位不存在')

            # 查找订餐的门店
            branch = Desk.enabled_objects.get(id=desk_list[i]).area.branch
            if branch.id not in branch_list:
                branch_list.append(branch.id)

            desk_list[i] = desk_id
        desks = json.dumps(desk_list)
    except KeyError or ValueError:
        return err_response('err_1', '参数不正确（缺少参数或者不符合格式）')

    # 桌位验证
    if (len(branch_list) != 1) or (branch is None) or \
            (branch.hotel != request.staff.hotel):
        return err_response('err_3', '桌位不存在')

    order_keys = ('name', 'contact', 'guest_number', 'gender', 'table_count',
                  'water_card', 'door_card', 'sand_table', 'welcome_screen',
                  'welcome_fruit', 'welcome_card', 'background_music',
                  'has_candle', 'has_flower', 'has_balloon', 'banquet',
                  'staff_description')

    with transaction.atomic():
        try:
            order = Order(dinner_date=dinner_date, dinner_time=dinner_time,
                          dinner_period=dinner_period, desks=desks,
                          internal_channel=request.staff, branch=branch)
            for k in order_keys:
                if k in kwargs:
                    setattr(order, k, kwargs[k])
            order.save()
            # 记录订单的操作日志
            order.logs.create(staff=request.staff, status=5, content='补录订单')
            order.save()
            return corr_response({'order_id': order.id})
        except IntegrityError as e:
            print(e)
            return err_response('err_5', '服务器创建订单错误')


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'order_id': forms.IntegerField(),
    'status': forms.IntegerField(min_value=0, max_value=3, required=False),
    'banquet': forms.CharField(max_length=200, required=False),
    'dinner_date': forms.DateField(required=False),
    'dinner_time': forms.TimeField(required=False),
    'dinner_period': forms.IntegerField(
        min_value=0, max_value=2, required=False),
    'name': forms.CharField(min_length=1, max_length=20, required=False),
    'contact': forms.CharField(max_length=11, required=False),
    'gender': forms.IntegerField(min_value=0, max_value=2, required=False),
    'guest_number': forms.IntegerField(required=False),
    'table_count': forms.IntegerField(required=False),
    'staff_description': forms.CharField(max_length=200, required=False),
    'water_card': forms.CharField(max_length=10, required=False),
    'door_card': forms.CharField(max_length=10, required=False),
    'sand_table': forms.CharField(max_length=10, required=False),
    'welcome_screen': forms.CharField(max_length=10, required=False),
    'welcome_fruit': forms.IntegerField(required=False),
    'welcome_card': forms.CharField(max_length=10, required=False),
    'background_music': forms.CharField(max_length=20, required=False),
    'has_candle': forms.BooleanField(required=False),
    'has_flower': forms.BooleanField(required=False),
    'has_balloon': forms.BooleanField(required=False),
})
@validate_json_args({
    'desks': forms.CharField(max_length=200, required=False)
})
@validate_staff_token()
def modify_order(request, token, order_id, **kwargs):
    """修改订单

    :param token: 令牌(必传)
    :param order_id: 订单ID(必传)
    :param kwargs:
        status: 订单状态, 0: 已订, 1: 客到, 2: 已完成, 3: 已撤单
        banquet: 宴会类型
        dinner_date: 预定就餐日期
        dinner_time: 预定就餐时间
        dinner_period: 餐段, 0: 午餐, 1: 晚餐, 2: 夜宵
        name: 联系人
        contact: 联系电话
        gender: 性别
        guest_number: 就餐人数
        table_count: 餐桌数
        desks: 预定桌位, 可以多桌, 数组
        staff_description: 员工备注
        water_card: 水牌
        door_card: 门牌
        sand_table: 沙盘
        welcome_screen: 欢迎屏
        welcome_fruit: 迎宾水果的价格
        welcome_card: 欢迎卡
        background_music: 背景音乐
        has_candle: 是否有糖果
        has_flower: 是否有鲜花
        has_balloon: 是否有气球
    """

    try:
        order = Order.objects.get(id=order_id)
    except ObjectDoesNotExist:
        return err_response('err_3', '订单不存在')

    order_keys = ('status', 'dinner_date', 'dinner_time', 'dinner_period',
                  'name', 'contact', 'guest_number', 'staff_description',
                  'water_card', 'door_card', 'sand_table', 'welcome_screen',
                  'welcome_fruit', 'welcome_card', 'background_music',
                  'has_candle', 'has_flower', 'has_balloon', 'banquet',
                  'table_count', 'gender')

    # 如果换门牌, 验证门牌是否重复
    if 'door_card' in kwargs:
        dinner_date = kwargs['dinner_date'] if \
            'dinner_date' in kwargs else order.dinner_date
        dinner_time = kwargs['dinner_time'] if \
            'dinner_time' in kwargs else order.dinner_time
        dinner_period = kwargs['dinner_period'] if \
            'dinner_period' in kwargs else order.dinner_period,
        door_card = kwargs['door_card']
        if Order.objects.filter(branch=order.branch,
                                dinner_date=dinner_date,
                                dinner_time=dinner_time,
                                dinner_period=dinner_period,
                                status__in=[0, 1],
                                door_card=door_card). \
                exclude(id=order.id).count() > 0:
            return err_response('err_7', '门牌重复')

    # 下单日期校验
    if 'dinner_date' in kwargs:
        if kwargs['dinner_date'] < timezone.now().date():
            return err_response('err_1', '参数不正确（缺少参数或者不符合格式）')

    # 订单状态切换验证
    if 'status' in kwargs:
        status = kwargs['status']
        # 客到
        if status == 1 and order.status == 0:
            order.arrival_time = timezone.now()
            # 记录订单的操作日志
            order.logs.create(staff=request.staff, status=1,
                              content='更改订单状态为客到')
        # 翻台
        elif status == 2 and order.status == 1:
            order.finish_time = timezone.now()
            # 记录订单的操作日志
            order.logs.create(staff=request.staff, status=2,
                              content='更改订单状态为已完成')
        # 撤单
        elif status == 3 and order.status != 2:
            order.cancel_time = timezone.now()
            # 记录订单的操作日志
            order.logs.create(staff=request.staff, status=4,
                              content='更改订单状态为已撤单')
        else:
            return err_response('err_5', '订单状态切换非法')

    # 如果换桌
    if 'desks' in kwargs:
        branch_list = []
        branch = None
        desk_list = kwargs['desks']
        new_desk_list = []
        old_desk_str = ''
        old_desks = order.desks
        # 获取原桌位编号字符串
        if old_desks:
            old_desk_list = []
            for old_desk in old_desk_list:
                old_desk_id = old_desk[1:-1]
                try:
                    desk = Desk.enabled_objects.get(id=old_desk_id)
                    old_desk_list.append(desk.number)
                except ObjectDoesNotExist:
                    pass
            old_desk_str = ', '.join(old_desk_list)

        # 验证桌位是否存在和是否被预定
        try:
            for i in range(len(desk_list)):
                # 桌位号加首尾限定符
                desk_id = '$' + str(desk_list[i]) + '$'
                if Desk.enabled_objects.filter(id=desk_list[i]).count() == 0:
                    return err_response('err_3', '桌位不存在')

                # 获取新桌位编号字符串
                desk = Desk.enabled_objects.get(id=desk_list[i])
                new_desk_list.append(desk.number)

                # 查找订餐的门店
                branch = Desk.enabled_objects.get(id=desk_list[i]).area.branch
                if branch.id not in branch_list:
                    branch_list.append(branch.id)

                if Order.objects.exclude(id=order_id).filter(
                        dinner_date=order.dinner_date,
                        dinner_time=order_id.dinner_time,
                        dinner_period=order.dinner_period,
                        status__in=[0, 1],
                        desk__icontains=desk_id).count() > 0:
                    return err_response('err_4', '桌位已被预定')
                desk_list[i] = desk_id
            desks = json.dumps(desk_list)
            order.desks = desks
            # 记录订单的操作日志
            new_desk_str = ', '.join(new_desk_list)
            content = '换桌[%s]为[%s]' % (old_desk_str, new_desk_str)
            order.logs.create(staff=request.staff, status=3, content=content)
        except KeyError or ValueError:
            return err_response('err_1', '参数不正确（缺少参数或者不符合格式）')

        # 桌位验证
        if (len(branch_list) != 1) or (branch is None) or \
                (branch.hotel != request.staff.hotel):
            return err_response('err_3', '桌位不存在')

    for k in order_keys:
        if k in kwargs:
            setattr(order, k, kwargs[k])
    order.save()

    return corr_response()


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'order_id': forms.IntegerField(),
})
@validate_staff_token()
def get_order_logs(request, token, order_id):
    """获取订单的操作日志
    :param token: 令牌(必传)
    :param order_id: 订单ID(必传)
    :return
        count: 总数
        list:
            content: 内容
            type: 操作类型, 0: 预定, 1: 客到, 2: 翻台, 3: 调桌, 4: 撤单, 5: 补录
            staff_id: 操作员工ID
            staff_name: 操作员工姓名
            create_time: 创建时间
    """

    try:
        order = Order.objects.get(id=order_id)
    except ObjectDoesNotExist:
        return err_response('err_3', '订单不存在')

    if order.branch.hotel != request.staff.hotel:
        return err_response('err_2', '权限错误')

    logs = order.logs.all()
    c = logs.count()

    l = [{'content': log.content,
          'type': log.type,
          'staff_id': log.staff.id,
          'staff_name': log.staff.name,
          'create_time': log.create_time} for log in logs]

    return corr_response({'count': c, 'list': l})


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'date_from': forms.DateField(required=False),
    'date_to': forms.DateField(required=False),
    'desk_id': forms.IntegerField(required=False),
    'offset': forms.IntegerField(min_value=0, required=False),
    'limit': forms.IntegerField(min_value=0, required=False),
})
@validate_staff_token()
def search_order_logs(request, token, offset=0, limit=10, **kwargs):
    """搜索订单的操作日志
    :param token: 令牌(必传)
    :param offset: 起始值
    :param limit: 偏移量
    :param kwargs
        date_from: 起始时间
        date_to: 终止时间
        desk_id: 桌位ID
    :return
        count: 总数
        list:
            type: 类型, 0: 预定, 1: 客到, 2: 翻台, 3: 调桌, 4: 撤单, 5: 补录
            content: 内容
            staff_id: 操作员工ID
            staff_name: 操作员工姓名
            order_id: 订单ID
            status: 订单状态
            name: 订餐人
            contact: 订餐人电话
            gender: 订餐人性别
            contact: 订餐电话
            guest_number: 人数
            dinner_date: 用餐日期
            dinner_time: 用餐时间
            dinner_period: 餐段
            internal_channel: 内部获客渠道
            external_channel： 外部获客渠道
            branch_id: 门店ID
            branch_name: 门店名称
            desks: 桌位[{"id":1, "number":110}, ...]
            create_time: 创建时间
    """

    hotel = request.staff.hotel

    logs = OrderLog.objects.filter(order__branch__hotel=hotel)

    if 'date_from' in kwargs:
        date_from = kwargs['date_from']
        date_from = datetime.datetime.strptime(str(date_from), '%Y-%m-%d')
        logs = logs.filter(Q(create_time__gte=date_from))

    if 'date_to' in kwargs:
        date_to = kwargs['date_to'] + timedelta(days=1)
        date_to = datetime.datetime.strptime(str(date_to), '%Y-%m-%d')
        logs = logs.filter(Q(create_time__lt=date_to))

    if 'desk_id' in kwargs:
        desk_id = '$' + kwargs['desk_id'] + '$'
        logs = logs.filter(Q(order__desks__icontains=desk_id))

    c = logs.count()
    logs = logs[offset: offset + limit]

    l = []
    for log in logs:
        d = {'content': log.content,
             'type': log.type,
             'staff_id': log.staff.id,
             'staff_name': log.staff.name,
             'order_id': log.order.id,
             'name': log.order.name,
             'contact': log.order.contact,
             'gender': log.order.gender,
             'guest_number': log.order.guest_number,
             'status': log.order.status,
             'dinner_date': log.order.dinner_date,
             'dinner_time': log.order.dinner_time,
             'dinner_period': log.order.dinner_period,
             'internal_channel': log.order.internal_channel.name,
             'external_channel': log.order.external_channel.name,
             'branch_id': log.order.branch.id,
             'branch_name': log.order.branch.name,
             'create_time': log.create_time}

        desks_list = json.loads(log.order.desks)
        for desk in desks_list:
            desk_id = int(desk[1:-1])
            try:
                number = Desk.objects.get(id=desk_id).number
            except ObjectDoesNotExist:
                number = ''
            d['desks'].append({'desk_id': desk_id, 'number': number})

    return corr_response({'count': c, 'list': l})


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'year': forms.IntegerField(required=False),
})
@validate_staff_token()
def get_month_orders(request, token, year=None):
    """获取月订单列表

    :param token: 令牌(必传)
    :param year: 年份
    :return:
        month: 月份, 例: 2017-05
        order_number: 订单数
        desk_number: 订的桌数
        guest_number: 用餐人数
        consumption: 总消费
        person_consumption: 人均消费
        desk_consumption: 桌均消费
    """

    if year is None:
        year = timezone.now().year

    hotel = request.staff.hotel
    month_consumptions = hotel.month_consumptions.filter(
        month__startswith=str(year)).order_by('-month')
    l = [{'month': c.month,
          'order_number': c.order_number,
          'desk_number': c.desk_number,
          'guest_number': c.guest_number,
          'consumption': c.consumption,
          'person_consumption': c.person_consumption,
          'desk_consumption': c.desk_consumption} for c in month_consumptions]
    return corr_response(l)


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'month': forms.CharField(
        validators=[RegexValidator(regex=r'^[0-9]{4}-[0-9]{2}$')]),
})
@validate_staff_token()
def get_day_orders(request, token, month):
    """获取日订单列表

    :param token: 令牌(必传)
    :param month: 月份(必传), 例: 2017-05
    :return:
        date: 日期, 例: 2017-05-01
        order_number: 订单数
        desk_number: 订的桌数
        guest_number: 用餐人数
        consumption: 总消费
        person_consumption: 人均消费
        desk_consumption: 桌均消费
    """

    # 日期处理
    t = time.strptime(month, "%Y-%m")
    y, m, d = t[0:3]
    first_day = datetime.date(y, m, d)
    if m >= 12:
        last_day = datetime.date(y + 1, 1, d)
    else:
        last_day = datetime.date(y, m + 1, d)

    hotel = request.staff.hotel
    day_consumptions = hotel.day_consumptions.filter(
        date__gte=first_day, date__lt=last_day).order_by('-date')
    l = [{'date': c.date,
          'order_number': c.order_number,
          'desk_number': c.desk_number,
          'guest_number': c.guest_number,
          'consumption': c.consumption,
          'person_consumption': c.person_consumption,
          'desk_consumption': c.desk_consumption} for c in day_consumptions]
    return corr_response(l)
