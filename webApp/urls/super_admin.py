from django.conf.urls import url

from webApp.views.super_admin import *

urlpatterns = [
    # 获取管理者列表(get)/注册新的管理者(post)/删除管理者(delete)
    url(r'^$', AdminList.as_view(), name='list'),
    # 登录(post)
    url(r'^token/$', Token.as_view(), name='token'),
    # 获取酒店列表(get)/注册新的酒店(post)/删除酒店(delete)
    url(r'^hotels/$', HotelList.as_view(), name='hotels'),
    # 修改酒店资料(post)
    url(r'^hotel/profile/$', HotelProfile.as_view(), name='hotel_profile'),
]
