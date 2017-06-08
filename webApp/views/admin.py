import os

from PIL import Image

from django import forms
from django.db import IntegrityError, transaction
from django.utils import timezone
from ..utils.response import corr_response, err_response
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist

from ..utils.decorator import validate_args, validate_admin_token
from ..models import Admin, Hotel, HotelBranch, Staff

__all__ = ['Token', 'HotelProfile', 'HotelIcon', 'HotelBranchList',
           'StaffList', 'StaffProfile']


class Token(View):
    @validate_args({
        'username': forms.CharField(min_length=1, max_length=20),
        'password': forms.CharField(min_length=1, max_length=128),
    })
    def post(self, request, username, password):
        """更新并返回管理者令牌

        :param username: 用户名(必传)
        :param password: 密码(必传)
        :return token: 管理员token
        """

        try:
            admin = Admin.objects.get(username=username)
        except Admin.DoesNotExist:
            err_response('err_2', '管理员不存在')
        else:
            if not admin.is_enabled:
                err_response('err_2', '管理员不存在')
            if admin.password != password:
                err_response('err_4', '密码错误')
            admin.update_token()
            admin.save()
            corr_response({'token': admin.token})


class HotelProfile(View):
    @validate_args({
        'token': forms.CharField(min_length=32, max_length=32),
        'name': forms.CharField(min_length=1, max_length=20, required=False),
        'owner_name': forms.CharField(min_length=1, max_length=20,
                                      required=False),
        'hotel_id': forms.IntegerField(),
    })
    @validate_admin_token()
    def post(self, request, token, hotel_id, **kwargs):
        """修改酒店信息

        :param token: 令牌(必传)
        :param hotel_id: 酒店ID(必传)
        :param kwargs:
            name: 酒店名
            owner_name: 法人代表
        :return: 200/400/403/404
        """

        hotel = None
        try:
            hotel = Hotel.objects.get(id=hotel_id)
        except Hotel.DoesNotExist:
            err_response('err_2', '酒店不存在')

        name = kwargs.pop('name') if 'name' in kwargs else None
        owner_name = kwargs.pop('owner_name') if \
            'owner_name' in kwargs else None
        if name:
            if Hotel.objects.filter(name=name).exists():
                err_response('err_2', '酒店名已注册')
            hotel.name = name

        if owner_name:
            hotel.owner_name = owner_name
        hotel.save()
        corr_response()


class HotelIcon(View):
    @validate_args({
        'token': forms.CharField(min_length=32, max_length=32),
        'hotel_id': forms.IntegerField(),
    })
    @validate_admin_token()
    def get(self, request, token, hotel_id):
        """获取头像

        :param token: 令牌(必传)
        :param hotel_id: 员工ID(必传)
        :return:
            icon: 头像地址
        """

        try:
            hotel = Hotel.enabled_objects.get(id=hotel_id)
            corr_response({'icon': hotel.icon})
        except ObjectDoesNotExist:
            err_response('err_2', '酒店不存在')

    @validate_args({
        'token': forms.CharField(min_length=32, max_length=32),
        'hotel_id': forms.IntegerField(),
    })
    @validate_admin_token()
    def post(self, request, token, hotel_id=None):
        """修改头像

        :param token: 令牌(必传)
        :param hotel_id: 酒店ID(必传)
        :return: 200
        """

        hotel = None
        try:
            hotel = Hotel.enabled_objects.get(id=hotel_id)
        except ObjectDoesNotExist:
            err_response('err_3', '酒店不存在')

        # 管理员只能管理自己的酒店
        if request.admin.type == 0 and hotel != request.admin.hotel:
            err_response('err_2', '权限错误')

        if request.method == 'POST':
            icon = request.FILES['icon']

            if icon:
                icon_time = timezone.now().strftime('%H%M%S%f')
                icon_tail = str(icon).split('.')[-1]
                dir_name = 'uploaded/icon/hotel/%d/' % request.staff.id
                os.makedirs(dir_name, exist_ok=True)
                file_name = dir_name + '%s.%s' % (icon_time, icon_tail)
                img = Image.open(icon)
                img.save(file_name, quality=90)

                # 删除旧文件, 保存新的文件路径
                if hotel.icon:
                    try:
                        os.remove(hotel.icon)
                    except OSError:
                        pass
                hotel.icon = file_name
                hotel.save()
                corr_response()

            err_response('err_4', '图片为空')


