from django import forms
from django.db import IntegrityError, transaction
from django.http import JsonResponse, HttpResponse
from django.views.generic import View

from ..utils.decorator import validate_args, validate_staff_token
from ..models import Course

__all__ = ['List']


class List(View):
    ORDERS = ('create_time', '-create_time')

    @validate_args({
        'token': forms.CharField(min_length=32, max_length=32),
        'tag': forms.CharField(min_length=1, max_length=20, required=False),
        'offset': forms.IntegerField(min_value=0, required=False),
        'limit': forms.IntegerField(min_value=0, required=False),
        'order': forms.IntegerField(min_value=0, max_value=1, required=False),
    })
    @validate_staff_token()
    def get(self, request, token, tag=None, offset=0, limit=10, order=1):
        """获取视频列表，返回已通过后台审核的视频

        :param token: 令牌(必传)
        :param tag: 标签, 默认获取全部
        :param offset: 起始值
        :param limit: 偏移量
        :param order: 排序方式
            0: 注册时间升序
            1: 注册时间降序（默认值）
            2: 昵称升序
            3: 昵称降序
        :return:
            count: 课程总数
            list: 课程列表
                course_id: ID
                videoID: 对应cc的videoID，如果课程需要付费且当前员工的酒店未付费则返回空
                price: 价格
                tags: 标签
                description: 描述
                create_time: 创建时间
        """

        if tag:
            c = Course.objects.filter(status=1, tags__icontains=tag).count()
            courses = Course.objects.filter(
                status=1, tags__icontains=tag).order_by(
                self.ORDERS[order])[offset:offset + limit]
        else:
            c = Course.objects.filter(status=1).count()
            courses = Course.objects.filter(status=1).order_by(
                self.ORDERS[order])[offset:offset + limit]
        l = []
        for c in courses:
            d = {'course_id': c.id,
                 'price': c.price,
                 'tags': c.tags,
                 'description': c.description,
                 'create_time': c.create_time}
            # 判断当前员工的酒店是否已经购买该课程，是则返回videoID，否则返回空
            if c.price == 0 or c.purchase_records.filter(
                    hotel=request.staff.hotel).exixt():
                d['videoID'] = c.videoID
            else:
                d['videoID'] = ''
            l.append(d)
        return JsonResponse({'count': c, 'list': l})

    @validate_args({
        'token': forms.CharField(min_length=32, max_length=32),
        'videoID': forms.CharField(min_length=1, max_length=20),
        'title': forms.CharField(min_length=1, max_length=20),
        'tags': forms.CharField(min_length=1, max_length=20),
        'description': forms.CharField(max_length=100, required=False),
        'price': forms.IntegerField(required=False),
    })
    @validate_staff_token()
    def post(self, request, token, videoID, title, tags, **kwargs):
        """

        :param token: 令牌(必传)
        :param videoID: 对应cc的videoID(必传)
        :param title: 标题(必传)
        :param tags: 标签(多个, 用"|"分割, 必传)
        :param kwargs:
            price: 价格
            description: 描述
        :return:
        """

        course_keys = ('price', 'description')
        with transaction.atomic():
            try:
                course = Course(videoID=videoID, title=title, tags=tags)
                for k in course_keys:
                    if k in kwargs:
                        setattr(course, k, kwargs[k])
                course.save()
                return HttpResponse('上传视频成功', status=200)
            except IntegrityError:
                return HttpResponse('上传视频失败', status=400)
