from sqlalchemy import Column, Integer, Float, Boolean, String 
from app.db.session import Base

class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    max_duration_min = Column(Integer, nullable=True)
    entry_price = Column(Float, nullable=False)
    stop_loss = Column(Float, nullable=False)
    take_profit = Column(Float, nullable=False)
    is_opend = Column(Boolean, nullable=False, default=False)
    time_frame = Column(Integer, nullable=False)
    session = Column(String, nullable=False)
    

