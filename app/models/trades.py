from sqlalchemy import Uuid, Column, Integer, Float, Boolean, String 
from app.db.session import Base

class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    max_duration_min = Column(Integer, nullable=True)
    entry = Column(Float, nullable=False)
    stop_loss = Column(Float, nullable=False)
    take_profit = Column(Float, nullable=False)
    is_closed = Column(Boolean, nullable=False, default=False)
    time_frame = Column(Integer, nullable=False)
    session = Column(String, nullable=False)
    strategy = Column(String, nullable=False) #is an enum in the frontend, but for simplicity, we can store it as a string in the database
    symbol_id = Column(Integer, nullable=False) # Foreign key to symbols table, assuming you have a symbols table with an integer primary key
    user_id = Column(Uuid, nullable=False) # Foreign key to users table, assuming you have a users table with a UUID primary key


class ClosedTrade(Base):
    __tablename__ = "closed_trades"

    id = Column(Integer, primary_key=True, index=True)
    exit = Column(Float, nullable=False)
    trade_id = Column(Integer, nullable=False) # Foreign key to trades table

class TradeNote(Base):
    __tablename__ = "trade_notes"

    id = Column(Integer, primary_key=True, index=True)
    note = Column(String, nullable=False)
    trade_id = Column(Integer, nullable=False) # Foreign key to trades table

class TradeScreenshot(Base):
    __tablename__ = "trade_screenshots"

    id = Column(Integer, primary_key=True, index=True)
    screenshot_url = Column(String, nullable=False)
    trade_id = Column(Integer, nullable=False) # Foreign key to trades table