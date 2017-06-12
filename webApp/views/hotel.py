from django import forms
from django.views.generic import View

from ..utils.decorator import validate_args, validate_staff_token
from ..utils.response import corr_response, err_response
from ..models import Hotel

__all__ = ['List']


class List(View):
    ORDERS = ('create_time', '-create_time', 'name', '-name')

    @validate_args({
        'token': forms.CharField(min_length=32, max_length=32),
        'offset': forms.IntegerField(min_value=0, required=False),
        'limit': forms.IntegerField(min_value=0, required=False),
        'order': forms.IntegerField(min_value=0, max_value=3, required=False),
    })
    @validate_staff_token()
    def get(self, request, token, offset=0, limit=10, order=1):
        """获取酒店列表

        :param token: 令牌(必传)
        :param offset: 起始值
        :param limit: 偏移量
        :param order: 排序方式
            0: 注册时间升序
            1: 注册时间降序（默认值）
            2: 名称升序
            3: 名称降序
        :return:
            count: 酒店总数
            list: 酒店列表
                hotel_id: ID
                name: 名称
                icon: 头像
                branches_count: 门店数
                owner_name: 法人代表
                create_time: 创建时间
        """

        c = Hotel.enabled_objects.count()
        hotels = Hotel.enabled_objects.order_by(
            self.ORDERS[order])[offset:offset + limit]
        l = [{'hotel_id': h.id,
              'name': h.name,
              'icon': h.icon,
              'branches_count': h.branches.count(),
              'owner_name': h.owner_name,
              'create_time': h.create_time} for h in hotels]
        return corr_response({'count': c, 'list': l})
