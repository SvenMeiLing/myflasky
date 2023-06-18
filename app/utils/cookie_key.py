# -*- coding: utf-8 -*-
# FileName: cookie_key.py
# Time : 2023/5/4 13:48
# Author: zzy

import base64


def encrypt_cookie(value):
    # 先转换成字节串
    data = value.encode('utf-8')
    # 进行base64编码
    encoded = base64.urlsafe_b64encode(data)
    # 返回加密后的信息
    return encoded.decode('utf-8')


def decrypt_cookie(data):
    # 先进行base64解码
    decoded = base64.urlsafe_b64decode(data.encode('utf-8'))
    # 将解码后的字节串转换成字符串
    email = decoded.decode('utf-8')
    # 返回解密后的邮箱
    return email

