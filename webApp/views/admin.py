import os
import string
import json
import datetime

from datetime import timedelta
from PIL import Image
from random import choice
from django import forms
from django.db import IntegrityError, transaction
from django.db.models import Q, Sum
from django.utils import timezone
from django.core.validators import RegexValidator
from django.core.exceptions import ObjectDoesNotExist

from ..utils.response import corr_response, err_response
from ..utils.decorator import validate_args, validate_json_args,\
    validate_admin_token
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
    'new_password': forms.CharField(min_length=1, max_length=32),
    'old_password': forms.CharField(min_length=1, max_length=32),
})
@validate_admin_token()
def modify_password(request, token, old_password, new_password):
    """修改密码

    :param token: 令牌(必传)
    :param old_password: 旧密码(md5加密结果, 32位, 必传)
    :param new_password: 新密码(md5加密结果, 32位, 必传)
    :return 200/403
    """

    if request.admin.password == old_password:
        request.admin.password = new_password
        return corr_response({'admin_id': request.admin.id})
    return err_response('err_3', '旧密码错误')


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
        positions: 职位列表
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
         'positions': json.loads(hotel.positions) if hotel.positions else [],
         'create_time': hotel.create_time}
    return corr_response(d)


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'name': forms.CharField(min_length=1, max_length=20, required=False),
    'owner_name': forms.CharField(min_length=1, max_length=20,
                                  required=False),
    'hotel_id': forms.IntegerField(),
})
@validate_json_args({
    'positions': forms.CharField(max_length=1000, required=False)
})
@validate_admin_token()
def modify_hotel_profile(request, token, hotel_id, **kwargs):
    """修改酒店信息

    :param token: 令牌(必传)
    :param hotel_id: 酒店ID(必传)
    :param kwargs:
        name: 酒店名
        owner_name: 法人代表
        positions: 职位列表
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

    if 'positions' in kwargs:
        hotel.positions = json.dumps(kwargs['positions'])

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
        branch_id: 门店ID
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
        hotel_id: 酒店ID
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
         'hotel_id': branch.hotel.id,
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
@validate_json_args({
    'phone': forms.CharField(max_length=50, required=False),
    'facility': forms.CharField(max_length=640, required=False),
    'pay_card': forms.CharField(max_length=120, required=False),
    'cuisine': forms.CharField(max_length=1000, required=False)
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
    for k in branch_keys:
        if k in kwargs:
            setattr(branch, k, kwargs[k])

    branch_json_keys = ('phone', 'facility', 'pay_card', 'cuisine')
    for k in branch_json_keys:
        if k in kwargs:
            setattr(branch, k, json.dumps(kwargs[k]))

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
@validate_json_args({
    'meal_period': forms.CharField(max_length=5000)
})
@validate_admin_token()
def modify_meal_period(request, token, branch_id, meal_period):
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
@validate_json_args({
    'personal_tailor': forms.CharField(max_length=2000)
})
@validate_admin_token()
def modify_personal_tailor(request, token, branch_id, personal_tailor):
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
    'area_id': forms.IntegerField(required=False),
    'branch_id': forms.IntegerField(required=False),
    'offset': forms.IntegerField(min_value=0, required=False),
    'limit': forms.IntegerField(min_value=0, required=False),
})
@validate_admin_token()
def get_desks(request, token, area_id=None, branch_id=None, offset=0, limit=10):
    """获取门店的桌位列表

    :param token: 令牌(必传)
    :param area_id: 区域ID，不传返回所有区域桌位
    :param branch_id: 门店ID，不传area_id时传
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

    if area_id:
        try:
            area = Area.objects.get(id=area_id)
        except ObjectDoesNotExist:
            return err_response('err_4', '该区域不存在')

        # 只能查看自己酒店的门店区域
        if area.branch.hotel != request.admin.hotel:
            return err_response('err_2', '权限错误')

        c = area.desks.count()
        ds = area.desks.order_by('-order')[offset:offset + limit]
    elif branch_id:
        try:
            branch = HotelBranch.objects.get(id=branch_id)
        except ObjectDoesNotExist:
            return err_response('err_4', '该门店不存在')

        # 只能查看自己酒店的门店区域
        if branch.hotel != request.admin.hotel:
            return err_response('err_2', '权限错误')

        qs = Desk.objects.filter(area__branch=branch)
        c = qs.count()
        ds = qs.order_by('-order')[offset:offset + limit]
    else:
        return err_response('err_1', '参数不正确（缺少参数或者不符合格式）')

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
    'description': forms.CharField(max_length=200, required=False),
})
@validate_json_args({
    'facility': forms.CharField(max_length=120, required=False),
    'expense': forms.CharField(max_length=500, required=False)
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
    desk_json_keys = ('facility', 'expense')

    with transaction.atomic():
        try:
            desk = Desk(number=number, order=order, area=area)

            for k in desk_keys:
                if k in kwargs:
                    setattr(desk, k, kwargs[k])

            for k in desk_json_keys:
                if k in kwargs:
                    setattr(desk, k, json.dumps(kwargs[k]))

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
    'description': forms.CharField(max_length=200, required=False),
    'is_enabled': forms.BooleanField(required=False)
})
@validate_json_args({
    'facility': forms.CharField(max_length=120, required=False),
    'expense': forms.CharField(max_length=500, required=False)
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
    for k in desk_keys:
        if k in kwargs:
            setattr(desk, k, kwargs[k])

    desk_json_keys = ('facility', 'expense')
    for k in desk_json_keys:
        if k in kwargs:
            setattr(desk, k, json.dumps(kwargs[k]))

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
    'branch_id': forms.IntegerField(),
    'guest_number': forms.IntegerField(),
    'offset': forms.IntegerField(min_value=0, required=False),
    'limit': forms.IntegerField(min_value=0, required=False),
})
@validate_admin_token()
def recommend_desks(request, token, branch_id, guest_number, offset=0, limit=10):
    """自动推荐桌位列表

    :param token: 令牌(必传)
    :param branch_id: 门店ID(必传)
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
        branch = HotelBranch.objects.get(id=branch_id)
    except ObjectDoesNotExist:
        return err_response('err_4', '该门店不存在')

    # 只能查看自己酒店的门店区域
    if branch.hotel != request.admin.hotel:
        return err_response('err_2', '权限错误')

    qs = Desk.objects.filter(area__branch=branch,
                             min_guest_num__lte=guest_number,
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
            authority: 职能权限
            guest_channel: 所属获客渠道
                0:无, 1:高层管理, 2:预定员和迎宾, 3:客户经理
            phone_private: 电话隐私
            sale_enabled: 销售职能
            order_sms_inform: 订单短信
            order_sms_attach: 短信附加
            order_bonus: 提成结算/接单提成(消费额百分比, 按订单数量, 按消费人数)
            new_customer_bonus: 提成结算/开新客提成(消费额百分比, 按订单数量, 按消费人数)
            manage_desks: 管辖桌位
            manage_areas: 管辖区域
            manage_channel: 管理渠道客户
            communicate: 沟通渠道
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

    in_channels = Staff.enabled_objects.filter(hotel=hotel, status=1). \
        exclude(guest_channel=0)
    list1 = [{'id': channel.id,
              'name': channel.name,
              'phone': channel.phone,
              'staff_number': channel.staff_number,
              'icon': channel.icon,
              'gender': channel.gender,
              'position': channel.position,
              'authority': json.loads(channel.authority)
              if channel.authority else [],
              'guest_channel': channel.guest_channel,
              'phone_private': channel.phone_private,
              'sale_enabled': channel.sale_enabled,
              'order_sms_inform': channel.order_sms_inform,
              'order_sms_attach': channel.order_sms_attach,
              'order_bonus': json.loads(channel.order_bonus)
              if channel.order_bonus else {},
              'new_customer_bonus': json.loads(channel.new_customer_bonus)
              if channel.new_customer_bonus else {},
              'manage_desks': json.loads(channel.manage_desks)
              if channel.manage_desks else [],
              'manage_areas': json.loads(channel.manage_areas)
              if channel.manage_areas else [],
              'manage_channel': json.loads(channel.manage_channel)
              if channel.manage_channel else [],
              'communicate': json.loads(channel.communicate)
              if channel.communicate else {},
              'create_time': channel.create_time
              } for channel in in_channels]

    ex_channels = ExternalChannel.objects.filter(staff__hotel=hotel)
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
          'authority': json.loads(s.authority) if s.authority else [],
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
    'description': forms.CharField(max_length=200, required=False),
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

    if Staff.objects.filter(phone=phone).count() > 0:
        return err_response('err_5', '该手机号已注册')
    id_number = kwargs['id_number']
    if Staff.objects.filter(id_number=id_number).count() > 0:
        return err_response('err_6', '该身份证已注册')

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
                    return err_response('err_7', '图片为空或图片格式错误')

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
            return err_response('err_8', '服务器创建员工失败')


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
        phone_private: 电话隐私
        sale_enabled: 销售职能
        order_sms_inform: 订单短信
        order_sms_attach: 短信附加
        order_bonus: 提成结算/接单提成 0:消费额百分比, 1:按订单数量, 2:按消费人数
        new_customer_bonus: 提成结算/开新客提成
                0:消费额百分比, 1:按订单数量, 2:按消费人数
        manage_desks: 管辖桌位
        manage_areas: 管辖区域
        manage_channel: 管理渠道客户
        communicate: 沟通渠道
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
         'authority': json.loads(staff.authority) if staff.authority else [],
         'phone_private': staff.phone_private,
         'sale_enabled': staff.sale_enabled,
         'order_sms_inform': staff.order_sms_inform,
         'order_sms_attach': staff.order_sms_attach,
         'order_bonus': json.loads(staff.order_bonus)
         if staff.order_bonus else {},
         'new_customer_bonus': json.loads(staff.new_customer_bonus)
         if staff.new_customer_bonus else {},
         'manage_desks': json.loads(staff.manage_desks)
         if staff.manage_desks else [],
         'manage_areas': json.loads(staff.manage_areas)
         if staff.manage_areas else [],
         'manage_channel': json.loads(staff.manage_channel)
         if staff.manage_channel else [],
         'communicate': json.loads(staff.communicate)
         if staff.communicate else {},
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
    'description': forms.CharField(max_length=200, required=False),
    'authority': forms.CharField(max_length=20, required=False),
    'status': forms.IntegerField(required=False),
    'is_enabled': forms.BooleanField(required=False),
    'staff_id': forms.IntegerField(),
    'phone_private': forms.BooleanField(required=False),
    'sale_enabled': forms.BooleanField(required=False),
    'order_sms_inform': forms.BooleanField(required=False),
    'order_sms_attach': forms.BooleanField(required=False),
})
@validate_json_args({
    'order_bonus': forms.CharField(max_length=60, required=False),
    'new_customer_bonus': forms.CharField(max_length=60, required=False),
    'manage_desks': forms.CharField(max_length=1000, required=False),
    'manage_areas': forms.CharField(max_length=500, required=False),
    'manage_channel': forms.CharField(max_length=1000, required=False),
    'communicate': forms.CharField(max_length=800, required=False),
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
        phone_private: 电话隐私
        sale_enabled: 销售职能
        order_sms_inform: 订单短信
        order_sms_attach: 短信附加
        order_bonus: 提成结算/接单提成(按消费额百分比, 按订单数量, 按消费人数)
        new_customer_bonus: 提成结算/开新客提成(按消费额百分比, 按订单数量, 按消费人数)
        manage_desks: 管辖桌位
        manage_areas: 管辖区域
        manage_channel: 管理渠道客户
        communicate: 沟通渠道
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
                  'description', 'authority', 'status', 'is_enabled',
                  'phone_private', 'sale_enabled', 'order_sms_inform',
                  'order_sms_attach')
    for k in staff_keys:
        if k in kwargs:
            setattr(staff, k, kwargs[k])

    staff_json_keys = ('order_bonus', 'new_customer_bonus', 'manage_desks',
                       'manage_areas', 'manage_channel', 'communicate')
    for k in staff_json_keys:
        if k in kwargs:
            setattr(staff, k, json.dumps(kwargs[k]))

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
    'date_from': forms.DateField(required=False),
    'date_to': forms.DateField(required=False),
    'dinner_period': forms.IntegerField(
        min_value=0, max_value=2, required=False),
    'status': forms.IntegerField(min_value=0, max_value=2, required=False),
    'is_FIT': forms.BooleanField(required=False),
    'search_key': forms.CharField(min_length=1, max_length=20, required=False),
    'offset': forms.IntegerField(min_value=0, required=False),
    'limit': forms.IntegerField(min_value=0, required=False),
    'order': forms.IntegerField(min_value=0, max_value=3, required=False),
})
@validate_admin_token()
def search_orders(request, token, status=0, offset=0, limit=10, order=1,
                  is_FIT=False, **kwargs):
    """搜索订单列表

    :param token: 令牌(必传)
    :param status: 订单状态, 0: 进行中(默认), 1: 已完成, 2: 已撤单
    :param offset: 起始值
    :param limit: 偏移量
    :param order: 排序方式
        0: 注册时间升序
        1: 注册时间降序（默认值）
    :param is_FIT: 是否是散客，默认否
    :param kwargs:
        search_key: 关键字
        date_from: 起始时间
        date_to: 终止时间
        dinner_period: 餐段, 0: 午餐, 1: 晚餐, 2: 夜宵
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
            gender: 性别
            contact: 联系电话
            guest_number: 客人数量
            table_count: 餐位数
            staff_description: 员工备注
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

    if is_FIT:
        rs = rs.filter(Q(contact=''))
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

    if 'dinner_period' in kwargs:
        rs = rs.filter(Q(dinner_period=kwargs['dinner_period']))

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
             'gender': r.gender,
             'guest_type': Guest.objects.get(phone=r.contact).name
             if Guest.objects.filter(phone=r.contact).count() == 1 else '',
             'contact': r.contact,
             'guest_number': r.guest_number,
             'table_count': r.table_count,
             'staff_description': r.staff_description,
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

    return corr_response({'count': c,
                          'consumption': consumption,
                          'guest_number': guest_number,
                          'guest_consumption': guest_consumption,
                          'list': l})


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
        gender: 性别
        guest_type: 顾客身份
        contact: 联系电话
        guest_number: 就餐人数
        table_count: 餐桌数
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
         'gender': order.gender,
         'guest_type': Guest.objects.get(phone=order.contact).name
         if Guest.objects.filter(
             phone=order.contact).count() == 1 else '',
         'guest_number': order.guest_number,
         'table_count': order.table_count,
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
    'contact': forms.CharField(max_length=11),
    'gender': forms.IntegerField(min_value=0, max_value=2, required=False),
    'guest_number': forms.IntegerField(),
    'table_count': forms.IntegerField(required=False),
    'banquet': forms.CharField(max_length=10, required=False),
    'staff_description': forms.CharField(max_length=200, required=False),
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
@validate_json_args({
    'desks': forms.CharField(max_length=200)
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
        gender: 性别
        guest_number: 就餐人数(必传)
        table_count: 餐桌数(必传)
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
        desk_list = kwargs['desks']
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
                  'has_candle', 'has_flower', 'has_balloon', 'banquet',
                  'table_count', 'gender')

    # 验证门牌是否重复
    if 'door_card' in kwargs:
        door_card = kwargs['door_card']
        if Order.objects.filter(branch=branch,
                                dinner_date=dinner_date,
                                dinner_time=dinner_time,
                                dinner_period=dinner_period,
                                status__in=[0, 1],
                                door_card=door_card).count() > 0:
            return err_response('err_7', '门牌重复')

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
    'contact': forms.CharField(max_length=11, required=False),
    'gender': forms.IntegerField(min_value=0, max_value=2, required=False),
    'guest_number': forms.IntegerField(required=False),
    'table_count': forms.IntegerField(required=False),
    'staff_description': forms.CharField(max_length=200, required=False),
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
@validate_json_args({
    'desks': forms.CharField(max_length=200)
})
@validate_admin_token()
def modify_order(request, token, order_id, **kwargs):
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
        gender: 性别
        guest_number: 就餐人数
        table_count: 餐桌数
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
                  'banquet', 'table_count', 'gender')

    # 如果换门牌, 验证门牌是否重复
    if 'door_card' in kwargs:
        dinner_date = kwargs['dinner_date'] if \
            'dinner_date' in kwargs else order.dinner_date
        dinner_time = kwargs['dinner_time'] if \
            'dinner_time' in kwargs else order.dinner_time
        dinner_period = kwargs['dinner_period'] if \
            'dinner_period' in kwargs else order.dinner_period,
        door_card = kwargs['door_card']
        if Order.objects.filter(branch=order.branch,
                                dinner_date=dinner_date,
                                dinner_time=dinner_time,
                                dinner_period=dinner_period,
                                status__in=[0, 1],
                                door_card=door_card). \
                exclude(id=order.id).count() > 0:
            return err_response('err_7', '门牌重复')

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

    # 如果换桌
    if 'desks' in kwargs:
        branch_list = []
        branch = None
        desk_list = kwargs['desks']
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
        except KeyError or ValueError:
            return err_response('err_1', '参数不正确（缺少参数或者不符合格式）')

        # 桌位验证
        if (len(branch_list) != 1) or (branch is None) or \
                (branch.hotel != request.admin.hotel):
            return err_response('err_5', '桌位不存在')

    for k in order_keys:
        if k in kwargs:
            setattr(order, k, kwargs[k])
    order.save()

    return corr_response()


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
@validate_admin_token()
def search_guest(request, token, offset=0, limit=10, order=0, **kwargs):
    """获取客户列表(搜索)

    :param token: 令牌(必传)
    :param offset: 起始值
    :param limit: 偏移量
    :param order: 排序方式: 0: 最近就餐，1: 总预定桌数，2: 人均消费，3: 消费频度，默认0
    :param kwargs:
        search_key: 搜索关键字, 姓名或手机号
        status: 客户类型, 0: 全部, 1: 活跃, 2: 沉睡, 3: 流失, 4: 无订单
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
            unit: 单位
            position: 职位
            status: 客户状态, 1: 活跃, 2: 沉睡, 3: 流失, 4: 无订单
            desk_number: 消费总桌数
            person_consumption: 人均消费
            order_per_month: 消费频度, 单/月
            last_consumption: 上次消费日期
    """

    hotel = request.admin.hotel

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
            return err_response('err_5', '外部销售渠道不存在')
        qs = qs.filter(Q(external_channel=ex_channel))

    c = qs.count()
    guests = qs[offset:offset + limit]

    # 按最近就餐时间先后排序
    guest_list = list()
    if order == 0:
        for g in guests:
            guest_list.append((g, g.last_consumption))
    # 总预定桌数
    elif order == 1:
        for g in guests:
            guest_list.append((g, g.desk_number))
    # 人均消费
    elif order == 2:
        for g in guests:
            guest_list.append((g, g.person_consumption))
    # 消费频度
    else:
        for g in guests:
            guest_list.append((g, g.order_per_month))

    # 排序
    sorted_guest_list = sorted(guest_list, key=lambda x: x[1], reverse=True)

    l = []
    for guest_tuple in sorted_guest_list:
        guest = guest_tuple[0]
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
    'guest_id': forms.IntegerField(required=False),
    'phone': forms.CharField(max_length=11, required=False),
})
@validate_admin_token()
def get_guest_profile(request, token, guest_id=None, phone=None):
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
        unit: 单位
        position: 职位
        status: 客户状态, 1: 活跃, 2: 沉睡, 3: 流失, 4: 无订单
        all_order_number: 历史所有有效订单数
        day60_order_number: 最近60天订单数
        all_consumption: 所有有效消费
        day60_consumption: 最近60天消费金额
    """

    hotel = request.admin.hotel

    if guest_id:
        try:
            guest = Guest.objects.get(id=guest_id, hotel=hotel)
        except ObjectDoesNotExist:
            return err_response('err_4', '客户不存在')
    elif phone:
        try:
            guest = Guest.objects.get(phone=phone, hotel=hotel)
        except ObjectDoesNotExist:
            return err_response('err_4', '客户不存在')
    else:
        return err_response('err_1', '参数不正确（缺少参数或者不符合格式）')

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
         'unit': guest.unit,
         'position': guest.position,
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
    'personal_need': forms.CharField(max_length=100, required=False),
    'unit': forms.CharField(max_length=60, required=False),
    'position': forms.CharField(max_length=20, required=False),
})
@validate_admin_token()
def add_guest(request, token, phone, name, **kwargs):
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

    hotel = request.admin.hotel

    if Guest.objects.filter(hotel=hotel, phone=phone).exists():
        return err_response('err_4', '该手机号已经存在')

    guest_keys = ('guest_type', 'gender', 'birthday', 'birthday_type', 'like',
                  'dislike', 'special_day', 'personal_need', 'unit', 'position')
    with transaction.atomic():
        try:
            guest = Guest(hotel=hotel, phone=phone, name=name)
            for k in guest_keys:
                if k in kwargs:
                    setattr(guest, k, kwargs[k])
            guest.save()
            return corr_response({'guest_id': guest.id})
        except IntegrityError:
            return err_response('err_5', '服务器创建员工错误')


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
    'personal_need': forms.CharField(max_length=100, required=False),
    'unit': forms.CharField(max_length=60, required=False),
    'position': forms.CharField(max_length=20, required=False),
})
@validate_admin_token()
def modify_guest(request, token, phone, **kwargs):
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

    hotel = request.admin.hotel
    try:
        guest = Guest.objects.get(hotel=hotel, phone=phone)
    except ObjectDoesNotExist:
        return err_response('err_4', '客户不存在')

    guest_keys = ('guest_type', 'gender', 'birthday', 'birthday_type', 'like',
                  'dislike', 'special_day', 'personal_need', 'unit', 'position')

    for k in guest_keys:
        if k in kwargs:
            setattr(guest, k, kwargs[k])
    guest.save()
    return corr_response({'guest_id': guest.id})


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
    'description': forms.CharField(max_length=200, required=False),
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
    'description': forms.CharField(max_length=200, required=False),
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
