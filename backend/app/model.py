from sqlalchemy import (
    Column, Integer, Numeric, Date, DateTime, String, Enum as SQLAlchemyEnum, ForeignKey
)
from sqlalchemy.sql import func
from .database import db
from enum import Enum

class StockStatus(Enum):
    HOLDING="holding"
    WATCHING="watching"
    BUY="buy"
    SELL="sell"
    DISABLED="disabled"

class TransactionType(Enum):
    BUY="buy"
    SELL="sell"

# stocksテーブルの定義
class Stock(db.Model):
    __tablename__ = 'stocks'

    stock_id = db.Column(Integer, primary_key=True, autoincrement=True)
    symbol = db.Column(String(10), nullable=False)
    purchase_price = db.Column(Numeric(10, 2), nullable=False)
    quantity = db.Column(Integer, nullable=False)
    target_price = db.Column(Numeric(10, 2), nullable=False)
    stop_loss_price = db.Column(Numeric(10, 2), nullable=False)
    status = db.Column(SQLAlchemyEnum(StockStatus), nullable=False)
    created_at = db.Column(DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

# transactionsテーブルの定義
class Transaction(db.Model):
    __tablename__ = 'transactions'

    transaction_id = db.Column(Integer, primary_key=True, autoincrement=True)
    stock_id = db.Column(Integer, ForeignKey('stocks.stock_id'), nullable=False)
    transaction_type = db.Column(SQLAlchemyEnum(TransactionType), nullable=False)
    price = db.Column(Numeric(10, 2), nullable=False)
    quantity = db.Column(Integer, nullable=False)
    profit_loss = db.Column(Numeric(10, 2), nullable=True)
    transaction_date = db.Column(DateTime, nullable=False)

    stock = db.relationship("Stock", back_populates="transactions")

Stock.transactions = db.relationship("Transaction", order_by=Transaction.transaction_id, back_populates="stock")

# goal_progressテーブルの定義
class GoalProgress(db.Model):
    __tablename__ = 'goal_progress'

    goal_id = db.Column(Integer, primary_key=True, autoincrement=True)
    traded_at = db.Column(Date, nullable=False)
    progress_rate = db.Column(Numeric(5, 2), nullable=False)
    period = db.Column(Integer, ForeignKey('goal_periods.period_id'), nullable=False)
    created_at = db.Column(DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

# goal_periodsテーブルの定義
class GoalPeriod(db.Model):
    __tablename__ = 'goal_periods'

    period_id = db.Column(Integer, primary_key=True, autoincrement=True)
    target_amount = db.Column(Numeric(10, 2), nullable=False)
    started_at = db.Column(Date, nullable=False)
    ended_at = db.Column(Date, nullable=False)
    created_at = db.Column(DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    progress = db.relationship("GoalProgress", back_populates="period_data")

GoalProgress.period_data = db.relationship("GoalPeriod", back_populates="progress")
