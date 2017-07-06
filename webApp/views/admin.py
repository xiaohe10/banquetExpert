import os
import string
import json

from PIL import Image
from random import choice
from django import forms
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.utils import timezone
from django.core.validators import RegexValidator
from django.core.exceptions import ObjectDoesNotExist

from ..utils.response import corr_response, err_response
from ..utils.decorator import validate_args, validate_admin_token
from ..utils.cc_sdk import create_live_room, update_live_room, replay_live_room
from ..models import Admin, Hotel, HotelBranch, Area, Desk, Staff, Live, Order,\
    Guest, ExternalChannel


@validate_args({
    'username': forms.CharField(min_length=1, max_length=20),
    'password': forms.CharField(min_length=1, max_length=32),
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
        # 将token放入session
        request.session['token'] = admin.token
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
        branch_number: 门店数量上限
        service: 开通的服务
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
         'branch_number': hotel.branch_number,
         'service': json.loads(hotel.service) if hotel.service else {},
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
        if Hotel.objects.filter(name=name).exclude(id=hotel.id).exists():
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
            pictures: 图片(最多5张，数组)
            province: 省
            city: 市
            county: 区/县
            address: 详细地址
            facility: 设施(数组)
            pay_card: 可以刷哪些卡(数组)
            phone: 联系电话(最多3个，数组)
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
          'pictures': json.loads(b.pictures) if b.pictures else [],
          'province': b.province,
          'city': b.city,
          'county': b.county,
          'address': b.address,
          'facility': json.loads(b.facility) if b.facility else [],
          'pay_card': json.loads(b.pay_card) if b.pay_card else [],
          'phone': json.loads(b.phone) if b.phone else [],
          'hotel_name': b.hotel.name,
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
        phone: 联系电话(最多3个，数组)
        facility: 设施(数组)
        pay_card: 可以刷哪些卡(数组)
        cuisine: 菜系(健值对)
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

    if hotel.branches.count() >= hotel.branch_number:
        return err_response('err_6', '门店数量已达上限')

    name = kwargs.pop('name')
    if hotel.branches.filter(name=name).count() > 0:
        return err_response('err_7', '门店名已存在')

    branch_keys = ('province', 'city', 'county', 'address')
    branch_other_keys = ('phone', 'facility', 'pay_card', 'cuisine')

    with transaction.atomic():
        try:
            branch = HotelBranch(name=name, hotel=hotel, manager=staff)
            for k in branch_keys:
                if k in kwargs:
                    setattr(branch, k, kwargs[k])

            data = json.loads(request.body)
            for k in branch_other_keys:
                if k in data:
                    try:
                        v = json.dumps(data[k])
                        setattr(branch, k, v)
                    except KeyError or ValueError:
                        return err_response(
                            'err_1', '参数不正确（缺少参数或者不符合格式）')
            branch.save()
            return corr_response({'branch_id': branch.id})
        except IntegrityError:
            return err_response('err_8', '服务器创建门店失败')


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
        pictures: 图片(最多5张，数组)
        province: 省
        city: 市
        county: 区/县
        address: 详细地址
        meal_period: 餐段设置(数组)
        facility: 设施(数组)
        pay_card: 可以刷哪些卡(数组)
        phone: 联系电话(最多3个，数组)
        cuisine: 菜系(键值对)
        personal_tailor: 私人订制项(最多10个，数组)
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
         'pictures': json.loads(branch.pictures) if branch.pictures else [],
         'province': branch.province,
         'city': branch.city,
         'county': branch.county,
         'address': branch.address,
         'meal_period': [],
         'facility': json.loads(branch.facility) if branch.facility else [],
         'pay_card': json.loads(branch.pay_card) if branch.pay_card else [],
         'phone': json.loads(branch.phone) if branch.phone else [],
         'cuisine': json.loads(branch.cuisine) if branch.cuisine else [],
         'personal_tailor': json.loads(branch.personal_tailor)
         if branch.personal_tailor else [],
         'hotel_name': branch.hotel.name,
         'manager_name': branch.manager.name,
         'is_enabled': branch.is_enabled,
         'create_time': branch.create_time}

    if branch.meal_period:
        try:
            meal_period = json.loads(branch.meal_period)
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                    'Saturday', 'Sunday']
            for day in days:
                d['meal_period'].append({
                    'lunch': {
                        'from': meal_period[day]['lunch'][0],
                        'to': meal_period[day]['lunch'][-1]},
                    'dinner': {
                        'from': meal_period[day]['dinner'][0],
                        'to': meal_period[day]['dinner'][-1]},
                    'supper': {
                        'from': meal_period[day]['supper'][0],
                        'to': meal_period[day]['supper'][-1]}
                    })
        except KeyError or ValueError:
            pass

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
        phone: 联系电话(最多3个，数组)
        facility: 设施(数组)
        pay_card: 可以刷哪些卡(数组)
        cuisine: 菜系(数组)
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

    if 'name' in kwargs:
        name = kwargs.pop('name')
        if HotelBranch.objects.filter(hotel=branch.hotel, name=name).exclude(
                id=branch_id).count() > 0:
            return err_response('err_7', '门店名已存在')

    branch_keys = ('province', 'city', 'county', 'address', 'is_enabled')
    branch_other_keys = ('phone', 'facility', 'pay_card', 'cuisine')

    for k in branch_keys:
        if k in kwargs:
            setattr(branch, k, kwargs[k])

    try:
        data = json.loads(request.body)
        for k in branch_other_keys:
            if k in data:
                v = json.dumps(data[k])
                setattr(branch, k, v)
    except KeyError or ValueError:
        return err_response('err_1', '参数不正确（缺少参数或者不符合格式）')

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
            return err_response('err_6', '图片为空或图片格式错误')

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
})
@validate_admin_token()
def modify_meal_period(request, token, branch_id):
    """修改门店的餐段

    :param token: 令牌(必传)
    :param branch_id: 酒店门店ID(必传)
    :param meal_period: 餐段设置, 格式如下
        [
            {
                "lunch": {
                    "from": "8:30",
                    "to": "12:00"
                },
                "dinner": {
                    "from": "12:00",
                    "to": "18:00"
                }
            },
            {
                "lunch": {
                    "from": "8:30",
                    "to": "12:00"
                },
                "dinner": {
                    "from": "12:00",
                    "to": "18:00"
                }
            },
            ...
        ]
    :return:
    """

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
            'Saturday', 'Sunday']

    try:
        branch = HotelBranch.objects.get(id=branch_id)
    except ObjectDoesNotExist:
        return err_response('err_4', '酒店不存在')

    # 解析餐段
    try:
        meal_period = json.loads(request.body)['meal_period']
        with open('data/meal_period.json') as json_file:
            data = json.load(json_file)
        result = {}
        for i in range(7):
            day = days[i]
            result[day] = {}
            # 午餐
            lunch = data['lunch']
            if 'lunch' in meal_period[i]:
                begin = meal_period[i]['lunch']['from']
                end = meal_period[i]['lunch']['to']
                result[day]['lunch'] = \
                    lunch[lunch.index(begin): lunch.index(end) + 1]
            # 晚餐
            dinner = data['dinner']
            if 'dinner' in meal_period[i]:
                begin = meal_period[i]['dinner']['from']
                end = meal_period[i]['dinner']['to']
                result[day]['dinner'] = \
                    dinner[dinner.index(begin): dinner.index(end) + 1]
            # 夜宵
            supper = data['supper']
            if 'supper' in meal_period[i]:
                begin = meal_period[i]['supper']['from']
                end = meal_period[i]['supper']['to']
                result[day]['supper'] = \
                    supper[supper.index(begin): supper.index(end) + 1]
        branch.meal_period = json.dumps(result)
        branch.save()
        return corr_response()
    except KeyError or ValueError:
        return err_response('err_1', '参数不正确（缺少参数或者不符合格式）')


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'branch_id': forms.IntegerField(),
})
@validate_admin_token()
def modify_personal_tailor(request, token, branch_id):
    """修改门店的私人订制项

    :param token: 令牌(必传)
    :param branch_id: 酒店门店ID(必传)
    :param personal_tailor: 私人订制项设置, 格式如下
        [
            {
                "name": "门牌",
                "labels": ["a", "b"],
                "order":1
            },
            {
                "name": "沙盘",
                "labels": ["a", "b"],
                "order":2
            },
            ...
        }
    :return:
    """

    try:
        branch = HotelBranch.objects.get(id=branch_id)
    except ObjectDoesNotExist:
        return err_response('err_4', '酒店不存在')

    # 解析私人订制项
    try:
        personal_tailor = json.loads(request.body)['personal_tailor']
        # 格式验证
        for p in personal_tailor:
            a = isinstance(p['name'], str)
            b = isinstance(p['labels'], list)
            c = isinstance(p['order'], int)
            if not (a and b and c):
                return err_response('err_1', '参数不正确（缺少参数或者不符合格式）')

        branch.personal_tailor = json.dumps(personal_tailor)
        branch.save()
        return corr_response()
    except KeyError or ValueError:
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
})
@validate_admin_token()
def delete_branch_picture(request, token, branch_id):
    """删除酒店门店介绍图片

    :param token: 令牌(必传)
    :param branch_id: 酒店ID(必传)
    :param pictures: 需要删除的酒店介绍图片, 数组, 最多5张
    :return:
    """

    try:
        branch = HotelBranch.objects.get(id=branch_id)
    except ObjectDoesNotExist:
        return err_response('err_4', '酒店不存在')

    try:
        picture_list = json.loads(request.body)['pictures']
    except KeyError or ValueError:
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
})
@validate_admin_token()
def get_areas(request, token, branch_id):
    """获取门店的餐厅区域列表

    :param token: 令牌(必传)
    :param branch_id: 门店ID(必传)
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
    areas = branch.areas.order_by('-order')

    l = [{'area_id': area.id,
          'name': area.name,
          'order': area.order,
          'is_enabled': area.is_enabled,
          'create_time': area.create_time} for area in areas]

    return corr_response({'count': c, 'list': l})


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'branch_id': forms.IntegerField()
})
@validate_admin_token()
def add_area(request, token, branch_id):
    """批量增加餐厅区域

    :param token: 令牌(必传)
    :param branch_id: 门店ID(必传)
    :param list(必传)
        name: 名称(必传)
        order: 排序(必传)
        is_enabled: 是否有效(必传)
    :return: 200
    """

    try:
        branch = HotelBranch.enabled_objects.get(id=branch_id)
    except ObjectDoesNotExist:
        return err_response('err_4', '酒店不存在')

    # 管理员只能管理自己酒店的门店
    if branch.hotel != request.admin.hotel:
        return err_response('err_2', '权限错误')

    # 检查区域名是否已存在
    try:
        l = json.loads(request.body)['list']
        for a in l:
            name = a['name']
            order = a['order']
            is_enabled = a['is_enabled']
            if not (isinstance(name, str) and isinstance(order, int) and isinstance(is_enabled, bool)):
                return err_response('err_1', '参数不正确（缺少参数或者不符合格式）')
            if branch.areas.filter(name=name).count() > 0:
                return err_response('err_5', '区域名已存在')
    except KeyError or ValueError:
        return err_response('err_1', '参数不正确（缺少参数或者不符合格式）')

    # 批量添加区域
    with transaction.atomic():
        for a in l:
            name = a['name']
            order = a['order']
            is_enabled = a['is_enabled']
            try:
                area = Area(name=name, order=order, is_enabled=is_enabled, branch=branch)
                area.save()
            except IntegrityError:
                return err_response('err_5', '服务器添加餐厅区域失败')

    return corr_response()


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32)
})
@validate_admin_token()
def modify_area(request, token):
    """批量修改餐厅区域信息

    :param token: 令牌(必传)
    :param list:
        name: 名称
        order: 排序
        is_enabled: 是否有效
    :return: 200
    """

    # 检查区域名是否已存在
    with transaction.atomic():
        try:
            l = json.loads(request.body)['list']
            for a in l:
                area_id = a['area_id']
                name = a['name']
                order = a['order']
                is_enabled = a['is_enabled']
                if not (isinstance(name, str) and isinstance(order, int) and isinstance(is_enabled, bool)):
                    return err_response('err_1', '参数不正确（缺少参数或者不符合格式）')

                area = Area.objects.get(id=area_id)

                if area.branch.hotel != request.admin.hotel:
                    return err_response('err_2', '权限错误')

                if area.branch.areas.filter(name=name).exclude(
                        id=area_id).count() > 0:
                    return err_response('err_5', '区域名重复')

                area.name = name
                area.order = order
                area.is_enabled = is_enabled
                area.save()
        except KeyError or ValueError:
            return err_response('err_1', '参数不正确（缺少参数或者不符合格式）')
        except ObjectDoesNotExist:
            return err_response('err_4', '酒店不存在')

    return corr_response()


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'area_id': forms.IntegerField(),
    'offset': forms.IntegerField(min_value=0, required=False),
    'limit': forms.IntegerField(min_value=0, required=False),
})
@validate_admin_token()
def get_desks(request, token, area_id, offset=0, limit=10):
    """获取门店的桌位列表

    :param token: 令牌(必传)
    :param area_id: 区域ID(必传)
    :param offset: 起始值
    :param limit: 偏移量
    :return:
        count: 桌位数
        list:
            desk_id: 桌位ID
            number: 编号
            order: 排序
            min_guest_num: 可容纳最小人数
            max_guest_num: 可容纳最大人数
            expense: 费用说明(数组)
            type: 房间类型
            facility: 房间设施（数组）
            picture: 图片
            is_beside_window: 是否靠窗
            description: 备注
            is_enabled: 是否有效
            create_time: 创建时间
    """

    try:
        area = Area.objects.get(id=area_id)
    except ObjectDoesNotExist:
        return err_response('err_4', '该区域不存在')

    # 只能查看自己酒店的门店区域
    if area.branch.hotel != request.admin.hotel:
        return err_response('err_2', '权限错误')

    c = area.desks.count()
    ds = area.desks.order_by('-order')[offset:offset + limit]

    l = [{'desk_id': desk.id,
          'number': desk.number,
          'order': desk.order,
          'min_guest_num': desk.min_guest_num,
          'max_guest_num': desk.max_guest_num,
          'expense': json.loads(desk.expense) if desk.expense else [],
          'type': desk.type,
          'facility': json.loads(desk.facility) if desk.facility else [],
          'picture': desk.picture,
          'is_enabled': desk.is_enabled,
          'is_beside_window': desk.is_beside_window,
          'description': desk.description,
          'create_time': desk.create_time} for desk in ds]

    return corr_response({'count': c, 'list': l})


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'desk_id': forms.IntegerField()
})
@validate_admin_token()
def get_desk_profile(request, token, desk_id):
    """获取桌位的详情

    :param token: 令牌(必传)
    :param desk_id: 桌位ID(必传)
    :return
        number: 桌位号
        order: 排序
        min_guest_num: 最小人数限制
        max_guest_num: 最大人数限制
        expense: 花费说明(数组)
        type: 桌位类型
        facility: 设施（数组）
        is_beside_window: 是否靠窗
        description: 描述
        is_enabled: 是否有效
        picture: 桌位介绍图片
    :return 200
    """
    try:
        desk = Desk.objects.get(id=desk_id)
    except ObjectDoesNotExist:
        return err_response('err_4', '该桌位不存在')

    # 只能查看自己酒店的桌位
    if desk.area.branch.hotel != request.admin.hotel:
        return err_response('err_2', '权限错误')

    d = {'desk_id': desk.id,
         'number': desk.number,
         'order': desk.order,
         'min_guest_num': desk.min_guest_num,
         'max_guest_num': desk.max_guest_num,
         'expense': json.loads(desk.expense) if desk.expense else [],
         'type': desk.type,
         'facility': json.loads(desk.facility) if desk.facility else [],
         'picture': desk.picture,
         'is_enabled': desk.is_enabled,
         'is_beside_window': desk.is_beside_window,
         'description': desk.description,
         'create_time': desk.create_time}

    return corr_response(d)


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'area_id': forms.IntegerField(),
    'number': forms.CharField(max_length=10),
    'order': forms.IntegerField(),
    'min_guest_num': forms.IntegerField(),
    'max_guest_num': forms.IntegerField(),
    'type': forms.CharField(max_length=10, required=False),
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
        facility: 设施(数组)
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

    if area.desks.filter(number=number).count() > 0:
        return err_response('err_5', '桌位已存在')

    desk_keys = ('min_guest_num', 'max_guest_num',
                 'type', 'facility', 'is_beside_window', 'description')
    with transaction.atomic():
        try:
            desk = Desk(number=number, order=order, area=area)

            for k in desk_keys:
                if k in kwargs:
                    setattr(desk, k, kwargs[k])

            try:
                data = json.loads(request.body)
                if 'facility' in data:
                    v = json.dumps(data['facility'])
                    setattr(desk, 'facility', v)

                if 'expense' in data:
                    v = json.dumps(data['expense'])
                    setattr(desk, 'expense', v)

            except KeyError or ValueError:
                return err_response('err_1', '参数不正确（缺少参数或者不符合格式）')

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
                    return err_response('err_6', '图片为空或图片格式错误')

            desk.save()
            return corr_response()
        except KeyError or ValueError:
            return err_response('err_1', '参数不正确（缺少参数或者不符合格式）')
        except IntegrityError:
            return err_response('err_7', '服务器创建桌位失败')


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'desk_id': forms.IntegerField(),
    'number': forms.CharField(max_length=10, required=False),
    'order': forms.IntegerField(required=False),
    'min_guest_num': forms.IntegerField(required=False),
    'max_guest_num': forms.IntegerField(required=False),
    'type': forms.CharField(max_length=10, required=False),
    'is_beside_window': forms.BooleanField(required=False),
    'description': forms.CharField(max_length=100, required=False),
    'is_enabled': forms.BooleanField(required=False)
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
        expense: 花费说明(数组)
        type: 桌位类型
        facility: 设施（数组）
        is_beside_window: 是否靠窗
        description: 描述
        is_enabled: 是否有效
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

    if 'number' in kwargs:
        if desk.area.desks.filter(number=kwargs['number']).\
                exclude(id=desk_id).count() > 0:
            return err_response('err_5', '桌位编号已存在')

    desk_keys = ('number', 'order', 'min_guest_num', 'max_guest_num',
                 'type', 'is_beside_window', 'description', 'is_enabled')

    try:
        data = json.loads(request.body)
        if 'expense' in data:
            v = json.dumps(data['expense'])
            setattr(desk, 'expense', v)
    except KeyError or ValueError:
        return err_response('err_1', '参数不正确（缺少参数或者不符合格式）')

    for k in desk_keys:
        if k in kwargs:
            setattr(desk, k, kwargs[k])

    try:
        if 'facility' in data:
            v = json.dumps(data['facility'])
            setattr(desk, 'facility', v)
    except KeyError or ValueError:
        return err_response('err_1', '参数不正确（缺少参数或者不符合格式）')

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
            return err_response('err_6', '图片为空或图片格式错误')

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
    'area_id': forms.IntegerField(),
    'guest_number': forms.IntegerField(),
    'offset': forms.IntegerField(min_value=0, required=False),
    'limit': forms.IntegerField(min_value=0, required=False),
})
@validate_admin_token()
def recommend_desks(request, token, area_id, guest_number, offset=0, limit=10):
    """自动推荐桌位列表

    :param token: 令牌(必传)
    :param area_id: 区域ID(必传)
    :param guest_number: 顾客人数(必传)
    :param offset: 起始值
    :param limit: 偏移量
    :return:
        count: 桌位数
        list:
            desk_id: 桌位ID
            number: 编号
            order: 排序
            min_guest_num: 可容纳最小人数
            max_guest_num: 可容纳最大人数
            expense: 费用说明(数组)
            type: 房间类型
            facility: 房间设施（数组）
            picture: 图片
            is_beside_window: 是否靠窗
            description: 备注
            is_enabled: 是否有效
            create_time: 创建时间
    """

    try:
        area = Area.objects.get(id=area_id)
    except ObjectDoesNotExist:
        return err_response('err_4', '该区域不存在')

    # 只能查看自己酒店的门店区域
    if area.branch.hotel != request.admin.hotel:
        return err_response('err_2', '权限错误')

    qs = area.desks.filter(min_guest_num__lte=guest_number,
                           max_guest_num__gte=guest_number)
    c = qs.count()
    ds = qs.order_by('-order')[offset:offset + limit]

    l = [{'desk_id': desk.id,
          'number': desk.number,
          'order': desk.order,
          'min_guest_num': desk.min_guest_num,
          'max_guest_num': desk.max_guest_num,
          'expense': json.loads(desk.expense) if desk.expense else [],
          'type': desk.type,
          'facility': json.loads(desk.facility) if desk.facility else [],
          'picture': desk.picture,
          'is_enabled': desk.is_enabled,
          'is_beside_window': desk.is_beside_window,
          'description': desk.description,
          'create_time': desk.create_time} for desk in ds]

    return corr_response({'count': c, 'list': l})


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32)
})
@validate_admin_token()
def modify_desks(request, token):
    """批量修改桌位

    :param token: 令牌(必传)
    :param list:
        number: 桌位号
        order: 排序
        is_enabled: 是否有效
    :return: 200
    """

    # 检查桌位编号是否已存在
    with transaction.atomic():
        try:
            l = json.loads(request.body)['list']
            for a in l:
                desk_id = a['desk_id']
                number = a['number']
                order = a['order']
                is_enabled = a['is_enabled']
                if not (isinstance(number, str) and isinstance(order, int) and
                        isinstance(is_enabled, bool)):
                    return err_response('err_1', '参数不正确（缺少参数或者不符合格式）')

                desk = Desk.objects.get(id=desk_id)

                if desk.area.branch.hotel != request.admin.hotel:
                    return err_response('err_2', '权限错误')

                if Desk.objects.filter(number=number).exclude(
                        id=desk_id).count() > 0:
                    return err_response('err_5', '桌位编号重复')

                desk.number = number
                desk.order = order
                desk.is_enabled = is_enabled
                desk.save()
        except KeyError or ValueError:
            return err_response('err_1', '参数不正确（缺少参数或者不符合格式）')
        except ObjectDoesNotExist:
            return err_response('err_4', '酒店不存在')

    return corr_response()


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32)
})
@validate_admin_token()
def get_channels(request, token):
    """获取客户的获客渠道

    :param token: 令牌
    :return:
        internal_channel: 内部销售
            id: ID
            phone: 手机
            name: 名称
            icon: 员工头像
            gender: 性别
            staff_number: 员工编号
            position: 职位
            guest_channel: 所属获客渠道
                0:无, 1:高层管理, 2:预定员和迎宾, 3:客户经理
            create_time: 创建时间
        external_channel: 外部销售
            id: ID
            name: 名称
            discount: 折扣
            icon: 头像
            begin_cooperate_time: 合作起始时间
            end_cooperate_time: 合作结束时间
            staff_name: 直属上级名称
            is_enabled: 是否有效
            create_time: 创建时间
    """

    hotel = request.admin.hotel

    in_channels = Staff.enabled_objects.exclude(hotel=hotel, guest_channel=0). \
        filter(status=1)
    list1 = [{'id': channel.id,
              'name': channel.name,
              'phone': channel.phone,
              'staff_number': channel.staff_number,
              'icon': channel.icon,
              'gender': channel.gender,
              'position': channel.position,
              'guest_channel': channel.guest_channel,
              'create_time': channel.create_time
              } for channel in in_channels]

    ex_channels = ExternalChannel.objects.all()
    list2 = [{'id': channel.id,
              'name': channel.name,
              'discount': channel.discount,
              'icon': channel.icon,
              'begin_cooperate_time': channel.begin_cooperate_time,
              'end_cooperate_time': channel.end_cooperate_time,
              'staff_name': channel.staff.name,
              'is_enabled': channel.is_enabled,
              'create_time': channel.name} for channel in ex_channels]

    return corr_response({'internal_channel': list1, 'external_channel': list2})


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'name': forms.CharField(max_length=20),
    'discount': forms.FloatField(required=False),
    'begin_cooperate_time': forms.DateField(required=False),
    'end_cooperate_time': forms.DateField(required=False),
    'commission_type': forms.IntegerField(required=False),
    'commission_value': forms.IntegerField(required=False),
    'staff_id': forms.IntegerField()
})
@validate_admin_token()
def add_external_channel(request, token, staff_id, name, **kwargs):
    """添加外部渠道

    :param token: 令牌(必传)
    :param staff_id: 直属上级ID(必传)
    :param name: 名称
    :param kwargs
        discount: 折扣
        begin_cooperate_time: 合作起始时间
        end_cooperate_time: 合作结束时间
        commission_type: 佣金核算方式, 0:无, 1:按消费额百分百比, 2:按订单数量, 3:按消费人数
        commission_value: 佣金核算数值
        icon: 头像[file]格式
    :return channel_id: 渠道ID
    """

    hotel = request.admin.hotel
    try:
        staff = hotel.staffs.get(id=staff_id)
    except ObjectDoesNotExist:
        return err_response('err_4', '员工不存在')

    channel_keys = ('discount', 'begin_cooperate_time', 'end_cooperate_time',
                    'commission_type', 'commission_value')

    with transaction.atomic():
        try:
            channel = ExternalChannel(staff=staff, name=name)
            for k in channel_keys:
                if k in kwargs:
                    setattr(channel, k, kwargs[k])

            # 添加头像
            if 'icon' in request.FILES:
                icon = request.FILES['icon']

                icon_time = timezone.now().strftime('%H%M%S%f')
                icon_tail = str(icon).split('.')[-1]
                dir_name = 'uploaded/icon/external_channel/%d/' % channel.id
                os.makedirs(dir_name, exist_ok=True)
                file_name = dir_name + '%s.%s' % (icon_time, icon_tail)
                try:
                    img = Image.open(icon)
                    img.save(file_name, quality=90)
                except OSError:
                    return err_response('err_5', '图片为空或图片格式错误')

                # 删除旧文件, 保存新的文件路径
                if channel.icon:
                    try:
                        os.remove(channel.icon)
                    except OSError:
                        pass
                channel.icon = file_name

            channel.save()
            return corr_response({'channel_id': channel.id})
        except IntegrityError:
            return err_response('err_6', '服务器创建外部渠道失败')


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'channel_id': forms.IntegerField(),
    'name': forms.CharField(max_length=20, required=False),
    'discount': forms.FloatField(required=False),
    'begin_cooperate_time': forms.DateField(required=False),
    'end_cooperate_time': forms.DateField(required=False),
    'commission_type': forms.IntegerField(required=False),
    'commission_value': forms.IntegerField(required=False),
    'staff_id': forms.IntegerField(required=False)
})
@validate_admin_token()
def modify_external_channel(request, token, channel_id, **kwargs):
    """修改外部渠道

    :param token: 令牌(必传)
    :param channel_id: 外部渠道ID(必传)
    :param kwargs
        staff_id: 直属上级ID
        name: 名称
        discount: 折扣
        icon: 头像[file]格式
        begin_cooperate_time: 合作起始时间
        end_cooperate_time: 合作结束时间
        commission_type: 佣金核算方式, 0:无, 1:按消费额百分百比, 2:按订单数量, 3:按消费人数
        commission_value: 佣金核算数值
        is_enabled: 是否有效
    :return channel_id: 渠道ID
    """

    hotel = request.admin.hotel

    try:
        channel = ExternalChannel.objects.get(id=channel_id)
    except ObjectDoesNotExist:
        return err_response('err_4', '外部渠道不存在')

    if channel.staff.hotel != hotel:
        return err_response('err_2', '权限错误')

    name = kwargs['name'] if 'name' in kwargs else ''
    if name:
        if ExternalChannel.objects.filter(staff__hotel=hotel, name=name). \
                exclude(id=channel_id).count() > 0:
            return err_response('err_5', '外部渠道名称已存在')

    staff_id = kwargs.pop('staff_id') if 'staff_id' in kwargs else None
    if staff_id:
        try:
            staff = Staff.enabled_objects.get(id=staff_id)
            if staff.hotel != hotel:
                return err_response('err_6', '员工不存在')
            channel.staff = staff
        except ObjectDoesNotExist:
            return err_response('err_6', '员工不存在')

    channel_keys = ('discount', 'begin_cooperate_time', 'end_cooperate_time',
                    'commission_type', 'commission_value', 'is_enabled')

    for k in channel_keys:
        if k in kwargs:
            setattr(channel, k, kwargs[k])

    # 修改头像
    if 'icon' in request.FILES:
        icon = request.FILES['icon']

        icon_time = timezone.now().strftime('%H%M%S%f')
        icon_tail = str(icon).split('.')[-1]
        dir_name = 'uploaded/icon/external_channel/%d/' % channel.id
        os.makedirs(dir_name, exist_ok=True)
        file_name = dir_name + '%s.%s' % (icon_time, icon_tail)
        try:
            img = Image.open(icon)
            img.save(file_name, quality=90)
        except OSError:
            return err_response('err_7', '图片为空或图片格式错误')

        # 删除旧文件, 保存新的文件路径
        if channel.icon:
            try:
                os.remove(channel.icon)
            except OSError:
                pass
        channel.icon = file_name

    channel.save()
    return corr_response()


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'channel_id': forms.IntegerField()
})
@validate_admin_token()
def get_external_channel_profile(request, token, channel_id):
    """获取外部渠道详情

    :param token: 令牌(必传)
    :param channel_id: 渠道ID(必传)
    :return:
        id: ID
        name: 名称
        discount: 折扣
        icon: 头像
        begin_cooperate_time: 合作起始时间
        end_cooperate_time: 合作结束时间
        commission_type: 佣金核算方式, 0:无, 1:按消费额百分百比, 2:按订单数量, 3:按消费人数
        commission_value: 佣金核算数值
        staff_id: 直属上级ID
        staff_name: 直属上级名称
        is_enabled: 是否有效
        create_time: 创建时间
    """

    try:
        channel = ExternalChannel.objects.get(id=channel_id)
    except ObjectDoesNotExist:
        return err_response('err_4', '渠道不存在')

    d = {'id': channel.id,
         'name': channel.name,
         'discount': channel.discount,
         'icon': channel.icon,
         'begin_cooperate_time': channel.begin_cooperate_time,
         'end_cooperate_time': channel.end_cooperate_time,
         'commission_type': channel.commission_type,
         'commission_value': channel.commission_value,
         'staff_id': channel.staff.id,
         'staff_name': channel.staff.name,
         'is_enabled': channel.is_enabled,
         'create_time': channel.name}

    return corr_response(d)


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'offset': forms.IntegerField(min_value=0, required=False),
    'limit': forms.IntegerField(min_value=0, required=False),
    'order': forms.IntegerField(min_value=0, max_value=3, required=False),
    'hotel_id': forms.IntegerField(),
})
@validate_admin_token()
def get_staffs(request, token, hotel_id, order=1):
    """获取酒店员工列表

    :param token: 令牌(必传)
    :param hotel_id: 酒店ID(必传)
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
            status: 状态,0:待审核,1:审核通过
            gender: 性别
            hotel_name: 员工所属酒店
            position: 职位
            guest_channel: 所属获客渠道
                0:无, 1:高层管理, 2:预定员和迎宾, 3:客户经理
            is_enabled: 是否有效
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

    c = hotel.staffs.count()
    staffs = hotel.staffs.order_by(ORDERS[order])

    l = [{'staff_id': s.id,
          'phone': s.phone,
          'name': s.name,
          'staff_number': s.staff_number,
          'icon': s.icon,
          'status': s.status,
          'gender': s.gender,
          'hotel_name': s.hotel.name,
          'position': s.position,
          'guest_channel': s.guest_channel,
          'authority': s.authority,
          'is_enabled': s.is_enabled,
          'create_time': s.create_time} for s in staffs]
    return corr_response({'count': c, 'list': l})


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'phone': forms.CharField(validators=[RegexValidator(regex=r'^[0-9]{11}$')]),
    'password': forms.CharField(min_length=1, max_length=32),
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
    'dinner_date_begin': forms.DateField(required=False),
    'dinner_date_end': forms.DateField(required=False),
    'dinner_period': forms.IntegerField(
        min_value=0, max_value=2, required=False),
    'status': forms.IntegerField(min_value=0, max_value=2, required=False),
    'search_key': forms.CharField(min_length=1, max_length=20, required=False),
    'offset': forms.IntegerField(min_value=0, required=False),
    'limit': forms.IntegerField(min_value=0, required=False),
    'order': forms.IntegerField(min_value=0, max_value=3, required=False),
})
@validate_admin_token()
def search_orders(request, token, status=0, offset=0, limit=10, order=1,
                  **kwargs):
    """搜索订单列表

    :param token: 令牌(必传)
    :param status: 订单状态, 0: 进行中(默认), 1: 已完成, 2: 已撤单
    :param offset: 起始值
    :param limit: 偏移量
    :param order: 排序方式
        0: 注册时间升序
        1: 注册时间降序（默认值）
    :param kwargs:
        search_key: 关键字
        dinner_date_begin: 预定用餐日期起始
        dinner_date_end: 预定用餐日期终止
        dinner_period: 餐段, 0: 午餐, 1: 晚餐, 2: 夜宵
    :return:
        count: 订单总数
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
            guest_number: 客人数量
            desks: 桌位, 数组
            internal_channel: 内部获客渠道, 即接单人名字, 如果存在
            external_channel: 外部获客渠道, 即外部渠道名称, 如果存在
    """
    ORDERS = ('create_time', '-create_time')

    if status == 0:
        rs = Order.objects.filter(Q(status__in=[0, 1]))
    elif status == 1:
        rs = Order.objects.filter(Q(status=2))
    else:
        rs = Order.objects.filter(Q(status=3))

    if 'search_key' in kwargs:
        rs = rs.filter(Q(name__icontains=kwargs['search_key']) |
                       Q(contact__icontains=kwargs['search_key']))

    if 'dinner_date_begin' in kwargs:
        rs = rs.filter(Q(dinner_date__gte=kwargs['dinner_date_begin']))

    if 'dinner_date_end' in kwargs:
        rs = rs.filter(Q(dinner_date__lte=kwargs['dinner_date_end']))

    if 'dinner_period' in kwargs:
        rs = rs.filter(Q(dinner_period=kwargs['dinner_period']))

    c = rs.count()
    rs = rs.order_by(ORDERS[order])[offset:offset + limit]

    l = []
    for r in rs:
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
             'internal_channel': r.internal_channel.name if
             r.internal_channel else '',
             'external_channel': r.external_channel.name if
             r.external_channel else ''}

        desks_list = json.loads(r.desks)
        d['desks'] = []
        for desk in desks_list:
            desk_id = int(desk[1:-1])
            d['desks'].append(desk_id)

        l.append(d)

    return corr_response({'count': c, 'list': l})


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'order_id': forms.IntegerField(),
})
@validate_admin_token()
def get_order_profile(request, token, order_id):
    """获取订单详情

    :param token: 令牌(必传)
    :param order_id: 订单ID(必传)
    :return
        dinner_date: 预定就餐日期
        dinner_time: 预定就餐时间
        dinner_period: 餐段, 0: 午餐, 1: 晚餐, 2: 夜宵
        status: 状态, 0: 已订, 1: 客到, 2: 已完成, 3: 已撤单
        banquet: 订单类型
        consumption: 消费金额
        name: 联系人
        guest_type: 顾客身份
        contact: 联系电话
        guest_number: 就餐人数
        desks: 预定桌位, 可以多桌, 数组, [{"desk_id":1,"number":"110"}, ...]
        user_description: 用户备注
        staff_description: 员工备注
        water_card: 水牌
        door_card: 门牌
        sand_table: 沙盘
        welcome_screen: 欢迎屏
        welcome_fruit: 迎宾水果的价格
        welcome_card: 欢迎卡
        pictures: 用户上传的图片(最多5张)
        group_photo: 用户上传的合照
        background_music: 背景音乐
        has_candle: 是否有糖果
        has_flower: 是否有鲜花
        has_balloon: 是否有气球
        create_time: 创建时间
        cancel_time: 撤销时间
        arrival_time: 客到时间
        finish_time: 完成时间
        internal_channel: 内部获客渠道, 即接单人名字, 如果存在
        external_channel: 外部获客渠道, 即外部渠道名称, 如果存在
    """

    try:
        order = Order.objects.get(id=order_id)
    except ObjectDoesNotExist:
        return err_response('err_4', '订单不存在')

    d = {'dinner_date': order.dinner_date,
         'dinner_time': order.dinner_time,
         'dinner_period': order.dinner_period,
         'status': order.status,
         'banquet': order.banquet,
         'consumption': order.consumption,
         'name': order.name,
         'contact': order.contact,
         'guest_type': Guest.objects.get(phone=order.contact).name
         if Guest.objects.filter(
             phone=order.contact).count() == 1 else '',
         'guest_number': order.guest_number,
         'user_description': order.user_description,
         'staff_description': order.staff_description,
         'water_card': order.water_card,
         'door_card': order.door_card,
         'sand_table': order.sand_table,
         'welcome_screen': order.welcome_screen,
         'welcome_fruit': order.welcome_fruit,
         'welcome_card': order.welcome_card,
         'pictures': json.loads(order.pictures) if order.pictures else [],
         'group_photo': order.group_photo,
         'background_music': order.background_music,
         'has_candle': order.has_candle,
         'has_flower': order.has_flower,
         'has_balloon': order.has_balloon,
         'create_time': order.create_time,
         'cancel_time': order.cancel_time,
         'arrival_time': order.arrival_time,
         'finish_time': order.finish_time,
         'internal_channel': order.internal_channel.name if
         order.internal_channel else '',
         'external_channel': order.external_channel.name if
         order.external_channel else '',
         'desks': []}

    desks_list = json.loads(order.desks)
    for desk in desks_list:
        desk_id = int(desk[1:-1])
        try:
            number = Desk.objects.get(id=desk_id).number
        except ObjectDoesNotExist:
            number = ''
        d['desks'].append({'desk_id': desk_id, 'number': number})

    return corr_response(d)


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'dinner_date': forms.DateField(),
    'dinner_time': forms.TimeField(),
    'dinner_period': forms.IntegerField(min_value=0, max_value=2),
    'name': forms.CharField(min_length=1, max_length=20),
    'contact': forms.RegexField(r'[0-9]{11}'),
    'guest_number': forms.IntegerField(),
    'banquet': forms.CharField(max_length=10, required=False),
    'staff_description': forms.CharField(max_length=100, required=False),
    'water_card': forms.CharField(max_length=10, required=False),
    'door_card': forms.CharField(max_length=10, required=False),
    'sand_table': forms.CharField(max_length=10, required=False),
    'welcome_screen': forms.CharField(max_length=10, required=False),
    'welcome_fruit': forms.IntegerField(required=False),
    'welcome_card': forms.CharField(max_length=10, required=False),
    'background_music': forms.CharField(max_length=20, required=False),
    'has_candle': forms.BooleanField(required=False),
    'has_flower': forms.BooleanField(required=False),
    'has_balloon': forms.BooleanField(required=False),
})
@validate_admin_token()
def submit_order(request, token, dinner_date, dinner_time,
                 dinner_period, **kwargs):
    """提交订单

    :param token: 令牌(必传)
    :param dinner_date: 预定就餐日期(必传)
    :param dinner_time: 预定就餐时间(必传)
    :param dinner_period: 餐段, 0: 午餐, 1: 晚餐, 2: 夜宵(必传)
    :param kwargs:
        name: 联系人(必传)
        contact: 联系电话(必传)
        guest_number: 就餐人数(必传)
        desks: 预定桌位, 可以多桌, 数组(必传)
        banquet: 宴会类型
        staff_description: 员工备注
        water_card: 水牌
        door_card: 门牌
        sand_table: 沙盘
        welcome_screen: 欢迎屏
        welcome_fruit: 迎宾水果的价格
        welcome_card: 欢迎卡
        background_music: 背景音乐
        has_candle: 是否有糖果
        has_flower: 是否有鲜花
        has_balloon: 是否有气球
    :return: order_id
    """

    # 下单日期校验
    if dinner_date < timezone.now().date():
        return err_response('err_1', '参数不正确（缺少参数或者不符合格式）')

    branch_list = []
    branch = None
    # 验证桌位是否存在和是否被预定
    try:
        desk_list = json.loads(request.body)['desks']
        for i in range(len(desk_list)):
            # 桌位号加首尾限定符
            desk_id = '$' + str(desk_list[i]) + '$'
            if not Desk.enabled_objects.filter(id=desk_list[i]).count() > 0:
                return err_response('err_4', '桌位不存在')

            # 查找订餐的门店
            branch = Desk.enabled_objects.get(id=desk_list[i]).area.branch
            if branch.id not in branch_list:
                branch_list.append(branch.id)

            if Order.objects.filter(dinner_date=dinner_date,
                                    dinner_time=dinner_time,
                                    dinner_period=dinner_period,
                                    status__in=[0, 1],
                                    desks__icontains=desk_id).count() > 0:
                return err_response('err_5', '桌位已被预定')
            desk_list[i] = desk_id
        desks = json.dumps(desk_list)
    except KeyError or ValueError:
        return err_response('err_1', '参数不正确（缺少参数或者不符合格式）')

    # 桌位验证
    if (len(branch_list) != 1) or (branch is None) or \
            (branch.hotel != request.admin.hotel):
        return err_response('err_4', '桌位不存在')

    order_keys = ('name', 'contact', 'guest_number', 'staff_description',
                  'water_card', 'door_card', 'sand_table', 'welcome_screen',
                  'welcome_fruit', 'welcome_card', 'background_music',
                  'has_candle', 'has_flower', 'has_balloon', 'banquet')

    with transaction.atomic():
        try:
            # todo 管理员预定时订单需绑定为前台
            order = Order(dinner_date=dinner_date, dinner_time=dinner_time,
                          dinner_period=dinner_period, desks=desks,
                          branch=branch)
            for k in order_keys:
                if k in kwargs:
                    setattr(order, k, kwargs[k])
            order.save()
            return corr_response({'order_id': order.id})
        except IntegrityError as e:
            print(e)
            return err_response('err_6', '服务器创建订单错误')


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'order_id': forms.IntegerField(),
    'status': forms.IntegerField(min_value=0, max_value=3, required=False),
    'banquet': forms.CharField(max_length=10, required=False),
    'dinner_date': forms.DateField(required=False),
    'dinner_time': forms.TimeField(required=False),
    'dinner_period': forms.IntegerField(
        min_value=0, max_value=2, required=False),
    'consumption': forms.IntegerField(min_value=0, required=False),
    'name': forms.CharField(min_length=1, max_length=20, required=False),
    'contact': forms.RegexField(r'[0-9]{11}', required=False),
    'guest_number': forms.IntegerField(required=False),
    'staff_description': forms.CharField(max_length=100, required=False),
    'water_card': forms.CharField(max_length=10, required=False),
    'door_card': forms.CharField(max_length=10, required=False),
    'sand_table': forms.CharField(max_length=10, required=False),
    'welcome_screen': forms.CharField(max_length=10, required=False),
    'welcome_fruit': forms.IntegerField(required=False),
    'welcome_card': forms.CharField(max_length=10, required=False),
    'background_music': forms.CharField(max_length=20, required=False),
    'has_candle': forms.BooleanField(required=False),
    'has_flower': forms.BooleanField(required=False),
    'has_balloon': forms.BooleanField(required=False),
})
@validate_admin_token()
def update_order(request, token, order_id, **kwargs):
    """修改订单

    :param token: 令牌(必传)
    :param order_id: 订单ID(必传)
    :param kwargs:
        status: 订单状态, 0: 已订, 1: 客到, 2: 已完成, 3: 已撤单
        banquet: 宴会类型
        dinner_date: 预定就餐日期
        dinner_time: 预定就餐时间
        dinner_period: 餐段, 0: 午餐, 1: 晚餐, 2: 夜宵
        consumption: 消费金额
        name: 联系人
        contact: 联系电话
        guest_number: 就餐人数
        desks: 预定桌位, 可以多桌, 数组
        staff_description: 员工备注
        water_card: 水牌
        door_card: 门牌
        sand_table: 沙盘
        welcome_screen: 欢迎屏
        welcome_fruit: 迎宾水果的价格
        welcome_card: 欢迎卡
        background_music: 背景音乐
        has_candle: 是否有糖果
        has_flower: 是否有鲜花
        has_balloon: 是否有气球
    """

    try:
        order = Order.objects.get(id=order_id)
    except ObjectDoesNotExist:
        return err_response('err_4', '订单不存在')

    if order.branch.hotel != request.admin.hotel:
        return err_response('err_2', '权限错误')

    order_keys = ('status', 'dinner_date', 'dinner_time', 'dinner_period',
                  'name', 'contact', 'guest_number', 'staff_description',
                  'water_card', 'door_card', 'sand_table', 'welcome_screen',
                  'welcome_fruit', 'welcome_card', 'background_music'
                  'has_candle', 'has_flower', 'has_balloon', 'consumption',
                  'banquet')

    # 下单日期校验
    if 'dinner_date' in kwargs:
        if kwargs['dinner_date'] < timezone.now().date():
            return err_response('err_1', '参数不正确（缺少参数或者不符合格式）')

    # 订单状态切换验证
    if 'status' in kwargs:
        status = kwargs['status']
        # 客到
        if status == 1 and order.status == 0:
            order.arrival_time = timezone.now()
        # 翻台
        elif status == 2 and order.status == 1:
            order.finish_time = timezone.now()
        # 撤单
        elif status == 3 and order.status != 2:
            order.cancel_time = timezone.now()
        else:
            return err_response('err_5', '订单状态切换非法')

    for k in order_keys:
        if k in kwargs:
            setattr(order, k, kwargs[k])
    order.save()

    # 如果换桌
    data = json.loads(request.body)
    if 'desks' in data:
        branch_list = []
        branch = None
        desk_list = data.pop('desks')
        # 验证桌位是否存在和是否被预定
        try:
            for i in range(len(desk_list)):
                # 桌位号加首尾限定符
                desk_id = '$' + str(desk_list[i]) + '$'
                if not Desk.enabled_objects.filter(id=desk_list[i]).count() > 0:
                    return err_response('err_5', '桌位不存在')

                # 查找订餐的门店
                branch = Desk.enabled_objects.get(id=desk_list[i]).area.branch
                if branch.id not in branch_list:
                    branch_list.append(branch.id)

                if Order.objects.exclude(id=order_id).filter(
                        dinner_date=order.dinner_date,
                        dinner_time=order_id.dinner_time,
                        dinner_period=order.dinner_period,
                        status__in=[0, 1],
                        desk__icontains=desk_id).count() > 0:
                    return err_response('err_6', '桌位已被预定')
                desk_list[i] = desk_id
            desks = json.dumps(desk_list)
            order.desks = desks
            order.save()
        except KeyError or ValueError:
            return err_response('err_1', '参数不正确（缺少参数或者不符合格式）')

        # 桌位验证
        if (len(branch_list) != 1) or (branch is None) or \
                (branch.hotel != request.admin.hotel):
            return err_response('err_5', '桌位不存在')

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
