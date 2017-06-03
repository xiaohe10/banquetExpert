from django import forms
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse
from django.db import transaction
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist

from ..utils.decorator import validate_args, validate_admin_token
from ..models import Admin, Hotel, Staff

__all__ = ['AdminList', 'Token', 'HotelList', 'HotelProfile',
           'StaffList', 'StaffProfile']


class AdminList(View):
    ORDERS = ('create_time', 'create_time', 'username', '-username')

    @validate_args({
        'token': forms.CharField(min_length=32, max_length=32),
        'offset': forms.IntegerField(min_value=0, required=False),
        'limit': forms.IntegerField(min_value=0, required=False),
        'order': forms.IntegerField(min_value=0, max_value=3, required=False),
    })
    @validate_admin_token()
    def get(self, request, token, offset=0, limit=10, order=1):
        """获取管理者列表

        :param token: 令牌(必传)
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
                authority: 权限
                is_enabled: 是否有效
                create_time: 创建时间
        """

        # 只有超级管理者才能访问
        if request.admin != 1:
            return HttpResponse('禁止访问', status=403)

        c = Admin.objects.count()
        admins = Admin.objects.order_by(
            self.ORDERS[order])[offset:offset + limit]
        l = [{'admin_id': a.id,
              'username': a.username,
              'authority': a.authority,
              'is_enabled': a.is_enabled,
              'create_time': a.create_time} for a in admins]
        return JsonResponse({'count': c, 'list': l})

    @validate_args({
        'username': forms.CharField(min_length=1, max_length=20),
        'password': forms.CharField(min_length=1, max_length=128),
        'type': forms.IntegerField(min_value=0, max_value=1, required=False),
        'hotel_id': forms.IntegerField(required=False),
    })
    @validate_admin_token()
    def post(self, request, username, password, type=0, hotel_id=None):
        """注册新的管理员, 只有超级管理者才能注册

        :param username: 用户名(必传)
        :param password: 密码(必传)
        :param type: 管理员类型, 0: 管理员, 1: 超级管理员
        :param hotel_id: 管理员所属酒店,
        :return 200/400/403/404
        """

        if request.admin != 1:
            return HttpResponse('禁止访问', status=403)
        if Admin.objects.filter(username=username).exists():
            return HttpResponse('该用户名已注册', status=403)

        if hotel_id is not None:
            if type == 0:
                try:
                    hotel = Hotel.enabled_objects.get(id=hotel_id)
                except ObjectDoesNotExist:
                    return HttpResponse('酒店不存在', status=404)
                else:
                    with transaction.atomic():
                        try:
                            admin = Admin(username=username, password=password,
                                          type=type, hotel=hotel)
                            admin.update_token()
                            admin.save()
                            return HttpResponse('创建管理员成功', status=200)
                        except IntegrityError:
                            return HttpResponse('创建管理员失败', status=400)
            else:
                return HttpResponse('超级管理员不属于任何酒店', status=400)
        else:
            if type == 1:
                with transaction.atomic():
                    try:
                        admin = Admin(username=username, password=password,
                                      type=type)
                        admin.update_token()
                        admin.save()
                        return HttpResponse('创建管理员成功', status=200)
                    except IntegrityError:
                        return HttpResponse('创建管理员失败', status=400)
            else:
                return HttpResponse('请提交管理员所属酒店', status=400)


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
            return HttpResponse('管理员不存在', status=404)
        else:
            if not admin.is_enabled:
                return HttpResponse('管理员已删除', status=400)
            if admin.password != password:
                return HttpResponse('密码错误', status=400)
            admin.update_token()
            admin.save()
            return JsonResponse({'token': admin.token})


class HotelList(View):
    ORDERS = ('create_time', 'create_time', 'name', '-name')

    @validate_args({
        'token': forms.CharField(min_length=32, max_length=32),
        'is_enabled': forms.BooleanField(required=False),
        'offset': forms.IntegerField(min_value=0, required=False),
        'limit': forms.IntegerField(min_value=0, required=False),
        'order': forms.IntegerField(min_value=0, max_value=3, required=False),
    })
    @validate_admin_token()
    def get(self, request, token, is_enabled=True, offset=0, limit=10, order=1):
        """获取酒店列表

        :param token: 令牌(必传)
        :param is_enabled: 是否有效, 默认:是
        :param offset: 起始值
        :param limit: 偏移量
        :param order: 排序方式
            0: 注册时间升序
            1: 注册时间降序（默认值）
            2: 昵称升序
            3: 昵称降序
        :return:
            count: 酒店总数
            list: 酒店列表
                hotel_id: ID
                name: 名称
                icon: 头像
                branches_count: 门店数
                owner_name: 法人代表
                create_time: 创建时间
        """

        # 只能超级管理员查看
        if request.admin.type != 1:
            return HttpResponse('没有权限', status=403)
        c = Hotel.objects.filter(is_enabled=is_enabled).count()
        hotels = Hotel.objects.filter(is_enabled=is_enabled).order_by(
            self.ORDERS[order])[offset:offset + limit]
        l = [{'hotel_id': h.id,
              'name': h.name,
              'icon': h.icon,
              'branches_count': h.branches.count(),
              'owner_name': h.owner_name,
              'create_time': h.create_time} for h in hotels]
        return JsonResponse({'count': c, 'list': l})

    @validate_args({
        'token': forms.CharField(min_length=32, max_length=32),
        'name': forms.CharField(min_length=1, max_length=20),
        'owner_name': forms.CharField(min_length=1, max_length=20),
    })
    @validate_admin_token()
    def post(self, request, token, name, owner_name):
        """注册新酒店

        :param token: 令牌(必传)
        :param name: 名称(必传)
        :param owner_name: 法人代表(必传)
        :return 200
        """

        # 只有超级管理员能注册
        if request.admin.type != 1:
            return HttpResponse('没有权限', status=403)

        try:
            Hotel.objects.create(name=name, owner_name=owner_name)
            return HttpResponse('创建酒店成功', status=200)
        except IntegrityError:
            return HttpResponse('创建酒店失败', status=400)


