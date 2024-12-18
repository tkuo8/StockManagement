from .model import Stock, StockStatus
from .database import db
from decimal import Decimal
import yfinance as yf
import pdb
from .util import model_to_dict
from datetime import datetime, timedelta


def create_stock(
    symbol: str,
    purchase_price: Decimal,
    quantity: int,
    target_price: Decimal,
    stop_loss_price: Decimal,
    status: StockStatus,
) -> Stock:
    try:
        stock = Stock(
            symbol=symbol,
            purchase_price=purchase_price,
            quantity=quantity,
            target_price=target_price,
            stop_loss_price=stop_loss_price,
            status=status,
        )
        db.session.add(stock)
        db.session.commit()
        return stock
    except Exception as e:
        db.session.rollback()  # 失敗した場合はトランザクションをロールバック
        raise e  # 呼び出し元に例外を再送


def read_all_stocks() -> list[Stock]:
    try:
        stocks = Stock.query.all()
        return stocks
    except Exception as e:
        print(f"error occured : {e}")
        raise e


def get_current_price_and_company_name(symbol):
    # yfinanceでデータを取得
    ticker = yf.Ticker(symbol + ".T")
    try:
        current_price = ticker.info.get("currentPrice", "0.0")
        company_name = ticker.info.get("longName", "情報がありません")
        # pdb.set_trace()
        return {"current_price": current_price, "company_name": company_name}
    except Exception as e:
        print(f"データ取得中にエラーが発生しました: {e}")


def get_finance_data_dict():
    # pdb.set_trace()
    return_data = []
    stocks = read_all_stocks()
    for stock in stocks:
        # pdb.set_trace()
        stock_dict = model_to_dict(stock)
        finance_data = get_current_price_and_company_name(stock.symbol)
        current_price = Decimal(finance_data["current_price"])
        history_dict = get_individual_stock_history_dict(stock.symbol)
        digits = Decimal("0.01")
        return_data.append(
            {
                **stock_dict,
                **finance_data,
                "reach_target_price": Decimal(
                    stock_dict["target_price"] - current_price
                ).quantize(digits),
                "left_stop_loss_price": Decimal(
                    current_price - stock_dict["stop_loss_price"]
                ).quantize(digits),
                "profit_and_loss": Decimal(
                    (current_price - stock_dict["purchase_price"])
                    * stock_dict["quantity"]
                ).quantize(digits),
                **history_dict,
            }
        )
    return return_data


def get_individual_stock_history_dict(symbol):
    # 直近２週間のデータを取得
    ticker = yf.Ticker(symbol + ".T")
    history = ticker.history(period="1mo")
    history_data = history[["Open", "Close", "High", "Low"]].reset_index()
    history_data["Date"] = history_data["Date"].dt.strftime(
        "%Y-%m-%d"
    )  # 日付フォーマット変換

    return {"history": history_data.to_dict(orient="records")}
