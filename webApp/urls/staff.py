from django.conf.urls import url

from webApp.views.staff import *

urlpatterns = [
    # 获取员工列表(get)/员工注册(post)
    url(r'^$', List.as_view(), name='staffs'),
    # 登录(post)
    url(r'^token/$', Token.as_view(), name='token'),
    # 修改密码(post)
    url(r'^password/$', Password.as_view(), name='password'),
    # 获取头像(get)/修改头像(post)
    url(r'^icon/$', Icon.as_view(), name='icon'),
    # 获取资料(get)/修改个人资料(post)
    url(r'^profile/$', Profile.as_view(), name='profile'),
]