class HotelProfile(View):
    @validate_args({
        'token': forms.CharField(min_length=32, max_length=32),
        'name': forms.CharField(min_length=1, max_length=20),
        'owner_name': forms.CharField(min_length=1, max_length=20),
        'staff_id': forms.IntegerField(),
    })
    @validate_admin_token()
    def post(self, request, token, hotel_id, **kwargs):
        """修改酒店信息

        :param token: 令牌(必传)
        :param hotel_id: 酒店ID(必传)
        :param kwargs:
            name: 名称
            owner_name: 法人代表
            is_enabled: 是否可用, True/False
        :return: 200
        """

        try:
            hotel = Hotel.objects.get(id=hotel_id)
        except Staff.DoesNotExist:
            return HttpResponse('酒店不存在', status=404)

        # 只有超级管理员能管理
        if request.admin.type != 1:
            return HttpResponse('没有权限', status=403)

        hotel_keys = ('name', 'owner_name', 'is_enabled')
        for k in hotel_keys:
            if k in kwargs:
                setattr(hotel, k, kwargs[k])
        hotel.save()
        return HttpResponse('修改信息成功', status=200)


class StaffList(View):
    ORDERS = ('create_time', 'create_time', 'name', '-name')

    @validate_args({
        'token': forms.CharField(min_length=32, max_length=32),
        'status': forms.IntegerField(min_value=0, max_value=1),
        'is_enabled': forms.BooleanField(required=False),
        'offset': forms.IntegerField(min_value=0, required=False),
        'limit': forms.IntegerField(min_value=0, required=False),
        'order': forms.IntegerField(min_value=0, max_value=3, required=False),
    })
    @validate_admin_token()
    def get(self, request, token, status=1, is_enabled=True, offset=0, limit=10,
            order=1):
        """获取员工列表

        :param token: 令牌(必传)
        :param status: 员工状态, 0: 待审核, 1: 审核通过, 默认1
        :param is_enabled: 是否有效, 默认:是
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
                hotel: 员工所属酒店
                position: 职位
                guest_channel: 所属获客渠道
                    0:无, 1:高层管理, 2:预定员和迎宾, 3:客户经理
                authority: 权限
                create_time: 创建时间
        """
        # 管理员只能查看自己酒店的员工
        if request.admin.type == 0:
            hotel = request.admin.hotel
            c = Staff.objects.filter(hotel=hotel, status=status,
                                     is_enabled=is_enabled).count()
            staffs = Staff.objects.filter(
                hotel=hotel, status=status, is_enabled=is_enabled).order_by(
                self.ORDERS[order])[offset:offset + limit]
        else:
            c = Staff.objects.filter(
                status=status, is_enabled=is_enabled).count()
            staffs = Staff.objects.filter(
                status=status, is_enabled=is_enabled).order_by(
                self.ORDERS[order])[offset:offset + limit]
        l = [{'staff_id': s.id,
              'name': s.name,
              'staff_number': s.staff_number,
              'icon': s.icon,
              'gender': s.gender,
              'hotel': s.hotel,
              'position': s.position,
              'guest_channel': s.guest_channel,
              'authority': s.authority,
              'create_time': s.create_time} for s in staffs]
        return JsonResponse({'count': c, 'list': l})

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

        try:
            hotel = Hotel.enabled_objects.get(id=hotel_id)
        except Hotel.DoesNotExist:
            return HttpResponse('酒店不存在', status=404)
        # 管理员只能添加自己酒店的员工
        if request.admin.type == 0 and hotel != request.admin.hotel:
            return HttpResponse('管理员只能添加自己酒店的员工', status=403)

        if Staff.objects.filter(phone=phone).exists():
            return HttpResponse('该手机号已注册', status=403)
        staff_keys = ('staff_number', 'name', 'gender', 'position', 'id_number')
        with transaction.atomic():
            try:
                staff = Staff(phone=phone, password=password, status=1,
                              hotel=hotel)
                staff.update_token()
                for k in staff_keys:
                    if k in kwargs:
                        setattr(staff, k, kwargs[k])
                staff.save()
                return HttpResponse('创建员工成功', status=200)
            except IntegrityError:
                return HttpResponse('创建员工失败', status=400)


class StaffProfile(View):
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
        'is_enabled': forms.BooleanField(required=False),
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

        try:
            staff = Staff.objects.get(id=staff_id)
        except Staff.DoesNotExist:
            return HttpResponse('员工不存在', status=404)

        # 管理员只能管理自己酒店的员工
        if request.admin.type == 0 and staff.hotel != request.admin.hotel:
            return HttpResponse('管理员只能添加自己酒店的员工', status=403)

        staff_keys = ('staff_number', 'gender', 'position', 'guest_channel',
                      'description', 'authority', 'status', 'is_enabled')
        for k in staff_keys:
            if k in kwargs:
                setattr(request.staff, k, kwargs[k])
        request.staff.save()
        return HttpResponse('修改信息成功', status=200)
