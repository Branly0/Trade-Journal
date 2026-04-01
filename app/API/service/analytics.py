from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, case
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.models.trades import Trade
from app.models.user import User
from app.models.accounts import Account
from app.schemas.analytics import AnalyticsSummary


router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/analytics/summary/{account_id}", response_model=AnalyticsSummary)
async def get_analytics_summary(account_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Check if the current user has access to the requested account
    user_id = db.query(Account.user_id).filter(Account.id == account_id).scalar()
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access denied not your account")

    total_trades = calculate_total_trades(db, account_id)
    average_rr = calculate_average_rr(db, account_id)
    win_rate = calculate_win_rate(db, account_id)
    expectancy = calculate_expectancy(db, account_id)
    profit_factor = calculate_profit_factor(db, account_id)
    net_profit = calculate_net_profit(db, account_id)

    return {
        "total_trades": total_trades,
        "average_rr": average_rr,
        "win_rate": win_rate,
        "expectancy": expectancy,
        "profit_factor": profit_factor,
        "net_profit": net_profit
    }

@router.get("/drawdon")
    







## fuctions to calculate analytics metrics\
def calculate_total_trades(db, account_id) -> int:
    total_trades = db.query(func.count(Trade.id)).filter(Trade.account_id == account_id).scalar()
    return total_trades
def calculate_win_rate(db, account_id) -> float:
    total_trades = calculate_total_trades(db, account_id)
    if total_trades == 0:
        return 0.0
    wins = db.query(func.count(Trade.id)).filter(Trade.account_id == account_id, Trade.exit > Trade.entry).scalar()
    win_rate = wins / total_trades * 100
    return win_rate
def calculate_average_rr(db, account_id):

    filters = [
        Trade.account_id == account_id,
        Trade.exit != None,
        Trade.stop_loss != None,
        Trade.entry != Trade.stop_loss
    ]

    total_trades = db.query(func.count(Trade.id)).filter(*filters).scalar()

    if total_trades == 0:
        return 0.0

    total_rr = db.query(
        func.sum(
            (Trade.exit - Trade.entry) /
            func.abs(Trade.entry - Trade.stop_loss)
        )
    ).filter(*filters).scalar() or 0

    return total_rr / total_trades
def calculate_profit_factor(db, account_id: int):

    filters = [
        Trade.account_id == account_id,
        Trade.exit != None
    ]

    total_profit = db.query(
        func.sum(Trade.exit - Trade.entry)
    ).filter(
        *filters,
        Trade.exit > Trade.entry
    ).scalar() or 0

    total_loss = db.query(
        func.sum(Trade.entry - Trade.exit)
    ).filter(
        *filters,
        Trade.exit < Trade.entry
    ).scalar() or 0

    if total_loss == 0:
        return 0

    return total_profit / total_loss
def calculate_net_profit(db, account_id) -> float:
    total_trades = calculate_total_trades(db, account_id)
    if total_trades == 0:
        return 0.0
    net_profit = db.query(func.sum(Trade.exit - Trade.entry)).filter(Trade.account_id == account_id).scalar() or 0.0
    return net_profit
def calculate_expectancy(db, account_id) -> float:
    filter = [
        Trade.account_id == account_id,
        Trade.exit != None
    ]
    total_trade = db.query(func.count(Trade.id)).filter(*filter).scalar()
    if total_trade == 0:
        return 0.0
    wins = db.query(func.count(Trade.id)).filter(*filter, Trade.exit > Trade.entry).scalar()
    total_profit = db.query(func.sum(Trade.exit - Trade.entry)).filter(*filter, Trade.exit > Trade.entry).scalar()
    total_loss = db.query(func.sum(Trade.entry - Trade.exit)).filter(*filter, Trade.exit < Trade.entry).scalar()
    if total_loss == None:
        total_loss = 0
    avrage_profit = total_profit / wins if wins > 0 else 0
    avrage_loss = total_loss / (total_trade - wins) if total_trade - wins > 0 else 0
    expectancy = (avrage_profit * (wins / total_trade)) - (avrage_loss * ((total_trade - wins) / total_trade))
    return expectancy
