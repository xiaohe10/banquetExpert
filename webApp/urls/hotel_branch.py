from django.conf.urls import url

from ..views.hotel_branch import *

urlpatterns = [
    # 获取门店的详情
    url(r'^profile/$', get_profile, name='get_profile'),
    # 获取门店区域列表
    url(r'^area/list/$', get_areas, name='get_area_list'),
    # 获取门店某日某餐段桌位使用情况列表
    url(r'^desk/list/$', get_desks, name='get_desk_list'),
]
