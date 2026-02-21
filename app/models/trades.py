from sqlalchemy import Uuid, Column, Integer, Float, Boolean, Enum, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base
import enum

class StrategyEnum(enum.Enum):
    scalping = "scalping"
    day_trading = "day_trading"
    swing_trading = "swing_trading"
    position_trading = "position_trading"
class SessionEnum(enum.Enum):
    London = "London"
    New_York = "New_York"
    Asia = "Asia"

class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    max_duration_min = Column(Integer, nullable=True)
    entry = Column(Float, nullable=False)
    exit = Column(Float, nullable=False)
    stop_loss = Column(Float, nullable=False)
    take_profit = Column(Float, nullable=False)
    is_closed = Column(Boolean, nullable=False, default=False)
    time_frame = Column(Integer, nullable=False)
    session = Column(Enum(SessionEnum), nullable=False)
    strategy = Column(Enum(StrategyEnum), nullable=False)
    symbol_id = Column(Integer, ForeignKey("symbols.id", ondelete="CASCADE")) # Foreign key to symbols table, assuming you have a symbols table with an integer primary key
    user_id = Column(Uuid, ForeignKey("users.id", ondelete="CASCADE")) # Foreign key to users table, assuming you have a users table with a UUID primary key

    trade_notes = relationship("TradeNote", back_populates="trade", cascade="all, delete-orphan")
    trade_screenshots = relationship("TradeScreenshot", back_populates="trade", cascade="all, delete-orphan")
    user = relationship("User", back_populates="trades")
    symbol = relationship("Symbol", back_populates="trades")


class TradeNote(Base):
    __tablename__ = "trade_notes"

    id = Column(Integer, primary_key=True, index=True)
    note = Column(String, nullable=False)
    trade_id = Column(Integer, ForeignKey("trades.id", ondelete="CASCADE")) # Foreign key to trades table

    trade = relationship("Trade", back_populates="trade_notes")

class TradeScreenshot(Base):
    __tablename__ = "trade_screenshots"

    id = Column(Integer, primary_key=True, index=True)
    screenshot_url = Column(String, nullable=False)
    trade_id = Column(Integer, ForeignKey("trades.id", ondelete="CASCADE")) # Foreign key to trades table

    trade = relationship("Trade", back_populates="trade_screenshots")