import json
import urllib.parse
import urllib.request


def send_message(phone, code, m="GET"):
    """调用聚合数据api 发送短信"""
    data = dict()
    # 模版
    data['tpl_id'] = "39335"
    data['key'] = '8c1e68771e359596efdf92866afed9db'
    data['mobile'] = phone
    data['tpl_value'] = urllib.parse.quote('#code#=%s' % code)
    params = urllib.parse.urlencode(data)
    url = "http://v.juhe.cn/sms/send"
    if m == "GET":
        wp = urllib.request.urlopen("%s?%s" % (url, params))
    else:
        wp = urllib.request.urlopen(url, params)

    content = wp.read()  # 获取接口返回内容

    result = json.loads(content)

    if result:
        error_code = result['error_code']
        if error_code == 0:
            # 发送成功
            return 1
        else:
            # 发送失败
            return 0
    else:
        # 请求失败
        return 0
