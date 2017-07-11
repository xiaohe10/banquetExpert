import json

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
        def returned_wrapper(request, *args, **kwargs):
            if 'token' not in kwargs:
                return err_response('err_1', '缺少 token')
            try:
                admin = Admin.objects.get(token=kwargs['token'])
            except ObjectDoesNotExist:
                return err_response('err_0', '您已下线，请重新登录！')
            else:
                if admin.type != 1:
                    return err_response('err_2', '权限错误')
                if admin.is_enabled is not True:
                    return err_response('err_3', '不存在该管理员')
                request.admin = admin
            return function(request, *args, **kwargs)
        return returned_wrapper
    return decorator


def validate_admin_token():
    """对被装饰的方法根据token对管理者进行身份认证"""
    def decorator(function):
        @wraps(function)
        def returned_wrapper(request, *args, **kwargs):
            if 'token' not in kwargs:
                return err_response('err_1', '缺少 token')
            try:
                admin = Admin.objects.get(token=kwargs['token'])
            except ObjectDoesNotExist:
                return err_response('err_0', '您已下线，请重新登录！')
            else:
                if admin.type != 0:
                    return err_response('err_2', '权限错误')
                if admin.is_enabled is not True:
                    return err_response('err_3', '不存在该管理员')
                request.admin = admin
            return function(request, *args, **kwargs)
        return returned_wrapper
    return decorator


def validate_staff_token():
    """对被装饰的方法根据token对员工进行身份认证"""
    def decorator(function):
        @wraps(function)
        def returned_wrapper(request, *args, **kwargs):
            if 'token' not in kwargs:
                return err_response('err_1', '缺少 token')
            try:
                staff = Staff.objects.get(token=kwargs['token'])
            except ObjectDoesNotExist:
                return err_response('err_0', '您已下线，请重新登录！')
            else:
                if staff.is_enabled is not True:
                    return err_response('err_3', '不存在该员工')
                if staff.status == 0:
                    return err_response('err_3', '不存在该员工')
                request.staff = staff
            return function(request, *args, **kwargs)
        return returned_wrapper
    return decorator


def validate_user_token():
    """对被装饰的方法根据token对用户进行身份认证"""
    def decorator(function):
        @wraps(function)
        def returned_wrapper(request, *args, **kwargs):
            if 'token' not in kwargs:
                return err_response('err_1', '缺少 token')
            try:
                user = User.objects.get(token=kwargs['token'])
            except ObjectDoesNotExist:
                return err_response('err_0', '您已下线，请重新登录！')
            else:
                if user.is_enabled is not True:
                    return err_response('err_3', '不存在该用户')
                request.user = user
            return function(request, *args, **kwargs)
        return returned_wrapper
    return decorator


def validate_args(dic):
    """对被装饰的方法利用 "参数名/表单模型" 字典进行输入数据验证，验证后的数据
    作为关键字参数传入view函数中，若部分数据非法则直接返回400 Bad Request
    """
    def decorator(function):
        @wraps(function)
        def returned_wrapper(request, *args, **kwargs):
            # 从session 中获取 token(如果存在)
            token = request.session.get('token', None)
            try:
                if request.method == "GET":
                    data = request.GET
                elif request.method == "POST":
                    data = json.loads(request.body)
                    if 'token' not in data:
                        data['token'] = token
                else:
                    data = QueryDict(request.body)
            except ValueError:
                return err_response(
                    'err_1', '参数不正确（缺少参数或者不符合格式）')
            for k, v in dic.items():
                try:
                    kwargs[k] = v.clean(data[k])
                except KeyError:
                    if v.required:
                        return err_response(
                            'err_1', '"%s" 参数不正确（缺少参数或者不符合格式）' % k)
                except ValidationError:
                    return err_response(
                        'err_1', '"%s" 参数不正确（缺少参数或者不符合格式）' % k)
            return function(request, *args, **kwargs)
        return returned_wrapper
    return decorator


def validate_json_args(dic):
    """对被装饰的方法利用 "参数名/表单模型" 字典进行输入数据验证，
    被验证的数据是数组或者键值对格式，验证后的数据作为关键字参数传入view函数中，
    若部分数据非法则直接返回400 Bad Request
    """
    def decorator(function):
        @wraps(function)
        def returned_wrapper(request, *args, **kwargs):
            try:
                if request.method == "GET":
                    data = request.GET
                elif request.method == "POST":
                    data = request.body
                else:
                    data = QueryDict(request.body)
            except ValueError:
                return err_response(
                    'err_1', '参数不正确（缺少参数或者不符合格式）')
            for k, v in dic.items():
                try:
                    kwargs[k] = json.loads(v.clean(data[k]))
                except KeyError or ValueError:
                    if v.required:
                        return err_response(
                            'err_1', '"%s" 参数不正确（缺少参数或者不符合格式）' % k)
                except ValidationError:
                    return err_response(
                        'err_1', '"%s" 参数不正确（缺少参数或者不符合格式）' % k)
            return function(request, *args, **kwargs)
        return returned_wrapper
    return decorator
