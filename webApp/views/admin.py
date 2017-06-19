import os
import string
import json

from PIL import Image
from random import choice
from django import forms
from django.db import IntegrityError, transaction
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from ..utils.response import corr_response, err_response
from ..utils.decorator import validate_args, validate_admin_token
from ..utils.cc_sdk import create_live_room, update_live_room, replay_live_room
from ..models import Admin, Hotel, HotelBranch, Area, Desk, Staff, Live


@validate_args({
    'username': forms.CharField(min_length=1, max_length=20),
    'password': forms.CharField(min_length=1, max_length=128),
})
def login(request, username, password):
    """更新并返回管理者令牌

    :param username: 用户名(必传)
    :param password: 密码(必传)
    :return token: 管理员token
    """

    try:
        admin = Admin.objects.get(username=username)
    except Admin.DoesNotExist:
        return err_response('err_2', '管理员不存在')
    else:
        if (not admin.is_enabled) or (admin.type != 0):
            return err_response('err_2', '管理员不存在')
        if admin.password != password:
            return err_response('err_3', '密码错误')
        admin.update_token()
        admin.save()
        return corr_response({'token': admin.token})


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
})
@validate_admin_token()
def get_hotel_profile(request, token):
    """获取酒店信息

    :param token: 令牌(必传)
    :return:
        hotel_id: ID
        name: 名称
        icon: 头像
        branches_count: 门店数
        owner_name: 法人代表
        create_time: 创建时间
    """

    try:
        hotel = request.admin.hotel
    except ObjectDoesNotExist:
        return err_response('err_4', '酒店不存在')
    if hotel.is_enabled is False:
        return err_response('err_4', '酒店不存在')

    d = {'hotel_id': hotel.id,
         'name': hotel.name,
         'icon': hotel.icon,
         'branches_count': hotel.branches.count(),
         'owner_name': hotel.owner_name,
         'create_time': hotel.create_time}
    return corr_response(d)


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'name': forms.CharField(min_length=1, max_length=20, required=False),
    'owner_name': forms.CharField(min_length=1, max_length=20,
                                  required=False),
    'hotel_id': forms.IntegerField(),
})
@validate_admin_token()
def modify_hotel_profile(request, token, hotel_id, **kwargs):
    """修改酒店信息

    :param token: 令牌(必传)
    :param hotel_id: 酒店ID(必传)
    :param kwargs:
        name: 酒店名
        owner_name: 法人代表
        icon: 头像，[file]文件
    :return: 200/400/403/404
    """

    try:
        hotel = Hotel.enabled_objects.filter(id=hotel_id)
    except Hotel.DoesNotExist:
        return err_response('err_4', '酒店不存在')

    # 管理员只能管理自己酒店
    if hotel != request.admin.hotel:
        return err_response('err_2', '权限错误')

    name = kwargs.pop('name') if 'name' in kwargs else None
    owner_name = kwargs.pop('owner_name') if \
        'owner_name' in kwargs else None
    if name:
        if Hotel.objects.filter(name=name).exists():
            return err_response('err_5', '酒店名已注册')
        hotel.name = name

    if owner_name:
        hotel.owner_name = owner_name

    if 'icon' in request.FILES:
        icon = request.FILES['icon']

        icon_time = timezone.now().strftime('%H%M%S%f')
        icon_tail = str(icon).split('.')[-1]
        dir_name = 'uploaded/icon/hotel/%d/' % hotel.id
        os.makedirs(dir_name, exist_ok=True)
        file_name = dir_name + '%s.%s' % (icon_time, icon_tail)
        try:
            img = Image.open(icon)
            img.save(file_name, quality=90)
        except OSError:
            return err_response('err6', '图片为空或图片格式错误')

        # 删除旧文件, 保存新的文件路径
        if hotel.icon:
            try:
                os.remove(hotel.icon)
            except OSError:
                pass
        hotel.icon = file_name

    hotel.save()
    return corr_response()


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'is_enabled': forms.BooleanField(required=False),
    'offset': forms.IntegerField(min_value=0, required=False),
    'limit': forms.IntegerField(min_value=0, required=False),
    'order': forms.IntegerField(min_value=0, max_value=3, required=False),
    'hotel_id': forms.IntegerField(),
})
@validate_admin_token()
def get_branches(request, token, hotel_id, is_enabled=True, offset=0, limit=10,
                 order=1):
    """获取酒店门店列表

    :param token: 令牌(必传)
    :param is_enabled: 是否有效, 默认:是
    :param hotel_id: 酒店ID(必传)
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
            pictures: 图片(最多5张，json)
            province: 省
            city: 市
            county: 区/县
            address: 详细地址
            facility: 设施(json)
            pay_card: 可以刷哪些卡(json)
            phone: 联系电话(最多3个，json)
            cuisine: 菜系(json)
            hotel_name: 所属酒店名
            manager_name: 店长名字
            create_time: 创建时间
    """
    ORDERS = ('create_time', '-create_time', 'name', '-name')

    try:
        hotel = Hotel.enabled_objects.get(id=hotel_id)
    except Hotel.DoesNotExist:
        return err_response('err_4', '酒店不存在')

    # 管理员只能查看自己酒店的门店
    if hotel != request.admin.hotel:
        return err_response('err_2', '权限错误')
    c = HotelBranch.objects.filter(
        hotel=hotel, is_enabled=is_enabled).count()
    branches = HotelBranch.objects.filter(
        hotel=hotel, is_enabled=is_enabled).order_by(
        ORDERS[order])[offset:offset + limit]

    l = [{'branch_id': b.id,
          'name': b.name,
          'icon': b.icon,
          'pictures': b.pictures,
          'province': b.province,
          'city': b.city,
          'county': b.county,
          'address': b.address,
          'facility': b.facility,
          'pay_card': b.pay_card,
          'phone': b.phone,
          'cuisine': b.cuisine,
          'hotel_name': b.hotel.hotel.name,
          'manager_name': b.manager.name,
          'create_time': b.create_time} for b in branches]
    return corr_response({'count': c, 'list': l})


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'hotel_id': forms.IntegerField(),
    'staff_id': forms.IntegerField(),
    'name': forms.CharField(min_length=1, max_length=20),
    'province': forms.CharField(min_length=1, max_length=20),
    'city': forms.CharField(min_length=1, max_length=20),
    'county': forms.CharField(min_length=1, max_length=20),
    'address': forms.CharField(min_length=1, max_length=50),
    'phone': forms.CharField(min_length=1, max_length=50, required=False),
    'facility': forms.CharField(max_length=100, required=False),
    'pay_card': forms.CharField(max_length=20, required=False),
    'cuisine': forms.CharField(max_length=100, required=False),
})
@validate_admin_token()
def register_branch(request, token, hotel_id, staff_id, **kwargs):
    """注册新的门店
    :param token: 令牌(必传)
    :param hotel_id: 酒店ID(必传)
    :param staff_id: 店长ID(必传)
    :param kwargs
        name: 名称(必传)
        province: 省(必传)
        city: 市(必传)
        county: 区/县(必传)
        address: 详细地址(必传)
        phone: 联系电话(最多3个，json)
        facility: 设施(json)
        pay_card: 可以刷哪些卡(json)
        cuisine: 菜系(json)
    :return 200/400
    """

    try:
        hotel = Hotel.enabled_objects.get(id=hotel_id)
    except Hotel.DoesNotExist:
        return err_response('err_4', '酒店不存在')
    try:
        staff = Staff.enabled_objects.get(id=staff_id)
    except Staff.DoesNotExist:
        return err_response('err_5', '员工不存在')

    branch_keys = ('name', 'province', 'city', 'county', 'address', 'phone',
                   'facility', 'pay_card', 'cuisine')
    with transaction.atomic():
        try:
            branch = HotelBranch(hotel=hotel, staff=staff)
            for k in branch_keys:
                if k in kwargs:
                    setattr(branch, k, kwargs[k])
            branch.save()
            return corr_response({'branch_id': branch.id})
        except IntegrityError:
            return err_response('error_6', '服务器创建门店失败')


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'branch_id': forms.IntegerField(),
})
@validate_admin_token()
def delete_branch(request, token, branch_id):
    """删除门店

    :param token: 令牌(必传)
    :param branch_id: 门店ID(必传)
    :return: 200/404
    """

    try:
        branch = HotelBranch.objects.get(id=branch_id)
    except HotelBranch.DoesNotExist:
        return err_response('err_4', '门店不存在')
    else:
        branch.is_enabled = False
        branch.save()
        return corr_response()


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'branch_id': forms.IntegerField(),
})
@validate_admin_token()
def get_branch_profile(request, token, branch_id, **kwargs):
    """获取酒店门店详情

    :param token: 令牌(必传)
    :param branch_id: 门店ID(必传)
    :return
        name: 名称
        icon: 头像
        pictures: 图片(最多5张，json)
        province: 省
        city: 市
        county: 区/县
        address: 详细地址
        meal_period: 餐段设置(json)
        facility: 设施(json)
        pay_card: 可以刷哪些卡(json)
        phone: 联系电话(最多3个，json)
        cuisine: 菜系(json)
        hotel_name: 所属酒店名
        manager_name: 店长名字
        is_enabled: 是否有效
        create_time: 创建时间
    """

    try:
        branch = HotelBranch.objects.get(id=branch_id)
    except ObjectDoesNotExist:
        return err_response('err_3', '门店不存在')

    # 管理员只能查看自己酒店的门店
    if branch.hotel != request.admin.hotel:
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
    'staff_id': forms.IntegerField(required=False),
    'name': forms.CharField(min_length=1, max_length=20, required=False),
    'province': forms.CharField(min_length=1, max_length=20,
                                required=False),
    'city': forms.CharField(min_length=1, max_length=20, required=False),
    'county': forms.CharField(min_length=1, max_length=20, required=False),
    'address': forms.CharField(min_length=1, max_length=50, required=False),
    'phone': forms.CharField(min_length=1, max_length=50, required=False),
    'facility': forms.CharField(max_length=100, required=False),
    'pay_card': forms.CharField(max_length=20, required=False),
    'cuisine': forms.CharField(max_length=100, required=False),
    'is_enabled': forms.BooleanField(required=False),
})
@validate_admin_token()
def modify_branch_profile(request, token, branch_id, staff_id=None, **kwargs):
    """修改门店信息
    :param token: 令牌(必传)
    :param branch_id: 酒店ID(必传)
    :param staff_id: 店长ID
    :param kwargs
        name: 名称
        province: 省
        city: 市
        county: 区/县
        address: 详细地址
        phone: 联系电话(最多3个，json)
        facility: 设施(json)
        pay_card: 可以刷哪些卡(json)
        cuisine: 菜系(json)
        is_enabled: 是否有效
        icon: 头像, [file]格式图片
    :return 200
    """

    try:
        branch = HotelBranch.objects.get(id=branch_id)
    except ObjectDoesNotExist:
        return err_response('err_4', '酒店不存在')

    if staff_id is not None:
        try:
            staff = Staff.enabled_objects.get(id=staff_id)
        except Staff.DoesNotExist:
            return err_response('err_5', '员工不存在')
        branch.manager = staff

    branch_keys = ('name', 'province', 'city', 'county', 'address', 'phone',
                   'facility', 'pay_card', 'cuisine', 'is_enabled')

    for k in branch_keys:
        if k in kwargs:
            setattr(branch, k, kwargs[k])

    # 修改头像
    if 'icon' in request.FILES:
        icon = request.FILES['icon']

        icon_time = timezone.now().strftime('%H%M%S%f')
        icon_tail = str(icon).split('.')[-1]
        dir_name = 'uploaded/icon/branch/%d/' % branch.id
        os.makedirs(dir_name, exist_ok=True)
        file_name = dir_name + '%s.%s' % (icon_time, icon_tail)
        try:
            img = Image.open(icon)
            img.save(file_name, quality=90)
        except OSError:
            return err_response('err6', '图片为空或图片格式错误')

        # 删除旧文件, 保存新的文件路径
        if branch.icon:
            try:
                os.remove(branch.icon)
            except OSError:
                pass
        branch.icon = file_name

    branch.save()
    return corr_response()


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'branch_id': forms.IntegerField(),
    'meal_period': forms.CharField(max_length=500),
})
@validate_admin_token()
def modify_meal_period(request, token, branch_id, meal_period):
    """修改门店的餐段

    :param token: 令牌(必传)
    :param branch_id: 酒店门店ID(必传)
    :param meal_period: 餐段设置, json字符串, 格式如下
        {
            "Monday": {
                "from": "8:30",
                "to": "12:00",
            },
            "TuesDay": {
                "from": "8:30",
                "to": "12:00",
            },
            ...
        }
    :return:
    """
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
            'Saturday', 'Sunday']

    try:
        branch = HotelBranch.objects.get(id=branch_id)
    except ObjectDoesNotExist:
        return err_response('err_4', '酒店不存在')

    # 解析餐段json字符串
    try:
        meal_period_dict = json.loads(meal_period)
        with open('data/meal_period.json') as json_file:
            data = json.load(json_file)
        result = {}
        for day in days:
            # 午餐
            lunch = data['lunch']
            if 'lunch' in meal_period_dict[day]:
                begin = meal_period_dict[day]['lunch']['from']
                end = meal_period_dict[day]['lunch']['to']
                result['lunch'] = \
                    lunch[lunch.index(begin): lunch.index(end) + 1]
            # 晚餐
            dinner = data['dinner']
            if 'dinner' in meal_period_dict[day]:
                begin = meal_period_dict[day]['dinner']['from']
                end = meal_period_dict[day]['dinner']['to']
                result['dinner'] = \
                    dinner[dinner.index(begin): dinner.index(end) + 1]
            # 夜宵
            supper = data['supper']
            if 'supper' in meal_period_dict[day]:
                begin = meal_period_dict[day]['supper']['from']
                end = meal_period_dict[day]['supper']['to']
                result['supper'] = \
                    supper[supper.index(begin): supper.index(end) + 1]
        branch.meal_period = json.dumps(result)
    except ValueError or KeyError:
        return err_response('err_1', '参数不正确（缺少参数或者不符合格式）')


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'branch_id': forms.IntegerField(),
})
@validate_admin_token()
def add_branch_picture(request, token, branch_id):
    """增加门店图片

    :param token: 令牌(必传)
    :param branch_id: 酒店门店ID(必传)
    :param picture: 酒店门店介绍图片, [file]格式图片, 增加图片时传
    :return 200/400
    """

    try:
        branch = HotelBranch.objects.get(id=branch_id)
    except ObjectDoesNotExist:
        return err_response('err_4', '酒店不存在')

    pictures = json.loads(branch.pictures)

    # 添加图片
    if 'picture' in request.FILES:
        picture = request.FILES['picture']

        if len(pictures) >= 5:
            return err_response('err5', '图片数量已超过限制')

        picture_time = timezone.now().strftime('%H%M%S%f')
        picture_tail = str(picture).split('.')[-1]
        dir_name = 'uploaded/picture/branch/%d/' % branch.id
        os.makedirs(dir_name, exist_ok=True)
        file_name = dir_name + '%s.%s' % (picture_time, picture_tail)
        try:
            img = Image.open(picture)
            img.save(file_name, quality=90)
        except OSError:
            return err_response('err6', '图片为空或图片格式错误')

        pictures.append(file_name)
        branch.pictures = json.dumps(pictures)

        branch.save()
        return corr_response()
    else:
        return err_response('err1', '参数不正确（缺少参数或者不符合格式）')


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'branch_id': forms.IntegerField(),
    'pictures': forms.CharField(max_length=300),
})
@validate_admin_token()
def delete_branch_picture(request, token, branch_id, pictures):
    """删除酒店门店介绍图片

    :param token: 令牌(必传)
    :param branch_id: 酒店ID(必传)
    :param pictures: 需要删除的酒店介绍图片, json数组, 最多5张
    :return:
    """

    try:
        branch = HotelBranch.objects.get(id=branch_id)
    except ObjectDoesNotExist:
        return err_response('err_4', '酒店不存在')

    try:
        picture_list = json.loads(pictures)
    except ValueError:
        return err_response('err_1', '参数不正确（缺少参数或者不符合格式）')

    pictures_tmp = json.loads(branch.pictures)

    with transaction.atomic():
        for picture in picture_list:
            if picture in pictures_tmp:
                pictures_tmp.remove(picture)
                # 删除旧文件
                try:
                    os.remove(picture)
                except OSError:
                    pass
            else:
                return err_response('err_5', '图片不存在')

        branch.pictures = json.dumps(pictures_tmp)
        branch.save()
        return corr_response()


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'branch_id': forms.IntegerField(),
    'order': forms.IntegerField(min_value=0, max_value=3, required=False),
})
@validate_admin_token()
def get_areas(request, token, branch_id, order=1):
    """获取门店的餐厅区域列表

    :param token: 令牌(必传)
    :param branch_id: 门店ID(必传)
    :param order: 排序方式
        0: 注册时间升序
        1: 注册时间降序（默认值）
        2: 名称升序
        3: 名称降序
    :return:
        count: 餐厅区域数
        list:
            area_id: 区域ID
            name: 区域名
            order: 排序
            is_enabled: 是否有效
            create_time: 创建时间
    """
    ORDERS = ('create_time', '-create_time', 'name', '-name')

    try:
        branch = HotelBranch.enabled_objects.get(id=branch_id)
    except ObjectDoesNotExist:
        return err_response('err_4', '门店不存在')

    # 只能查看自己酒店的门店
    if branch.hotel != request.admin.hotel:
        return err_response('err_2', '权限错误')

    c = branch.areas.count()
    areas = branch.areas.order_by(ORDERS[order])

    l = [{'area_id': area.id,
          'name': area.name,
          'order': area.order,
          'is_enabled': area.is_enabled,
          'create_time': area.create_time} for area in areas]

    return corr_response({'count': c, 'list': l})


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'branch_id': forms.IntegerField(),
    'name': forms.CharField(min_length=1, max_length=10),
    'order': forms.IntegerField(min_value=0),
})
@validate_admin_token()
def add_area(request, token, branch_id, name, order):
    """增加餐厅区域

    :param token: 令牌(必传)
    :param branch_id: 门店ID(必传)
    :param name: 名称(必传)
    :param order: 排序(必传)
    :return: 200
    """

    try:
        branch = HotelBranch.enabled_objects.get(id=branch_id)
    except ObjectDoesNotExist:
        return err_response('err_4', '酒店不存在')

    # 管理员只能查看自己酒店的门店
    if branch.hotel != request.admin.hotel:
        return err_response('err_2', '权限错误')

    with transaction.atomic():
        try:
            area = Area(name=name, order=order, branch=branch)
            area.save()
            return corr_response()
        except IntegrityError:
            return err_response('err_5', '服务器添加餐厅区域失败')


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'area_id': forms.IntegerField(),
    'name': forms.CharField(min_length=1, max_length=10, required=False),
    'order': forms.IntegerField(min_value=0, required=False),
    'is_enabled': forms.BooleanField(required=False),
})
@validate_admin_token()
def modify_area(request, token, area_id, **kwargs):
    """修改餐厅区域信息

    :param token: 令牌(必传)
    :param area_id: 门店ID(必传)
    :param kwargs:
        name: 名称
        order: 排序
        is_enabled: 是否有效
    :return: 200
    """

    try:
        area = Area.objects.get(id=area_id)
    except ObjectDoesNotExist:
        return err_response('err_4', '酒店不存在')

    # 管理员只能查看自己酒店的门店
    if area.branch.hotel != request.admin.hotel:
        return err_response('err_2', '权限错误')

    area_keys = ('name', 'order', 'is_enabled')

    for k in kwargs:
        if k in area_keys:
            setattr(area, k, kwargs[k])

    area.save()
    return corr_response()


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'area_id': forms.IntegerField(),
    'offset': forms.IntegerField(min_value=0, required=False),
    'limit': forms.IntegerField(min_value=0, required=False),
    'order': forms.IntegerField(min_value=0, max_value=3, required=False),
})
@validate_admin_token()
def get_desks(request, token, area_id, offset=0, limit=10, order=2):
    """获取门店的桌位列表

    :param token: 令牌(必传)
    :param area_id: 区域ID(必传)
    :param offset: 起始值
    :param limit: 偏移量
    :param order: 排序方式
        0: 注册时间升序
        1: 注册时间降序
        2: 房间号升序（默认值）
        3: 房间号降序
    :return:
        count: 桌位数
        list:
            desk_id: 桌位ID
            number: 编号
            order: 排序
            min_guest_num: 可容纳最小人数
            max_guest_num: 可容纳最大人数
            expense: 费用说明
            type: 房间类型
            facility: 房间设施
            picture: 图片
            is_beside_window: 是否靠窗
            description: 备注
            create_time: 创建时间
    """

    ORDERS = ('create_time', '-create_time', 'number', '-number')

    try:
        area = Area.objects.get(id=area_id)
    except ObjectDoesNotExist:
        return err_response('err_4', '该区域不存在')

    # 只能查看自己酒店的门店区域
    if area.branch.hotel != request.admin.hotel:
        return err_response('err_2', '权限错误')

    c = area.desks.count()
    ds = area.desks.order_by(ORDERS[order])[offset:offset + limit]

    l = [{'desk_id': desk.id,
          'number': desk.number,
          'order': desk.order,
          'min_guest_num': desk.min_guest_number,
          'max_guest_num': desk.max_guest_number,
          'expense': desk.expense,
          'type': desk.type,
          'facility': desk.facility,
          'picture': desk.picture,
          'is_beside_window': desk.is_beside_window,
          'description': desk.description,
          'create_time': desk.create_time} for desk in ds]

    return corr_response({'count': c, 'list': l})


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'area_id': forms.IntegerField(),
    'number': forms.CharField(max_length=10),
    'order': forms.IntegerField(),
    'min_guest_num': forms.IntegerField(),
    'max_guest_num': forms.IntegerField(),
    'expense': forms.CharField(max_length=100, required=False),
    'type': forms.CharField(max_length=10, required=False),
    'facility': forms.CharField(max_length=100, required=False),
    'is_beside_window': forms.BooleanField(required=False),
    'description': forms.CharField(max_length=100, required=False),
})
@validate_admin_token()
def add_desk(request, token, area_id, number, order, **kwargs):
    """增加门店区域的桌位

    :param token: 令牌(必传)
    :param area_id: 区域ID(必传)
    :param number: 桌位号(必传)
    :param order: 排序(必传)
    :param kwargs:
        min_guest_num: 最小人数限制(必传)
        max_guest_num: 最大人数限制(必传)
        expense: 花费说明
        type: 桌位类型
        facility: 设施, json字符串
        is_beside_window: 是否靠窗
        description: 描述
    :return 200
    """

    try:
        area = Area.enabled_objects.get(id=area_id)
    except ObjectDoesNotExist:
        return err_response('err_4', '地区不存在')

    # 管理员只能添加自己酒店的桌位
    if area.branch.hotel != request.admin.hotel:
        return err_response('err_2', '权限错误')

    desk_keys = ('min_guest_num', 'max_guest_num', 'expense',
                 'type', 'facility', 'is_beside_window', 'description')
    with transaction.atomic():
        try:
            desk = Desk(number=number, order=order)
            for k in desk_keys:
                if k in kwargs:
                    setattr(desk, k, kwargs[k])

            # 图片
            if 'picture' in request.FILES:
                picture = request.FILES['picture']

                picture_time = timezone.now().strftime('%H%M%S%f')
                picture_tail = str(picture).split('.')[-1]
                dir_name = 'uploaded/picture/desk/%d/' % desk.id
                os.makedirs(dir_name, exist_ok=True)
                file_name = dir_name + '%s.%s' % (picture_time, picture_tail)
                try:
                    img = Image.open(picture)
                    img.save(file_name, quality=90)
                except OSError:
                    return err_response('err5', '图片为空或图片格式错误')

            desk.save()
            return corr_response()
        except IntegrityError:
            return err_response('err_6', '服务器创建桌位失败')


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'desk_id': forms.IntegerField(),
    'number': forms.CharField(max_length=10, required=False),
    'order': forms.IntegerField(required=False),
    'min_guest_num': forms.IntegerField(required=False),
    'max_guest_num': forms.IntegerField(required=False),
    'expense': forms.CharField(max_length=100, required=False),
    'type': forms.CharField(max_length=10, required=False),
    'facility': forms.CharField(max_length=100, required=False),
    'is_beside_window': forms.BooleanField(required=False),
    'description': forms.CharField(max_length=100, required=False),
})
@validate_admin_token()
def modify_desk(request, token, desk_id, **kwargs):
    """修改门店区域的桌位

    :param token: 令牌(必传)
    :param desk_id: 桌位ID(必传)
    :param kwargs:
        number: 桌位号
        order: 排序
        min_guest_num: 最小人数限制
        max_guest_num: 最大人数限制
        expense: 花费说明
        type: 桌位类型
        facility: 设施, json字符串
        is_beside_window: 是否靠窗
        description: 描述
    :param picture: 桌位介绍图片,[file]文件
    :return 200
    """

    try:
        desk = Desk.enabled_objects.get(id=desk_id)
    except ObjectDoesNotExist:
        return err_response('err_4', '桌位不存在')

    # 管理员只能添加自己酒店的桌位
    if desk.area.branch.hotel != request.admin.hotel:
        return err_response('err_2', '权限错误')

    desk_keys = ('number', 'order', 'min_guest_num', 'max_guest_num', 'expense',
                 'type', 'facility', 'is_beside_window', 'description')

    for k in desk_keys:
        if k in kwargs:
            setattr(desk, k, kwargs[k])

    # 修改图片
    if 'picture' in request.FILES:
        picture = request.FILES['picture']

        picture_time = timezone.now().strftime('%H%M%S%f')
        picture_tail = str(picture).split('.')[-1]
        dir_name = 'uploaded/picture/desk/%d/' % desk.id
        os.makedirs(dir_name, exist_ok=True)
        file_name = dir_name + '%s.%s' % (picture_time, picture_tail)
        try:
            img = Image.open(picture)
            img.save(file_name, quality=90)
        except OSError:
            return err_response('err_5', '图片为空或图片格式错误')

        # 删除旧文件, 保存新的文件路径
        if desk.picture:
            try:
                os.remove(desk.picture)
            except OSError:
                pass
        desk.picture = file_name

    desk.save()
    return corr_response()


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'status': forms.IntegerField(min_value=0, max_value=1, required=False),
    'is_enabled': forms.BooleanField(required=False),
    'offset': forms.IntegerField(min_value=0, required=False),
    'limit': forms.IntegerField(min_value=0, required=False),
    'order': forms.IntegerField(min_value=0, max_value=3, required=False),
    'hotel_id': forms.IntegerField(),
})
@validate_admin_token()
def get_staffs(request, token, hotel_id, status=1, is_enabled=True, offset=0,
               limit=10, order=1):
    """获取酒店员工列表

    :param token: 令牌(必传)
    :param status: 员工状态, 0: 待审核, 1: 审核通过, 默认1
    :param is_enabled: 是否有效, 默认:是
    :param hotel_id: 酒店ID(必传)
    :param offset: 起始值
    :param limit: 偏移量
    :param order: 排序方式
        0: 注册时间升序
        1: 注册时间降序（默认值）
        2: 昵称升序
        3: 昵称降序
    :return:
        count: 员工总数
        list: 员工列表
            staff_id: ID
            staff_number: 员工编号
            name: 员工姓名
            icon: 员工头像
            gender: 性别
            hotel_name: 员工所属酒店
            position: 职位
            guest_channel: 所属获客渠道
                0:无, 1:高层管理, 2:预定员和迎宾, 3:客户经理
            authority: 权限
            create_time: 创建时间
    """
    ORDERS = ('create_time', '-create_time', 'name', '-name')

    try:
        hotel = Hotel.enabled_objects.get(id=hotel_id)
    except Hotel.DoesNotExist:
        return err_response('err_4', '酒店不存在')

    # 管理员只能查看自己酒店的员工
    if hotel != request.admin.hotel:
        return err_response('err_2', '权限错误')

    c = Staff.objects.filter(hotel=hotel, status=status,
                             is_enabled=is_enabled).count()
    staffs = Staff.objects.filter(
        hotel=hotel, status=status, is_enabled=is_enabled).order_by(
        ORDERS[order])[offset:offset + limit]

    l = [{'staff_id': s.id,
          'name': s.name,
          'staff_number': s.staff_number,
          'icon': s.icon,
          'gender': s.gender,
          'hotel_name': s.hotel.name,
          'position': s.position,
          'guest_channel': s.guest_channel,
          'authority': s.authority,
          'create_time': s.create_time} for s in staffs]
    return corr_response({'count': c, 'list': l})


