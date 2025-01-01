from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    Date,
    DateTime,
    DECIMAL,
    String,
    Enum as SQLAlchemyEnum,
    ForeignKey,
    UniqueConstraint,
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


class StockPrice(db.Model):
    __tablename__ = "stock_prices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    open_price = Column(DECIMAL(scale=2))
    high_price = Column(DECIMAL(scale=2))
    low_price = Column(DECIMAL(scale=2))
    close_price = Column(DECIMAL(scale=2))
    volume = Column(Integer)
    ma_5 = Column(DECIMAL(scale=2))
    ma_20 = Column(DECIMAL(scale=2))
    ma_60 = Column(DECIMAL(scale=2))
    ma_100 = Column(DECIMAL(scale=2))

    __table_args__ = (UniqueConstraint("symbol", "date", name="uix_symbol_date"),)
