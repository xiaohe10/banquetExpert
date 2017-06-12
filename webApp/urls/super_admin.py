from django.conf.urls import url

from webApp.views.super_admin import *

urlpatterns = [
    # 获取管理者列表(get)
    url(r'^list/$', AdminList.as_view(), name='list'),
    # 注册新的管理者(post)
    url(r'^register/$', AdminList.as_view(), name='register'),
    # 删除管理者(delete)
    url(r'^delete/$', AdminList.as_view(), name='delete'),
    # 登录(post)
    url(r'^login/$', Token.as_view(), name='login'),
    # 获取酒店列表(get)
    url(r'^hotel/list/$', HotelList.as_view(), name='hotel_list'),
    # 注册新的酒店(post)
    url(r'^hotel/register/$', HotelList.as_view(), name='hotel_register'),
    # 删除酒店(delete)
    url(r'^hotel/delete/$', HotelList.as_view(), name='hotel_delete'),
    # 获取酒店资料(get)/修改酒店资料(post)
    url(r'^hotel/profile/$', HotelProfile.as_view(), name='hotel_profile'),
]
