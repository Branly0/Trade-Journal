from typing import Optional
from fastapi import Depends, FastAPI, APIRouter
from app.API.v1.auth import router
# from app.db.session import Base

# Base.metadata.create_all(bind=Base.metadata.bind)
from app.core.dependencies import get_current_user

app = FastAPI(title="Trade Journal API", version="1.0.0")

app.include_router(router)

@app.get("/")
async def read_root():
    return {"message": "Hello, world!"}

@app.get("/me")
async def read_current_user(current_user: dict = Depends(get_current_user)):
    return current_user