from django.conf.urls import url

from ..views.hotel import *

urlpatterns = [
    # 获取酒店列表
    url(r'^list/$', get_hotels, name='hotels'),
    # 获取酒店门店列表
    url(r'^hotel_branch/list/$', get_branches, name='get_branch_list'),
]
