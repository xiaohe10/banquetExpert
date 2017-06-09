from django.http import JsonResponse


def corr_response(data=None):
    """正确时的返回

    :param data: 字典
    """

    if data is None:
        params = {
            "status": "true",
        }
    else:
        params = {
            "status": "true",
            "data": data
        }
    print(params)
    return JsonResponse(params)


def err_response(err_code, description):
    """发生错误时的返回

    :param err_code: 错误码字符串
    :param description: 错误描述

    """
    params = {
        "status": "false",
        "err_code": err_code,
        "description": description
    }
    return JsonResponse(params)
