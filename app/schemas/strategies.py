from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class StrategyBase(BaseModel):
    name: str
    description: Optional[str] = None

class StrategyCreate(StrategyBase):
    pass

class StrategyResponse(StrategyBase):
    id: int
    user_id: UUID

    class Config:
        from_attributes = True