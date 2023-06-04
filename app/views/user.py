# -*- coding: utf-8 -*-
# FileName: user.py
# Time : 2023/5/10 11:16
# Author: zzy
import pickle

from flask import make_response, render_template, request, g, session, current_app, redirect, url_for, abort, flash
from flask.views import View
from flask_jwt_extended import create_access_token, get_jwt_identity, set_access_cookies, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.confirmation import ConfirmationModel
from app.models.user import UserModel
from app.utils.cookie_key import encrypt_cookie
from app.utils.generate_code import check_code, codeImgPath
from app.utils.send_email import send_email

t_code = [""]


class User(View):
    methods = ("GET", "POST")  # 允许的url
    register_template = "hint.html"
    login_template = "index.html"
    encry_method = "sha256"  # 加密方法

    def get_register(self):
        return make_response(
            render_template(self.register_template), 200
        )

    def get_login(self):
        img, code = check_code()
        img.save(codeImgPath)
        t_code[0] = code

        temp = render_template(self.login_template)
        response = make_response(temp)
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
        form_data = request.form  # 接受表单数据
        if form_data.get("code").upper() == t_code[0]:
            if form_data.get("email") and form_data.get("password"):  # 检测是否含有必填字段
                user = g.db_session.query(UserModel).filter(UserModel.email == form_data['email']).first()
                if not user:
                    return render_template("index.html", error="邮箱不存在")
                if not user.activated:  # 用户未激活
                    return render_template("wait_activate.html", email=user.email)

                if check_password_hash(user.password, form_data["password"]):  # 校验成功
                    resp = make_response(redirect("/file/upload"))  # 创建一个重定向的响应对象

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

                return render_template(
                    "index.html",
                    error='密码错误',
                    email=form_data['email'] if form_data['email'] else ""
                )
            return render_template("index.html", error='缺少必填字段')
        flash("验证码错误请重试!")
        return redirect(url_for("index"))
        # return render_template("index.html")

    @classmethod
    @jwt_required(locations="cookies")
    def get_logout(cls):
        resp = make_response({"path": url_for("index")})
        resp.delete_cookie("email")  # 删cookie email
        g.redis_session.delete("session:" + session.sid)  # 删redis 缓存的session
        session.clear()  # 删cookie session...
        return resp

    def dispatch_request(self):
        endpoint = request.endpoint  # as_view("register") --> endpoint = users.register

        if request.method == "GET":
            if 'user.register' == endpoint:
                return self.get_register()

            elif 'user.login' == endpoint:
                user_info = g.redis_session.get('session:' + session.sid)  # 获取redis中用户信息
                if user_info:
                    user_info = pickle.loads(user_info)  # 解析成dict类型
                    s_email, u_email = session.get('email'), user_info.get('email')
                    if s_email and u_email:
                        if s_email == u_email:
                            return render_template("menu_layout.html", email=s_email)
                return self.get_login()

            elif 'user.logout' == endpoint:
                return self.get_logout()

        elif request.method == "POST":
            if request.path == "/user/register":
                return self.post_register()

            elif request.path == "/user/login":

                return self.post_login()
