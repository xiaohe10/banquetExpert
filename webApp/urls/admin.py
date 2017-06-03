from django.conf.urls import url

from webApp.views.admin import *

urlpatterns = [
    # 获取管理者列表(get)/注册新的管理者(post)
    url(r'^$', AdminList.as_view(), name='admins'),
    # 登录(post)
    url(r'^token/$', Token.as_view(), name='token'),
    # 获取酒店列表(get)/注册新的酒店(post)
    url(r'^hotels/$', HotelList.as_view(), name='hotels'),
    # 修改酒店资料(post)
    url(r'^hotel/(?P<hotel_id>\d+)/profile/$', HotelProfile.as_view(),
        name='hotel_profile'),
    # 获取酒店头像(get)/修改酒店头像(post)
    url(r'^hotel/(?P<hotel_id>\d+)/icon/$', HotelIcon.as_view(),
        name='hotel_icon'),
    # 获取酒店员工列表(get)/注册新的员工(post)
    url(r'^staffs/(?P<hotel_id>\d+)/$', StaffList.as_view(), name='staffs'),
    # 修改员工资料, 包括账号审核(post)
    url(r'^staff/(?P<staff_id>\d+)/profile/$', StaffProfile.as_view(),
        name='staff_profile'),
]
