# -*- coding: utf-8 -*-
# FileName: delkey.py
# Time : 2023/5/10 12:53
# Author: zzy
def send_email(link, *receiver):
    msg = [
        "Hello! flask 向你发来了一条激活信息",
        [*(receiver if receiver else '2744726697@qq.com')],  # 收件人
        link
    ]

