# -*- coding: utf-8 -*-
# FileName: database.py
# Time : 2023/4/29 17:31
# Author: zzy
from flask import g
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash

from app.scripts.load_config import load_configure

engine = create_engine(load_configure().get("SQLALCHEMY_DATABASE_URI"))  # 创建一个引擎

Base = declarative_base()  # 声明模型, Base是我们数据模型的基类


# Base.query = g.db_session.query_property()  # 创建一个查询属性 则可以这样写Base.query(User).all()
def get_db_session():
    """获取当前请求的数据库会话"""
    if 'db_session' not in g:
        g.db_session = scoped_session(  # 建立于数据库会话
            sessionmaker(
                autocommit=False,  # 关闭自动提交, 我们采取手动
                autoflush=False,  # 关闭自动刷新
                bind=engine))  # 绑定我们的引擎
    return g.db_session


def init_db():
    # 在这里导入定义模型所需要的所有模块，这样它们就会正确的注册在
    # 元数据上。否则你就必须在调用 init_db() 之前导入它们。
    from app.models import user
    from app.models import confirmation
    from app.models import data
    from app.models import plant_details
    Base.metadata.create_all(bind=engine)  # 创建模型定义的表


def init_data():  # 初始化用户
    """
    email: admin@qq.com
    password: admin
    :return:
    """
    from app.models.user import UserModel
    from app.models.data import DataModel  # 此处还需导入相互建立关系的模型
    from app.models.plant_details import PlantDetailModel
    session = g.db_session
    admin = UserModel(email="admin@qq.com", password=generate_password_hash("admin", "sha256", 8))
    user = session.query(UserModel).filter(UserModel.email == admin.email).first()
    if not user:
        session.add(admin)
        session.commit()
        session.flush(admin)

