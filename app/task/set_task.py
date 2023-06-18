# -*- coding: utf-8 -*-
# FileName: set_task.py
# Time : 2023/6/18 23:10
# Author: zzy
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab

cel = Celery(
    'celery_demo',
)

# 时区
cel.conf.timezone = 'Asia/Shanghai'
# 是否使用UTC
cel.conf.enable_utc = False

cel.conf.beat_schedule = {
    # 名字随意命名
    'add-every-10-seconds': {
        # 执行tasks1下的test_celery函数
        'task': 'app.task.remove_code_img',
        'schedule': crontab(hour="*/2"),
    },
}
