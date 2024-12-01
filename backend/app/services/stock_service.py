from app.repositories.stock_repository import create_stock
from sqlalchemy.orm import Session
from decimal import Decimal

def register_stock(symbol: str, purchase_price: Decimal, quantity: int, target_price: Decimal, cutloss_price: Decimal):
    # TODO:すでに同じ銘柄が登録されているか確認する処理を入れる
    return create_stock(symbol, purchase_price, quantity, target_price, cutloss_price)