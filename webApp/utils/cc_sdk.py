import hashlib
import time
import json
import urllib.parse
import urllib.request

# CC Account
# http://doc.bokecc.com/

USER_ID = 'D1202B6FCA1991FD'
API_KEY = 'IahwRk1RJOTLi90JywVsmID87K3D9XJG'

CREATE_LIVE_URL = 'http://api.csslcloud.net/api/room/create'
UPDATE_LIVE_URL = 'http://api.csslcloud.net/api/room/update'
REPLAY_LIVE_URL = 'http://api.csslcloud.net/api/live/info'
QUERY_LIVE_URL = 'http://api.csslcloud.net/api/rooms/publishing'


def create_live_room(publisher_password, play_password, name, description):
    """调用CC接口，创建直播间

    :param publisher_password: 推送密码
    :param play_password: 播放密码
    :param name: 直播间名称
    :param description: 直播间描述
    :return
    """

    # 需要传输的参数
    query_map = {'userid': USER_ID,
                 'name': urllib.parse.quote(name),
                 'desc': urllib.parse.quote(description),
                 'templatetype': 5,
                 'authtype': 1,
                 'publisherpass': publisher_password,
                 'assistantpass': "beijingyan",
                 'playpass': play_password,
                 'barrage': 0,
                 'foreignpublish': 0}
    # 加密参数
    query_hash = create_hashed_query_string(query_map)

    url = CREATE_LIVE_URL + "?" + query_hash
    f = urllib.request.urlopen(url)

    content = f.read().decode('utf-8')
    res = json.loads(content)

    return res


def update_live_room(cc_room_id, publisher_password, play_password, name,
                     description):
    """调用CC接口，更新直播间信息

    :param cc_room_id: 对应CC上的roomid
    :param publisher_password: 推送密码
    :param play_password: 播放密码
    :param name: 直播间名称
    :param description: 直播间描述
    :return
    """

    # 需要传输的参数
    query_map = {'roomid': cc_room_id,
                 'userid': USER_ID,
                 'name': urllib.parse.quote(name),
                 'desc': urllib.parse.quote(description),
                 'authtype': 1,
                 'publisherpass': publisher_password,
                 'assistantpass': "beijingyan",
                 'playpass': play_password,
                 'barrage': 0}
    # 加密参数
    query_hash = create_hashed_query_string(query_map)

    url = UPDATE_LIVE_URL + "?" + query_hash
    f = urllib.request.urlopen(url)

    content = f.read().decode('utf-8')
    res = json.loads(content)
    print(res)
    return res


def query_live_room(cc_room_ids):
    """批量查询直播间状态

    :param cc_room_ids: 需要查询的房间列表
    :return
    """

    cc_room_id_str = ','.join(cc_room_ids)
    # 需要传输的参数
    query_map = {'userid': USER_ID,
                 'roomids': cc_room_id_str}
    # 加密参数
    query_hash = create_hashed_query_string(query_map)

    url = QUERY_LIVE_URL + "?" + query_hash
    f = urllib.request.urlopen(url)

    content = f.read().decode('utf-8')
    res = json.loads(content)

    return res


def create_hashed_query_string(query_map):
    """ 将一个Map按照Key字母升序构成一个QueryString.并且加入时间混淆的hash串

    :param query_map: query内容
    :return: 加密结果字符串
    """

    # 按key排序，拼接，转义
    sorted_keys = sorted(query_map.keys())
    query_str = ''
    for key in sorted_keys:
        if not query_str:
            query_str = key + "=" + str(query_map[key])
        else:
            query_str = query_str + "&" + key + "=" + str(query_map[key])

    # 获取时间戳
    now = int(time.time())

    # 拼接
    result_str = "{0}&time={1}&salt={2}".format(query_str, now, API_KEY)

    # MD5加密
    hash_str = hashlib.md5(result_str.encode(encoding='utf-8'))
    hash_str = hash_str.hexdigest().upper()

    result = "{0}&time={1}&hash={2}".format(query_str, now, hash_str)
    return result
