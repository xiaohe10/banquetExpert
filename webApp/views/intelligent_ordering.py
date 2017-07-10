from datetime import timedelta

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from django.db import IntegrityError, transaction
from django.db.models import Q, Sum
from django.utils import timezone
from django.http import HttpResponse

from ..utils.decorator import validate_args, validate_staff_token
from ..models import Guest, Staff, ExternalChannel, Order, Desk


def login(request, phone, password):
    """登录，返回员工令牌(不更新)

    :param phone: 手机号(11位, 必传)
    :param password: 密码(md5加密结果, 32位, 必传)
    :return token: 员工token
    """

    try:
        staff = Staff.objects.get(phone=phone)
    except Staff.DoesNotExist:
        return HttpResponse('err_2', '不存在该用户')
    else:
        if not staff.is_enabled:
            return HttpResponse('err_2', '不存在该用户')
        if staff.status == 0:
            return HttpResponse('err_2', '不存在该用户')
        if staff.password != password:
            return HttpResponse('err_3', '密码错误')
        staff.save()
        return HttpResponse({'token': staff.token})
