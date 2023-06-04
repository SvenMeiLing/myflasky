# -*- coding: utf-8 -*-
# FileName: confirmation.py
# Time : 2023/5/8 22:56
# Author: zzy
from time import time
from uuid import uuid4

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean  # 导入一些常用列类型
from sqlalchemy.orm import relationship
from flask import g

from app.db.database import Base

CONFIRMATION_EXPIRATION_DELTA = 1800  # 30 min


class ConfirmationModel(Base):
    __tablename__ = 'confirmations'  # 设置表名

    id = Column(String(50), primary_key=True)
    expire_at = Column(Integer, nullable=False)
    confirmed = Column(Boolean, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("UserModel", back_populates="confirmation")

    def __init__(self, user_id: int, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.id = uuid4().hex
        self.expire_at = int(time()) + CONFIRMATION_EXPIRATION_DELTA  # 加时30分钟, 作为激活期限
        self.confirmed = False

    @classmethod
    def find_by_id(cls, _id: int) -> "ConfirmationModel":
        return g.db_session.query(cls).filter(cls.id == _id).first()

    @property
    def expired(self) -> bool:
        """
        是否已过期
        :return: bool
        """
        return time() > self.expire_at  # 当前时间已经过了增量30min后的时间, 则过期

    def force_to_expire(self) -> None:
        """
        强制使其过期
        :return:
        """
        if not self.expired:  # 如果没有过期
            self.expire_at = int(time())  # 把有效期重置为当前的时间戳
            self.sava_to_db()

    def sava_to_db(self) -> None:
        g.db_session.add(self)
        g.db_session.commit()

    def delete_from_db(self) -> None:
        g.db_session.delete(self)
