from django.conf.urls import url

from webApp.views.score import *

urlpatterns = [
    # 搜索订单评分
    url(r'^search/$', search_scores, name='search'),
]
