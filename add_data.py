# coding:utf-8
import django
import os

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

if __name__ == "__main__":
    add_super_admin()
