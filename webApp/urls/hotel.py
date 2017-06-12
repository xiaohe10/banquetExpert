from django.conf.urls import url

from ..views.hotel import *

urlpatterns = [
    # 获取酒店列表(get)
    url(r'^list/$', List.as_view(), name='hotels'),
]
