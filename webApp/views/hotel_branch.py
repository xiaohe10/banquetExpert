from django import forms
from django.core.exceptions import ObjectDoesNotExist

from ..utils.decorator import validate_args, validate_staff_token
from ..utils.response import corr_response, err_response
from ..models import HotelBranch, Order


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
        pictures: 图片(最多5张，json数组)
        province: 省
        city: 市
        county: 区/县
        address: 详细地址
        meal_period: 餐段设置(json字符串)
        facility: 设施(json字符串)
        pay_card: 可以刷哪些卡(json字符串)
        phone: 联系电话(最多3个，json数组)
        cuisine: 菜系(json字符串)
        hotel_name: 所属酒店名
        manager_name: 店长名字
        is_enabled: 是否有效
        create_time: 创建时间
    """

    try:
        branch = HotelBranch.enabled_objects.get(id=branch_id)
    except ObjectDoesNotExist:
        return err_response('err_3', '门店不存在')

    # 只能查看自己酒店的门店
    if branch.hotel != request.staff.hotel:
        return err_response('err_2', '权限错误')

    d = {'branch_id': branch.id,
         'name': branch.name,
         'icon': branch.icon,
         'pictures': branch.pictures,
         'province': branch.province,
         'city': branch.city,
         'county': branch.county,
         'address': branch.address,
         'meal_period': branch.meal_period,
         'facility': branch.facility,
         'pay_card': branch.pay_card,
         'phone': branch.phone,
         'cuisine': branch.cuisine,
         'hotel_name': branch.hotel.hotel.name,
         'manager_name': branch.manager_name,
         'is_enabled': branch.is_enabled,
         'create_time': branch.create_time}
    return corr_response(d)


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'branch_id': forms.IntegerField(),
    'position': forms.CharField(min_length=1, max_length=10, required=False),
    'order': forms.IntegerField(min_value=0, max_value=3, required=False),
    'date': forms.DateField(),
    'dinner_period': forms.IntegerField(),
})
@validate_staff_token()
def get_desks(request, token, branch_id, date, dinner_period, position=None,
              order=2):
    """获取门店某一天某餐段的桌位使用情况列表

    :param token: 令牌(必传)
    :param branch_id: 门店ID(必传)
    :param date: 日期, 例: 2017-05-12(必传)
    :param dinner_period: 餐段, 0:午餐, 1:晚餐, 2:夜宵(必传)
    :param position: 所在楼层位置
    :param order: 排序方式
        0: 注册时间升序
        1: 注册时间降序
        2: 房间号升序（默认值）
        3: 房间号降序
    :return:
        count: 桌位数
        list:
            desk_id: 桌位ID
            position: 楼层位置
            min_guest_num: 可容纳最小人数
            max_guest_num: 可容纳最大人数
            status: 桌位使用状态, 0: 空闲, 1: 预定中, 2: 用餐中
    """

    ORDERS = ('create_time', '-create_time', 'number', '-number')

    try:
        branch = HotelBranch.enabled_objects.get(id=branch_id)
    except ObjectDoesNotExist:
        return err_response('err_3', '门店不存在')

    # 只能查看自己酒店的门店
    if branch.hotel != request.staff.hotel:
        return err_response('err_2', '权限错误')

    if position is None:
        c = branch.desks.filter(is_enabled=True).count()
        ds = branch.desks.filter(is_enabled=True).order_by(ORDERS[order])
    else:
        c = branch.desks.filter(position=position, is_enabled=True).count()
        ds = branch.desks.filter(
            position=position, is_enabled=True).order_by(ORDERS[order])

    l = []
    for desk in ds:
        d = {'desk_id': desk.id,
             'position': desk.position,
             'min_guest_num': desk.min_guest_number,
             'max_guest_num': desk.max_guest_number}

        # 判断桌位在查询日和查询餐段的状态
        if Order.objects.filter(
                dinner_period=dinner_period, dinner_date=date, status=0). \
                exists():
            d['status'] = 1
        elif Order.objects.filter(
                dinner_period=dinner_period, dinner_date=date, status=1). \
                exists():
            d['status'] = 2
        else:
            d['status'] = 0
        l.append(d)

    return corr_response({'count': c, 'list': l})
