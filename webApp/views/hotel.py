import json

from django import forms
from django.core.exceptions import ObjectDoesNotExist

from ..utils.decorator import validate_args
from ..utils.response import corr_response, err_response
from ..models import Hotel


@validate_args({
    'offset': forms.IntegerField(min_value=0, required=False),
    'limit': forms.IntegerField(min_value=0, required=False),
    'order': forms.IntegerField(min_value=0, max_value=3, required=False),
})
def get_hotels(request, offset=0, limit=10, order=1):
    """获取酒店列表

    :param offset: 起始值
    :param limit: 偏移量
    :param order: 排序方式
        0: 注册时间升序
        1: 注册时间降序（默认值）
        2: 名称升序
        3: 名称降序
    :return:
        count: 酒店总数
        list: 酒店列表
            hotel_id: ID
            name: 名称
            icon: 头像
            branches_count: 门店数
            owner_name: 法人代表
            positions: 职位列表
            create_time: 创建时间
    """
    ORDERS = ('create_time', '-create_time', 'name', '-name')

    c = Hotel.enabled_objects.count()
    hotels = Hotel.enabled_objects.order_by(
        ORDERS[order])[offset:offset + limit]
    l = [{'hotel_id': h.id,
          'name': h.name,
          'icon': h.icon,
          'branches_count': h.branches.count(),
          'owner_name': h.owner_name,
          'positions': json.loads(h.positions) if h.positions else [],
          'create_time': h.create_time} for h in hotels]
    return corr_response({'count': c, 'list': l})


@validate_args({
    'hotel_id': forms.IntegerField(),
    'offset': forms.IntegerField(min_value=0, required=False),
    'limit': forms.IntegerField(min_value=0, required=False),
    'order': forms.IntegerField(min_value=0, max_value=3, required=False),
})
def get_branches(request, hotel_id, offset=0, limit=10, order=1):
    """获取员工所在酒店的门店列表

    :param hotel_id: 酒店ID
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

    try:
        hotel = Hotel.enabled_objects.get(id=hotel_id)
    except ObjectDoesNotExist:
        return err_response('err_4', '酒店不存在')

    c = hotel.branches.filter(is_enabled=True).count()
    branches = hotel.branches.filter(is_enabled=True).order_by(
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
