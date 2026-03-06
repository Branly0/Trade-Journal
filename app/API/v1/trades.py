from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.models.trades import Trade
from app.models.user import User
from app.schemas.trades import TradeCreate, TradeResponse


router = APIRouter(prefix="/trades", tags=["trades"])

@router.post("/trade", response_model=TradeResponse)
async def create_trade(trade: TradeCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        new_trade = Trade(
            user_id=current_user.id
        )
        db.add(new_trade)
        db.commit()
        db.refresh(new_trade)
        return new_trade

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))