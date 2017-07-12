import os
import json
import datetime

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
from ..utils.http import send_message
from ..models import Staff, Hotel, Order, Guest, Desk, \
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
        # 调用第三方短信平台给手机号发短信验证码
        result = send_message(phone, code)
        if result == 1:
            return corr_response()
        else:
            return err_response('err_3', '发送短信失败')
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

    if Staff.objects.filter(phone=phone).count() > 0:
        return err_response('err_2', '该手机号已经注册过')

    if Staff.objects.filter(id_number=kwargs['id_number']).count() > 0:
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
    """登录，更新并返回员工令牌

    :param phone: 手机号(11位, 必传)
    :param password: 密码(md5加密结果, 32位, 必传)
    :return token: 员工token
    """

    try:
        staff = Staff.objects.get(phone=phone)
    except Staff.DoesNotExist:
        return err_response('err_2', '员工不存在')
    else:
        if not staff.is_enabled:
            return err_response('err_2', '员工不存在')
        if staff.status == 0:
            return err_response('err_2', '员工待审核')
        if staff.password != password:
            return err_response('err_3', '密码错误')
        staff.update_token()
        staff.save()
        # 将token放入session
        request.session['token'] = staff.token
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
    'description': forms.CharField(max_length=200, required=False),
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
            return err_response('err_4', '图片为空或图片格式错误')

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
    'status': forms.IntegerField(min_value=0, max_value=4, required=False),
    'offset': forms.IntegerField(min_value=0, required=False),
    'limit': forms.IntegerField(min_value=0, required=False),
})
@validate_staff_token()
def get_guests(request, token, offset=0, limit=10, **kwargs):
    """获取客户列表(搜索)

    :param token: 令牌(必传)
    :param offset: 起始值
    :param limit: 偏移量
    :param kwargs:
        search_key: 搜索关键字, 姓名或手机号
        status: 客户类型, 0: 全部, 1: 活跃, 2: 沉睡, 3: 流失, 4: 无订单
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
            unit: 单位
            position: 职位
            status: 客户状态, 1: 活跃, 2: 沉睡, 3: 流失, 4: 无订单
            desk_number: 消费总桌数
            person_consumption: 人均消费
            order_per_month: 消费频度, 单/月
            last_consumption: 上次消费日期
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
        if status == 1:
            phones = Order.objects.filter(
                branch__hotel=hotel, status=2, finish_time__gte=min_day). \
                values_list("contact", flat=True).distinct()
            qs = qs.filter(Q(phone__in=phones))
        # 沉睡客户
        elif status == 2:
            phones = Order.objects.filter(
                branch__hotel=hotel, status=2, finish_time__lt=min_day,
                finish_time__gte=max_day).values_list(
                "contact", flat=True).distinct()
            qs = qs.filter(Q(phone__in=phones))
        # 流失客户
        elif status == 3:
            phones = Order.objects.filter(
                branch__hotel=hotel, status=2, finish_time__lt=max_day). \
                values_list("contact", flat=True).distinct()
            qs = qs.filter(Q(phone__in=phones))
        # 无订单客户
        elif status == 4:
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
             'personal_need': guest.personal_need,
             'unit': guest.unit,
             'position': guest.position,
             'desk_number': guest.desk_number,
             'person_consumption': guest.person_consumption,
             'order_per_month': guest.order_per_month,
             'last_consumption': ''}

        # 最后用餐时间
        qs = Order.objects.filter(
            contact=guest.phone, branch__hotel=hotel, status=2). \
            order_by('-dinner_date')
        if qs:
            d['last_consumption'] = qs[0].dinner_date

        if (status is None) or (status == 0):
            if Order.objects.filter(
                    branch__hotel=hotel, contact=guest.phone, status=2).\
                    count() == 0:
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


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'date_from': forms.DateField(required=False),
    'date_to': forms.DateField(required=False),
    'order_date': forms.DateField(required=False),
    'dinner_date': forms.DateField(required=False),
    'dinner_time': forms.TimeField(required=False),
    'dinner_period': forms.IntegerField(
        min_value=0, max_value=2, required=False),
    'status': forms.IntegerField(min_value=0, max_value=2, required=False),
    'search_key': forms.CharField(min_length=1, max_length=20, required=False),
    'desk_id': forms.IntegerField(required=False),
    'offset': forms.IntegerField(min_value=0, required=False),
    'limit': forms.IntegerField(min_value=0, required=False),
    'order': forms.IntegerField(min_value=0, max_value=1, required=False),
})
@validate_staff_token()
def search_orders(request, token, status=0, offset=0, limit=10, order=1,
                  **kwargs):
    """搜索员工自己的订单列表

    :param token: 令牌(必传)
    :param status: 订单状态, 0: 进行中(默认), 1: 已完成, 2: 已撤单
    :param offset: 起始值
    :param limit: 偏移量
    :param order: 排序方式
        0: 注册时间升序
        1: 注册时间降序（默认值）
    :param kwargs:
        search_key: 关键字
        date_from: 订单创建日期起始时间
        date_to: 订单创建日期终止时间
        order_date: 下单日期
        dinner_date: 预定用餐日期
        dinner_time: 预定用餐时间
        dinner_period: 餐段, 0: 午餐, 1: 晚餐, 2: 夜宵
        desk_id: 桌位ID
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
            gender: 性别
            guest_number: 客人数量
            table_count: 餐桌数
            staff_description: 员工备注
            desks: 桌位, 数组, [{"desk_id":1,"number":"110"}, ...]
    """
    ORDERS = ('create_time', '-create_time')

    hotel = request.staff.hotel

    if status == 0:
        rs = Order.objects.filter(Q(branch__hotel=hotel, status__in=[0, 1],
                                    internal_channel=request.staff))
    elif status == 1:
        rs = Order.objects.filter(Q(branch__hotel=hotel, status=2,
                                    internal_channel=request.staff))
    else:
        rs = Order.objects.filter(Q(branch__hotel=hotel, status=3,
                                    internal_channel=request.staff))

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

    if 'desk_id' in kwargs:
        desk_id = '$' + str(kwargs['desk_id']) + '$'
        rs = rs.filter(Q(desks__icontains=desk_id))

    c = rs.count()
    orders = rs.order_by(ORDERS[order])[offset:offset + limit]

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
             'gender': r.gender,
             'table_count': r.table_count,
             'staff_description': r.staff_description,
             'internal_channel': r.internal_channel.name if
             r.internal_channel else '',
             'external_channel': r.external_channel.name if
             r.external_channel else '',
             'desks': []}

        desks_list = json.loads(r.desks)
        for desk in desks_list:
            desk_id = int(desk[1:-1])
            try:
                number = Desk.objects.get(id=desk_id).number
            except ObjectDoesNotExist:
                number = ''
            d['desks'].append({'desk_id': desk_id, 'number': number})

        l.append(d)

    return corr_response({'count': c,
                          'consumption': consumption,
                          'guest_number': guest_number,
                          'guest_consumption': guest_consumption,
                          'list': l})
