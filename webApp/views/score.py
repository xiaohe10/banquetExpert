import json
import datetime

from datetime import timedelta
from PIL import Image
from django import forms
from django.db import IntegrityError, transaction
from django.db.models import Q, Sum
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from ..utils.decorator import validate_args, validate_staff_token
from ..utils.response import corr_response, err_response
from ..utils.http import send_message
from ..models import Staff, Hotel, Order, Guest, Desk


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
def search_scores(request, token, status=0, offset=0, limit=10, order=1,
                  **kwargs):
    """搜索评分列表

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
            score_id: 评分ID
            score: 总分
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
             r.external_channel else '',
             'score_id': r.order_score.id
             if r.order_score.all().count() == 1 else 0,
             'score': r.order_score.score
             if r.order_score.all().count() == 1 else 0}

        # 桌位信息
        desks_list = json.loads(r.desks)
        d['desks'] = []
        for desk in desks_list:
            desk_id = int(desk[1:-1])
            try:
                number = Desk.objects.get(id=desk_id).number
            except ObjectDoesNotExist:
                number = ''
            d['desks'].append(number)

        l.append(d)

    return corr_response({'count': c,
                          'consumption': consumption,
                          'guest_number': guest_number,
                          'guest_consumption': guest_consumption,
                          'list': l})


def add_score(request):
    pass
