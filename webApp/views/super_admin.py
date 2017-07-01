import os

from PIL import Image

from django import forms
from django.utils import timezone
from django.db import IntegrityError, transaction
from django.core.exceptions import ObjectDoesNotExist

from ..utils.decorator import validate_args, validate_super_admin_token
from ..utils.response import corr_response, err_response
from ..models import Admin, Hotel


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'is_enabled': forms.BooleanField(required=False),
    'offset': forms.IntegerField(min_value=0, required=False),
    'limit': forms.IntegerField(min_value=0, required=False),
    'order': forms.IntegerField(min_value=0, max_value=3, required=False),
})
@validate_super_admin_token()
def get_admins(request, token, is_enabled=True, offset=0, limit=10, order=1):
    """获取管理者列表

    :param token: 令牌(必传)
    :param is_enabled: 是否有效(默认有)
    :param offset: 起始值
    :param limit: 偏移量
    :param order: 排序方式
        0: 注册时间升序
        1: 注册时间降序（默认值）
        2: 昵称升序
        3: 昵称降序
    :return:
        count: 管理者总数
        list: 管理者列表
            admin_id: ID
            username: 用户名
            type: 类别, 0: 管理员, 1: 超级管理员
            hotel_name: 所属酒店名, 超级管理员不属于任何酒店
            authority: 权限
            is_enabled: 是否有效
            create_time: 创建时间
    """
    ORDERS = ('create_time', '-create_time', 'username', '-username')

    c = Admin.objects.filter(is_enabled=is_enabled).count()
    admins = Admin.objects.filter(is_enabled=is_enabled).order_by(
        ORDERS[order])[offset:offset + limit]
    l = [{'admin_id': a.id,
          'username': a.username,
          'type': a.type,
          'hotel_name': a.hotel.name if a.hotel else '',
          'authority': a.authority,
          'is_enabled': a.is_enabled,
          'create_time': a.create_time} for a in admins]
    return corr_response({'count': c, 'list': l})


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'username': forms.CharField(min_length=1, max_length=20),
    'password': forms.CharField(min_length=1, max_length=128),
    'type': forms.IntegerField(min_value=0, max_value=1, required=False),
    'hotel_id': forms.IntegerField(required=False),
})
@validate_super_admin_token()
def register(request, token, username, password, type=1, hotel_id=None):
    """注册新的管理员

    :param token: 令牌(必传)
    :param username: 用户名(必传)
    :param password: 密码(必传)
    :param type: 管理员类型, 0: 管理员, 1: 超级管理员
    :param hotel_id: 管理员所属酒店
    :return 200/400/403/404
    """

    if Admin.enabled_objects.filter(username=username).exists():
        return err_response('err_4', '该用户名已注册')

    if hotel_id is not None:
        if type == 0:
            try:
                hotel = Hotel.enabled_objects.get(id=hotel_id)
            except ObjectDoesNotExist:
                return err_response('err_3', '该酒店不存在')
            else:
                with transaction.atomic():
                    try:
                        admin = Admin(username=username, password=password,
                                      type=type, hotel=hotel)
                        admin.update_token()
                        admin.save()
                        return corr_response({'admin_id': admin.id})
                    except IntegrityError:
                        return err_response('error_5', '服务器创建管理员失败')
        else:
            return err_response('err_2', '权限错误')
    else:
        if type == 1:
            with transaction.atomic():
                try:
                    admin = Admin(username=username, password=password,
                                  type=type)
                    admin.update_token()
                    admin.save()
                    return corr_response({'admin_id': admin.id})
                except IntegrityError:
                    return err_response('error_5', '服务器创建管理员失败')
        else:
            return err_response('err_1', '参数不正确（缺少参数或者不符合格式）')


@validate_args({
    'admin_id': forms.IntegerField(required=False),
})
@validate_super_admin_token()
def delete_admin(request, token, admin_id):
    """删除管理员

    :param token: 令牌
    :param admin_id: 管理员ID(必传)
    :return: 200/404
    """

    try:
        admin = Admin.objects.get(id=admin_id)
    except Admin.DoesNotExist:
        return err_response('err_3', '管理员不存在')

    if admin == request.admin:
        return err_response('err_4', '操作错误')

    admin.is_enabled = False
    return corr_response()


