from sqlalchemy import Uuid, Column, Integer, Float, Boolean, String 
from sqlalchemy.orm import relationship
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Uuid, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=True)
    hashed_password = Column(String, nullable=False)
    user_type = Column(String, nullable=False) #is an enum in the frontend, but for simplicity, we can store it as a string in the database
    profile_picture_url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    trades = relationship("Trade", back_populates="user", cascade="all, delete-orphan")