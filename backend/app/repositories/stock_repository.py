from app.models.stock import Stock
from app.database import get_db
from sqlalchemy.orm import Session
from decimal import Decimal

def create_stock(symbol: str, purchase_price: Decimal, quantity: int, target_price: Decimal, cutloss_price: Decimal) -> Stock:
    try:
        with get_db() as db:
            stock = Stock(symbol=symbol, purchase_price=purchase_price, quantity=quantity, target_price=target_price, cutloss_price=cutloss_price)
            db.add(stock)
            db.commit()
            db.refresh(stock)
            return stock
    except Exception as e:
        db.rollback()  # 失敗した場合はトランザクションをロールバック
        raise e  # 呼び出し元に例外を再送