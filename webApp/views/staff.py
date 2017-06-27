import os
import time

from datetime import timedelta
from PIL import Image
from django import forms
from django.db import IntegrityError, transaction
from django.db.models import Q, Sum
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator

from ..utils.decorator import validate_args, validate_staff_token
from ..utils.response import corr_response, err_response
from ..models import Staff, Hotel, Order, Guest,\
    ValidationCode as ValidationCodeModel


@validate_args({
    'phone': forms.CharField(validators=[RegexValidator(regex=r'^[0-9]{11}$')]),
})
def get_validation_code(request, phone):
    """获取短信验证码

    :param phone:
    :return:
    """

    code = ValidationCodeModel.generate(phone)
    if code:
        # 调用第三方短信平台给手机号发短信
        # todo
        # send_message(phone_number, code)
        return corr_response()
    else:
        return err_response('err_2', '接口访问频率限制')


@validate_args({
    'phone': forms.CharField(validators=[RegexValidator(regex=r'^[0-9]{11}$')]),
    'password': forms.CharField(min_length=1, max_length=32),
    'validation_code': forms.CharField(min_length=6, max_length=6),
    'staff_number': forms.CharField(
        min_length=1, max_length=20, required=False),
    'name': forms.CharField(min_length=1, max_length=20),
    'gender': forms.IntegerField(min_value=0, max_value=2, required=False),
    'position': forms.CharField(max_length=20),
    'id_number': forms.CharField(min_length=18, max_length=18),
    'hotel_id': forms.IntegerField(),
})
def register(request, phone, password, validation_code, hotel_id, **kwargs):
    """员工注册

    :param phone: 手机号(必传)
    :param password: 密码(必传)
    :param validation_code: 验证码(必传)
    :param hotel_id: 酒店ID(必传)
    :param kwargs:
        staff_number: 员工编号
        name: 姓名(必传)
        gender: 性别, 0: 保密, 1: 男, 2: 女, 默认为0
        position: 职位(必传)
        id_number: 身份证号(必传)
    :return 200
    """

    try:
        hotel = Hotel.enabled_objects.get(id=hotel_id)
    except Hotel.DoesNotExist:
        return err_response('err_4', '酒店不存在')

    if Staff.objects.filter(phone=phone).exists():
        return err_response('err_2', '该手机号已经注册过')

    if Staff.objects.filter(id_number=kwargs['id_number']).exists():
        return err_response('err_3', '身份证号已经注册过')

    if not ValidationCodeModel.verify(phone, validation_code):
        return err_response('err_6', '验证码错误或超时')

    staff_keys = ('staff_number', 'name', 'gender', 'position', 'id_number')
    with transaction.atomic():
        try:
            staff = Staff(phone=phone, password=password, hotel=hotel)
            staff.update_token()
            for k in staff_keys:
                if k in kwargs:
                    setattr(staff, k, kwargs[k])
            staff.save()
            return corr_response({'staff_id': staff.id})
        except IntegrityError:
            return err_response('err_5', '服务器创建员工错误')


