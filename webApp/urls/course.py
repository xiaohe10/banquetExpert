from django.conf.urls import url

from webApp.views.course import List

urlpatterns = [
    # 获取视频列表(get)/上传新的视频(post)
    url(r'^$', List.as_view(), name='list'),
]
