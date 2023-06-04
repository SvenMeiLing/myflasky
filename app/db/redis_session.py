# -*- coding: utf-8 -*-
# FileName: redis_session.py
# Time : 2023/4/30 18:11
# Author: zzy
from flask import g
from flask import current_app


def get_redis_session():
    if 'redis_session' not in g:
        g.redis_session = current_app.config.get("SESSION_REDIS")
    return g.redis_session
