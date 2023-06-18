# -*- coding: utf-8 -*-
# FileName: main.py
# Time : 2023/4/29 17:07
# Author: zzy
from json import JSONDecodeError

from flask import url_for, redirect, render_template, request, g

from app.create_app import create_app


app = create_app()  # 创建一个app


# 首页
@app.route("/", endpoint='index', methods=("GET", ))
def index():
    resp = redirect(url_for("user.login"))  # 把请求转发给login视图
    return resp


@app.errorhandler(404)  # 处理404的错误返回指定页面
def page_not_found(error):
    print(error)
    return render_template("404.html")


@app.errorhandler(JSONDecodeError)  # 处理500的状态码错误
def server_error(error):
    print(error)
    return "api off", 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
