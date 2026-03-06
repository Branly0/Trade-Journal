from pydantic import BaseModel, Field
import uuid
from typing import Optional
from datetime import datetime

class AccountBase(BaseModel):
    name: str
    account_type: str
    currency: str
    initial_deposit: float
    balance: float
    equity: float

class AccountCreate(AccountBase):
    pass

class AccountUpdate(AccountBase):
    balance: Optional[float] = None

class AccountResponse(AccountBase):
    id: int
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class BalanceUpdate(BaseModel):
    amount: float = Field(..., description="the changed value of the balance, it can be positive or negative")
