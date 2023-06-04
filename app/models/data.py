# -*- coding: utf-8 -*-
# FileName: data.py
# Time : 2023/5/11 12:57
# Author: zzy
from sqlalchemy import Column, Integer, String, ForeignKey, REAL  # 导入一些常用列类型
from sqlalchemy.orm import relationship

from app.db.database import Base


class DataModel(Base):
    __tablename__ = "data"

    id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=False)
    time = Column(REAL, nullable=False)
    description = Column(String(512))
    filename = Column(String(32))
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("UserModel", back_populates="data")

    def __init__(self, title, time, description, filename, user_id):
        self.title = title
        self.time = time
        self.description = description
        self.filename = filename
        self.user_id = user_id




