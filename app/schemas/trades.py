from pydantic import BaseModel, Field
from typing import Optional


class TradeBase(BaseModel):
    max_duration_min: Optional[int] = None
    entry: Optional[float] = None
    exit: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    is_closed: Optional[bool] = False
    time_frame: Optional[str] = None
    session: Optional[str] = None
    strategy_id: Optional[int] = None
    symbol_id: Optional[int] = None

class TradeCreate(BaseModel):
    account_id: int

class TradeUpdate(TradeBase):
    pass

class TradeResponse(TradeBase):
    id: int
    account_id: int

    class Config:
        from_attributes = True