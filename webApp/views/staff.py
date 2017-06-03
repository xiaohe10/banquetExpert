import os

from PIL import Image
from django import forms
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View

from ..utils.decorator import validate_args, validate_staff_token
from ..models import Staff, Hotel

__all__ = ['List', 'Token', 'Password', 'Icon', 'Profile']


class List(View):
    ORDERS = ('create_time', 'create_time', 'name', '-name')

    @validate_args({
        'token': forms.CharField(min_length=32, max_length=32),
        'status': forms.IntegerField(min_value=0, max_value=1, required=False),
        'offset': forms.IntegerField(min_value=0, required=False),
        'limit': forms.IntegerField(min_value=0, required=False),
        'order': forms.IntegerField(min_value=0, max_value=3, required=False),
    })
    @validate_staff_token()
    def get(self, request, token, status=1, offset=0, limit=10, order=1):
        """获取员工列表

        :param token: 令牌(必传)
        :param status: 员工状态, 0: 待审核, 1: 审核通过, 默认1
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
                position: 职位
                guest_channel: 所属获客渠道
                    0:无, 1:高层管理, 2:预定员和迎宾, 3:客户经理
                authority: 权限
                create_time: 创建时间
        """
        c = Staff.enabled_objects.filter(status=status).count()
        staffs = Staff.enabled_objects.filter(status=status).order_by(
            self.ORDERS[order])[offset:offset + limit]
        l = [{'staff_id': s.id,
              'name': s.name,
              'staff_number': s.staff_number,
              'icon': s.icon,
              'gender': s.gender,
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
    def post(self, request, phone, password, hotel_id, **kwargs):
        """员工注册

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

        if Staff.objects.filter(phone=phone).exists():
            return HttpResponse('该手机号已注册', status=403)
        staff_keys = ('staff_number', 'name', 'gender', 'position', 'id_number')
        with transaction.atomic():
            try:
                staff = Staff(phone=phone, password=password, hotel=hotel)
                staff.update_token()
                for k in staff_keys:
                    if k in kwargs:
                        setattr(staff, k, kwargs[k])
                staff.save()
                return HttpResponse('创建员工成功', status=200)
            except IntegrityError:
                return HttpResponse('创建员工失败', status=400)


class Token(View):
    @validate_args({
        'phone': forms.RegexField(r'[0-9]{11}'),
        'password': forms.CharField(min_length=1, max_length=128),
    })
    def post(self, request, phone, password):
        """更新并返回员工令牌

        :param phone: 手机号(11位, 必传)
        :param password: 密码(必传)
        :return token: 员工token
        """

        try:
            staff = Staff.objects.get(phone=phone)
        except Staff.DoesNotExist:
            return HttpResponse('员工不存在', status=404)
        else:
            if not staff.is_enabled:
                return HttpResponse('员工已删除', status=403)
            if staff.status == 0:
                return HttpResponse('账号待审核', status=403)
            if staff.password != password:
                return HttpResponse('密码错误', status=400)
            staff.update_token()
            staff.save()
            return JsonResponse({'token': staff.token})


class Password(View):
    @validate_args({
        'token': forms.CharField(min_length=32, max_length=32),
        'new_password': forms.CharField(min_length=6, max_length=20),
        'old_password': forms.CharField(min_length=6, max_length=20),
    })
    @validate_staff_token()
    def post(self, request, token, old_password, new_password):
        """修改密码

        :param token: 令牌(必传)
        :param old_password: 旧密码(6-20位, 必传)
        :param new_password: 新密码(6-20位, 必传)
        :return 200/403
        """

        if request.staff.password == old_password:
            request.staff.password = new_password
            return HttpResponse('密码修改成功', status=200)
        return HttpResponse('旧密码错误', status=403)


class Icon(View):
    @validate_args({
        'token': forms.CharField(min_length=32, max_length=32),
        'staff_id': forms.IntegerField(required=False),
    })
    @validate_staff_token()
    def get(self, request, token, staff_id=None):
        """获取头像

        :param token: 令牌(必传)
        :param staff_id: 员工ID
        :return:
            icon: 头像地址
        """
        if staff_id:
            try:
                staff = Staff.enabled_objects.get(id=staff_id)
            except ObjectDoesNotExist:
                return HttpResponse('员工不存在', status=404)
        else:
            staff = request.staff

        return JsonResponse({'icon': staff.icon})

    @validate_args({
        'token': forms.CharField(min_length=32, max_length=32),
    })
    @validate_staff_token()
    def post(self, request, token):
        """修改头像

        :param token: 令牌(必传)
        :return: 200
        """
        if request.method == 'POST':
            icon = request.FILES['icon']

            if icon:
                icon_time = timezone.now().strftime('%H%M%S%f')
                icon_tail = str(icon).split('.')[-1]
                dir_name = 'uploaded/icon/staff/%d/' % request.staff.id
                os.makedirs(dir_name, exist_ok=True)
                file_name = dir_name + '%s.%s' % (icon_time, icon_tail)
                img = Image.open(icon)
                img.save(file_name, quality=90)

                # 删除旧文件, 保存新的文件路径
                if request.staff.icon:
                    try:
                        os.remove(request.staff.icon)
                    except OSError:
                        pass
                request.staff.icon = file_name
                request.staff.save()
                return HttpResponse('上传成功', status=200)

            return HttpResponse('图片为空', status=400)


class Profile(View):
    @validate_args({
        'token': forms.CharField(min_length=32, max_length=32),
        'staff_id': forms.IntegerField(required=False),
    })
    @validate_staff_token()
    def get(self, request, token, staff_id=None):
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
                return HttpResponse('员工不存在', status=404)
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
        return JsonResponse(r)

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
    })
    @validate_staff_token()
    def post(self, request, token, **kwargs):
        """修改员工信息

        :param token: 令牌(必传)
        :param kwargs:
            staff_number: 员工编号
            gender: 性别
            position: 职位
            guest_channel: 所属获客渠道, 0:无, 1:高层管理, 2:预定员和迎宾, 3:客户经理
            description: 备注
            authority: 权限
        :return: 200
        """

        staff_keys = ('staff_number', 'gender', 'position', 'guest_channel',
                      'description', 'authority')
        for k in staff_keys:
            if k in kwargs:
                setattr(request.staff, k, kwargs[k])
        request.staff.save()
        return HttpResponse('修改信息成功', status=200)
