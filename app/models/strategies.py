from sqlalchemy import Column, Enum, Integer, String, String, ForeignKey, Uuid, func, DateTime
from sqlalchemy.orm import relationship
from app.db.session import Base
import enum

class CreatorEnum(enum.Enum):
    trader = "trader"
    admin = "admin"

class Strategy(Base):
    __tablename__ = "strategies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    creator = Column(Enum(CreatorEnum), nullable=False, default=CreatorEnum.trader)
    user_id = Column(Uuid, ForeignKey("users.id", ondelete="CASCADE")) # Foreign key to users table, assuming you have a users table with a UUID primary key
    created_at = Column(DateTime, server_default=func.now(), nullable=False) #we can store the created_at as a string in the database, but in the frontend, we can convert it to a date object for better handling
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False) #we can store the updated_at as a string in the database, but in the frontend, we can convert it to a date object for better handling

    trades = relationship("Trade", back_populates="strategy", cascade="all, delete-orphan")
    user = relationship("User", back_populates="strategies")