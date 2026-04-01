from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.models.trades import Trade
from app.models.user import User
from app.models.accounts import Account
from app.schemas.trades import TradeCreate, TradeGet, TradeMain, TradeResponse, TradeBase, TradeUpdate, map_trade


router = APIRouter(prefix="/trades", tags=["trades"])

@router.post("/trade", response_model=TradeResponse)
async def create_trade(trade: TradeCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        new_trade = Trade(
            account_id=trade.account_id
        )
        db.add(new_trade)
        db.commit()
        db.refresh(new_trade)
        return new_trade

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[TradeGet])
async def get_trades(db: Session = Depends(get_db), current_user: User = Depends(get_current_user), limit: int = 10, offset: int = 0):
    trades = db.query(Trade).join(Trade.account).filter(Trade.account.has(user_id=current_user.id)).offset(offset).limit(limit).all()
    if not trades:
        raise HTTPException(status_code=404, detail="No trades found for the current user")
    return trades

@router.get("/account/{account_id}", response_model=list[TradeGet])
async def get_trades_by_account(account_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    trades = db.query(Trade).join(Trade.account).filter(Trade.account.has(id=account_id, user_id=current_user.id)).all()
    if not trades:
        raise HTTPException(status_code=404, detail="No trades found for the specified account")
    
    return trades  

@router.get("/{trade_id}", response_model=TradeResponse)
async def get_trade(trade_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    trade = db.query(Trade).filter(Trade.id == trade_id).first()
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    if trade.account.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this trade")
    return trade

@router.put("/{trade_id}", response_model=TradeResponse)
async def update_trade(trade_id: int, trade_update: TradeUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    trade = db.query(Trade).filter(Trade.id == trade_id).first()
    account = db.query(Account).filter(Account.id == trade.account_id).first()
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    if trade.account.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this trade")
    if trade.session == "London" or trade.session == "New_York" or trade.session == "Asia":
        raise HTTPException(status_code=400, detail="Invalid session value. Must be 'London', 'New_York', or 'Asia'.")
    
    old_exit = trade.exit


    for key, value in trade_update.dict(exclude_unset=True).items():
        setattr(trade, key, value)
    
    if trade.exit != old_exit:
        if old_exit == None:
            old_exit = 0
        account.balance += trade.exit - old_exit
    
    db.commit()
    db.refresh(trade)
    db.refresh(account)
    return map_trade(trade)

@router.put("/{trade_id}/close", response_model=TradeResponse)
async def close_trade(trade_id: int, exit: float, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    trade = db.query(Trade).filter(Trade.id == trade_id).first()
    account = db.query(Account).filter(Account.id == trade.account_id).first()
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    if trade.account.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to close this trade")
    if trade.is_closed:
        raise HTTPException(status_code=400, detail="Trade is already closed")

    trade.is_closed = True
    trade.exit = exit
    account.balance += (trade.exit - trade.entry) if trade.exit and trade.entry else 0
    
    db.commit()
    db.refresh(trade)
    db.refresh(account)
    return map_trade(trade)

@router.delete("/{trade_id}")
async def delete_trade(trade_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    trade = db.query(Trade).filter(Trade.id == trade_id).first()
    if not trade:
        raise HTTPException(status_code=404, detail="Trade not found")
    if trade.account.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this trade")

    db.delete(trade)
    db.commit()
    return {"detail": "Trade deleted successfully"}