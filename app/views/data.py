# -*- coding: utf-8 -*-
# FileName: admin.py
# Time : 2023/5/11 12:44
# Author: zzy
"""
remark: 提供一个api, 用于管理员调用数据
当管理员登录后会给管理员单独设置一个session, 这个session中存储管理员的access_token,
凭借这个token来请求相应的api来获取数据
"""
import math
from math import ceil

from flask import g, request, jsonify, make_response
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token
from flask_paginate import get_page_args, Pagination
from werkzeug.security import generate_password_hash, check_password_hash

from app.cache.data_cache import get_data
from app.instance.blacklist import BLACKLIST
from app.models.data import DataModel
from app.models.user import UserModel
from app.utils.cookie_key import decrypt_cookie


class DataShow(MethodView):
    secret = generate_password_hash("ipython")
    """
    获取用户ip, 如果ip在黑名单中无法打开开发者模式
    如果不在, 则可以正常访问, remote_addr
    """

    def get(self):  # 把accessToken传给ajax
        """
        此函数是获取cookie中的token, 所以过期要重新登录会自动生成新的token
        schema1: 携带count的请求, 要处理是否在黑名单中
        schema2: 携带secret的请求, 校验身份且返回access_token
        schema3: 携带email的请求, 校验用户身份
        """
        email = request.args.get("email", "null")
        auth_count = request.args.get("count")

        if auth_count is not None:  # 是否携带验证参数
            try:
                auth_count = int(auth_count)
            except AttributeError as e:
                return {"status": False}

            if request.remote_addr in BLACKLIST:
                return {"status": False}, 201
            if auth_count >= 5:
                BLACKLIST.add(request.remote_addr)
                return {"status": False}, 202
            return {"status": True}

        elif email:
            if check_password_hash(self.secret, email):
                return {
                    "access_token": create_access_token(identity=email)
                }, 200
            acc_tok = request.cookies.get("access_token_cookie")
            cok_email = decrypt_cookie(request.cookies.get("email"))
            if email == cok_email:  # cookie中存储的email和页面email一致
                return jsonify({"access_token": acc_tok})

            return {
                "msg": "If the verification fails, please log in again",
                "status": False
            }, 401

    @jwt_required(locations='headers')
    def post(self):
        force = request.get_json().get("refresh")
        result = []
        email = get_jwt_identity()  # 获取用户身份
        page = get_page_args(page_parameter="page")[0]

        page_size = 3
        page_start = (page - 1) * page_size
        page_end = page_start + page_size

        current_user = g.db_session.query(UserModel).filter(UserModel.email == email).first()

        if email == "admin@qq.com":
            admin_data = {
                "total":
                    get_data(DataModel)
                    if not force else g.db_session.query(DataModel).count()
                ,
                "data":
                    get_data(DataModel, "data")
                    if not force else g.db_session.query(DataModel).all()

            }
            print(admin_data["total"])
            # print("cache:-->", get_data(DataModel, "data")[-1].title)
            # print("nocache:-->", g.db_session.query(DataModel).all()[-1].title)

            total = math.ceil(admin_data["total"] / page_size)
            data_lst = admin_data['data'][page_start:page_end]
        else:
            user_data = {
                "total":
                    get_data(DataModel, filter_=DataModel.user_id == current_user.id)
                    if not force else g.db_session.query(DataModel).filter(DataModel.user_id == current_user.id).count()
                ,
                "data":
                    get_data(DataModel, "data", filter_=DataModel.user_id == current_user.id)
                    if not force else g.db_session.query(DataModel).filter(DataModel.user_id == current_user.id).all()
            }

            total = math.ceil(user_data["total"] / page_size)
            data_lst = user_data["data"][page_start:page_end]  # [base, base, ......]

        for data in data_lst:
            context = {
                "id": data.id,
                "title": data.title,
                "time": round(data.time, 2),
                "description": data.description,
                "filename": data.filename,
                "user_id": data.user_id
            }
            result.append(context)

        page_total, remainder = divmod(total, page_size)  # 页码数量
        if remainder:
            page_total += 1

        page_obj = Pagination(
            page=page,  # 当前页码
            total=page_total,  # db中数据总条数
            per_page=page_size,  # 每页展示数据条数
        )
        response = make_response(
            jsonify({
                "result": result if result else False,
                "pagination": {
                    'page': page_obj.page,
                    'total': total,
                    'per_page': page_obj.per_page,
                    'max_page': ceil(total / page_size),  # 页面最大数量
                    "next": page_obj.page + 1 if page < total else 1,
                    "prev": page_obj.page - 1 if page > 1 else 1
                }
            })
        )

        return response
