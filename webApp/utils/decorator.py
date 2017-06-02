from functools import wraps
from django.http import QueryDict, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ValidationError

from ..models import Staff, User


def validate_staff_token():
    """对被装饰的方法根据token对员工进行身份认证"""
    def decorator(function):
        @wraps(function)
        def returned_wrapper(self, request, *args, **kwargs):
            if 'token' not in kwargs:
                return HttpResponse('需要参数 "token"', status=400)
            try:
                staff = Staff.objects.get(token=kwargs['token'])
            except ObjectDoesNotExist:
                return HttpResponse('"token" 错误', status=404)
            else:
                if staff.is_enabled is not True:
                    return HttpResponse('账号已删除', status=400)
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
                return HttpResponse('需要参数 "token"', status=400)
            try:
                user = User.objects.get(token=kwargs['token'])
            except ObjectDoesNotExist:
                return HttpResponse('"token" 错误', status=404)
            else:
                if user.is_enabled is not True:
                    return HttpResponse('账号已删除', status=400)
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
                        return HttpResponse('需要参数 "%s"' % k, status=400)
                except ValidationError:
                    return HttpResponse('含有不合法参数 "%s"' % k, status=400)
            return function(self, request, *args, **kwargs)
        return returned_wrapper
    return decorator
