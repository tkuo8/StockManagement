from app.extensions import db
from datetime import datetime

class Stock(db.Model):
    __tablename__ = 'stocks'

    stock_id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主キー、自動インクリメント
    symbol = db.Column(db.String(10), nullable=False)  # ティッカーシンボル、NULL不可
    purchase_price = db.Column(db.Numeric(10, 2), nullable=False)  # 取得単価
    quantity = db.Column(db.Integer, nullable=False)  # 保有株数
    target_price = db.Column(db.Numeric(10, 2), nullable=True)  # 売却目標価格
    cutloss_price = db.Column(db.Numeric(10, 2), nullable=True)  # 損切り価格
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 登録日時、デフォルトで現在日時
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新日時、更新時に自動更新

    def __repr__(self):
        return f"<Stock(stock_id={self.stock_id}, symbol='{self.symbol}', purchase_price={self.purchase_price}, quantity={self.quantity})>"
