from django.conf.urls import url

from webApp.views.live import *

urlpatterns = [
    # 获取直播间列表
    url(r'^list/$', get_lives, name='list'),
    # 获取自己预约的直播间列表
    url(r'^subscribed_list/$', get_subscribed_lives,
        name='subscribed_list'),
    # 预约直播间
    url(r'^subscribe/$', subscribe_live, name='subscribe'),
    # 获取直播间的回放列表
    url(r'^playback/$', get_subscribed_lives, name='play_back'),
]
