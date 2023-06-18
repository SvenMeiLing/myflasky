# -*- coding: utf-8 -*-
# FileName: crops_data.py
# Time : 2023/6/11 18:17
# Author: zzy
from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from ..scripts.read_json import use_region, get_province_option


class Crops(MethodView):

    @jwt_required(locations='cookies')
    def get(self):
        return get_province_option()

    @jwt_required(locations='cookies')
    def post(self):
        province = request.get_json().get("province", None)
        if not province:
            return {"error": "Missing argument!"}, 401
        try:
            return use_region(province)
        except KeyError as ke:
            return {"error": "此省份未收录在数据集中, 请等待给后续更新!"}
