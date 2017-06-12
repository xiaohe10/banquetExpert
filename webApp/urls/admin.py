from django.conf.urls import url

from webApp.views.admin import *

urlpatterns = [
    # 登录(post)
    url(r'^login/$', Token.as_view(), name='login'),
    # 获取酒店资料(get)/修改酒店资料(post)
    url(r'^hotel/profile/$', HotelProfile.as_view(), name='hotel_profile'),
    # 获取酒店门店列表(get)
    url(r'^hotel_branch/list/$',
        HotelBranchList.as_view(), name='hotel_branch_list'),
    # 注册新的门店(post)
    url(r'^hotel_branch/register/$',
        HotelBranchList.as_view(), name='hotel_branch_register'),
    # 删除门店(delete)
    url(r'^hotel_branch/delete/$',
        HotelBranchList.as_view(), name='hotel_branch_delete'),
    # 获取酒店员工列表(get)
    url(r'^staff/list/$', StaffList.as_view(), name='staff_list'),
    # 注册新的员工(post)
    url(r'^staff/register/$', StaffList.as_view(), name='staff_register'),
    # 删除员工(delete)
    url(r'^staff/delete/$', StaffList.as_view(), name='staff_delete'),
    # 获取员工资料(get)/修改员工资料, 包括账号审核(post)
    url(r'^staff/profile/$', StaffProfile.as_view(),
        name='staff_profile'),
    # 获取自己酒店的直播间列表(get)
    url(r'^live/list/$', LiveList.as_view(), name='live_list'),
    # 创建直播间(post)
    url(r'^live/push/$', LiveList.as_view(), name='push_live'),
    # 修改直播间信息(post)
    url(r'^live/profile/$', LiveProfile.as_view(), name='live_profile'),
    # 获取直播间的回放列表
    url(r'^playback/', LivePlayBack.as_view(), name='play_back'),
]
