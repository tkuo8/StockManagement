from .model import Stock, StockPrice
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
        ticker = yf.Ticker(symbol + ".T")
        company_name = ticker.info.get("longName", "情報がありません")
        stock = Stock(
            symbol=symbol,
            purchase_price=purchase_price,
            quantity=quantity,
            company_name=company_name,
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


def read_paginated_stocks(page: int, page_size=10) -> list[Stock]:
    offset = (page - 1) * page_size
    try:
        stocks = db.session.query(Stock).limit(page_size).offset(offset).all()
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
        stock.purchase_price = purchase_price
        stock.quantity = quantity

        # データベースに保存
        db.session.commit()
        return get_one_finance_data_dict(stock_id)
    except Exception as e:
        db.session.rollback()
        return f"Error occurred: {e}"


def get_total_count():
    return db.session.query(Stock).count()


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


def get_paginated_finance_data_dict(page: int, page_size=10):
    # pdb.set_trace()
    return_data = []
    stocks = read_paginated_stocks(page, page_size)
    for stock in stocks:
        # pdb.set_trace()
        finance_data = create_finance_data(stock)
        return_data.append(finance_data)
    return return_data


def get_one_finance_data_dict(stock_id):
    # pdb.set_trace()
    stock = Stock.query.get(stock_id)
    stock_dict = model_to_dict(stock)
    return_data = create_finance_data(stock_dict)
    return return_data


def create_finance_data(stock: Stock):
    stock_dict = model_to_dict(stock)
    history = get_six_month_history(stock)

    # 日付を datetime 型に変換して、降順にソート
    sorted_history = sorted(
        history, key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"), reverse=True
    )

    # 最近の行
    if len(sorted_history) > 0:
        latest_entry = sorted_history[0]
    else:
        latest_entry = None

    # 一つ前の日付の行
    if len(sorted_history) > 1:
        previous_entry = sorted_history[1]
    else:
        previous_entry = None

    bool_buy = is_buy(
        open=latest_entry["open_price"],
        close=latest_entry["close_price"],
        short_ma_yesterday=previous_entry["ma_5"],
        short_ma=latest_entry["ma_5"],
        very_long_ma=latest_entry["ma_100"],
    )

    bool_sell = is_sell(
        open=latest_entry["open_price"],
        close=latest_entry["close_price"],
        short_ma_yesterday=previous_entry["ma_5"],
        short_ma=latest_entry["ma_5"],
    )

    bool_exclusion = is_exclusion(
        close=latest_entry["close_price"], very_long_ma=latest_entry["ma_100"]
    )

    finance_data = {
        **stock_dict,
        "profit_and_loss": Decimal(
            (latest_entry["close_price"] - stock_dict["purchase_price"])
            * stock_dict["quantity"]
        ).quantize(Decimal("0.01")),
        "history": history,
        "alerts": {
            "is_buy": bool(bool_buy),
            "is_sell": bool(bool_sell),
            "is_exclusion": bool(bool_exclusion),
        },
    }
    return finance_data


# プロットする直近6ヶ月分のデータを得る
def get_six_month_history(stock: Stock) -> list[dict]:
    today = datetime.today()
    six_months_ago = today - timedelta(days=6 * 30)
    query = (
        db.session.query(StockPrice)
        .filter(StockPrice.symbol == stock.symbol, StockPrice.date >= six_months_ago)
        .all()
    )
    return_data = [model_to_dict(row) for row in query]
    return return_data


# ストキャスティクスの計算（現在は使っていない）
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


def main():
    from .__init__ import create_app

    app = create_app()
    with app.app_context():
        # stocks = read_all_stocks()
        pdb.set_trace()
        stocks = [Stock.query.get(1)]
        for stock in stocks:
            # stock_dict = model_to_dict(stock)
            # stock_dict = {"symbol": "7570"}
            print(stock.symbol)
            ohlc_list = get_six_month_ohlc_list_of_dict(stock)
            print(ohlc_list)
            # ticker = yf.Ticker(stock.symbol + ".T")
            # company_name = ticker.info.get("longName", "情報がありません")
            # history = ticker.history(period="1y").dropna()
            # history["MA5"] = history["Close"].rolling(window=5).mean()
            # history["MA20"] = history["Close"].rolling(window=20).mean()
            # history["MA60"] = history["Close"].rolling(window=60).mean()
            # history["MA100"] = history["Close"].rolling(window=100).mean()
            # for index, row in history.iterrows():
            #     stock_price = StockPrice(
            #         symbol=stock_dict["symbol"],
            #         date=index.date(),
            #         open_price=row["Open"],
            #         high_price=row["High"],
            #         low_price=row["Low"],
            #         close_price=row["Close"],
            #         volume=row["Volume"],
            #         ma_5=row["MA5"],
            #         ma_20=row["MA20"],
            #         ma_60=row["MA60"],
            #         ma_100=row["MA100"],
            #     )
            #     db.session.add(stock_price)
            # if company_name:
            #     stock.company_name = company_name
            # else:
            #     print(f"Couldn't retrieve company name for {stock.symbol}")

        # db.session.commit()


if __name__ == "__main__":
    main()
