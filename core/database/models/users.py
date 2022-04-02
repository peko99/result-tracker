# Copyright 2022 Marin Pejcin


from sqlalchemy import Column, Integer, String

from core.database.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
