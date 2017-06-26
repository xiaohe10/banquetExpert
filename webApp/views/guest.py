from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, transaction

from ..utils.decorator import validate_args, validate_staff_token
from ..utils.response import corr_response, err_response
from ..models import Guest, Staff, ExternalChannel


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'search_key': forms.CharField(max_length=11, required=False),
    'guest_type': forms.CharField(required=False),
    'guest_from': forms.IntegerField(required=False),
    'offset': forms.IntegerField(min_value=0, required=False),
    'limit': forms.IntegerField(min_value=0, required=False),
    'order': forms.IntegerField(min_value=0, max_value=3, required=False),
})
@validate_staff_token()
def get_guests(request, token, offset=0, limit=10, order=1, **kwargs):
    """获取客户列表(搜索)

    :param token: 令牌(必传)
    :param offset: 起始值
    :param limit: 偏移量
    :param order: 排序方式: 0: 最近就餐，1: 总预定桌数，2: 人均消费，3: 消费频度，默认0
    :param kwargs:
        search_key: 搜索关键字, 姓名或手机号
        guest_type: 客户类型
        guest_from: 获客渠道
    :return:
    """

    c = Guest.objects.count()
    guests = Guest.objects.all()

    l = [{'guest_id': guest.id,
          'name': guest.name,
          'birthday': guest.birthday,
          'birthday_type': guest.birthday_type,
          'guest_type': guest.type,
          'like': guest.like,
          'dislike': guest.dislike,
          'special_day': guest.special_day,
          'personal_need': guest.personal_need,
          'status': 0} for guest in guests]

    # todo 客户状态定义和查询结果排序

    return corr_response({'count': c, 'list': l})


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32)
})
@validate_staff_token()
def get_channels(request, token):
    """获取客户销售来源

    :param token: 令牌
    :return:
        internal_channel: 内部销售
            id: ID
            name: 名称
        external_channel: 外部销售
            id: ID
            name: 名称
    """

    in_channels = Staff.objects.exclude(guest_channel=0)
    list1 = [{'id': channel.id,
              'name': channel.name} for channel in in_channels]

    ex_channels = ExternalChannel.objects.all()
    list2 = [{'id': channel.id,
              'name': channel.name} for channel in ex_channels]

    return corr_response({'internal_channel': list1, 'external_channel': list2})


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
})
@validate_staff_token()
def get_profile_general(request, token):
    pass


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'guest_id': forms.IntegerField(required=False),
    'phone': forms.CharField(required=False),
})
@validate_staff_token()
def get_profile(request, token, guest_id=None, phone=None):
    """获取客户档案详情(根据ID或电话)

    :param token: 令牌(必传)
    :param guest_id: 顾客ID
    :param phone: 电话
    :return:
        guest_id: 顾客ID
        name: 名称
        birthday: 生日
        birthday_type: 生日类型，0:阳历，1:农历
        guest_type: 顾客类型
        like: 喜好
        dislike: 忌讳
        special_day: 特殊
        personal_need: 个性化需求
        status: 客户状态, 0: 活跃, 1: 沉睡, 2: 流失, 3: 无订单
        all_order_number: 历史所有有效订单数
        day60_order_number: 最近60天订单数
        all_consumption: 所有有效消费
        day60_consumption: 最近60天消费金额
    """

    if guest_id:
        try:
            guest = Guest.objects.get(id=guest_id)
        except ObjectDoesNotExist:
            return corr_response()
    elif phone:
        try:
            guest = Guest.objects.get(phone=phone)
        except ObjectDoesNotExist:
            return corr_response()
    else:
        return err_response('err_1', '参数不正确（缺少参数或者不符合格式）')

    d = {'guest_id': guest.id,
         'name': guest.name,
         'birthday': guest.birthday,
         'birthday_type': guest.birthday_type,
         'guest_type': guest.type,
         'like': guest.like,
         'dislike': guest.dislike,
         'special_day': guest.special_day,
         'personal_need': guest.personal_need,
         'status': 0,
         'all_order_number': 0,
         'day60_order_number':0,
         'all_consumption': 0,
         'day60_consumption': 0}

    # todo 客户状态定义和消费金额统计

    return corr_response(d)


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'phone': forms.CharField(max_length=11),
    'name': forms.CharField(max_length=20),
    'guest_type': forms.CharField(max_length=10, required=False),
    'birthday': forms.DateField(required=False),
    'birthday_type': forms.IntegerField(
        min_value=0, max_value=1, required=False),
    'like': forms.CharField(max_length=100, required=False),
    'dislike': forms.CharField(max_length=100, required=False),
    'special_day': forms.CharField(max_length=20, required=False),
    'personal_need': forms.CharField(max_length=100, required=False)
})
@validate_staff_token()
def add_profile(request, token, phone, name, **kwargs):

    if Guest.objects.filter(phone=phone).exists():
        return err_response('err_2', '该客户已经存在')

    guest_keys = ('guest_type', 'birthday', 'birthday_type', 'like', 'dislike',
                  'special_day', 'personal_need')
    with transaction.atomic():
        try:
            guest = Guest(phone=phone, name=name)
            for k in guest_keys:
                if k in kwargs:
                    setattr(guest, k, kwargs[k])
            guest.save()
            return corr_response({'guest_id': guest.id})
        except IntegrityError:
            return err_response('err_4', '服务器创建员工错误')


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'phone': forms.CharField(max_length=11),
    'name': forms.CharField(max_length=20, required=False),
    'guest_type': forms.CharField(max_length=10, required=False),
    'birthday': forms.DateField(required=False),
    'birthday_type': forms.IntegerField(
        min_value=0, max_value=1, required=False),
    'like': forms.CharField(max_length=100, required=False),
    'dislike': forms.CharField(max_length=100, required=False),
    'special_day': forms.CharField(max_length=20, required=False),
    'personal_need': forms.CharField(max_length=100, required=False)
})
@validate_staff_token()
def modify_profile(request, token, phone, **kwargs):
    try:
        guest = Guest.objects.get(phone=phone)
    except ObjectDoesNotExist:
        return err_response('err_2', '客户档案不存在')

    guest_keys = ('guest_type', 'birthday', 'birthday_type', 'like', 'dislike',
                  'special_day', 'personal_need')

    for k in guest_keys:
        if k in kwargs:
            setattr(guest, k, kwargs[k])
    guest.save()
    return corr_response({'guest_id': guest.id})
