from django.conf.urls import url

from ..views.guest import *

urlpatterns = [
    # 获取客户来源
    url(r'channel/list/$', get_channels, name='channel_list'),
    # 获取客户列表(搜索)
    url(r'list/$', get_guests, name='list'),
    # 获取顾客概况
    url(r'profile/general/$', get_profile_general, name='profile_general'),
    # 获取客户档案详情
    url(r'profile/$', get_profile, name='profile'),
    # 添加客户档案
    url(r'profile/add/$', add_profile, name='profile_add'),
    # 修改客户档案
    url(r'profile/modify/$', modify_profile, name='profile_modify'),
]
