from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.models.accounts import Account
from app.schemas.accounts import AccountCreate, AccountResponse, AccountUpdate, BalanceUpdate
from app.models.user import User

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.post("/account", response_model=AccountResponse)
async def create_account(account: AccountCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        new_account = Account(
            name=account.name,
            account_type=account.account_type,
            currency=account.currency,
            initial_deposit=account.balance,
            balance=account.balance,
            equity=account.equity,
            user_id=current_user.id
        )
        db.add(new_account)
        db.commit()
        db.refresh(new_account)
        return new_account

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/", response_model=list[AccountResponse])
async def get_accounts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user), limit: int = 10, offset: int = 0):
    accounts = db.query(Account).filter(Account.user_id == current_user.id).offset(offset).limit(limit).all()
    if not accounts:
        raise HTTPException(status_code=404, detail="No accounts found for the current user")
    return accounts

@router.get("/{account_id}", response_model=AccountResponse)
async def get_account(account_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    account = db.query(Account).filter(Account.id == account_id, Account.user_id == current_user.id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@router.put("/{account_id}", response_model=AccountResponse)
async def update_account(account_id: int, account_update: AccountUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    account = db.query(Account).filter(Account.id == account_id, Account.user_id == current_user.id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    for key, value in account_update.dict(exclude_unset=True).items():
        setattr(account, key, value)
    
    db.commit()
    db.refresh(account)
    return account

@router.put("/{account_id}/balance", response_model=AccountResponse)
async def update_account_balance(account_id: int, balance_update: BalanceUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    account = db.query(Account).filter(Account.id == account_id, Account.user_id == current_user.id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    account.balance += balance_update.amount
    db.commit()
    db.refresh(account)
    return account

@router.delete("/{account_id}", response_model=AccountResponse)
async def delete_account(account_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    account = db.query(Account).filter(Account.id == account_id, Account.user_id == current_user.id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    db.delete(account)
    db.commit()
    return account