@validate_args({
    'username': forms.CharField(min_length=1, max_length=20),
    'password': forms.CharField(min_length=1, max_length=128),
})
def login(request, token, username, password):
    """登录，更新并返回超级管理者令牌

    :param token: 令牌
    :param username: 用户名(必传)
    :param password: 密码(必传)
    :return token: 管理员token
    """

    try:
        admin = Admin.objects.get(username=username)
    except Admin.DoesNotExist:
        return err_response('err_2', '管理员不存在')
    else:
        if not admin.is_enabled:
            return err_response('err_2', '管理员不存在')
        if admin.type != 1:
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
    'is_enabled': forms.BooleanField(required=False),
    'offset': forms.IntegerField(min_value=0, required=False),
    'limit': forms.IntegerField(min_value=0, required=False),
    'order': forms.IntegerField(min_value=0, max_value=3, required=False),
})
@validate_super_admin_token()
def get_hotels(request, token, is_enabled=True, offset=0, limit=10, order=1):
    """获取酒店列表

    :param token: 令牌(必传)
    :param is_enabled: 是否有效, 默认:是
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
            is_enabled: 是否有效
            create_time: 创建时间
    """
    ORDERS = ('create_time', '-create_time', 'name', '-name')

    c = Hotel.objects.filter(is_enabled=is_enabled).count()
    hotels = Hotel.objects.filter(is_enabled=is_enabled).order_by(
        ORDERS[order])[offset:offset + limit]
    l = [{'hotel_id': h.id,
          'name': h.name,
          'icon': h.icon,
          'branches_count': h.branches.count(),
          'owner_name': h.owner_name,
          'is_enabled': h.is_enabled,
          'create_time': h.create_time} for h in hotels]
    return corr_response({'count': c, 'list': l})


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'name': forms.CharField(min_length=1, max_length=20),
    'owner_name': forms.CharField(min_length=1, max_length=20),
})
@validate_super_admin_token()
def register_hotel(request, token, name, owner_name):
    """注册新酒店

    :param token: 令牌(必传)
    :param name: 名称(必传)
    :param owner_name: 法人代表(必传)
    :return 200
    """

    if Hotel.enabled_objects.filter(name=name).exists():
        return err_response('err_4', '酒店名已注册')
    try:
        hotel = Hotel.objects.create(name=name, owner_name=owner_name)
        return corr_response({'hotel_id': hotel.id})
    except IntegrityError:
        return err_response('err_5', '服务器创建酒店失败')


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'hotel_id': forms.IntegerField(),
})
@validate_super_admin_token()
def delete_hotel(request, token, hotel_id):
    """删除酒店

    :param token: 令牌(必传)
    :param hotel_id: 酒店ID(必传)
    :return: 200/404
    """

    try:
        hotel = Hotel.objects.get(id=hotel_id)
    except Hotel.DoesNotExist:
        return err_response('err_4', '酒店不存在')
    else:
        hotel.is_enabled = False
        hotel.save()
        return corr_response()


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'hotel_id': forms.IntegerField(),
})
@validate_super_admin_token()
def get_hotel_profile(request, token, hotel_id):
    """获取酒店信息

    :param token: 令牌(必传)
    :param hotel_id: 酒店ID(必传)
    :return:
        hotel_id: ID
        name: 名称
        icon: 头像
        branches_count: 门店数
        owner_name: 法人代表
        is_enabled: 是否有效
        create_time: 创建时间
    """

    try:
        hotel = Hotel.objects.get(id=hotel_id)
    except Hotel.DoesNotExist:
        return err_response('err_4', '酒店不存在')
    else:
        d = {'hotel_id': hotel.id,
             'name': hotel.name,
             'icon': hotel.icon,
             'branches_count': hotel.branches.count(),
             'owner_name': hotel.owner_name,
             'is_enabled': hotel.is_enabled,
             'create_time': hotel.create_time}
        return corr_response(d)


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'name': forms.CharField(min_length=1, max_length=20, required=False),
    'owner_name': forms.CharField(min_length=1, max_length=20,
                                  required=False),
    'hotel_id': forms.IntegerField(),
})
@validate_super_admin_token()
def modify_hotel_profile(request, token, hotel_id, **kwargs):
    """修改酒店信息

    :param token: 令牌(必传)
    :param hotel_id: 酒店ID(必传)
    :param kwargs:
        name: 名称
        owner_name: 法人代表
        icon: 头像[file]
    :return: 200/400/403/404
    """

    try:
        hotel = Hotel.enabled_objects.get(id=hotel_id)
    except Hotel.DoesNotExist:
        return err_response('err_4', '酒店不存在')

    name = kwargs.pop('name') if 'name' in kwargs else None
    if name:
        if Hotel.enabled_objects.filter(name=name).exists():
            return err_response('err_5', '酒店名已注册')
        hotel.name = name

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

    hotel_keys = ('owner_name', 'is_enabled')
    for k in hotel_keys:
        if k in kwargs:
            setattr(hotel, k, kwargs[k])

    hotel.save()
    return corr_response()
