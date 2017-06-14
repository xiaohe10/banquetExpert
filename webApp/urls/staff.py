from django.conf.urls import url

from webApp.views.staff import *

urlpatterns = [
    # 员工注册
    url(r'^register/$', register, name='register'),
    # 登录
    url(r'^login/$', login, name='login'),
    # 修改密码
    url(r'^pass_modify/$', modify_password, name='modify_password'),
    # 获取资料
    url(r'^profile/get/$', get_profile, name='get_profile'),
    # 修改个人资料
    url(r'^profile/modify/$', modify_password, name='modify_profile'),
]
