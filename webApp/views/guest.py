from django import forms
from django.core.exceptions import ObjectDoesNotExist

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
          'personal_need': guest.personal_need} for guest in guests]
    # todo

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
def get_profile_general(request):
    pass


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'guest_id': forms.IntegerField(required=False),
    'phone': forms.CharField(required=False),
})
@validate_staff_token()
def get_profile(request, token, guest_id=None, phone=None):
    """获取客户档案详情

    :param token: 令牌(必传)
    :param guest_id: 顾客ID
    :param phone: 电话
    :return:
    """
    pass


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
})
@validate_staff_token()
def add_profile(request):
    pass


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
})
@validate_staff_token()
def modify_profile(request):
    pass
