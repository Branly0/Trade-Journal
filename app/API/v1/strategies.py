from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.models.strategies import Strategy
from app.models.user import User
from app.schemas.strategies import StrategyCreate, StrategyResponse

router = APIRouter(prefix="/strategies", tags=["strategies"])

@router.post("/", response_model=StrategyResponse)
async def create_strategy(strategy: StrategyCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        new_strategy = Strategy(
            name=strategy.name,
            description=strategy.description,
            creator=current_user.user_type.value,  # Set creator based on user type
            user_id=current_user.id
        )
        db.add(new_strategy)
        db.commit()
        db.refresh(new_strategy)
        return new_strategy

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{strategy_id}", response_model=StrategyResponse)
async def get_strategy(strategy_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    strategy = db.query(Strategy).filter(Strategy.id == strategy_id).first()
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    if strategy.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this strategy")
    return strategy

@router.get("/", response_model=list[StrategyResponse])
async def list_strategies(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    strategies = db.query(Strategy).filter(Strategy.user_id == current_user.id).all()
    return strategies

@router.put("/{strategy_id}", response_model=StrategyResponse)
async def update_strategy(strategy_id: int, strategy_update: StrategyCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    strategy = db.query(Strategy).filter(Strategy.id == strategy_id).first()
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    if strategy.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this strategy")

    strategy.name = strategy_update.name
    strategy.description = strategy_update.description
    db.commit()
    db.refresh(strategy)
    return strategy

@router.delete("/{strategy_id}")
async def delete_strategy(strategy_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    strategy = db.query(Strategy).filter(Strategy.id == strategy_id).first()
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    if strategy.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this strategy")

    db.delete(strategy)
    db.commit()
    return {"detail": "Strategy deleted successfully"}