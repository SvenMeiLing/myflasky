# -*- coding: utf-8 -*-
# FileName: user.py
# Time : 2023/5/10 11:16
# Author: zzy
import pickle
import uuid

from flask import make_response, render_template, request, g, session, current_app, redirect, url_for, abort, flash
from flask.views import View
from flask_jwt_extended import create_access_token, get_jwt_identity, set_access_cookies, jwt_required
from redis.client import Redis
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.confirmation import ConfirmationModel
from app.models.user import UserModel
from app.utils.check_login_state import login_required
from app.utils.cookie_key import encrypt_cookie, decrypt_cookie
from app.utils.generate_code import check_code, codeImgPath
from app.utils.send_email import send_email

t_code = [""]


class User(View):
    methods = ("GET", "POST")  # 允许的url
    register_template = "hint.html"
    login_template = "oldindex.html"
    encry_method = "sha256"  # 加密方法

    def get_register(self):
        return make_response(
            render_template(self.register_template), 200
        )

    def get_login(self):
        return render_template(self.login_template)

    def put_code(self):
        """发送验证码"""
        u4 = uuid.uuid4().hex
        img, code = check_code()
        code_file_name = str(codeImgPath) % u4
        img.save(code_file_name)  # 保存验证码图片
        g.redis_session.set(name="code:" + u4, value=code, ex=2000)  # 设置验证码, 专属于某个用户
        start = code_file_name.find('static')

        response = make_response({"filename": code_file_name[start:]})
        # 给cookie编码
        response.set_cookie("code_key", encrypt_cookie("code:" + u4))
        return response

    def post_register(self):  # 注册
        """
        首先对用户字段合法性校验, 然后存储用户信息, 和激活状态, 对于刚注册的用户:
            我们要存储到confirmation中并且, 发送一个激活链接或网页到这个邮箱, 点击网页链接, 进入一个路由,
            这个路由负责把数据库的activate字段改成True, 同时登陆校验也需要校验用户是否已激活.
        发送邮件后, 需要也给用户设置cookie email以防检查器不过关
        """
        form_data: dict = request.form  # 获取表单数据

        if ["email", "password"] == [key for key in form_data]:  # 请求携带必填字段
            if not g.db_session.query(UserModel).filter(
                    UserModel.email == form_data['email']
            ).first():  # 用户不存在则可以注册
                hash_password = generate_password_hash(form_data["password"], method=self.encry_method, salt_length=8)

                user = UserModel(email=form_data['email'], password=hash_password)

                g.db_session.add(user)
                g.db_session.commit()
                g.db_session.flush(user)

                confirmation = ConfirmationModel(user_id=user.id)
                confirmation.sava_to_db()
                # 将用户信息保存到 session 中
                session['email'] = user.email
                session['password'] = user.password

                # # 用户激活成功后将 session 存储到 Redis 中
                # g.redis_session.set('session:' + session.sid, str(session), ex=
                link = request.url_root + "/confirm/" + confirmation.id

                send_email(link, user.email)

                return render_template("wait_activate.html", email=user.email)
            return {"message": "User already exists"}
        return {"message": "缺少必填字段"}

    @classmethod
    def post_login(cls):
        reqs_json = request.get_json()  # 接受表单数据
        code_key = decrypt_cookie(request.cookies.get("code_key"))  # 获取code_key值
        code = g.redis_session.get(code_key).decode('utf-8')

        if reqs_json.get("code").upper() == code.upper():
            if reqs_json.get("email") and reqs_json.get("password"):  # 检测是否含有必填字段
                user = g.db_session.query(UserModel).filter(UserModel.email == reqs_json['email']).first()
                if not user:
                    return {"error": "邮箱不存在!"}, 401
                if not user.activated:  # 用户未激活
                    return {"activated": False, "email": user.email}, 402

                if check_password_hash(user.password, reqs_json["password"]):  # 校验成功
                    resp = make_response({"url": "/upload/file"}, 200)  # 创建一个重定向的响应对象

                    if request.cookies.get('email') != user.email:  # 先检查浏览器存储cookie-email是否和登录用户email一致
                        resp.set_cookie(  # 不一致则更新
                            'email',
                            encrypt_cookie(user.email),
                            max_age=60 * 60 * 24 * 7  # 设置一个有效期为一周的 cookie，max_age 单位为秒
                        )
                    set_access_cookies(  # 每次重新登录, 都重新颁发token
                        resp,
                        create_access_token(user.email),
                        max_age=60 * 60 * 24 * 7
                    )
                    g.redis_session.set('session:' + session.sid, str(session), ex=2000)
                    return resp

                return {
                    "url": "/user/login",
                    "error": '密码错误',
                    "email": reqs_json['email'] if reqs_json['email'] else ""
                }, 401
            return {"error": '缺少必填字段!'}
        return {"error": "验证码错误!"}, 401  # 此处要处理前端提示

    @classmethod
    def get_logout(cls):
        # 获取所有的 cookie 名称
        resp = make_response({"path": url_for("index")})
        cookie_names = request.cookies.keys()

        # 循环遍历所有 cookie 名称并将其过期时间设置为 0
        for cookie_name in cookie_names:
            resp.set_cookie(cookie_name, '', expires=0)
        resp.delete_cookie("email")  # 删cookie email
        g.redis_session.delete("session:" + session.sid)  # 删redis 缓存的session
        session.clear()  # 删cookie session...

        return resp

    @jwt_required(locations="cookies")
    def get_email(self):
        email = get_jwt_identity()
        return email

    def dispatch_request(self):
        endpoint = request.endpoint  # as_view("register") --> endpoint = users.register
        print(request.method, request.endpoint)

        if request.method == "GET":
            if 'user.register' == endpoint:
                return self.get_register()
            if 'user.code' == endpoint:
                return self.put_code()

            elif 'user.login' == endpoint:
                user_info = g.redis_session.get('session:' + session.sid)  # 获取redis中用户信息
                if user_info:
                    user_info = pickle.loads(user_info)  # 解析成dict类型
                    s_email, u_email = session.get('email'), user_info.get('email')
                    if s_email and u_email:
                        if s_email == u_email:
                            return {"url": "/file/uoload", "email": s_email}
                return self.get_login()

            elif 'user.logout' == endpoint:
                return self.get_logout()

            elif 'user.get_email' == endpoint:
                return self.get_email()

        elif request.method == "POST":
            if request.path == "/user/register":
                return self.post_register()

            elif request.path == "/user/login":

                return self.post_login()
