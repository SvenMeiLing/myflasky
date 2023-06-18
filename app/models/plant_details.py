# -*- coding: utf-8 -*-
# FileName: plant_details.py
# Time : 2023/6/15 8:49
# Author: zzy
from sqlalchemy import (  # 导入一些常用列类型
    Column,
    Integer,
    String,
    ForeignKey,
    REAL,
    Date
)
from sqlalchemy.orm import relationship

from app.db.database import Base


class PlantDetailModel(Base):
    __tablename__ = "plant_details"

    id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=False)
    time_consume = Column(REAL, nullable=False)
    description = Column(String(512))
    date = Column(Date)
    filename = Column(String(32))
    recognition_rate = Column(REAL, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("UserModel", back_populates="plant_details")

    def __init__(
            self,
            title, time_consume,
            description, date,
            filename, recognition_rate,
            user_id
    ):
        self.title = title
        self.time_consume = time_consume
        self.description = description
        self.date = date
        self.filename = filename
        self.recognition_rate = recognition_rate
        self.user_id = user_id
