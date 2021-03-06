from django.conf.urls import url

from webApp.views.staff import *

urlpatterns = [
    # 获取验证码
    url(r'validation_code/$', get_validation_code, name='validation_code'),
    # 员工注册
    url(r'^register/$', register, name='register'),
    # 登录
    url(r'^login/$', login, name='login'),
    # 修改密码
    url(r'^pass_modify/$', modify_password, name='modify_password'),
    # 根据员工权限获取web端模块
    url(r'^web/authority/$', get_web_authority, name='web_authority'),
    # 获取资料
    url(r'^profile/get/$', get_profile, name='get_profile'),
    # 修改个人资料
    url(r'^profile/modify/$', modify_profile, name='modify_profile'),
    # 获取员工所在的酒店信息
    url(r'^hotel/$', get_hotel, name='get_hotel'),
    # 获取员工所在酒店的门店列表
    url(r'^hotel_branch/list/$', get_branches, name='get_branch_list'),
    # 获取员工的客户列表
    url(r'^guest/list/$', get_guests, name='get_guest_list'),
    # 获取员工的客户统计
    url(r'^guest/statistic/$', get_guest_statistic, name='get_guest_statistic'),
    # 搜索员工的订单
    url(r'^order/search/$', search_orders, name='search_order'),
]
