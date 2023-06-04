# -*- coding: utf-8 -*-
# FileName: check_login_state.py
# Time : 2023/5/2 23:45
# Author: zzy
import functools

from flask import redirect, url_for, request, make_response

from app.models.user import UserModel
from app.utils.cookie_key import decrypt_cookie, encrypt_cookie
from app.db.database import get_db_session


def login_required(view):
    """
    一个装饰器函数, 用于需要登录才能使用的视图
    :param view: view func
    :return: Response
    """

    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        cookie = request.cookies.get('email')

        if cookie == 'ipython':  # 开发特殊入口
            return view(*args, **kwargs)

        elif cookie is not None:  # 如果cookie中有email
            email = decrypt_cookie(cookie)
            if get_db_session().query(UserModel).filter(UserModel.email == email).first():
                return view(*args, **kwargs)  # 验证成功则正确响应

        return redirect(url_for('index'))  # 验证失败返回登录视图

    return wrapped_view
