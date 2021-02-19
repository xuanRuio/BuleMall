# -*- encoding: utf-8 -*-
"""
@File    : demo.py
@Time    : 2021/*/* 00:00
@Author  : xuanRui
"""
import django
import os

""" 导入环境; 启动环境; """

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BuleMall.settings.dev")
django.setup()

""" 操作模型 """

from apps.users.models import User
# 增加用户
User.objects.create(username='xuanRui',mobile='13753949664',password='123456')
res = User.objects.all()
print(res)