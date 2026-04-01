from pydantic import BaseModel, Field
from typing import Optional

class AnalyticsSummary(BaseModel):
    total_trades: int
    average_rr: float
    win_rate:float
    expectancy: float
    profit_factor: float
    net_profit: float