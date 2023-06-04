# -*- coding: utf-8 -*-
# FileName: uploadfile.py
# Time : 2023/5/10 11:17
# Author: zzy
import binascii
import time

from flask import render_template, request, jsonify, g
from flask.views import View

from app.models.data import DataModel
from app.utils.check_login_state import login_required, decrypt_cookie
from app.utils.get_baike import get_baike
from app.vision.image_analysis import get_analysis_index, retrieval_result
from ..models.user import UserModel
from ..scripts.load_config import PROJECT_APP_DIR


class UpLoadFile(View):
    methods = ("GET", "POST")
    upload_template = "menu_layout.html"

    @login_required
    def get_page(self):  # 返回页面供用户上传文件
        cookie_email = request.cookies.get('email')
        if cookie_email == 'ipython':  # 开放特殊入口
            return render_template(self.upload_template, email='test@qq.com')

        cookie_email = decrypt_cookie(cookie_email)
        return render_template(self.upload_template, email=cookie_email)

    @classmethod
    def new_post(cls):  # 接收文件上传
        files = request.files.getlist("file")  # 获取文件列表
        file_names = []  # 存放识别图片的 文件名
        time_tables = []  # 存放识别图片的 耗时数据
        result = []  # 存放响应数据
        insert_data = []  # 存放dataModel对象的

        for file in files:
            filename = file.filename
            file.save(f'{PROJECT_APP_DIR}/upload/' + filename)
            file_names.append(filename)

            # 此处调用识别函数获取结果, 提取关键字, 把每个内容封装成字典加入上面列表
            start_time = time.perf_counter()
            name = retrieval_result(get_analysis_index, f'{PROJECT_APP_DIR}/upload/' + filename)
            end_time = time.perf_counter()

            time_consuming = end_time - start_time
            context = {"name": name, "description": get_baike(name), "time": round(time_consuming, 2)}

            result.append(context)
            time_tables.append(time_consuming)

        email = request.cookies.get('email')

        current_user = None
        current_email = None
        try:
            current_email = decrypt_cookie(email)
            current_user = g.db_session.query(UserModel).filter(UserModel.email == current_email).first()
        except binascii.Error as ipe:
            print(ipe, "测试用户登录此报错正常")

        for i, res in enumerate(result):
            name, description = res.get("name"), res.get("description")

            data = DataModel(
                title=name,
                time=time_tables[i],
                description=description,
                filename=file_names[i],
                user_id=current_user.id if current_email else '1'
            )
            insert_data.append(data)

        g.db_session.add_all(insert_data)  # 批量插入多条记录
        g.db_session.commit()

        return jsonify({
            "result": result
        })

    def dispatch_request(self):
        if request.method == "GET":
            return self.get_page()
        return self.new_post()
