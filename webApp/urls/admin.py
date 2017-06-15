from django.conf.urls import url

from webApp.views.admin import *

urlpatterns = [
    # 登录
    url(r'^login/$', login, name='login'),
    # 获取酒店资料
    url(r'^hotel/profile/get/$', get_hotel_profile, name='get_hotel_profile'),
    # 修改酒店资料
    url(r'^hotel/profile/modify/$', modify_hotel_profile,
        name='modify_hotel_profile'),
    # 获取酒店门店列表
    url(r'^hotel_branch/list/$', get_branches, name='hotel_branch_list'),
    # 注册新的门店
    url(r'^hotel_branch/register/$', register_branch,
        name='hotel_branch_register'),
    # 删除门店
    url(r'^hotel_branch/delete/$', delete_branch, name='hotel_branch_delete'),
    # 获取门店资料
    url(r'^hotel_branch/profile/get/$', get_branch_profile,
        name='get_hotel_branch_profile'),
    # 修改门店资料
    url(r'^hotel_branch/profile/modify/$', modify_branch_profile,
        name='modify_hotel_branch_profile'),
    # 修改门店餐段设置
    url(r'^hotel_branch/meal_period/modify/$', modify_meal_period,
        name='modify_meal_period'),
    # 增加门店介绍图片
    url(r'^hotel_branch/picture/add/$', add_branch_picture,
        name='add_hotel_branch_picture'),
    # 删除门店介绍图片
    url(r'^hotel_branch/picture/delete/$', delete_branch_picture,
        name='delete_hotel_branch_picture'),
    # 获取门店的餐厅区域
    url(r'^hotel_branch/area/list/$', get_areas, name='get_area_list'),
    # 增加门店的餐厅区域
    url(r'^hotel_branch/area/add/$', add_area, name='add_area'),
    # 修改门店的餐厅区域
    url(r'^hotel_branch/area/modify/$', modify_area, name='modify_area'),
    # 获取门店桌位列表
    url(r'^hotel_branch/desk/list/$', get_desks, name='get_desk_list'),
    # 增加门店桌位
    url(r'^hotel_branch/desk/add/$', add_desk, name='add_desk'),
    # 修改门店桌位
    url(r'^hotel_branch/desk/modify/$',modify_desk, name='modify_desk'),
    # 获取酒店员工列表
    url(r'^staff/list/$', get_staffs, name='staff_list'),
    # 注册新的员工
    url(r'^staff/register/$', register_staff, name='register_staff'),
    # 删除员工
    url(r'^staff/delete/$', delete_staff, name='delete_staff'),
    # 获取员工资料
    url(r'^staff/profile/get/$', get_staff_profile, name='get_staff_profile'),
    # 修改员工资料, 包括账号审核
    url(r'^staff/profile/modify/$', modify_staff_profile,
        name='modify_staff_profile'),
    # 获取自己酒店的直播间列表
    url(r'^live/list/$', get_lives, name='live_list'),
    # 发布直播间
    url(r'^live/push/$', push_live, name='push_live'),
    # 修改直播间信息
    url(r'^live/profile/modify/$', modify_live_profile,
        name='modify_live_profile'),
    # 获取直播间的回放列表
    url(r'^playback/$', get_playbacks, name='playbacks'),
]
