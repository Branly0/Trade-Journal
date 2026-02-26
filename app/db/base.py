# app/db/base.py  (or wherever makes sense)
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import all models here so metadata gets populated
from app.models.user import User
from app.models.trades import Trade, TradeNote, TradeScreenshot
from app.models.symbol import Symbol