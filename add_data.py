# coding:utf-8
import django
import os
import json

from django.db import IntegrityError

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "banquetExpert.settings")

if django.VERSION >= (1, 7):  # 自动判断版本
    django.setup()


def add_super_admin():
    """添加后台超级管理员"""
    from webApp.models import Admin
    username = "admin"
    password = "admin"
    type = 1
    try:
        admin = Admin(username=username, password=password, type=type,
                      is_enabled=True)
        admin.update_token()
        admin.save()
    except IntegrityError:
        pass


def initial_authority():
    """初始化权限表"""
    from webApp.models import Authority
    Authority.objects.all().delete()
    try:
        with open('data/authority.json') as json_file:
            data = json.load(json_file)
            id = 1
            for authority in data:
                parent = Authority.objects.create(
                    id=id,
                    title=authority['title'],
                    name=authority['menu_id'])
                parent.save()
                id += 1
                item = authority['item']
                for i in item:
                    child = Authority.objects.create(
                        id=id,
                        title=i['title'],
                        name=i['item_id'],
                        parent_id=parent.id)
                    child.save()
                    id += 1
    except KeyError or ValueError:
        print('json文件解析出错')
    except IntegrityError:
        print('插入数据错误')

if __name__ == "__main__":
    add_super_admin()
    initial_authority()
