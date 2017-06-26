from datetime import timedelta

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from django.db import IntegrityError, transaction
from django.db.models import Q, Sum
from django.utils import timezone

from ..utils.decorator import validate_args, validate_staff_token
from ..utils.response import corr_response, err_response
from ..models import Guest, Staff, ExternalChannel, Order


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'search_key': forms.CharField(max_length=11, required=False),
    'status': forms.IntegerField(min_value=0, max_value=3, required=False),
    'internal_channel': forms.IntegerField(required=False),
    'external_channel': forms.IntegerField(required=False),
    'offset': forms.IntegerField(min_value=0, required=False),
    'limit': forms.IntegerField(min_value=0, required=False),
    'order': forms.IntegerField(min_value=0, max_value=3, required=False),
})
@validate_staff_token()
def get_guests(request, token, offset=0, limit=10, order=0, **kwargs):
    """获取客户列表(搜索)

    :param token: 令牌(必传)
    :param offset: 起始值
    :param limit: 偏移量
    :param order: 排序方式: 0: 最近就餐，1: 总预定桌数，2: 人均消费，3: 消费频度，默认0
    :param kwargs:
        search_key: 搜索关键字, 姓名或手机号
        status: 客户类型, 0: 活跃, 1: 沉睡, 2: 流失, 3: 无订单
        internal_channel: 内部销售渠道ID
        external_channel: 外部销售渠道ID
    :return:
        count: 客户数量
        list:
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
            status: 客户状态, 0: 活跃, 1: 沉睡, 2: 流失, 3: 无订单
    """

    hotel = request.staff.hotel

    # 会员价值分类的最小区间
    min_day = timezone.now() - timedelta(days=hotel.min_vip_category)
    # 会员价值分类的最大区间
    max_day = timezone.now() - timedelta(days=hotel.max_vip_category)

    qs = Guest.objects.filter(hotel=hotel)

    if 'search_key' in kwargs:
        search_key = kwargs['search_key']
        qs = qs.filter(Q(phone__icontains=search_key) |
                       Q(name__icontains=search_key))

    status = None
    if 'status' in kwargs:
        status = kwargs['status']

        # 活跃客户
        if status == 0:
            phones = Order.objects.filter(
                branch__hotel=hotel, status=2, finish_time__gte=min_day). \
                values_list("contact", flat=True)
        # 沉睡客户
        elif status == 1:
            phones = Order.objects.filter(
                branch__hotel=hotel, status=2, finish_time__lt=min_day,
                finish_time__gte=max_day).values_list("contact", flat=True)
        # 流失客户
        elif status == 2:
            phones = Order.objects.filter(
                branch__hotel=hotel, status=2, finish_time__lt=max_day). \
                values_list("contact", flat=True)
        # 无订单客户
        else:
            phones = Order.objects.filter(
                branch__hotel=hotel, status=2).values_list("contact", flat=True)

        qs = qs.filter(Q(phone__in=phones))

    if 'internal_channel' in kwargs:
        internal_channel = kwargs['internal_channel']
        try:
            in_channel = Staff.objects.filter(id=internal_channel)
        except ObjectDoesNotExist:
            return err_response('err_4', '内部销售渠道不存在')
        qs = qs.filter(Q(internal_channel=in_channel))

    if 'external_channel' in kwargs:
        external_channel = kwargs['external_channel']
        try:
            ex_channel = Staff.objects.filter(id=external_channel)
        except ObjectDoesNotExist:
            return err_response('err_4', '外部销售渠道不存在')
        qs = qs.filter(Q(external_channel=ex_channel))

    c = qs.count()
    guests = qs[offset:offset + limit]

    # todo 查询结果排序

    l = []
    for guest in guests:
        d = {'guest_id': guest.id,
             'phone': guest.phone,
             'name': guest.name,
             'gender': guest.gender,
             'birthday': guest.birthday,
             'birthday_type': guest.birthday_type,
             'guest_type': guest.type,
             'like': guest.like,
             'dislike': guest.dislike,
             'special_day': guest.special_day,
             'personal_need': guest.personal_need}

        if status is None:
            if Order.objects.filter(
                    branch__hotel=hotel, contact=guest.phone, status=2).\
                    count() == 0:
                d['status'] = 3
            elif Order.objects.filter(
                    branch__hotel=hotel, contact=guest.phone, status=2,
                    finish_time__gte=min_day).count() > 0:
                d['status'] = 0
            elif Order.objects.filter(
                    branch__hotel=hotel, contact=guest.phone, status=2,
                    finish_time__gte=max_day).count() > 0:
                d['status'] = 1
            else:
                d['status'] = 2
        else:
            d['status'] = status

        l.append(d)

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

    hotel = request.staff.hotel

    in_channels = Staff.objects.filter(hotel=hotel).exclude(guest_channel=0)
    list1 = [{'id': channel.id,
              'name': channel.name} for channel in in_channels]

    ex_channels = ExternalChannel.objects.filter(staff__hotel=hotel).all()
    list2 = [{'id': channel.id,
              'name': channel.name} for channel in ex_channels]

    return corr_response({'internal_channel': list1, 'external_channel': list2})


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
})
@validate_staff_token()
def get_profile_general(request, token):
    """获取客户概况

    :param token:
    :return:
        all_guest_number: 所有客户数量
        active_guest_number: 活跃客户数量
        sleep_guest_number: 沉睡客户数量
        lost_guest_number: 流失客户数量
        blank_guest_number: 无订单客户数量
        guest_from_manager: 客户来源：客户经理
        guest_from_order: 客户来源：预订台
        guest_from_outer: 客户来源：外部渠道
    """

    hotel = request.staff.hotel

    # 会员价值分类的最小区间
    min_day = timezone.now() - timedelta(days=hotel.min_vip_category)
    # 会员价值分类的最大区间
    max_day = timezone.now() - timedelta(days=hotel.max_vip_category)

    # 活跃客户数量
    phones = Order.objects.filter(
        branch__hotel=hotel, status=2, finish_time__gte=min_day).\
        values_list("contact", flat=True)
    active_guest_number = Guest.objects.filter(phone__in=phones).count()

    # 沉睡客户数量
    phones = Order.objects.filter(
        branch__hotel=hotel, status=2, finish_time__lt=min_day,
        finish_time__gte=max_day).values_list("contact", flat=True)
    sleep_guest_number = Guest.objects.filter(phone__in=phones).count()

    # 流失客户数量
    phones = Order.objects.filter(
        branch__hotel=hotel, status=2, finish_time__lt=max_day). \
        values_list("contact", flat=True)
    lost_guest_number = Guest.objects.filter(phone__in=phones).count()

    # 无订单客户数量
    phones = Order.objects.filter(
        branch__hotel=hotel, status=2).values_list("contact", flat=True)
    blank_guest_number = Guest.objects.exclude(phone__in=phones).count()

    d = {'all_guest_number': Guest.objects.all().count(),
         'active_guest_number': active_guest_number,
         'sleep_guest_number': sleep_guest_number,
         'lost_guest_number': lost_guest_number,
         'blank_guest_number': blank_guest_number,
         'guest_from_manager': Guest.objects.filter(
             internal_channel__guest_channel=3).count(),
         'guest_from_order': Guest.objects.filter(
             internal_channel__guest_channel=2).count(),
         'guest_from_outer': Guest.objects.exclude(
             external_channel=None).count()}

    return corr_response(d)


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
        status: 客户状态, 0: 活跃, 1: 沉睡, 2: 流失, 3: 无订单
        all_order_number: 历史所有有效订单数
        day60_order_number: 最近60天订单数
        all_consumption: 所有有效消费
        day60_consumption: 最近60天消费金额
    """

    hotel = request.staff.hotel

    if guest_id:
        try:
            guest = Guest.objects.get(id=guest_id, hotel=hotel)
        except ObjectDoesNotExist:
            return corr_response()
    elif phone:
        try:
            guest = Guest.objects.get(phone=phone, hotel=hotel)
        except ObjectDoesNotExist:
            return corr_response()
    else:
        return err_response('err_1', '参数不正确（缺少参数或者不符合格式）')

    # 近60天
    day60 = timezone.now() - timedelta(days=60)
    # 全部订单
    orders = Order.objects.filter(
        branch__hotel=hotel, contact=guest.phone, status=2)

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
         'all_consumption': orders.values('contact').annotate(
             sum=Sum('consumption')).order_by('-sum')[0]['sum'],
         'day60_consumption': orders.filter(finish_time__gte=day60).values(
             'contact').annotate(sum=Sum('consumption')).order_by(
             '-sum')[0]['sum']}

    # 会员价值分类的最小区间
    min_day = timezone.now() - timedelta(days=hotel.min_vip_category)
    # 会员价值分类的最大区间
    max_day = timezone.now() - timedelta(days=hotel.max_vip_category)

    if Order.objects.filter(
            branch__hotel=hotel, contact=guest.phone, status=2).count() == 0:
        d['status'] = 3
    elif Order.objects.filter(
            branch__hotel=hotel, contact=guest.phone, status=2,
            finish_time__gte=min_day).count() > 0:
        d['status'] = 0
    elif Order.objects.filter(
            branch__hotel=hotel, contact=guest.phone, status=2,
            finish_time__gte=max_day).count() > 0:
        d['status'] = 1
    else:
        d['status'] = 2

    return corr_response(d)


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'phone': forms.CharField(validators=[RegexValidator(regex=r'^[0-9]{11}$')]),
    'name': forms.CharField(max_length=20),
    'guest_type': forms.CharField(max_length=10, required=False),
    'gender': forms.IntegerField(min_value=0, max_value=2, required=False),
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
    """添加新的客户档案(谁添加的就是谁的客户)

    :param token: 令牌
    :param phone: 电话
    :param name: 姓名
    :param kwargs:
        guest_type: 客户类型
        gender: 性别, 0: 保密, 1: 男, 2: 女
        birthday: 生日
        birthday_type: 生日类型, 0: 阳历, 1: 阴历
        like: 喜好
        dis_like: 忌讳
        special_day: 纪念日
        personal_need: 个性化需求
    :return:
        guest_id: 顾客ID
    """

    hotel = request.staff.hotel

    if Guest.objects.filter(hotel=hotel, phone=phone).exists():
        return err_response('err_2', '该客户已经存在')

    guest_keys = ('guest_type', 'gender', 'birthday', 'birthday_type', 'like',
                  'dislike', 'special_day', 'personal_need')
    with transaction.atomic():
        try:
            guest = Guest(hotel=hotel, phone=phone, name=name,
                          internal_channel=request.staff)
            for k in guest_keys:
                if k in kwargs:
                    setattr(guest, k, kwargs[k])
            guest.save()
            return corr_response({'guest_id': guest.id})
        except IntegrityError as e:
            print(e)
            return err_response('err_4', '服务器创建员工错误')


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'phone': forms.CharField(max_length=11),
    'name': forms.CharField(max_length=20, required=False),
    'guest_type': forms.CharField(max_length=10, required=False),
    'gender': forms.IntegerField(min_value=0, max_value=2, required=False),
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
    """修改客户档案

    :param token: 令牌(必传)
    :param phone: 手机(必传，作为查询客户档案依据)
    :param kwargs:
        guest_type: 客户类型
        gender: 性别, 0: 保密, 1: 男, 2: 女
        birthday: 生日
        birthday_type: 生日类型, 0: 阳历, 1: 阴历
        like: 喜好
        dis_like: 忌讳
        special_day: 纪念日
        personal_need: 个性化需求
    :return:
    """

    hotel = request.staff.hotel
    try:
        guest = Guest.objects.get(hotel=hotel, phone=phone)
    except ObjectDoesNotExist:
        return err_response('err_2', '客户档案不存在')

    guest_keys = ('guest_type', 'gender', 'birthday', 'birthday_type', 'like',
                  'dislike', 'special_day', 'personal_need')

    for k in guest_keys:
        if k in kwargs:
            setattr(guest, k, kwargs[k])
    guest.save()
    return corr_response({'guest_id': guest.id})
