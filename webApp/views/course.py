from django import forms
from django.db import IntegrityError, transaction

from ..utils.decorator import validate_args, validate_staff_token
from ..utils.response import corr_response, err_response
from ..models import Course


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'tag': forms.CharField(min_length=1, max_length=20, required=False),
    'offset': forms.IntegerField(min_value=0, required=False),
    'limit': forms.IntegerField(min_value=0, required=False),
    'order': forms.IntegerField(min_value=0, max_value=3, required=False),
})
@validate_staff_token()
def get_courses(request, token, tag=None, offset=0, limit=10, order=1):
    """获取视频列表，返回已通过后台审核的视频

    :param token: 令牌(必传)
    :param tag: 标签, 默认获取全部
    :param offset: 起始值
    :param limit: 偏移量
    :param order: 排序方式
        0: 注册时间升序
        1: 注册时间降序（默认值）
        2: 标题升序
        3: 标题降序
    :return:
        count: 课程总数
        list: 课程列表
            course_id: ID
            title: 课程标题
            pusher: 上传者姓名
            buyer_count: 已购买数
            cc_video_id: 对应CC的videoid，如果课程需要付费且当前员工的酒店未付费则返回空
            price: 价格
            tags: 标签
            description: 描述
            create_time: 创建时间
    """
    ORDERS = ('create_time', '-create_time', 'title', '-title')

    if tag:
        c = Course.objects.filter(status=1, tags__icontains=tag).count()
        courses = Course.objects.filter(
            status=1, tags__icontains=tag).order_by(
            ORDERS[order])[offset:offset + limit]
    else:
        c = Course.objects.filter(status=1).count()
        courses = Course.objects.filter(status=1).order_by(
            ORDERS[order])[offset:offset + limit]
    l = []
    for course in courses:
        d = {'course_id': course.id,
             'price': course.price,
             'title': course.title,
             'pusher': course.staff.name,
             'tags': course.tags,
             'buyer_count': course.purchase_records.count(),
             'description': course.description,
             'create_time': course.create_time}

        # 判断当前员工的酒店是否已经购买该课程，是则返回videoid，否则返回空
        if (course.price == 0) or (course.staff == request.staff) or \
                (course.purchase_records.filter(
                    hotel=request.staff.hotel).exixt()):
            d['cc_video_id'] = course.cc_video_id
        else:
            d['cc_video_id'] = ''
        l.append(d)
    return corr_response({'count': c, 'list': l})


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'cc_video_id': forms.CharField(min_length=1, max_length=32),
    'title': forms.CharField(min_length=1, max_length=20),
    'tags': forms.CharField(min_length=1, max_length=20),
    'description': forms.CharField(max_length=100, required=False),
    'price': forms.IntegerField(required=False),
})
@validate_staff_token()
def push_course(request, token, cc_video_id, title, tags, **kwargs):
    """

    :param token: 令牌(必传)
    :param cc_video_id: 对应CC的videoid(必传)
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
            course = Course(cc_video_id=cc_video_id, title=title, tags=tags)
            for k in course_keys:
                if k in kwargs:
                    setattr(course, k, kwargs[k])
            course.save()
            return corr_response()
        except IntegrityError:
            return err_response('err_2', '服务器上传视频失败')


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'offset': forms.IntegerField(min_value=0, required=False),
    'limit': forms.IntegerField(min_value=0, required=False),
    'order': forms.IntegerField(min_value=0, max_value=3, required=False),
})
@validate_staff_token()
def get_owned_courses(request, token, offset=0, limit=10, order=1):
    """获取自己发布的视频列表

    :param token: 令牌(必传)
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
            title: 课程标题
            buyer_count: 已购买数
            cc_video_id: 对应cc的videoid
            price: 价格
            tags: 标签
            status: 课程状态, 0: 待审核, 1: 审核通过, 2: 审核未通过
            description: 描述
            create_time: 创建时间
    """
    ORDERS = ('create_time', '-create_time', 'title', '-title')

    c = request.staff.courses.count()
    courses = request.staff.courses.order_by(
        ORDERS[order])[offset:offset + limit]
    l = [{'course_id': course.id,
          'cc_video_id': course.cc_video_id,
          'status': course.status,
          'buyer_count': course.purchase_records.count(),
          'price': course.price,
          'title': course.title,
          'tags': course.tags,
          'description': course.description,
          'create_time': course.create_time} for course in courses]
    return corr_response({'count': c, 'list': l})


@validate_args({
    'token': forms.CharField(min_length=32, max_length=32),
    'course_id': forms.IntegerField(),
    'status': forms.IntegerField(min_value=1, max_value=2),
})
@validate_staff_token()
def check_course(request, token, course_id, status):
    """视频审核

    :param token: 令牌(必传)
    :param course_id: 课程ID
    :param status: 审核结果, 1: 审核通过, 2: 审核未通过
    :return 200
    """

    # 验证是否有权限审核视频
    # todo

    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return err_response('err_4', '课程不存在')

    course.status = status
    corr_response()
