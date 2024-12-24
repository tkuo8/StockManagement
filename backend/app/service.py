from .model import Stock
from .database import db
from decimal import Decimal
import yfinance as yf
import pdb
from .util import model_to_dict
from datetime import datetime, timedelta
import pandas as pd

###
# DB操作
###


def create_stock(
    symbol: str,
    purchase_price: Decimal,
    quantity: int,
    stop_loss_price: Decimal,
) -> Stock:
    try:
        stock = Stock(
            symbol=symbol,
            purchase_price=purchase_price,
            quantity=quantity,
            stop_loss_price=stop_loss_price,
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


def update_stock(
    stock_id: int,
    purchase_price: Decimal,
    quantity: int,
    stop_loss_price: Decimal,
):
    # 更新対象の行を取得
    try:
        stock = Stock.query.get(stock_id)

        if stock is None:
            return f"Stock with id {stock_id} not found"

        # 属性を変更
        stock.stock_id = stock_id
        stock.purchase_price = purchase_price
        stock.quantity = quantity
        stock.stop_loss_price = stop_loss_price

        # データベースに保存
        db.session.commit()
        return get_one_finance_data_dict(stock_id)
    except Exception as e:
        db.session.rollback()
        return f"Error occurred: {e}"


###
# 表示データ作成
###


def get_all_finance_data_dict():
    # pdb.set_trace()
    return_data = []
    stocks = read_all_stocks()
    for stock in stocks:
        # pdb.set_trace()
        stock_dict = model_to_dict(stock)
        finance_data = create_finance_data(stock_dict)
        return_data.append(finance_data)
    return return_data


def get_one_finance_data_dict(stock_id):
    # pdb.set_trace()
    stock = Stock.query.get(stock_id)
    stock_dict = model_to_dict(stock)
    return_data = create_finance_data(stock_dict)
    return return_data


def create_finance_data(stock_dict):
    ticker = yf.Ticker(stock_dict["symbol"] + ".T")

    price_and_name = get_current_price_and_company_name(ticker)

    history = get_individual_stock_history(ticker)
    history_dict = history_to_dict_for_plot_period(history)

    finance_data = {
        "stock_id": stock_dict["stock_id"],
        **stock_dict,
        **price_and_name,
        "profit_and_loss": Decimal(
            (Decimal(price_and_name["current_price"]) - stock_dict["purchase_price"])
            * stock_dict["quantity"]
        ).quantize(Decimal("0.01")),
        **history_dict,
    }
    return finance_data


def get_current_price_and_company_name(ticker):
    # yfinanceでデータを取得
    try:
        current_price = ticker.info.get("currentPrice", "0.0")
        company_name = ticker.info.get("longName", "情報がありません")
        # pdb.set_trace()
        return {"current_price": current_price, "company_name": company_name}
    except Exception as e:
        print(f"データ取得中にエラーが発生しました: {e}")


def get_individual_stock_history(ticker):
    # 直近3ヶ月のデータを取得
    history = ticker.history(period="3mo")
    history = history.dropna(subset=["Open", "Close", "High", "Low"])
    return history


# プロットするのは直近1ヶ月のデータなので、その分だけのhistoryを得る
def history_to_dict_for_plot_period(history: pd.DataFrame):
    one_month_ago = pd.Timestamp.now(tz="Asia/Tokyo") - pd.Timedelta(days=60)
    recent_one_month_history = history[history.index >= one_month_ago]
    return_history = recent_one_month_history[
        ["Open", "Close", "High", "Low"]
    ].reset_index()
    return_history["Date"] = return_history["Date"].dt.strftime(
        "%Y-%m-%d"
    )  # 日付フォーマット変換
    return {"history": return_history.to_dict(orient="records")}


def calculate_moving_avarage(close_history: pd.Series, short_window, long_window):
    short_ma = close_history.rolling(window=short_window).mean()
    long_ma = close_history.rolling(window=long_window).mean()

    return {"short_ma": short_ma, "long_ma": long_ma}
