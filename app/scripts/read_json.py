# -*- coding: utf-8 -*-
# FileName: read_json.py
# Time : 2023/6/11 15:15
# Author: zzy
import pprint
from json import load
from .load_config import PROJECT_APP_DIR


def read_json(j_file: str = "db/crops.json") -> dict:
    """
    读取json文件
    :param j_file: 文件路径, 以base_url开头
    :return: 字典形式返回
    """
    json_file = PROJECT_APP_DIR / j_file
    with open(json_file, 'r', encoding='utf-8') as j:
        json = load(j)
    return json


def get_province_option(callback=read_json):
    return [key for key in callback()]


def use_region(province: str, callback=read_json) -> dict | str:
    """
    使用地区获取农作物详情, ex: 北京
    :param province: 北京
    :param callback: 可调用的, 默认为read_json()
    :return: {
                土壤质量: " ",
                大豆: {
                    "": "", ...
                }
            }
    """
    return callback().get(province, "暂未收录此地区, 等待更新")


