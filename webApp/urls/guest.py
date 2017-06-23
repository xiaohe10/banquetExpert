from django.conf.urls import url

from ..views.guest import *

urlpatterns = [
    # 获取客户列表(搜索)
    url(r'list/$', get_guests, name='list'),
    # 获取客户档案详情
    url(r'profile/$', get_profile, name='profile'),
]
