from django.conf.urls import url

from webApp.views.course import List

urlpatterns = [
    # 获取视频列表(get)/上传新的视频(post)
    url(r'^$', List.as_view(), name='list'),
    # 获取自己上传的视频列表(get)
    url(r'^owned/$', List.as_view(), name='list'),
]
