import string

from random import choice
from django import forms
from django.db import IntegrityError, transaction
from django.http import JsonResponse, HttpResponse
from django.views.generic import View

from ..utils.decorator import validate_args, validate_staff_token
from ..utils.cc_sdk import create_live_room, query_live_room
from ..models import Live

__all__ = ['List', 'OwnedList']


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
        """获取直播间列表

        :param token: 令牌(必传)
        :param offset: 起始值
        :param limit: 偏移量
        :param order: 排序方式
            0: 注册时间升序
            1: 注册时间降序（默认值）
            2: 昵称升序
            3: 昵称降序
        :return:
            count: 直播总数
            list: 直播列表
                live_id: ID
                cc_room_id: 对应CC的roomid
                status: 直播间状态, 0: 未开始, 1: 正在直播
                play_password: 播放密码，如果直播需要付费且当前员工的酒店未付费则返回空
                price: 价格
                buyer_count: 已购买数
                description: 描述
                start_date: 直播开始日期
                end_date: 直播结束日期
                start_time: 直播开始时间
                end_time: 直播结束时间
                create_time: 创建时间
        """

        c = Live.objects.all().count()
        lives = Live.objects.all().order_by(
            self.ORDERS[order])[offset:offset + limit]
        # 批量查询直播间状态
        cc_room_ids = [live.cc_room_id for live in lives]
        res = query_live_room(cc_room_ids)
        if res['result'] != 'OK':
            return HttpResponse('查询直播间状态失败', status=400)
        try:
            rooms = res['rooms']
            rooms_status = {room['roomId']: room['liveStatus'] for room
                            in rooms}
        except KeyError:
            return HttpResponse('查询直播间状态失败', status=400)
        l = []
        for live in lives:
            cc_room_id = live.cc_room_id
            d = {'live_id': live.id,
                 'cc_room_id': cc_room_id,
                 'price': live.price,
                 'buyer_count': live.purchase_records.count(),
                 'description': live.description,
                 'start_date': live.start_date,
                 'end_date': live.end_date,
                 'start_time': live.start_time,
                 'end_time': live.end_time,
                 'create_time': live.create_time}

            # 判断当前员工的酒店是否已经购买该直播，是则返回播放密码，否则返回空
            if live.price == 0 or live.purchase_records.filter(
                    hotel=request.staff.hotel).exixt():
                d['play_password'] = live.play_password
            else:
                d['play_password'] = ''
            # 读取直播间状态
            if cc_room_id in rooms_status:
                d['status'] = rooms_status[cc_room_id]
            else:
                d['status'] = 0
            l.append(d)
        return JsonResponse({'count': c, 'list': l})

    @validate_args({
        'token': forms.CharField(min_length=32, max_length=32),
        'name': forms.CharField(min_length=1, max_length=20),
        'start_date': forms.DateField(),
        'end_date': forms.DateField(),
        'start_time': forms.TimeField(),
        'end_time': forms.TimeField(),
        'price': forms.IntegerField(required=False),
        'description': forms.CharField(max_length=100, required=False),
    })
    @validate_staff_token()
    def post(self, request, token, name, **kwargs):
        """

        :param token: 令牌(必传)
        :param name: 直播间名称(必传)
        :param kwargs:
            start_date: 开始日期(必传)
            end_date: 结束日期(必传)
            start_time: 开始时间(必传)
            end_time: 结束时间(必传)
            price: 价格
            description: 描述
        :return:
            live_id: 直播间id
            cc_room_id: 对应cc上的roomid
            publisher_password: 推送密码
        """

        # 验证当前用户是否有权限发布直播
        # todo
        description = kwargs['description'] if 'description' in kwargs else ''

        live_keys = ('start_date', 'end_date', 'start_time', 'end_time',
                     'price')
        # 生成推送和播放随机密码
        chars = string.ascii_letters + string.digits
        publisher_password = ''.join([choice(chars) for i in range(6)])
        play_password = ''.join([choice(chars) for i in range(6)])

        with transaction.atomic():
            try:
                # 向CC发送http请求，创建直播间
                res = create_live_room(publisher_password, play_password,
                                       name, description)
                try:
                    if res['result'] == 'OK':
                        cc_room_id = res['room']['id']
                    else:
                        return HttpResponse('创建直播间失败', status=400)
                except KeyError:
                    return HttpResponse('创建直播间失败', status=400)
                live = Live(cc_room_id=cc_room_id, name=name,
                            description=description, staff=request.staff)
                for k in live_keys:
                    if k in kwargs:
                        setattr(live, k, kwargs[k])
                live.save()
                d = {'live_id': live.id,
                     'cc_room_id': cc_room_id,
                     'publisher_password': publisher_password}
                return JsonResponse(d)
            except IntegrityError:
                return HttpResponse('创建直播间失败', status=400)


class OwnedList(View):
    ORDERS = ('create_time', '-create_time', 'name', '-name')

    @validate_args({
        'token': forms.CharField(min_length=32, max_length=32),
        'offset': forms.IntegerField(min_value=0, required=False),
        'limit': forms.IntegerField(min_value=0, required=False),
        'order': forms.IntegerField(min_value=0, max_value=3, required=False),
    })
    @validate_staff_token()
    def get(self, request, token, offset=0, limit=10, order=1):
        """获取自己创建的直播间
        :param token: 令牌(必传)
        :param offset: 起始值
        :param limit: 偏移量
        :param order: 排序方式
            0: 注册时间升序
            1: 注册时间降序（默认值）
            2: 昵称升序
            3: 昵称降序
        :return:
            count: 直播总数
            list: 直播列表
                live_id: ID
                cc_room_id: 对应cc的roomid
                publisher_password: 推送密码
                price: 价格
                buyer_count: 已购买数
                description: 描述
                start_date: 直播开始日期
                end_date: 直播结束日期
                start_time: 直播开始时间
                end_time: 直播结束时间
                create_time: 创建时间
        """

        c = request.staff.lives.count()
        lives = request.staff.lives.order_by(
            self.ORDERS[order])[offset:offset + limit]
        l = [{'live_id': live.id,
              'cc_room_id': live.cc_room_id,
              'price': live.price,
              'buyer_count': live.purchase_records.count(),
              'publisher_password': live.play_password,
              'description': live.description,
              'start_date': live.start_date,
              'end_date': live.end_date,
              'start_time': live.start_time,
              'end_time': live.end_time,
              'create_time': live.create_time} for live in lives]
        return JsonResponse({'count': c, 'list': l})
