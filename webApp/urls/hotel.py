from django.conf.urls import url

from ..views.hotel import *

urlpatterns = [
    # 获取酒店列表(get)
    url(r'^list/$', get_hotels, name='hotels'),
]
