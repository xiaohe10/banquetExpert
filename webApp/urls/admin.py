from django.conf.urls import url

from webApp.views.admin import *

urlpatterns = [
    # 登录(post)
    url(r'^token/$', Token.as_view(), name='token'),
    # 修改酒店资料(post)
    url(r'^hotel/profile/$', HotelProfile.as_view(), name='hotel_profile'),
    # 获取酒店门店列表(get)/注册新的门店(post)/删除门店(delete)
    url(r'^hotel_branch/profile/$',
        HotelBranchList.as_view(), name='hotel_branch'),
    # 获取酒店员工列表(get)/注册新的员工(post)/删除员工(delete)
    url(r'^staffs/$', StaffList.as_view(), name='staffs'),
    # 获取员工资料(get)/修改员工资料, 包括账号审核(post)
    url(r'^staff/profile/$', StaffProfile.as_view(),
        name='staff_profile'),
]
