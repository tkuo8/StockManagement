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

    # 移動平均線の計算のため、直近１年のデータを取得する
    history = ticker.history(period="1y").dropna(
        subset=["Open", "Close", "High", "Low"]
    )
    ohlc_list = get_2month_list_from_dataframe_with_date_index(history)
    short_moving_average_list = get_2month_list_from_dataframe_with_date_index(
        calculate_moving_avarage(history[["Close"]], 5)
    )
    long_moving_average_list = get_2month_list_from_dataframe_with_date_index(
        calculate_moving_avarage(history[["Close"]], 15)
    )
    hundred_moving_average_list = get_2month_list_from_dataframe_with_date_index(
        calculate_moving_avarage(history[["Close"]], 100)
    )
    stochastics_list = get_2month_list_from_dataframe_with_date_index(
        calculate_stochastics(history[["High", "Low", "Close"]])
    )

    finance_data = {
        "stock_id": stock_dict["stock_id"],
        **stock_dict,
        **price_and_name,
        "profit_and_loss": Decimal(
            (Decimal(price_and_name["current_price"]) - stock_dict["purchase_price"])
            * stock_dict["quantity"]
        ).quantize(Decimal("0.01")),
        "history": ohlc_list,
        "short_ma": short_moving_average_list,
        "long_ma": long_moving_average_list,
        "hundred_ma": hundred_moving_average_list,
        "stochastics": stochastics_list,
        "alerts": {"condition1": True, "condition2": False, "condition3": False},
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


# プロットするのは直近2ヶ月のデータなので、その分だけのdataframeを得る
def get_2month_list_from_dataframe_with_date_index(dataframe: pd.DataFrame):
    one_month_ago = pd.Timestamp.now(tz="Asia/Tokyo") - pd.Timedelta(days=60)
    recent_one_month_dataframe = dataframe[dataframe.index >= one_month_ago]
    return get_list_of_dict_reseted_date_index(recent_one_month_dataframe)


def calculate_moving_avarage(close_history: pd.DataFrame, window_size):
    close_history["MA"] = close_history["Close"].rolling(window=window_size).mean()
    return close_history[["MA"]]


def get_list_of_dict_reseted_date_index(dataframe: pd.DataFrame) -> list[dict]:
    return_dataframe = dataframe.reset_index()
    return_dataframe["Date"] = return_dataframe["Date"].dt.strftime("%Y-%m-%d")
    # 次の式では、各カラムをキーとして格納しているdict（行に相当する）のlist（つまり、行データを並べたもの）が返される。
    return_list_of_dict = return_dataframe.to_dict(orient="records")
    return return_list_of_dict


def calculate_stochastics(df: pd.DataFrame) -> pd.DataFrame:
    df["Lowest_Low"] = df["Low"].rolling(window=9).min()
    df["Highest_High"] = df["High"].rolling(window=9).max()

    df["K"] = (
        (df["Close"] - df["Lowest_Low"]) / (df["Highest_High"] - df["Lowest_Low"]) * 100
    )

    df["D"] = df["K"].rolling(window=3).mean()

    df["Slow_D"] = df["D"].rolling(window=3).mean()

    return df[["K", "D", "Slow_D"]]
