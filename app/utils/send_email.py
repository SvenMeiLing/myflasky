# -*- coding: utf-8 -*-
# FileName: send_email.py
# Time : 2023/5/9 21:17
# Author: zzy
from flask_mail import Message
from flask import g


def send_email(link, *receiver):

    msg = Message(
        "Hello! flask 向你发来了一条激活信息",
        recipients=[*(receiver if receiver else '2744726697@qq.com')],  # 收件人
        body=link
    )
    g.mail.send(msg)


