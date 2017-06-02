from django.conf.urls import url

from webApp.views.admin import *

urlpatterns = [
    # 获取管理者列表(get)/注册新的管理者(post)
    url(r'^$', AdminList.as_view(), name='admins'),
    # 登录(post)
    url(r'^token/$', Token.as_view(), name='token'),
    # 获取酒店员工列表(get)/注册新的员工(post)
    url(r'^staffs/$', StaffList.as_view(), name='staffs'),
    # 修改员工资料, 包括账号审核(post)
    url(r'^staff/$', StaffProfile.as_view(), name='staff'),
]
