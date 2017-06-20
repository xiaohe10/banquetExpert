import json

from django import forms
from django.db.models import Q, timezone
from django.db import IntegrityError, transaction
from django.core.exceptions import ObjectDoesNotExist

from ..utils.decorator import validate_args, validate_staff_token
from ..utils.response import corr_response, err_response
from ..models import Desk, Order, UserArchives


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'order_date': forms.DateField(required=False),
    'dinner_date': forms.DateField(required=False),
    'dinner_time': forms.TimeField(required=False),
    'status': forms.IntegerField(min_value=0, max_value=1, required=False),
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
    :param status: 订单状态, 0: 进行中(默认), 1: 已完成
    :param offset: 起始值
    :param limit: 偏移量
    :param order: 排序方式
        0: 注册时间升序
        1: 注册时间降序（默认值）
    :param kwargs:
        search_key: 关键字
        order_date: 下单日期
        dinner_date: 预定用餐日期
        dinner_time: 预定用餐时间
        dinner_period: 餐段
    :return:
        count: 订单总数
        list: 订单列表
            order_id: 订单ID
            create_time: 创建日期
            cancel_time: 撤销日期
            arrival_time: 客到日期
            finish_time: 完成日期
            state: 状态, 0: 已订, 1: 客到, 2: 已完成, 3: 已撤单
            dinner_date: 预定用餐日期
            dinner_time: 预定用餐时间
            dinner_period: 订餐时段, 0: 午餐, 1: 晚餐, 2: 夜宵
            name: 联系人
            guest_type: 顾客身份
            contact: 联系电话
            guest_number: 客人数量
            desks: 桌位, 数组
            internal_channel: 内部获客渠道, 即接单人名字, 如果存在
            external_channel: 外部获客渠道, 即外部渠道名称, 如果存在
    """
    ORDERS = ('create_time', '-create_time')

    if status:
        rs = Order.objects.filter(Q(status__in=[0, 1]))
    else:
        rs = Order.objects.filter(Q(status__in=[2, 3]))

    if 'search_key' in kwargs:
        rs = rs.filter(Q(name__icontains=kwargs['search_key']) |
                       Q(contact__icontains=kwargs['search_key']))

    if 'dinner_date' in kwargs:
        rs = rs.filter(Q(dinner_date=kwargs['dinner_date']))

    if 'dinner_time' in kwargs:
        rs = rs.filter(Q(dinner_time=kwargs['dinner_time']))

    if 'order_date' in kwargs:
        rs = rs.filter(Q(create_time__startswith=kwargs['order_date']))

    c = rs.count()
    rs = rs.order_by(ORDERS[order])[offset:offset + limit]

    l = [{'order_id': r.id,
          'create_time': r.create_time,
          'cancel_time': r.cancel_time,
          'arrival_time': r.arrival_time,
          'finish_time': r.finish_time,
          'status': r.status,
          'dinner_date': r.dinner_date,
          'dinner_time': r.dinner_time,
          'dinner_period': r.dinner_period,
          'name': r.name,
          'guest_type': UserArchives.objects.get(phone=r.contact).name
          if UserArchives.objects.filter(phone=r.contact).count() == 1 else '',
          'contact': r.contact,
          'guest_number': r.guest_number,
          'desks': json.loads(r.desks),
          'internal_channel': r.internal_channel.name if
          r.internal_channel else '',
          'external_channel': r.external_channel.name if
          r.internal_channel else ''} for r in rs]

    return corr_response({'count': c, 'list': l})


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
        name: 联系人
        guest_type: 顾客身份
        contact: 联系电话
        guest_number: 就餐人数
        desks: 预定桌位, 可以多桌, json数组
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

    d = {'dinner_date': order.dinner_date,
         'dinner_time': order.dinner_time,
         'dinner_period': order.dinner_period,
         'status': order.status,
         'name': order.name,
         'contact': order.contact,
         'guest_type': UserArchives.objects.get(phone=order.contact).name
         if UserArchives.objects.filter(
             phone=order.contact).count() == 1 else '',
         'guest_number': order.guest_number,
         'user_description': order.user_description,
         'staff_description': order.staff_description,
         'water_card': order.water_card,
         'door_card': order.door_card,
         'sand_table': order.sand_table,
         'welcome_screen': order.welcome_screen,
         'welcome_fruit': order.welcome_fruit,
         'welcome_card': order.welcome_card,
         'pictures': order.pictures,
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
        d['desks'].append(desk[1:-1])

    return corr_response(d)


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'dinner_date': forms.DateField(),
    'dinner_time': forms.TimeField(),
    'dinner_period': forms.IntegerField(min_value=0, max_value=2),
    'name': forms.CharField(min_length=1, max_length=20),
    'contact': forms.RegexField(r'[0-9]{11}'),
    'guest_number': forms.IntegerField(),
    'desks': forms.CharField(max_length=50),
    'staff_description': forms.CharField(max_length=100, required=False),
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
@validate_staff_token()
def submit_order(request, token, dinner_date, dinner_time, dinner_period,
                 **kwargs):
    """提交订单

    :param token: 令牌(必传)
    :param dinner_date: 预定就餐日期(必传)
    :param dinner_time: 预定就餐时间(必传)
    :param dinner_period: 餐段, 0: 午餐, 1: 晚餐, 2: 夜宵(必传)
    :param kwargs:
        name: 联系人(必传)
        contact: 联系电话(必传)
        guest_number: 就餐人数(必传)
        desks: 预定桌位, 可以多桌, json数组(必传)
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

    desks = kwargs.pop('desks')
    # 验证桌位是否存在和是否被预定
    try:
        desk_list = json.loads(desks)
        for i in range(len(desk_list)):
            # 桌位号加首尾限定符
            desk_id = '$' + str(desk_list[i]) + '$'
            if Desk.enabled_objects.filter(id=desk_id).exists():
                return err_response('err_3', '桌位不存在')
            if Order.objects.filter(dinner_date=dinner_date,
                                    dinner_time=dinner_time,
                                    dinner_period=dinner_period,
                                    status__in=[0, 1],
                                    desks__icontains=desk_id).exisits():
                return err_response('err_4', '桌位已被预定')
            desk_list[i] = desk_id
        desks = json.dumps(desk_list)
    except KeyError or ValueError:
        return err_response('err_1', '参数不正确（缺少参数或者不符合格式）')

    order_keys = ('name', 'contact', 'guest_number', 'staff_description',
                  'water_card', 'door_card', 'sand_table', 'welcome_screen',
                  'welcome_fruit', 'welcome_card', 'background_music',
                  'has_candle', 'has_flower', 'has_balloon')

    with transaction.atomic():
        try:
            order = Order(dinner_date=dinner_date, dinner_time=dinner_time,
                          dinner_period=dinner_period, desks=desks)
            for k in order_keys:
                if k in kwargs:
                    setattr(order, k, kwargs[k])
            order.save()
            return corr_response({'order_id': order.id})
        except IntegrityError:
            return err_response('err_5', '服务器创建订单错误')


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'order_id': forms.IntegerField(),
    'dinner_date': forms.DateField(required=False),
    'dinner_time': forms.TimeField(required=False),
    'dinner_period': forms.IntegerField(
        min_value=0, max_value=2, required=False),
    'name': forms.CharField(min_length=1, max_length=20, required=False),
    'contact': forms.RegexField(r'[0-9]{11}', required=False),
    'guest_number': forms.IntegerField(required=False),
    'desks': forms.CharField(max_length=50, required=False),
    'staff_description': forms.CharField(max_length=100, required=False),
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
@validate_staff_token()
def modify_order(request, token, order_id, **kwargs):
    """修改订单

    :param token: 令牌(必传)
    :param order_id: 订单ID(必传)
    :param kwargs:
        status: 订单状态, 0: 已订, 1: 客到, 2: 已完成, 3: 已撤单
        dinner_date: 预定就餐日期
        dinner_time: 预定就餐时间
        dinner_period: 餐段, 0: 午餐, 1: 晚餐, 2: 夜宵
        name: 联系人
        contact: 联系电话
        guest_number: 就餐人数
        desks: 预定桌位, 可以多桌, json数组
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
                  'has_candle', 'has_flower', 'has_balloon')

    # 订单状态切换验证
    if 'status' in kwargs:
        status = kwargs['status']
        # 客到
        if status == 1 and order.status == 0:
            order.arrival_time = timezone.now()
        # 翻台
        elif status == 2 and order.status == 1:
            order.finish_time = timezone.now()
        # 撤单
        elif status == 3 and order.status != 2:
            order.cancel_time = timezone.now()
        else:
            return err_response('err_5', '订单状态切换非法')

    for k in order_keys:
        if k in kwargs:
            setattr(order, k, kwargs[k])
    order.save()

    # 如果换桌
    if 'desks' in kwargs:
        desks = kwargs.pop('desks')
        # 验证桌位是否存在和是否被预定
        try:
            desk_list = json.loads(desks)
            for i in range(len(desk_list)):
                # 桌位号加首尾限定符
                desk_id = '$' + str(desk_list[i]) + '$'
                if Desk.enabled_objects.filter(id=desk_id).exists():
                    return err_response('err_3', '桌位不存在')
                if Order.objects.exclude(id=order_id).filter(
                        dinner_date=order.dinner_date,
                        dinner_time=order_id.dinner_time,
                        dinner_period=order.dinner_period,
                        status__in=[0, 1],
                        desk__icontains=desk_id).exisits():
                    return err_response('err_4', '桌位已被预定')
                desk_list[i] = desk_id
            desks = json.dumps(desk_list)
            order.desks = desks
            order.save()
        except KeyError or ValueError:
            return err_response('err_1', '参数不正确（缺少参数或者不符合格式）')

    return corr_response()
