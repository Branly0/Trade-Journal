from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Token(BaseModel):
    token : str
    is_revoked: bool = False
    user_id: str

class TokenResponse(Token):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True