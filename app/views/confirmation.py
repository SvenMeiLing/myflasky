# -*- coding: utf-8 -*-
# FileName: confirmation.py
# Time : 2023/5/10 11:18
# Author: zzy
from flask import request, g, render_template
from flask.views import MethodView

from app.models.confirmation import ConfirmationModel
from app.models.user import UserModel


class Confirmation(MethodView):
    """
    返回用户页面之前, 激活账号
    """
    confirmation = "confirmation.html"

    def get(self, _id):
        url = request.path[request.path.rindex("/") + 1:]  # 拿到请求id
        print(_id)
        confirm = ConfirmationModel.find_by_id(_id=_id)
        print(confirm.user_id)
        if confirm.expired:  # 如果过期
            return {"message": "The activate message has expired"}, 201
        user = g.db_session.query(UserModel).filter(UserModel.id == confirm.user_id).first()
        user.activated = True

        g.db_session.add(user)
        g.db_session.commit()
        g.db_session.flush(user)

        return render_template("confirmation.html")
        # g.db_session.query(ConfirmationModel).filter(ConfirmationModel.id == url)
        # return render_template(self.confirmation)
