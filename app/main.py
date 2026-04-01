from typing import Optional
from fastapi import Depends, FastAPI, APIRouter
from app.API.v1.auth import router as auth_router
from app.API.v1.trades import router as trades_router
from app.API.v1.accounts import router as accounts_router
from app.API.v1.strategies import router as strategies_router
from app.API.service.analytics import router as analytics_router
# from app.db.session import Base

# Base.metadata.create_all(bind=Base.metadata.bind)
from app.core.dependencies import get_current_user

app = FastAPI(title="Trade Journal API", version="1.0.0")

app.include_router(auth_router)
app.include_router(trades_router)
app.include_router(accounts_router)
app.include_router(strategies_router)
app.include_router(analytics_router)

@app.get("/")
async def read_root():
    return {"message": "Hello, world!"}

@app.get("/me")
async def read_current_user(current_user: dict = Depends(get_current_user)):
    return current_user