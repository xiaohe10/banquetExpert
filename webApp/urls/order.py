from django.conf.urls import url

from ..views.order import *

urlpatterns = [
    # 搜索订单
    url(r'^search/$', search_orders, name='search'),
    # 获取订单详细信息
    url(r'^profile/$', get_profile, name='profile'),
    # 提交订单
    url(r'^submit/$', submit_order, name='submit'),
    # 补录订单
    url(r'^supply/$', supply_order, name='supply'),
    # 修改订单
    url(r'^update/$', modify_order, name='modify'),
    # 获取订单操作日志
    url(r'^log/list/$', get_order_logs, name='log_list'),
    # 搜索订单操作日志
    url(r'^log/search/$', search_order_logs, name='log_search'),
    # 获取月订单列表
    url(r'^month_list/$', get_month_orders, name='month_list'),
    # 获取日订单列表
    url(r'^day_list/$', get_day_orders, name='day_list'),
]
