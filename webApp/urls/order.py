from django.conf.urls import url

from ..views.order import *

urlpatterns = [
    # 搜索订单
    url(r'^search/$', search_orders, name='search'),
    # 获取订单详细信息
    url(r'^profile/$', get_profile, name='profile'),
    # 提交订单
    url(r'^submit/$', submit_order, name='submit'),
    # 修改订单
    url(r'^modify/$', modify_order, name='modify'),
]
