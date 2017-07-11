from django.conf.urls import url

from ..views.intelligent_ordering import *
urlpatterns = [
    # 登录
    url(r'^login/$', login, name='login'),
    # 获取客户档案详情
    url(r'profile/$', get_profile, name='profile'),
    # 获取电话处理列表
    url(r'call_record/list', get_call_records, name='get_call_records'),
    # 保存电话来电记录
    url(r'call_record/save', save_call_record, name='save_call_record'),
]
