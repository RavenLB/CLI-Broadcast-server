from datetime import datetime

import sqlalchemy
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey



Base = sqlalchemy.orm.declarative_base()

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(256), nullable=False)
    active_connection = relationship("ActiveConnection", back_populates="user", uselist=False)

class ActiveConnection(Base):
    __tablename__ = 'active_connections'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    last_seen = Column(DateTime, default=datetime.utcnow)
    user = relationship("UserModel", back_populates="active_connection")

