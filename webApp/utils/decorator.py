from functools import wraps
from django.http import QueryDict
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ValidationError

from ..models import Admin, Staff, User
from ..utils.response import err_response


def validate_super_admin_token():
    """对被装饰的方法根据token对超级管理者进行身份认证"""
    def decorator(function):
        @wraps(function)
        def returned_wrapper(self, request, *args, **kwargs):
            if 'token' not in kwargs:
                return err_response('err_1', '参数不正确（缺少参数或者不符合格式）')
            try:
                admin = Admin.objects.get(token=kwargs['token'])
            except ObjectDoesNotExist:
                return err_response('err_3', '不存在该管理员')
            else:
                if admin.type != 1:
                    return err_response('err_2', '权限错误')
                if admin.is_enabled is not True:
                    return err_response('err_3', '不存在该管理员')
                request.admin = admin
            return function(self, request, *args, **kwargs)
        return returned_wrapper
    return decorator


def validate_admin_token():
    """对被装饰的方法根据token对管理者进行身份认证"""
    def decorator(function):
        @wraps(function)
        def returned_wrapper(self, request, *args, **kwargs):
            if 'token' not in kwargs:
                return err_response('err_1', '参数不正确（缺少参数或者不符合格式）')
            try:
                admin = Admin.objects.get(token=kwargs['token'])
            except ObjectDoesNotExist:
                return err_response('err_3', '不存在该管理员')
            else:
                if admin.type != 0:
                    return err_response('err_2', '权限错误')
                if admin.is_enabled is not True:
                    return err_response('err_3', '不存在该管理员')
                request.admin = admin
            return function(self, request, *args, **kwargs)
        return returned_wrapper
    return decorator


def validate_staff_token():
    """对被装饰的方法根据token对员工进行身份认证"""
    def decorator(function):
        @wraps(function)
        def returned_wrapper(self, request, *args, **kwargs):
            if 'token' not in kwargs:
                return err_response('err_1', '参数不正确（缺少参数或者不符合格式）')
            try:
                staff = Staff.objects.get(token=kwargs['token'])
            except ObjectDoesNotExist:
                return err_response('err_1', '不存在该员工')
            else:
                if staff.is_enabled is not True:
                    return err_response('err_3', '不存在该员工')
                if staff.status == 0:
                    return err_response('err_3', '不存在该员工')
                request.staff = staff
            return function(self, request, *args, **kwargs)
        return returned_wrapper
    return decorator


def validate_user_token():
    """对被装饰的方法根据token对用户进行身份认证"""
    def decorator(function):
        @wraps(function)
        def returned_wrapper(self, request, *args, **kwargs):
            if 'token' not in kwargs:
                return err_response('err_1', '参数不正确（缺少参数或者不符合格式）')
            try:
                user = User.objects.get(token=kwargs['token'])
            except ObjectDoesNotExist:
                return err_response('err_3', '不存在该用户')
            else:
                if user.is_enabled is not True:
                    return err_response('err_3', '不存在该用户')
                request.user = user
            return function(self, request, *args, **kwargs)
        return returned_wrapper
    return decorator


def validate_args(dic):
    """对被装饰的方法利用 "参数名/表单模型" 字典进行输入数据验证，验证后的数据
    作为关键字参数传入view函数中，若部分数据非法则直接返回400 Bad Request
    """
    def decorator(function):
        @wraps(function)
        def returned_wrapper(self, request, *args, **kwargs):
            if request.method == "GET":
                data = request.GET
            elif request.method == "POST":
                data = request.POST
            else:
                data = QueryDict(request.body)
            for k, v in dic.items():
                try:
                    kwargs[k] = v.clean(data[k])
                except KeyError:
                    if v.required:
                        return err_response(
                            'err_1', '参数不正确（缺少参数或者不符合格式）')
                except ValidationError:
                    return err_response(
                        'err_1', '参数不正确（缺少参数或者不符合格式）')
            return function(self, request, *args, **kwargs)
        return returned_wrapper
    return decorator