class HotelBranchList(View):
    ORDERS = ('create_time', '-create_time', 'name', '-name')

    @validate_args({
        'token': forms.CharField(min_length=32, max_length=32),
        'is_enabled': forms.BooleanField(required=False),
        'offset': forms.IntegerField(min_value=0, required=False),
        'limit': forms.IntegerField(min_value=0, required=False),
        'order': forms.IntegerField(min_value=0, max_value=3, required=False),
        'hotel_id': forms.IntegerField(),
    })
    @validate_admin_token()
    def get(self, request, token, hotel_id, is_enabled=True, offset=0, limit=10,
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
            2: 昵称升序
            3: 昵称降序
        :return:
            count: 员工总数
            list: 员工列表
                branch_id: ID
                name: 名称
                icon: 头像
                picture: 图片(最多5张，用"|"分割)
                province: 省
                city: 市
                county: 区/县
                address: 详细地址
                facility: 设施(json字符串)
                pay_card: 可以刷哪些卡(json字符串)
                phone: 联系电话(最多3个，用"|"分割)
                cuisine: 菜系(json字符串)
                hotel_name: 所属酒店名
                manager: 店长
                create_time: 创建时间
        """
        hotel = None
        try:
            hotel = Hotel.enabled_objects.get(id=hotel_id)
        except Hotel.DoesNotExist:
            err_response('err_3', '酒店不存在')

        # 管理员只能查看自己酒店的门店
        if request.admin.type == 0 and hotel != request.admin.hotel:
            err_response('err_2', '权限错误')
        c = HotelBranch.objects.filter(
            hotel=hotel, is_enabled=is_enabled).count()
        branches = HotelBranch.objects.filter(
            hotel=hotel, is_enabled=is_enabled).order_by(
            self.ORDERS[order])[offset:offset + limit]

        l = [{'branch_id': b.id,
              'name': b.name,
              'icon': b.icon,
              'picture': b.picture,
              'province': b.province,
              'city': b.city,
              'county': b.county,
              'address': b.address,
              'facility': b.facility,
              'pay_card': b.pay_card,
              'phone': b.phone,
              'cuisine': b.cuisine,
              'hotel_name': b.hotel.hotel.name,
              'manager': b.manager,
              'create_time': b.create_time} for b in branches]
        corr_response({'count': c, 'list': l})

    @validate_args({
        'token': forms.CharField(min_length=32, max_length=32),
        'hotel_id': forms.IntegerField(),
        'staff_id': forms.IntegerField(),
        'name': forms.CharField(min_length=1, max_length=20),
        'province': forms.CharField(min_length=1, max_length=20),
        'city': forms.CharField(min_length=1, max_length=20),
        'county': forms.CharField(min_length=1, max_length=20),
        'address': forms.CharField(min_length=1, max_length=50),
        'phone': forms.CharField(min_length=1, max_length=50),
        'facility': forms.CharField(max_length=100, required=False),
        'pay_card': forms.CharField(max_length=20, required=False),
        'cuisine': forms.CharField(max_length=100, required=False),
    })
    @validate_admin_token()
    def post(self, request, token, hotel_id, staff_id, **kwargs):
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
            phone: 联系电话(最多3个，用"|"分割，必传)
            facility: 设施(json字符串)
            pay_card: 可以刷哪些卡(json字符串)
            cuisine: 菜系(json字符串)
        :return 200/400
        """

        hotel, staff = None, None
        try:
            hotel = Hotel.enabled_objects.get(id=hotel_id)
        except Hotel.DoesNotExist:
            err_response('err_3', '酒店不存在')
        try:
            staff = Staff.enabled_objects.get(id=staff_id)
        except Staff.DoesNotExist:
            err_response('err_4', '员工不存在')

        branch_keys = ('name', 'province', 'city', 'county', 'address', 'phone',
                       'facility', 'pay_card', 'cuisine')
        with transaction.atomic():
            try:
                branch = HotelBranch(hotel=hotel, staff=staff)
                for k in branch_keys:
                    if k in kwargs:
                        setattr(branch, k, kwargs[k])
                branch.save()
                corr_response()
            except IntegrityError:
                err_response('error_5', '服务器创建门店失败')

    @validate_args({
        'token': forms.CharField(min_length=32, max_length=32),
        'branch_id': forms.IntegerField(),
    })
    @validate_admin_token()
    def delete(self, request, token, branch_id):
        """删除门店

        :param token: 令牌(必传)
        :param branch_id: 门店ID(必传)
        :return: 200/404
        """

        try:
            branch = HotelBranch.objects.get(id=branch_id)
        except HotelBranch.DoesNotExist:
            err_response('err_4', '门店不存在')
        else:
            branch.is_enabled = False
            branch.save()
            corr_response()


class StaffList(View):
    ORDERS = ('create_time', '-create_time', 'name', '-name')

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
    def get(self, request, token, hotel_id, status=1, is_enabled=True, offset=0,
            limit=10, order=1):
        """获取员工列表

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

        hotel = None
        try:
            hotel = Hotel.enabled_objects.get(id=hotel_id)
        except Hotel.DoesNotExist:
            err_response('err_4', '酒店不存在')

        # 管理员只能查看自己酒店的员工
        if request.admin.type == 0 and hotel != request.admin.hotel:
            err_response('err_2', '权限错误')
        c = Staff.objects.filter(hotel=hotel, status=status,
                                 is_enabled=is_enabled).count()
        staffs = Staff.objects.filter(
            hotel=hotel, status=status, is_enabled=is_enabled).order_by(
            self.ORDERS[order])[offset:offset + limit]

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
        corr_response({'count': c, 'list': l})

    @validate_args({
        'phone': forms.RegexField(r'[0-9]{11}'),
        'password': forms.CharField(min_length=1, max_length=128),
        'staff_number': forms.CharField(
            min_length=1, max_length=20, required=False),
        'name': forms.CharField(min_length=1, max_length=20),
        'gender': forms.IntegerField(min_value=0, max_value=2, required=False),
        'position': forms.CharField(max_length=20),
        'id_number': forms.CharField(min_length=18, max_length=18),
        'hotel_id': forms.IntegerField(),
    })
    @validate_admin_token()
    def post(self, request, phone, password, hotel_id, **kwargs):
        """注册新员工

        :param phone: 手机号(必传)
        :param password: 密码(必传)
        :param hotel_id: 酒店ID(必传)
        :param kwargs:
            staff_number: 员工编号
            name: 姓名(必传)
            gender: 性别, 0: 保密, 1: 男, 2: 女
            position: 职位(必传)
            id_number: 身份证号(必传)
        :return 200
        """

        hotel = None
        try:
            hotel = Hotel.enabled_objects.get(id=hotel_id)
        except Hotel.DoesNotExist:
            err_response('err_4', '酒店不存在')
        # 管理员只能添加自己酒店的员工
        if request.admin.type == 0 and hotel != request.admin.hotel:
            err_response('err_2', '权限错误')

        if Staff.objects.filter(phone=phone).exists():
            err_response('err_3', '该手机号已注册')
        staff_keys = ('staff_number', 'name', 'gender', 'position', 'id_number')
        with transaction.atomic():
            try:
                staff = Staff(phone=phone, password=password, status=1,
                              hotel=hotel)
                # 更新令牌
                staff.update_token()
                for k in staff_keys:
                    if k in kwargs:
                        setattr(staff, k, kwargs[k])
                staff.save()
                corr_response()
            except IntegrityError:
                err_response('err_5', '服务器创建员工失败')

    @validate_args({
        'token': forms.CharField(min_length=32, max_length=32),
        'staff_id': forms.IntegerField(),
    })
    @validate_admin_token()
    def delete(self, request, token, staff_id):
        """删除员工

        :param token: 令牌(必传)
        :param staff_id: 员工ID(必传)
        :return: 200/404
        """

        staff = None
        try:
            staff = Staff.objects.get(id=staff_id)
        except Staff.DoesNotExist:
            err_response('err_3', '员工不存在')
        # 管理员只能管理自己酒店的员工
        if request.admin.type == 0 and staff.hotel != request.admin.hotel:
            err_response('err_2', '权限错误')

        staff.is_enabled = False
        staff.save()
        corr_response()


class StaffProfile(View):
    @validate_args({
        'token': forms.CharField(min_length=32, max_length=32),
        'staff_id': forms.IntegerField(),
    })
    @validate_admin_token()
    def get(self, request, token, staff_id):
        """

        :param request:
        :param token: 令牌(必传)
        :param staff_id: 员工ID(必传)
        :return:
            staff_id: ID
            staff_number: 员工编号
            name: 员工姓名
            icon: 员工头像
            gender: 性别
            status: 员工状态，0: 待审核，1: 审核通过
            hotel_name: 员工所属酒店
            description: 备注
            position: 职位
            guest_channel: 所属获客渠道
                0:无, 1:高层管理, 2:预定员和迎宾, 3:客户经理
            authority: 权限
            create_time: 创建时间
        """

        staff = None
        try:
            staff = Staff.objects.get(id=staff_id)
        except Staff.DoesNotExist:
            err_response('err_3', '员工不存在')

        # 管理员只能查看自己酒店的员工
        if request.admin.type == 0 and staff.hotel != request.admin.hotel:
            err_response('err_2', '权限错误')

        d = {'staff_id': staff.id,
             'staff_number': staff.staff_number,
             'name': staff.name,
             'gender': staff.gender,
             'position': staff.position,
             'guest_channel': staff.guest_channel,
             'description': staff.description,
             'authority': staff.authority,
             'status': staff.status,
             'create_time': staff.create_time}
        corr_response(d)

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
        'status': forms.IntegerField(required=False),
        'staff_id': forms.IntegerField(),
    })
    @validate_admin_token()
    def post(self, request, token, staff_id, **kwargs):
        """修改员工信息

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

        staff = None
        try:
            staff = Staff.objects.get(id=staff_id)
        except Staff.DoesNotExist:
            err_response('err_3', '员工不存在')

        # 管理员只能管理自己酒店的员工
        if request.admin.type == 0 and staff.hotel != request.admin.hotel:
            err_response('err_2', '权限错误')

        staff_keys = ('staff_number', 'gender', 'position', 'guest_channel',
                      'description', 'authority', 'status', 'is_enabled')
        for k in staff_keys:
            if k in kwargs:
                setattr(staff, k, kwargs[k])
        staff.save()
        corr_response()
