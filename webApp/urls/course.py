from django.conf.urls import url

from webApp.views.course import *

urlpatterns = [
    # 获取视频列表
    url(r'^list/$', get_courses, name='list'),
    # 上传新的视频
    url(r'^push/$', push_course, name='push'),
    # 获取自己上传的视频列表
    url(r'^owned_list/$', get_owned_courses, name='owned_list'),
    # 视频审核
    url(r'^check/$', check_course, name='check'),
]
