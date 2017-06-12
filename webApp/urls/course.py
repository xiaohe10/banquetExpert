from django.conf.urls import url

from webApp.views.course import List, OwnedList, Check

urlpatterns = [
    # 获取视频列表(get)
    url(r'^list/$', List.as_view(), name='list'),
    # 上传新的视频(post)
    url(r'^push/$', List.as_view(), name='push'),
    # 获取自己上传的视频列表(get)
    url(r'^owned_list/$', OwnedList.as_view(), name='owned_list'),
    # 视频审核
    url(r'^check/$', Check.as_view(), name='check'),
]
