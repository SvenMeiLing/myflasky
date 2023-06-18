# -*- coding: utf-8 -*-
# FileName: other.py
# Time : 2023/6/18 21:17
# Author: zzy
from flask import current_app, render_template


# 等待激活
@current_app.route("/wait_activating", methods=("GET",))
def tips_active():
    return render_template("wait_activate.html")
