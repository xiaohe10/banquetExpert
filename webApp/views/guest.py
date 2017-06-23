from django import forms
from django.core.exceptions import ObjectDoesNotExist

from ..utils.decorator import validate_args, validate_staff_token
from ..utils.response import corr_response, err_response
from ..models import Guest


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'search_key': forms.CharField(max_length=11, required=False),
    'guest_type': forms.CharField(required=False),
    'guest_from': forms.IntegerField(required=False),
})
@validate_staff_token()
def get_guests(request, token, search_key, guest_type, guest_from):
    """获取客户列表(搜索)

    :param token: 令牌(必传)
    :param search_key: 搜索关键字, 姓名或手机号
    :param guest_type: 客户类型
    :param guest_from: 获客渠道
    :return:
    """
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