@validate_args({
    'phone': forms.RegexField(r'[0-9]{11}'),
    'password': forms.CharField(min_length=1, max_length=128),
    'staff_number': forms.CharField(
        min_length=1, max_length=20, required=False),
    'name': forms.CharField(min_length=1, max_length=20),
    'gender': forms.IntegerField(min_value=0, max_value=2, required=False),
    'position': forms.CharField(max_length=20),
    'id_number': forms.CharField(min_length=18, max_length=18),
    'guest_channel': forms.IntegerField(
        min_value=0, max_value=3, required=False),
    'description': forms.CharField(max_length=100, required=False),
    'authority': forms.CharField(max_length=20, required=False),
    'hotel_id': forms.IntegerField(),
})
@validate_admin_token()
def register_staff(request, phone, password, hotel_id, **kwargs):
    """注册新员工

    :param phone: 手机号(必传)
    :param password: 密码(必传)
    :param hotel_id: 酒店ID(必传)
    :param kwargs:
        staff_number: 员工编号
        name: 姓名(必传)
        position: 职位(必传)
        gender: 性别, 0: 保密, 1: 男, 2: 女
        id_number: 身份证号(必传)
        guest_channel: 所属获客渠道, 0:无, 1:高层管理, 2:预定员和迎宾, 3:客户经理
        description: 备注
        authority: 权限
        icon: 头像, [file]格式
    :return 200
    """

    try:
        hotel = Hotel.enabled_objects.get(id=hotel_id)
    except Hotel.DoesNotExist:
        return err_response('err_4', '酒店不存在')
    # 管理员只能添加自己酒店的员工
    if hotel != request.admin.hotel:
        return err_response('err_2', '权限错误')

    if Staff.objects.filter(phone=phone).exists():
        return err_response('err_5', '该手机号已注册')
    staff_keys = ('staff_number', 'name', 'gender', 'position', 'id_number',
                  'guest_channel', 'description', 'authority')
    with transaction.atomic():
        try:
            staff = Staff(phone=phone, password=password, status=1,
                          hotel=hotel)
            # 更新令牌
            staff.update_token()
            for k in staff_keys:
                if k in kwargs:
                    setattr(staff, k, kwargs[k])

            # 设置头像
            if 'icon' in request.FILES:
                icon = request.FILES['icon']

                icon_time = timezone.now().strftime('%H%M%S%f')
                icon_tail = str(icon).split('.')[-1]
                dir_name = 'uploaded/icon/staff/%d/' % staff.id
                os.makedirs(dir_name, exist_ok=True)
                file_name = dir_name + '%s.%s' % (icon_time, icon_tail)
                try:
                    img = Image.open(icon)
                    img.save(file_name, quality=90)
                except OSError:
                    return err_response('err6', '图片为空或图片格式错误')

                # 删除旧文件, 保存新的文件路径
                if staff.icon:
                    try:
                        os.remove(staff.icon)
                    except OSError:
                        pass
                staff.icon = file_name

            staff.save()
            return corr_response()
        except IntegrityError:
            return err_response('err_7', '服务器创建员工失败')


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'staff_id': forms.IntegerField(),
})
@validate_admin_token()
def delete_staff(request, token, staff_id):
    """删除员工

    :param token: 令牌(必传)
    :param staff_id: 员工ID(必传)
    :return: 200/404
    """

    try:
        staff = Staff.objects.get(id=staff_id)
    except Staff.DoesNotExist:
        return err_response('err_4', '员工不存在')
    # 管理员只能管理自己酒店的员工
    if staff.hotel != request.admin.hotel:
        return err_response('err_2', '权限错误')

    staff.is_enabled = False
    staff.save()
    return corr_response()


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'staff_id': forms.IntegerField(),
})
@validate_admin_token()
def get_staff_profile(request, token, staff_id):
    """查看员工信息

    :param token: 令牌(必传)
    :param staff_id: 员工ID(必传)
    :return:
        staff_id: ID
        staff_number: 员工编号
        name: 员工姓名
        icon: 员工头像
        gender: 性别
        status: 员工状态，0: 待审核，1: 审核通过
        description: 备注
        position: 职位
        guest_channel: 所属获客渠道
            0:无, 1:高层管理, 2:预定员和迎宾, 3:客户经理
        authority: 权限
        create_time: 创建时间
    """

    try:
        staff = Staff.objects.get(id=staff_id)
    except Staff.DoesNotExist:
        return err_response('err_4', '员工不存在')

    # 管理员只能查看自己酒店的员工
    if staff.hotel != request.admin.hotel:
        return err_response('err_2', '权限错误')

    d = {'staff_id': staff.id,
         'staff_number': staff.staff_number,
         'name': staff.name,
         'icon': staff.icon,
         'gender': staff.gender,
         'position': staff.position,
         'guest_channel': staff.guest_channel,
         'description': staff.description,
         'authority': staff.authority,
         'status': staff.status,
         'create_time': staff.create_time}
    return corr_response(d)


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'staff_number': forms.CharField(
        min_length=1, max_length=20, required=False),
    'gender': forms.IntegerField(min_value=0, max_value=2, required=False),
    'position': forms.CharField(max_length=20, required=False),
    'guest_channel': forms.IntegerField(
        min_value=0, max_value=3, required=False),
    'description': forms.CharField(max_length=100, required=False),
    'authority': forms.CharField(max_length=20, required=False),
    'status': forms.IntegerField(required=False),
    'is_enabled': forms.BooleanField(required=False),
    'staff_id': forms.IntegerField(),
})
@validate_admin_token()
def modify_staff_profile(request, token, staff_id, **kwargs):
    """修改员工信息，包括账号审核

    :param token: 令牌(必传)
    :param staff_id: 员工ID(必传)
    :param kwargs:
        staff_number: 员工编号
        gender: 性别
        position: 职位
        guest_channel: 所属获客渠道, 0:无, 1:高层管理, 2:预定员和迎宾, 3:客户经理
        description: 备注
        authority: 权限
        status: 状态, 0: 待审核, 1: 审核通过
        is_enabled: 是否可用, True/False
    :return: 200
    """

    try:
        staff = Staff.objects.get(id=staff_id)
    except Staff.DoesNotExist:
        return err_response('err_4', '员工不存在')

    # 管理员只能管理自己酒店的员工
    if staff.hotel != request.admin.hotel:
        return err_response('err_2', '权限错误')

    staff_keys = ('staff_number', 'gender', 'position', 'guest_channel',
                  'description', 'authority', 'status', 'is_enabled')
    for k in staff_keys:
        if k in kwargs:
            setattr(staff, k, kwargs[k])

    # 修改头像
    if 'icon' in request.FILES:
        icon = request.FILES['icon']

        icon_time = timezone.now().strftime('%H%M%S%f')
        icon_tail = str(icon).split('.')[-1]
        dir_name = 'uploaded/icon/staff/%d/' % staff.id
        os.makedirs(dir_name, exist_ok=True)
        file_name = dir_name + '%s.%s' % (icon_time, icon_tail)
        try:
            img = Image.open(icon)
            img.save(file_name, quality=90)
        except OSError:
            return err_response('err_5', '图片为空或图片格式错误')

        # 删除旧文件, 保存新的文件路径
        if staff.icon:
            try:
                os.remove(staff.icon)
            except OSError:
                pass
        staff.icon = file_name

    staff.save()
    return corr_response()


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'offset': forms.IntegerField(min_value=0, required=False),
    'limit': forms.IntegerField(min_value=0, required=False),
    'order': forms.IntegerField(min_value=0, max_value=3, required=False),
})
@validate_admin_token()
def get_lives(request, token, offset=0, limit=10, order=1):
    """获取自己酒店的直播间

    :param token: 令牌(必传)
    :param offset: 起始值
    :param limit: 偏移量
    :param order: 排序方式
        0: 注册时间升序
        1: 注册时间降序（默认值）
        2: 名称升序
        3: 名称降序
    :return:
        count: 直播总数
        list: 直播列表
            live_id: ID
            name: 直播间名称
            cc_room_id: 对应cc的roomid
            publisher_password: 推流密码
            price: 价格
            buyer_count: 已购买数
            description: 描述
            start_date: 直播开始日期
            end_date: 直播结束日期
            start_time: 直播开始时间
            end_time: 直播结束时间
            create_time: 创建时间
    """
    ORDERS = ('create_time', '-create_time', 'name', '-name')

    hotel = request.admin.hotel
    c = hotel.lives.count()
    lives = hotel.lives.order_by(ORDERS[order])[offset:offset + limit]
    l = [{'live_id': live.id,
          'name': live.name,
          'cc_room_id': live.cc_room_id,
          'price': live.price,
          'buyer_count': live.purchase_records.count(),
          'publisher_password': live.play_password,
          'description': live.description,
          'start_date': live.start_date,
          'end_date': live.end_date,
          'start_time': live.start_time,
          'end_time': live.end_time,
          'create_time': live.create_time} for live in lives]
    return corr_response({'count': c, 'list': l})


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'name': forms.CharField(min_length=1, max_length=20),
    'start_date': forms.DateField(),
    'end_date': forms.DateField(),
    'start_time': forms.TimeField(),
    'end_time': forms.TimeField(),
    'price': forms.IntegerField(required=False),
    'description': forms.CharField(max_length=100, required=False),
})
@validate_admin_token()
def push_live(request, token, name, **kwargs):
    """发布直播间

    :param token: 令牌(必传)
    :param name: 直播间名称(必传)
    :param kwargs:
        start_date: 开始日期(必传)
        end_date: 结束日期(必传)
        start_time: 开始时间(必传)
        end_time: 结束时间(必传)
        price: 价格
        description: 描述
    :return:
        live_id: 直播间id
        cc_room_id: 对应cc上的roomid
        publisher_password: 推流密码
    """

    # 验证是否有权限发布直播
    # todo

    description = kwargs.pop('description') \
        if 'description' in kwargs else ''

    live_keys = ('start_date', 'end_date', 'start_time', 'end_time',
                 'price')

    # 生成推送和播放随机密码
    chars = string.ascii_letters + string.digits
    publisher_password = ''.join([choice(chars) for i in range(6)])
    play_password = ''.join([choice(chars) for i in range(6)])

    with transaction.atomic():
        try:
            # 向CC发送http请求，创建直播间
            res = create_live_room(publisher_password, play_password,
                                   name, description)
            try:
                if res['result'] == 'OK':
                    cc_room_id = res['room']['id']
                else:
                    return err_response('err_4', '服务器创建直播间失败')
            except KeyError:
                return err_response('err_4', '服务器创建直播间失败')
            live = Live(cc_room_id=cc_room_id, name=name,
                        description=description, hotel=request.admin.hotel,
                        publisher_password=publisher_password,
                        play_password=play_password)
            for k in live_keys:
                if k in kwargs:
                    setattr(live, k, kwargs[k])
            live.save()
            d = {'live_id': live.id,
                 'cc_room_id': cc_room_id,
                 'publisher_password': publisher_password}
            return corr_response(d)
        except IntegrityError:
            return err_response('err_4', '服务器创建直播间失败')


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'live_id': forms.IntegerField(),
    'name': forms.CharField(min_length=1, max_length=20, required=False),
    'start_date': forms.DateField(required=False),
    'end_date': forms.DateField(required=False),
    'start_time': forms.TimeField(required=False),
    'end_time': forms.TimeField(required=False),
    'price': forms.IntegerField(required=False),
    'description': forms.CharField(max_length=100, required=False),
})
@validate_admin_token()
def modify_live_profile(request, token, live_id, **kwargs):
    """修改直播间信息

    :param token: 员工令牌(必传)
    :param live_id: 直播间ID(必传)
    :param kwargs:
        name: 直播间名称
        start_date: 开始日期
        end_date: 结束日期
        start_time: 开始时间
        end_time: 结束时间
        price: 价格
        description: 描述
    :return:
    """

    try:
        live = Live.objects.get(id=live_id)
    except Live.DoesNotExist:
        return err_response('err_4', '直播间不存在')

    # 管理员只能管理自己酒店的直播间
    if live.hotel != request.admin.hotel:
        return err_response('err_2', '权限错误')

    name = kwargs.pop('name') if 'name' in kwargs else None
    description = kwargs.pop('description') \
        if 'description' in kwargs else None

    live_keys = ('start_date', 'end_date', 'start_time', 'end_time',
                 'price')
    with transaction.atomic():
        try:
            # 向CC发送http请求，修改直播间信息
            if name is not None:
                live.name = name
                if description is not None:
                    live.description = description
            else:
                if description is not None:
                    live.description = description

            if (name is not None) or (description is not None):
                res = update_live_room(live.cc_room_id,
                                       live.publisher_password,
                                       live.play_password,
                                       live.name,
                                       live.description)
                try:
                    if res['result'] != 'OK':
                        return err_response('err_5', '服务器修改直播间信息失败')
                except KeyError:
                    return err_response('err_5', '服务器修改直播间信息失败')

            # 修改数据库
            for k in live_keys:
                if k in kwargs:
                    setattr(live, k, kwargs[k])
            live.save()
            return corr_response()
        except IntegrityError:
            return err_response('err_5', '服务器修改直播间信息失败')


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'live_id': forms.IntegerField(),
    'page_index': forms.IntegerField(min_value=0, required=False),
    'page_num': forms.IntegerField(min_value=0, required=False),
})
@validate_admin_token()
def get_playbacks(request, token, live_id, page_index=0, page_num=10):
    """获取直播间的回放列表

    :param token: 令牌
    :param live_id: 直播间ID
    :param page_index: 页码起始值, 默认为1
    :param page_num: 每页数量, 默认为10
    :return:
        count: 回放数
        list:
            cc_live_id: 回放id
            start_time: 开始时间
            end_time: 结束时间
            record_status: 录制状态，0表示录制未结束，1表示录制完成
            record_video_id: 录制视频id，如果recordStatus为0则返回-1
            replay_url: 回放地址，当recordStatus为0时返回""
    """

    try:
        live = Live.objects.get(id=live_id)
    except Live.DoesNotExist:
        return err_response('err_4', '直播间不存在')

    # 判断该直播是否属于当前管理员的酒店
    if live.hotel != request.admin.hotel:
        return err_response('err_2', '权限错误')

    # 获取直播间回放
    res = replay_live_room(live.cc_room_id, page_index, page_num)
    if res['result'] != 'OK':
        return err_response('err_5', '服务器查询直播间状态失败')
    try:
        lives = res['lives']
        c = res['count']
    except KeyError:
        return err_response('err_5', '服务器查询直播间状态失败')

    l = [{'cc_live_id': cc_live['id'],
          'start_time': cc_live['startTime'],
          'end_time': cc_live['endTime'],
          'record_status': cc_live['recordStatus'],
          'record_video_id': cc_live['recordVideoId'],
          'replay_url': cc_live['replayUrl']} for cc_live in lives]

    return corr_response({'count': c, 'list': l})
