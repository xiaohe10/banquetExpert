from django.conf.urls import url

from webApp.views.score import *

urlpatterns = [
    # 搜索订单评分
    url(r'^search/$', search_scores, name='search'),
    # 提交(修改)评分记录
    url(r'^submit/$', submit_score, name='submit'),
    # 审核评分
    url(r'^check/$', check_score, name='check'),
]
