from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    Date,
    DateTime,
    String,
    Enum as SQLAlchemyEnum,
    ForeignKey,
)
from sqlalchemy.sql import func
from .database import db


# stocksテーブルの定義
class Stock(db.Model):
    __tablename__ = "stocks"

    stock_id = db.Column(Integer, primary_key=True, autoincrement=True)
    symbol = db.Column(String(10), nullable=False)
    purchase_price = db.Column(Numeric(10, 2), nullable=False)
    quantity = db.Column(Integer, nullable=False)
    created_at = db.Column(DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )
