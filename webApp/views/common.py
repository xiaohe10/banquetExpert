import os

from django.shortcuts import render
from django.http import HttpResponse
from webApp.utils.response import *


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def upload_android_app(request):
    """上传安卓app安装包，返回下载目录"""

    if 'file' in request.FILES:
        file = request.FILES['file']

        dir_name = 'uploaded/android_app/'
        os.makedirs(dir_name, exist_ok=True)
        # filename = dir_name + file.name
        filename = dir_name + 'base.apk'

        try:
            destination = open(filename, 'wb+')
            for chunk in file.chunks():
                destination.write(chunk)
            destination.close()
        except IOError:
            return None

        url = 'http://114.215.220.241/' + filename

        return corr_response({'url': url})
    else:
        return err_response('err_1', '参数不正确（缺少参数或者不符合格式）')
