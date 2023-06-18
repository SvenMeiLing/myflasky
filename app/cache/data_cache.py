# -*- coding: utf-8 -*-
# FileName: data_cache.py
# Time : 2023/5/15 21:17
# Author: zzy
from flask import g

from app.create_app import cache
from sqlalchemy.ext.declarative import declarative_base

"""
如果我想使用缓存, 首先需要把所有数据都取过来, 用一个函数打包这些数据, 
然后用视图函数来处理我每次这些数据到底要展示多少, 响应多少条记录
"""


@cache.memoize()
def get_data(
        model: declarative_base,
        schema="total",
        filter_by=None,
):
    """
    description:
        提取处于缓存中的数据或数据条数, 可选的过滤条件
        
    :param model: sqlalchemy模型类
    :param schema: "total" or "data"
    :param filter_by: 过滤数据条件
    :return: 经过缓存的数据
    """
    if schema == "total":
        if filter_by is not None:
            return g.db_session.query(model).filter(filter_by).count()
        return g.db_session.query(model).count()

    elif schema == "data":
        print(filter_by)
        if filter_by is not None:
            return g.db_session.query(model).filter(filter_by).all()
        return g.db_session.query(model).all()
    else:
        raise "scheme参数错误."


def group_by_(model, field, filter_=None):
    from sqlalchemy import func
    """
    给某个字段做分组
    :param model: 要分组的表
    :param field: 要分组的字段
    :param filter_: 过滤条件
    :return: 分组后的数据总条数
    """
    if filter_ is not None:
        return g.db_session.query(func.count, getattr(model, field)).group_by(getattr(model, field)).filter(filter_).all()
    return g.db_session.query(func.count, getattr(model, field)).group_by(getattr(model, field)).all()
