from django import forms
from django.views.generic import View

from ..utils.decorator import validate_args, validate_staff_token
from ..utils.response import corr_response, err_response
from ..utils.cc_sdk import query_live_room, replay_live_room
from ..models import Live

__all__ = ['List', 'SubscribedList', 'PlayBack']


class List(View):
    ORDERS = ('create_time', '-create_time', 'name', '-name')

    @validate_args({
        'token': forms.CharField(min_length=32, max_length=32),
        'offset': forms.IntegerField(min_value=0, required=False),
        'limit': forms.IntegerField(min_value=0, required=False),
        'order': forms.IntegerField(min_value=0, max_value=3, required=False)
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
                name: 直播间名称
                hotel_name: 直播间所属酒店名
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

        rooms_status = {}
        # 批量查询直播间状态
        cc_room_ids = [live.cc_room_id for live in lives]
        if len(cc_room_ids) > 0:
            res = query_live_room(cc_room_ids)
            if res['result'] != 'OK':
                return err_response('err_4', '服务器查询直播间状态失败')
            try:
                rooms = res['rooms']
                rooms_status = {room['roomId']: room['liveStatus']
                                for room in rooms}
            except KeyError:
                return err_response('err_4', '服务器查询直播间状态失败')
        l = []
        for live in lives:
            cc_room_id = live.cc_room_id
            d = {'live_id': live.id,
                 'name': live.name,
                 'hotel_name': live.hotel.name,
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
            if (live.price == 0) or (live.hotel == request.staff.hotel) or \
                    (live.purchase_records.filter(
                        hotel=request.staff.hotel).exixt()):
                d['play_password'] = live.play_password
            else:
                d['play_password'] = ''
            # 读取直播间状态
            if cc_room_id in rooms_status:
                d['status'] = rooms_status[cc_room_id]
            else:
                d['status'] = 0
            l.append(d)
        return corr_response({'count': c, 'list': l})


class SubscribedList(View):
    ORDERS = ('create_time', '-create_time', 'name', '-name')

    @validate_args({
        'token': forms.CharField(min_length=32, max_length=32),
        'offset': forms.IntegerField(min_value=0, required=False),
        'limit': forms.IntegerField(min_value=0, required=False),
        'order': forms.IntegerField(min_value=0, max_value=3, required=False)
    })
    @validate_staff_token()
    def get(self, request, token, offset=0, limit=10, order=1):
        """获取自己预约的直播间
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
                name: 直播间名称
                hotel_name: 直播间所属酒店名
                cc_room_id: 对应cc的roomid
                play_password: 播放密码
                price: 价格
                buyer_count: 已购买数
                description: 描述
                start_date: 直播开始日期
                end_date: 直播结束日期
                start_time: 直播开始时间
                end_time: 直播结束时间
                create_time: 创建时间
        """

        c = request.staff.subscrib_lives.count()
        lives = request.staff.subscrib_lives.order_by(
            self.ORDERS[order])[offset:offset + limit]

        rooms_status = {}
        # 批量查询直播间状态
        cc_room_ids = [live.cc_room_id for live in lives]
        if len(cc_room_ids) > 0:
            res = query_live_room(cc_room_ids)
            if res['result'] != 'OK':
                return err_response('err_4', '服务器查询直播间状态失败')
            try:
                rooms = res['rooms']
                rooms_status = {room['roomId']: room['liveStatus']
                                for room in rooms}
            except KeyError:
                return err_response('err_4', '服务器查询直播间状态失败')
        l = []
        for live in lives:
            cc_room_id = live.cc_room_id
            d = {'live_id': live.id,
                 'name': live.name,
                 'hotel_name': live.hotel.name,
                 'cc_room_id': cc_room_id,
                 'price': live.price,
                 'play_password': live.play_password,
                 'buyer_count': live.purchase_records.count(),
                 'description': live.description,
                 'start_date': live.start_date,
                 'end_date': live.end_date,
                 'start_time': live.start_time,
                 'end_time': live.end_time,
                 'create_time': live.create_time}

            # 读取直播间状态
            if cc_room_id in rooms_status:
                d['status'] = rooms_status[cc_room_id]
            else:
                d['status'] = 0
            l.append(d)
        return corr_response({'count': c, 'list': l})

    @validate_args({
        'token': forms.CharField(min_length=32, max_length=32),
        'live_id': forms.IntegerField()
    })
    @validate_staff_token()
    def post(self, request, token, live_id):
        """预约直播间

        :param token: 员工令牌
        :param live_id: 直播间ID
        :return
        """

        staff = request.staff
        try:
            live = Live.objects.get(id=live_id)
        except Live.DoesNotExist:
            return err_response('err_4', '直播间不存在')

        if staff.subscribe_lives.filter(live=live).exists():
            return err_response('err_3', '已经预约了该直播间')

        # 检查该直播是否需要付款，同时该员工的酒店是否已付款
        if live.price > 0 and (live.hotel != staff.hotel) and \
                live.purchase_records.filter(hotel=staff.hotel).exists():
            return err_response('err_5', '该直播需要付款')
        else:
            staff.subscribe_lives.create(live)
            staff.save()
            return corr_response()


class PlayBack(View):
    @validate_args({
        'token': forms.CharField(min_length=32, max_length=32),
        'live_id': forms.IntegerField(),
        'page_index': forms.IntegerField(min_value=0, required=False),
        'page_num': forms.IntegerField(min_value=0, required=False),
    })
    @validate_staff_token()
    def get(self, request, token, live_id, page_index=1, page_num=10):
        """

        :param token: 令牌
        :param live_id: 直播间ID
        :param page_index: 页码起始值, 默认为1
        :param page_num: 每页数量, 默认为10
        :return:
            count: 回放数
            list:
                cc_live_id: 回放id
                start_time: 开始时间
                end_time: 结束时间
                record_status: 录制状态，0表示录制未结束，1表示录制完成
                record_video_id: 录制视频id，如果recordStatus为0则返回-1
                replay_url: 回放地址，当recordStatus为0时返回""
        """

        staff = request.staff
        try:
            live = Live.objects.get(id=live_id)
        except Live.DoesNotExist:
            return err_response('err_4', '直播间不存在')

        # 判断当前员工的酒店是否需要购买和是否已经购买该直播
        if (live.price > 0) and (live.hotel != staff.hotel) and \
                (not live.purchase_records.filter(hotel=staff.hotel).exixt()):
            return err_response('err_2', '未购买该直播')

        # 获取直播间回放
        res = replay_live_room(live.cc_room_id, page_index, page_num)
        if res['result'] != 'OK':
            return err_response('err_5', '服务器查询直播间状态失败')
        try:
            lives = res['lives']
            c = res['count']
        except KeyError:
            return err_response('err_5', '服务器查询直播间状态失败')

        l = [{'cc_live_id': cc_live['id'],
              'start_time': cc_live['startTime'],
              'end_time': cc_live['endTime'],
              'record_status': cc_live['recordStatus'],
              'record_video_id': cc_live['recordVideoId'],
              'replay_url': cc_live['replayUrl']} for cc_live in lives]

        return corr_response({'count': c, 'list': l})
