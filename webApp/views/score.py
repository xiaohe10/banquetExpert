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
from ..models import Staff, Hotel, Order, Guest, Desk, OrderScore


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
            total_score: 总分
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
             'total_score': r.order_score.total_score
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


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'score_id': forms.IntegerField()
})
def score_profile(request, token, score_id):
    """获取评分详情

    :param token: 令牌(必传)
    :param score_id: 评分ID(必传)

    """

    try:
        score = OrderScore.objects.get(id=score_id)
    except ObjectDoesNotExist:
        return err_response('err_4', '该评分不存在')

    # 读取评分项
    with open('data/personal_tailor.json') as json_file:
        json_data = json.loads(json_file)

    d = {'id': score.id,
         'total_score': score.total_score,
         'create_time': score.create_time}

    for item in json_data:
        item_key = item['item_key']
        item_need_picture = item['item_need_picture']
        # 根据该评分项是否需要照片, 来获取对象的照片地址
        if item_need_picture == 1:
            picture = item_key + '_picture'
            d[picture] = getattr(score, picture)
        own_score = item_key + '_score'
        checked_score = 'check_' + item_key + '_score'
        d[own_score] = getattr(score, own_score)
        d[checked_score] = getattr(score, checked_score)

    d1 = {'id': score.id,
          'door_card_picture': score.door_card_picture,
          'door_card_score': score.door_card_score,
          'check_door_card_score': score.check_door_card_score,
          'sand_table_picture': score.sand_table_picture,
          'sand_table_score': score.sand_table_score,
          'check_sand_table_score': score.check_sand_table_score,
          'welcome_screen_picture': score.welcome_screen_picture,
          'welcome_screen_score': score.welcome_screen_score,
          'check_welcome_screen_score': score.check_welcome_screen_score,
          'atmosphere_picture': score.atmosphere_picture,
          'atmosphere_score': score.atmosphere_score,
          'check_atmosphere_score': score.check_atmosphere_score,
          'group_photo_picture': score.group_photo_picture,
          'group_photo_score': score.group_photo_score,
          'check_group_photo_score': score.check_group_photo_score,
          'cup_picture': score.cup_picture,
          'cup_score': score.cup_score,
          'check_cup_score': score.check_cup_score,
          'brochure_picture': score.brochure_picture,
          'brochure_score': score.brochure_score,
          'check_brochure_score': score.check_brochure_score,
          'calendar_picture': score.calendar_picture,
          'calendar_score': score.calendar_score,
          'check_calendar_score': score.check_calendar_score,
          'honor_certificate_picture': score.honor_certificate_picture,
          'honor_certificate_score': score.honor_certificate_score,
          'check_honor_certificate_score': score.check_honor_certificate_score,
          'work_in_heart_picture': score.work_in_heart_picture,
          'work_in_heart_score': score.work_in_heart_score,
          'check_work_in_heart_score': score.check_work_in_heart_score,
          'innovation_picture': score.innovation_picture,
          'innovation_score': score.innovation_score,
          'check_innovation_score': score.check_innovation_score,
          'praise_letter_picture': score.praise_letter_picture,
          'praise_letter_score': score.praise_letter_score,
          'check_praise_letter_score': score.check_praise_letter_score,
          'friend_circle_picture': score.friend_circle_picture,
          'friend_circle_score': score.friend_circle_score,
          'check_friend_circle_score': score.check_friend_circle_score,
          'network_comment_picture': score.network_comment_picture,
          'network_comment_score': score.network_comment_score,
          'check_network_comment_score': score.check_network_comment_score,
          'single_table_transform_score': score.single_table_transform_score,
          'check_single_table_transform_score':
              score.check_single_table_transform_score,
          'multi_table_transform_score': score.multi_table_transform_score,
          'check_multi_table_transform_score':
              score.check_multi_table_transform_score,
          'total_score': score.total_score,
          'create_time': score.create_time}

    return corr_response(d)


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'order_id': forms.IntegerField(),
    'door_card_score': forms.IntegerField(),
    'sand_table_score': forms.IntegerField(),
    'welcome_screen_score': forms.IntegerField(),
    'atmosphere_score': forms.IntegerField(),
    'group_photo_score': forms.IntegerField(),
    'cup_score': forms.IntegerField(),
    'brochure_score': forms.IntegerField(),
    'calendar_score': forms.IntegerField(),
    'honor_certificate_score': forms.IntegerField(),
    'work_in_heart_score': forms.IntegerField(),
    'innovation_score': forms.IntegerField(),
    'praise_letter_score': forms.IntegerField(),
    'friend_circle_score': forms.IntegerField(),
    'network_comment_score': forms.IntegerField(),
    'single_table_transform_score': forms.IntegerField(),
    'multi_table_transform_score': forms.IntegerField(),
})
@validate_staff_token()
def submit_score(request, token, order_id, **kwargs):
    """增加私人订制评分

    :param token: 令牌(必传)
    :param order_id: 订单ID(必传)
    :param kwargs:
        door_card_score: 门牌
        sand_table_score: 沙盘
        welcome_screen_score: 欢迎屏
        atmosphere_score: 氛围
        group_photo_score: 拍合照
        cup_score: 烤杯子
        brochure_score: 小册子
        calendar_score: 台历
        honor_certificate_score: 荣誉证书
        work_in_heart_score: 用心工作
        innovation_score: 私人订制创新
        praise_letter_score: 表扬信
        friend_circle_score: 朋友圈评论
        network_comment_score: 网评
        single_table_transform_score: 单桌转化率
        multi_table_transform_score: 多桌转化率
    """

    try:
        order = Order.objects.get(id=order_id)
    except ObjectDoesNotExist:
        return err_response('err_4', '订单不存在')

    score_keys = ('door_card_score', 'sand_table_score', 'welcome_screen_score',
                  'atmosphere_score', 'group_photo_score', 'cup_score',
                  'brochure_score', 'calendar_score', 'honor_certificate_score',
                  'work_in_heart_score', 'innovation_score',
                  'praise_letter_score', 'friend_circle_score',
                  'network_comment_score', 'single_table_transform_score',
                  'multi_table_transform_score')

    with transaction.atomic():
        try:
            score = order.score.create(staff=request.staff)
            for k in score_keys:
                if k in kwargs:
                    setattr(score, k, kwargs[k])

            # todo 图片上传
            score.save()
            return corr_response({'score_id': score.id})
        except IntegrityError:
            return err_response('err_5', '服务器创建评分记录失败')


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'score_id': forms.IntegerField(),
    'check_door_card_score': forms.IntegerField(required=False),
    'check_sand_table_score': forms.IntegerField(required=False),
    'check_welcome_screen_score': forms.IntegerField(required=False),
    'check_atmosphere_score': forms.IntegerField(required=False),
    'check_group_photo_score': forms.IntegerField(required=False),
    'check_cup_score': forms.IntegerField(required=False),
    'check_brochure_score': forms.IntegerField(required=False),
    'check_calendar_score': forms.IntegerField(required=False),
    'check_honor_certificate_score': forms.IntegerField(required=False),
    'check_work_in_heart_score': forms.IntegerField(required=False),
    'check_innovation_score': forms.IntegerField(required=False),
    'check_praise_letter_score': forms.IntegerField(required=False),
    'check_friend_circle_score': forms.IntegerField(required=False),
    'check_network_comment_score': forms.IntegerField(required=False),
    'check_single_table_transform_score': forms.IntegerField(required=False),
    'check_multi_table_transform_score': forms.IntegerField(required=False),
})
@validate_staff_token()
def check_score(request, token, score_id, **kwargs):
    """审阅私人订制评分

    :param token: 令牌(必传)
    :param score_id: 评分ID(必传)
    :param kwargs:
        check_door_card_score: 门牌
        check_sand_table_score: 沙盘
        check_welcome_screen_score: 欢迎屏
        check_atmosphere_score: 氛围
        check_group_photo_score: 拍合照
        check_cup_score: 烤杯子
        check_brochure_score: 小册子
        check_calendar_score: 台历
        check_honor_certificate_score: 荣誉证书
        check_work_in_heart_score: 用心工作
        check_innovation_score: 私人订制创新
        check_praise_letter_score: 表扬信
        check_friend_circle_score: 朋友圈评论
        check_network_comment_score: 网评
        check_single_table_transform_score: 单桌转化率
        check_multi_table_transform_score: 多桌转化率
    """

    try:
        score = OrderScore.objects.get(id=score_id)
    except ObjectDoesNotExist:
        return err_response('err_4', '评分记录不存在')

    score_keys = ('check_door_card_score', 'check_sand_table_score',
                  'check_welcome_screen_score', 'check_atmosphere_score',
                  'check_group_photo_score', 'check_cup_score',
                  'check_brochure_score', 'check_calendar_score',
                  'check_honor_certificate_score', 'check_work_in_heart_score',
                  'check_innovation_score', 'check_praise_letter_score',
                  'check_friend_circle_score', 'check_network_comment_score',
                  'check_single_table_transform_score',
                  'check_multi_table_transform_score')

    for k in score_keys:
        if k in kwargs:
            setattr(score, k, kwargs[k])

    # 保存审阅人信息
    score.check_staff = request.staff
    score.modify_time = timezone.now()
    score.save()
    return corr_response()
