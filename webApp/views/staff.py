from django import forms
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse
from django.db import transaction
from django.views.generic import View

from ..models import Staff

__all__ = ['List', 'Token']


class List(View):
    ORDERS = ('create_time', 'create_time', 'name', '-name')

    def get(self, request, offset=0, limit=10, order=1):
        """获取员工列表

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
                id: ID
                staff_number: 员工编号
                name: 员工姓名
                icon: 员工头像
                gender: 性别
                position: 职位
                guest_channel: 所属获客渠道
                    0:无, 1:高层管理, 2:预定员和迎宾, 3:客户经理
                authority: 权限
                create_time: 注册时间
        """
        c = Staff.enabled_objects.count()
        staffs = Staff.enabled_objects.order_by(
            self.ORDERS[order])[offset:offset + limit]
        l = [{'id': s.id,
              'name': s.name,
              'staff_number': s.staff_number,
              'icon': s.icon,
              'gender': s.gender,
              'position': s.position,
              'guest_channel': s.channel,
              'authority': s.authority,
              'create_time': s.create_time} for s in staffs]
        return JsonResponse({'count': c, 'list': l})

    def post(self, request, phone, password, **kwargs):
        """注册，若成功返回令牌"""

        staff_keys = ('staff_number', 'name', 'gender', 'position', 'id_number')
        with transaction.atomic():
            try:
                staff = Staff(phone=phone, password=password)
                staff.update_token()
                for k in staff_keys:
                    if k in kwargs:
                        setattr(staff, k, kwargs[k])
                staff.save()
                return JsonResponse({'token': staff.token})
            except IntegrityError:
                return HttpResponse(400, '创建员工失败')


class Token(View):

    def post(self, request, phone, password):
        """更新并返回员工令牌

        :param phone: 手机号
        :param password: 密码
        :return token: 员工token
        """

        try:
            staff = Staff.objects.get(phone=phone)
        except Staff.DoesNotExist:
            return HttpResponse(404, '员工不存在')
        else:
            if not staff.is_enabled:
                return HttpResponse(400, '员工已删除')
            if staff.password != password:
                return HttpResponse(401, '密码错误')
            staff.update_token()
            staff.save()
            return JsonResponse({'token': staff.token})
