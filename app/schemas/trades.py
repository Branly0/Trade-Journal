from pydantic import BaseModel, Field
from typing import Optional


class TradeBase(BaseModel):
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    entry: Optional[float] = None
    symbol_id: Optional[int] = None
    exit: Optional[float] = None
    

class TradeMain(TradeBase):
    time_frame: Optional[str] = None
    session: Optional[str] = None
    strategy_id: Optional[int] = None
    max_duration_min: Optional[int] = None
    is_closed: Optional[bool] = False

class TradeGet(TradeBase):
    id: Optional[int] = None

    class Config:
        from_attributes = True
 

class TradeCreate(BaseModel):
    account_id: int

class TradeUpdate(TradeMain):
    pass

class TradeResponse(TradeMain):
    id: Optional[int] = None
    account_id: int
    profit: Optional[float] = None
    outcome: Optional[str] = None

    class Config:
        from_attributes = True

    
def map_trade(trade) -> dict:
    profit = None
    outcome = None

    if trade.exit:
        profit = trade.exit - trade.entry
        if profit > 0:
            outcome = "win"
        elif profit < 0:
            outcome = "loss"
        else:
            outcome = "breakeven"

    return {
        "id": trade.id,
        "account_id": trade.account_id,
        "max_duration_min": trade.max_duration_min,
        "entry": trade.entry,
        "exit": trade.exit,
        "stop_loss": trade.stop_loss,
        "take_profit": trade.take_profit,
        "is_closed": trade.is_closed,
        "time_frame": trade.time_frame,
        "session": trade.session,
        "strategy_id": trade.strategy_id,
        "symbol_id": trade.symbol_id,
        "profit": profit,
        "outcome": outcome
    }