from django.conf.urls import url

from webApp.views.live import List, OwnedList

urlpatterns = [
    # 获取直播间列表(get)/发布直播(post)
    url(r'^$', List.as_view(), name='list'),
    # 获取自己的直播间列表(get)
    url(r'^owned/$', OwnedList.as_view(), name='owned_list'),
]
