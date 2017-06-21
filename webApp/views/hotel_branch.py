import json

from django import forms
from django.core.exceptions import ObjectDoesNotExist

from ..utils.decorator import validate_args, validate_staff_token
from ..utils.response import corr_response, err_response
from ..models import HotelBranch, Area, Desk, Order


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'branch_id': forms.IntegerField(),
})
@validate_staff_token()
def get_profile(request, token, branch_id):
    """获取酒店门店详情

    :param token: 令牌(必传)
    :param branch_id: 门店ID(必传)
    :return
        name: 名称
        icon: 头像
        pictures: 图片(最多5张，数组)
        province: 省
        city: 市
        county: 区/县
        address: 详细地址
        meal_period: 餐段设置(键值对)
        facility: 设施(数组)
        pay_card: 可以刷哪些卡(数组)
        phone: 联系电话(数组)
        cuisine: 菜系(键值对)
        hotel_name: 所属酒店名
        manager_name: 店长名字
        create_time: 创建时间
    """

    try:
        branch = HotelBranch.enabled_objects.get(id=branch_id)
    except ObjectDoesNotExist:
        return err_response('err_4', '门店不存在')

    # 只能查看自己酒店的门店
    if branch.hotel != request.staff.hotel:
        return err_response('err_2', '权限错误')

    d = {'branch_id': branch.id,
         'name': branch.name,
         'icon': branch.icon,
         'pictures': json.loads(branch.pictures) if branch.pictures else '',
         'province': branch.province,
         'city': branch.city,
         'county': branch.county,
         'address': branch.address,
         'meal_period': json.loads(branch.meal_period)
         if branch.meal_period else '',
         'facility': json.loads(branch.facility) if branch.facility else '',
         'pay_card': json.loads(branch.pay_card) if branch.pay_card else '',
         'phone': json.loads(branch.phone) if branch.phone else '',
         'cuisine': json.loads(branch.cuisine) if branch.cuisine else '',
         'hotel_name': branch.hotel.name,
         'manager_name': branch.manager.name,
         'create_time': branch.create_time}
    return corr_response(d)


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'branch_id': forms.IntegerField(),
    'order': forms.IntegerField(min_value=0, max_value=3, required=False),
})
@validate_staff_token()
def get_areas(request, token, branch_id, order=2):
    """获取门店区域列表

    :param token: 令牌(必传)
    :param branch_id: 门店ID(必传)
    :param order: 排序方式
        0: 注册时间升序
        1: 注册时间降序（默认值）
        2: 名称升序
        3: 名称降序
    :return:
        count: 区域数
        list:
            area_id: 区域ID
            name: 区域名
            order: 排序
            create_time: 创建时间
    """
    ORDERS = ('create_time', '-create_time', 'name', '-name')

    try:
        branch = HotelBranch.enabled_objects.get(id=branch_id)
    except ObjectDoesNotExist:
        return err_response('err_4', '门店不存在')

    # 只能查看自己酒店的门店
    if branch.hotel != request.staff.hotel:
        return err_response('err_2', '权限错误')

    c = branch.areas.filter(is_enabled=True).count()
    areas = branch.areas.filter(is_enabled=True).order_by(ORDERS[order])

    l = [{'area_id': area.id,
          'name': area.name,
          'order': area.order,
          'create_time': area.create_time} for area in areas]

    return corr_response({'count': c, 'list': l})


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'branch_id': forms.IntegerField(),
    'area_id': forms.IntegerField(required=False),
    'order': forms.IntegerField(min_value=0, max_value=3, required=False),
    'date': forms.DateField(),
    'dinner_period': forms.IntegerField(),
})
@validate_staff_token()
def get_desks(request, token, branch_id, date, dinner_period, area_id=None,
              order=2):
    """获取门店某一天某餐段的桌位使用情况列表

    :param token: 令牌(必传)
    :param branch_id: 门店ID(必传)
    :param date: 日期, 例: 2017-05-12(必传)
    :param dinner_period: 餐段, 0:午餐, 1:晚餐, 2:夜宵(必传)
    :param area_id: 用餐区域ID
    :param order: 排序方式
        0: 注册时间升序
        1: 注册时间降序
        2: 房间号升序（默认值）
        3: 房间号降序
    :return:
        count: 桌位数
        list:
            desk_id: 桌位ID
            number: 桌位编号
            order: 排序
            area_name: 用餐区域名称
            min_guest_num: 可容纳最小人数
            max_guest_num: 可容纳最大人数
            status: 桌位使用状态, 0: 空闲, 1: 预定中, 2: 用餐中
    """
    ORDERS = ('create_time', '-create_time', 'number', '-number')

    try:
        branch = HotelBranch.enabled_objects.get(id=branch_id)
    except ObjectDoesNotExist:
        return err_response('err_4', '门店不存在')

    # 只能查看自己酒店的门店
    if branch.hotel != request.staff.hotel:
        return err_response('err_2', '权限错误')

    if area_id is None:
        c = Desk.enabled_objects.filter(area__branch=branch).count()
        ds = Desk.enabled_objects.filter(
            area__branch=branch).order_by(ORDERS[order])
    else:
        try:
            area = Area.enabled_objects.get(id=area_id)
        except ObjectDoesNotExist:
            return err_response('err_5', '餐厅区域不存在')

        c = area.desks.filter(is_enabled=True).count()
        ds = area.desks.filter(is_enabled=True).order_by(ORDERS[order])

    l = []
    for desk in ds:
        d = {'desk_id': desk.id,
             'number': desk.number,
             'order': desk.order,
             'area_name': desk.area.name,
             'min_guest_num': desk.min_guest_num,
             'max_guest_num': desk.max_guest_num}

        # 判断桌位在查询日和查询餐段的状态
        desk_id = '$' + str(desk.id) + '$'
        if Order.objects.filter(
                dinner_period=dinner_period, dinner_date=date, status=0,
                desks__icontains=desk_id). \
                exists():
            d['status'] = 1
        elif Order.objects.filter(
                dinner_period=dinner_period, dinner_date=date, status=1,
                desks__icontains=desk_id). \
                exists():
            d['status'] = 2
        else:
            d['status'] = 0
        l.append(d)

    return corr_response({'count': c, 'list': l})
