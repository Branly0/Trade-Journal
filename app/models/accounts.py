from sqlalchemy import String, Uuid, Enum, Column, DateTime, String, Integer, Float, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.session import Base
import enum

class CurrencyEnumA(enum.Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    JPY = "JPY"

class AccountTypeEnum(enum.Enum):
    demo = "demo"
    live = "live"

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    account_type = Column(Enum(AccountTypeEnum), nullable=False)
    currency = Column(Enum(CurrencyEnumA), nullable=False, default=CurrencyEnumA.USD)
    initial_deposit = Column(Float, nullable=False, default=0.0)
    balance = Column(Float, nullable=False, default=0.0)
    equity = Column(Float, nullable=False, default=0.0)
    user_id = Column(Uuid, ForeignKey("users.id", ondelete="CASCADE")) # Foreign key to users table, assuming you have a users table with a UUID primary key
    created_at = Column(DateTime, server_default=func.now(), nullable=False) #we can store the created_at as a string in the database, but in the frontend, we can convert it to a date object for better handling
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False) #we can store the updated_at as a string in the database, but in the frontend, we can convert it to a date object for better handling

    user = relationship("User", back_populates="accounts")
    trades = relationship("Trade", back_populates="account", cascade="all, delete-orphan")