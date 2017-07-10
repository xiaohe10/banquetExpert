import urllib.parse

from datetime import timedelta

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.utils import timezone
from django.http import HttpResponse

from ..utils.decorator import validate_args, validate_staff_token
from ..models import Guest, Staff, Order


@validate_args({
    'phone': forms.CharField(11),
    'password': forms.CharField(min_length=1, max_length=32),
})
def login(request, phone, password):
    """登录，返回员工令牌(不更新)

    :param phone: 手机号(11位, 必传)
    :param password: 密码(md5加密结果, 32位, 必传)
    :return token: 员工token
    """

    try:
        staff = Staff.objects.get(phone=phone)
    except ObjectDoesNotExist:
        return HttpResponse('不存在该员工')
    else:
        if not staff.is_enabled:
            return HttpResponse('不存在该员工')
        if staff.status == 0:
            return HttpResponse('员工待审核')
        if staff.password != password:
            return HttpResponse('密码错误')
        return HttpResponse(staff.token)


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'phone': forms.CharField(max_length=11, required=False),
})
@validate_staff_token()
def get_profile(request, token, phone=None):
    """获取客户档案详情(根据电话)

    :param token: 令牌(必传)
    :param phone: 电话
    :return:
        guest_id: 顾客ID
        phone: 电话
        name: 名称
        gender: 性别, 0: 保密, 1: 男, 2: 女
        birthday: 生日
        birthday_type: 生日类型，0:阳历，1:农历
        guest_type: 顾客类型
        like: 喜好
        dislike: 忌讳
        special_day: 特殊
        personal_need: 个性化需求
        status: 客户状态, 1: 活跃, 2: 沉睡, 3: 流失, 4: 无订单
        all_order_number: 历史所有有效订单数
        day60_order_number: 最近60天订单数
        all_consumption: 所有有效消费
        day60_consumption: 最近60天消费金额
    """

    hotel = request.staff.hotel

    try:
        guest = Guest.objects.get(phone=phone, hotel=hotel)
    except ObjectDoesNotExist:
        return HttpResponse('err_4', '客户不存在')

    # 近60天
    day60 = timezone.now() - timedelta(days=60)
    # 全部订单
    orders = Order.objects.filter(
        branch__hotel=hotel, contact=guest.phone, status=2)

    all_consumption, day60_consumption = 0, 0
    qs = orders.values('contact').annotate(sum=Sum('consumption')). \
        order_by('contact')
    if qs:
        all_consumption = qs[0]['sum']
    qs = orders.filter(finish_time__gte=day60).values('contact').annotate(
        sum=Sum('consumption')).order_by('contact')
    if qs:
        day60_consumption = qs[0]['sum']

    d = {'guest_id': guest.id,
         'name': guest.name,
         'phone': guest.phone,
         'gender': guest.gender,
         'birthday': guest.birthday,
         'birthday_type': guest.birthday_type,
         'guest_type': guest.type,
         'like': guest.like,
         'dislike': guest.dislike,
         'special_day': guest.special_day,
         'personal_need': guest.personal_need,
         'all_order_number': orders.count(),
         'day60_order_number': orders.filter(finish_time__gte=day60).count(),
         'all_consumption': all_consumption,
         'day60_consumption': day60_consumption}

    # 会员价值分类的最小区间
    min_day = timezone.now() - timedelta(days=hotel.min_vip_category)
    # 会员价值分类的最大区间
    max_day = timezone.now() - timedelta(days=hotel.max_vip_category)

    if Order.objects.filter(
            branch__hotel=hotel, contact=guest.phone, status=2).count() == 0:
        d['status'] = 4
    elif Order.objects.filter(
            branch__hotel=hotel, contact=guest.phone, status=2,
            finish_time__gte=min_day).count() > 0:
        d['status'] = 1
    elif Order.objects.filter(
            branch__hotel=hotel, contact=guest.phone, status=2,
            finish_time__gte=max_day).count() > 0:
        d['status'] = 2
    else:
        d['status'] = 3

    return HttpResponse(urllib.parse.urlencode(d))


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'offset': forms.IntegerField(min_value=0, required=False),
    'limit': forms.IntegerField(min_value=0, required=False),
})
@validate_staff_token()
def get_call_records(request, token, branch_id, offset=0, limit=10):
    """获取电话处理列表

    :param token: 令牌(必传)
    :param branch_id: 门店ID(必传)
    :param offset: 起始值
    :param limit: 偏移量
    :return
        count: 数量
        list: 电话列表
    """

    qs = request.staff.dealt_call_records.all()
    c = qs.count()
    records = qs.order_by('-create_time')[offset:offset + limit]

    l = [{'phone': r.phone,
          'create_time': r.create_time} for r in records]
    return HttpResponse(urllib.parse.urlencode({'count': c, 'list': l}))


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'phone': forms.CharField(max_length=11, required=False)
})
@validate_staff_token()
def save_call_record(request, token, branch_id, phone):
    """保存电话来电记录

    :param token: 令牌(必传)
    :param phone: 电话
    :return OK/err_1
    """

    request.staff.dealt_call_records.create(phone=phone)
    return HttpResponse('OK')
