from sqlalchemy import Uuid, Column, Integer, Float, Boolean, String, Enum, DateTime
import enum 
from sqlalchemy.orm import relationship
from app.db.session import Base
from datetime import datetime
import sqlalchemy as sa

class UserTypeEnum(enum.Enum):
    admin = "admin"
    trader = "trader"


class User(Base):
    __tablename__ = "users"

    id = Column(Uuid, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=True)
    hashed_password = Column(String, nullable=False)
    user_type = Column(Enum(UserTypeEnum), nullable=False)
    profile_picture_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=sa.func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False)

    # trades = relationship("Trade", back_populates="user", cascade="all, delete-orphan")
    tokens = relationship("Token", back_populates="user", cascade="all, delete-orphan")
    accounts = relationship("Account", back_populates="user", cascade="all, delete-orphan")
    strategies = relationship("Strategy", back_populates="user", cascade="all, delete-orphan")