# -*- coding: utf-8 -*-
# FileName: user.py
# Time : 2023/4/29 17:36
# Author: zzy
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean  # 导入一些常用列类型
from sqlalchemy.orm import relationship

from app.db.database import Base


class UserModel(Base):
    __tablename__ = 'users'  # 设置表名

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(120), unique=True)
    password = Column(String(10), nullable=False)
    activated = Column(Boolean, default=False)

    confirmation = relationship(
        # 懒惰加载意味着当你创建一个新的用户模型时未从数据库中检索确认, 当您访问属性时, 才进入数据库检索他
        "ConfirmationModel",
        lazy="dynamic",
        cascade="all, delete-orphan",  # 级联删除
        back_populates="user"
    )
    data = relationship(
        "DataModel",
        lazy="dynamic",
        cascade="all, delete-orphan",
        back_populates="user",
        #: 当你访问data对象的user属性时这会很有用
    )
    plant_details = relationship(
        "PlantDetailModel",
        lazy="dynamic",
        cascade="all, delete-orphan",
        back_populates="user"
    )

    def __init__(self, name=None, email=None, *, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.email