@validate_args({
    'phone': forms.CharField(validators=[RegexValidator(regex=r'^[0-9]{11}$')]),
    'password': forms.CharField(min_length=1, max_length=32),
})
def login(request, phone, password):
    """更新并返回员工令牌

    :param phone: 手机号(11位, 必传)
    :param password: 密码(md5加密结果, 32位, 必传)
    :return token: 员工token
    """

    try:
        staff = Staff.objects.get(phone=phone)
    except Staff.DoesNotExist:
        return err_response('err_2', '不存在该用户')
    else:
        if not staff.is_enabled:
            return err_response('err_2', '不存在该用户')
        if staff.status == 0:
            return err_response('err_2', '不存在该用户')
        if staff.password != password:
            return err_response('err_3', '密码错误')
        staff.update_token()
        staff.save()
        return corr_response({'token': staff.token})


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'new_password': forms.CharField(min_length=1, max_length=32),
    'old_password': forms.CharField(min_length=1, max_length=32),
})
@validate_staff_token()
def modify_password(request, token, old_password, new_password):
    """修改密码

    :param token: 令牌(必传)
    :param old_password: 旧密码(md5加密结果, 32位, 必传)
    :param new_password: 新密码(md5加密结果, 32位, 必传)
    :return 200/403
    """

    if request.staff.password == old_password:
        request.staff.password = new_password
        return corr_response({'staff_id': request.staff.id})
    return err_response('err_3', '旧密码错误')


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'staff_id': forms.IntegerField(required=False),
})
@validate_staff_token()
def get_profile(request, token, staff_id=None):
    """获取员工信息

    :param token: 令牌(必传)
    :param staff_id: 员工ID
    :return:
        staff_id: ID
        staff_number: 员工编号
        name: 员工姓名
        icon: 员工头像
        gender: 性别
        position: 职位
        guest_channel: 所属获客渠道, 0:无, 1:高层管理, 2:预定员和迎宾, 3:客户经理
        description: 备注
        authority: 权限
        create_time: 创建时间
    """

    if staff_id:
        try:
            staff = Staff.enabled_objects.get(id=staff_id)
        except ObjectDoesNotExist:
            return err_response('err_2', '不存在该员工')
    else:
        staff = request.staff
    r = {'staff_id': staff.id,
         'staff_number': staff.staff_number,
         'name': staff.name,
         'icon': staff.icon,
         'gender': staff.gender,
         'position': staff.position,
         'guest_channel': staff.guest_channel,
         'description': staff.description,
         'authority': staff.authority,
         'create_time': staff.create_time}
    return corr_response(r)


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'staff_number': forms.CharField(
        min_length=1, max_length=20, required=False),
    'name': forms.CharField(min_length=1, max_length=20, required=False),
    'gender': forms.IntegerField(min_value=0, max_value=2, required=False),
    'position': forms.CharField(max_length=20, required=False),
    'guest_channel': forms.IntegerField(
        min_value=0, max_value=3, required=False),
    'description': forms.CharField(max_length=100, required=False),
    'authority': forms.CharField(max_length=20, required=False),
})
@validate_staff_token()
def modify_profile(request, token, **kwargs):
    """修改员工信息

    :param token: 令牌(必传)
    :param kwargs:
        staff_number: 员工编号
        gender: 性别
        position: 职位
        guest_channel: 所属获客渠道, 0:无, 1:高层管理, 2:预定员和迎宾, 3:客户经理
        description: 备注
        authority: 权限
        icon: 头像, [file]格式
    :return: 200
    """

    staff_keys = ('staff_number', 'gender', 'position', 'guest_channel',
                  'description', 'authority')
    for k in staff_keys:
        if k in kwargs:
            setattr(request.staff, k, kwargs[k])

    # 修改头像
    if 'icon' in request.FILES:
        icon = request.FILES['icon']

        icon_time = timezone.now().strftime('%H%M%S%f')
        icon_tail = str(icon).split('.')[-1]
        dir_name = 'uploaded/icon/staff/%d/' % request.staff.id
        os.makedirs(dir_name, exist_ok=True)
        file_name = dir_name + '%s.%s' % (icon_time, icon_tail)
        try:
            img = Image.open(icon)
            img.save(file_name, quality=90)
        except OSError:
            return err_response('err4', '图片为空或图片格式错误')

        # 删除旧文件, 保存新的文件路径
        if request.staff.icon:
            try:
                os.remove(request.staff.icon)
            except OSError:
                pass
        request.staff.icon = file_name

    request.staff.save()
    return corr_response()


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
})
@validate_staff_token()
def get_hotel(request, token):
    """获取员工所在酒店信息

    :param token: 令牌(必传)
    :return:
        hotel_id: ID
        name: 名称
        icon: 头像
        branches_count: 门店数
        owner_name: 法人代表
        create_time: 创建时间
    """

    hotel = request.staff.hotel

    d = {'hotel_id': hotel.id,
         'name': hotel.name,
         'icon': hotel.icon,
         'branches_count': hotel.branches.count(),
         'owner_name': hotel.owner_name,
         'create_time': hotel.create_time}
    return corr_response(d)


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'offset': forms.IntegerField(min_value=0, required=False),
    'limit': forms.IntegerField(min_value=0, required=False),
    'order': forms.IntegerField(min_value=0, max_value=3, required=False),
})
@validate_staff_token()
def get_branches(request, token, offset=0, limit=10, order=1):
    """获取员工所在酒店的门店列表

    :param token: 令牌(必传)
    :param offset: 起始值
    :param limit: 偏移量
    :param order: 排序方式
        0: 注册时间升序
        1: 注册时间降序（默认值）
        2: 名称升序
        3: 名称降序
    :return:
        count: 门店总数
        list: 门店列表
            branch_id: ID
            name: 名称
            icon: 头像
            province: 省
            city: 市
            county: 区/县
            address: 详细地址
            hotel_name: 所属酒店名
            manager_name: 店长名字
            create_time: 创建时间
    """
    ORDERS = ('create_time', '-create_time', 'name', '-name')

    c = request.staff.hotel.branches.filter(is_enabled=True).count()
    branches = request.staff.hotel.branches.filter(is_enabled=True).order_by(
        ORDERS[order])[offset:offset + limit]

    l = [{'branch_id': b.id,
          'name': b.name,
          'icon': b.icon,
          'province': b.province,
          'city': b.city,
          'county': b.county,
          'address': b.address,
          'hotel_name': b.hotel.name,
          'manager_name': b.manager.name,
          'create_time': b.create_time} for b in branches]
    return corr_response({'count': c, 'list': l})


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'search_key': forms.CharField(max_length=11, required=False),
    'status': forms.IntegerField(min_value=0, max_value=3, required=False),
    'offset': forms.IntegerField(min_value=0, required=False),
    'limit': forms.IntegerField(min_value=0, required=False),
})
@validate_staff_token()
def get_guests(request, token, offset=0, limit=10, order=0, **kwargs):
    """获取客户列表(搜索)

    :param token: 令牌(必传)
    :param offset: 起始值
    :param limit: 偏移量
    :param kwargs:
        search_key: 搜索关键字, 姓名或手机号
        status: 客户类型, 0: 活跃, 1: 沉睡, 2: 流失, 3: 无订单
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

    qs = Guest.objects.filter(hotel=hotel, internal_channel=request.staff)

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
                values_list("contact", flat=True).distinct()
            qs = qs.filter(Q(phone__in=phones))
        # 沉睡客户
        elif status == 1:
            phones = Order.objects.filter(
                branch__hotel=hotel, status=2, finish_time__lt=min_day,
                finish_time__gte=max_day).values_list(
                "contact", flat=True).distinct()
            qs = qs.filter(Q(phone__in=phones))
        # 流失客户
        elif status == 2:
            phones = Order.objects.filter(
                branch__hotel=hotel, status=2, finish_time__lt=max_day). \
                values_list("contact", flat=True).distinct()
            qs = qs.filter(Q(phone__in=phones))
        # 无订单客户
        else:
            phones = Order.objects.filter(
                branch__hotel=hotel, status=2).values_list(
                "contact", flat=True).distinct()
            qs = qs.exclude(Q(phone__in=phones))

    c = qs.count()
    guests = qs[offset:offset + limit]

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
    'token': forms.CharField(min_length=32, max_length=32),
})
@validate_staff_token()
def get_guest_statistic(request, token):
    """获取员工的客户统计

    :param token:
    :return:
        all_guest_number: 所有客户数量
        active_guest_number: 活跃客户数量
        sleep_guest_number: 沉睡客户数量
        lost_guest_number: 流失客户数量
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
    active_guest_number = Guest.objects.filter(
        hotel=hotel, internal_channel=request.staff, phone__in=phones).count()

    # 沉睡客户数量
    phones = Order.objects.filter(
        branch__hotel=hotel, status=2, finish_time__lt=min_day,
        finish_time__gte=max_day).values_list("contact", flat=True)
    sleep_guest_number = Guest.objects.filter(
        hotel=hotel, internal_channel=request.staff, phone__in=phones).count()

    # 流失客户数量
    phones = Order.objects.filter(
        branch__hotel=hotel, status=2, finish_time__lt=max_day). \
        values_list("contact", flat=True)
    lost_guest_number = Guest.objects.filter(
        hotel=hotel, internal_channel=request.staff, phone__in=phones).count()

    d = {'all_guest_number': Guest.objects.all().count(),
         'active_guest_number': active_guest_number,
         'sleep_guest_number': sleep_guest_number,
         'lost_guest_number': lost_guest_number}

    return corr_response(d)
