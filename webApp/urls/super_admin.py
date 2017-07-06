from django.conf.urls import url

from webApp.views.super_admin import *

urlpatterns = [
    # 获取管理者列表
    url(r'^manager/list/$', get_admins, name='list_manager'),
    # 注册新的管理者
    url(r'^manager/register/$', register, name='register_manager'),
    # 修改管理者
    url(r'^manager/modify/$', modify_admin, name='modify_manager'),
    # 登录
    url(r'^login/$', login, name='login'),
    # 获取酒店列表
    url(r'^hotel/list/$', get_hotels, name='hotel_list'),
    # 注册新的酒店
    url(r'^hotel/register/$', register_hotel, name='register_hotel'),
    # 删除酒店
    url(r'^hotel/delete/$', delete_hotel, name='delete_hotel'),
    # 获取酒店资料
    url(r'^hotel/profile/get/$', get_hotel_profile, name='get_hotel_profile'),
    # 修改酒店资料
    url(r'^hotel/profile/modify/$', modify_hotel_profile,
        name='modify_hotel_profile'),
]
