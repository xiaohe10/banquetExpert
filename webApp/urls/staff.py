from django.conf.urls import url

from webApp.views.staff import *

urlpatterns = [
    # 获取员工列表(get)
    url(r'^$', List.as_view(), name='staffs'),
    # 员工注册(post)
    url(r'^register/$', List.as_view(), name='register'),
    # 登录(post)
    url(r'^login/$', Token.as_view(), name='login'),
    # 修改密码(post)
    url(r'^pass_modify/$', Password.as_view(), name='pass_modify'),
    # 获取资料(get)/修改个人资料(post)
    url(r'^profile/$', Profile.as_view(), name='profile'),
]
