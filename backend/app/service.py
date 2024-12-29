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
) -> Stock:
    try:
        stock = Stock(
            symbol=symbol,
            purchase_price=purchase_price,
            quantity=quantity,
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
    ohlc_list = get_six_month_list_from_dataframe_with_date_index(history)
    short_moving_average_list = get_six_month_list_from_dataframe_with_date_index(
        calculate_moving_avarage(history[["Close"]], 5)
    )
    middle_moving_average_list = get_six_month_list_from_dataframe_with_date_index(
        calculate_moving_avarage(history[["Close"]], 20)
    )
    long_moving_average_list = get_six_month_list_from_dataframe_with_date_index(
        calculate_moving_avarage(history[["Close"]], 60)
    )
    very_long_moving_average_list = get_six_month_list_from_dataframe_with_date_index(
        calculate_moving_avarage(history[["Close"]], 100)
    )
    # stochastics_list = get_six_month_list_from_dataframe_with_date_index(
    #     calculate_stochastics(history[["High", "Low", "Close"]])
    # )

    bool_buy = is_buy(
        history.iloc[-1]["Open"],
        history.iloc[-1]["Close"],
        short_moving_average_list[-2]["MA"],
        short_moving_average_list[-1]["MA"],
        very_long_moving_average_list[-1]["MA"],
    )
    bool_sell = is_sell(
        history.iloc[-1]["Open"],
        history.iloc[-1]["Close"],
        short_moving_average_list[-2]["MA"],
        short_moving_average_list[-1]["MA"],
    )
    bool_exclusion = is_exclusion(
        history.iloc[-1]["Close"], very_long_moving_average_list[-1]["MA"]
    )

    # pdb.set_trace()

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
        "middle_ma": middle_moving_average_list,
        "long_ma": long_moving_average_list,
        "very_long_ma": very_long_moving_average_list,
        "stochastics": [],
        "alerts": {
            "is_buy": bool(bool_buy),
            "is_sell": bool(bool_sell),
            "is_exclusion": bool(bool_exclusion),
        },
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


# プロットするのは直近6ヶ月のデータなので、その分だけのdataframeを得る
def get_six_month_list_from_dataframe_with_date_index(dataframe: pd.DataFrame):
    one_month_ago = pd.Timestamp.now(tz="Asia/Tokyo") - pd.Timedelta(days=180)
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


# 買い時を判定する
# 買い時の条件は、次の1, 2を全て満たすこと
# 1 株価が100日線を上回っている
# 2 株価が下半身を持つ
#   「下半身」の条件は、次の(1)から(4)までを全て満たすこと
#  (1) 5日移動平均線が横ばい又は上向き
#  (2) 陽線である
#  (3) 終値が5日移動平均線より上
#  (4) ローソク足の実態の、5日移動平均線より上に飛び出している部分の長さが実態全体の2分の1以上である
def is_buy(open, close, short_ma_yesterday, short_ma, very_long_ma):
    # pdb.set_trace()
    return (
        very_long_ma < close  # 1
        and short_ma_yesterday <= short_ma  # 2(1)
        and open < close  # 2(2)
        and short_ma < close  # 2(3)
        and (short_ma <= open or (close - short_ma) / (close - open) >= 0.5)  # 2(4)
    )


# 売り時を判定する
# 売り時の条件は、株価が逆下半身を持つこと。
# 「逆下半身」の条件は、次の(1)から(4)までを全て満たすこと
# (1) 5日移動平均線が横ばい又は下向き
# (2) 陰線である
# (3) 終値が5日移動平均線より下
# (4) ローソク足の実態の、5日移動平均線より下に飛び出している部分の長さが実態全体の2分の1以上である
def is_sell(open, close, short_ma_yesterday, short_ma):
    return (
        short_ma_yesterday >= short_ma  # (1)
        and open > close  # (2)
        and short_ma > close  # (3)
        and (short_ma >= open or (short_ma - close) / (open - close) >= 0.5)  # (4)
    )


# 株価が100日移動平均線より下なので注目から除外するかどうかを判定する
# 基本的に、買いの戦略でいくから、株価が100日移動平均線を割り込んでいると手を出さない
# よって、株価が100日移動平均線を割り込んでいる場合は、注目から除外する
def is_exclusion(close, very_long_ma):
    return close < very_long_ma
