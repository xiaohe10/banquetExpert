from django.conf.urls import url

from webApp.views.live import List, SubscribedList, PlayBack

urlpatterns = [
    # 获取直播间列表(get)
    url(r'^list/$', List.as_view(), name='list'),
    # 获取自己预约的直播间列表(get)
    url(r'^subscribed_list/$', SubscribedList.as_view(),
        name='subscribed_list'),
    # 预约直播间(post)
    url(r'^subscribe/$', SubscribedList.as_view(), name='subscribe'),
    # 获取直播间的回放列表
    url(r'^playback/', PlayBack.as_view(), name='play_back'),
]
