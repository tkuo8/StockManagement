from .model import Stock, StockPrice, Status, Alert
from .database import db
from decimal import Decimal
import yfinance as yf
import pdb
from .util import model_to_dict
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import exists, func, desc

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


def get_filtered_query(status: Status, possession: str, search_symbol: str):
    # pdb.set_trace()
    if search_symbol:
        try:
            query = db.session.query(Stock).filter(Stock.symbol == search_symbol)
            return query
        except Exception as e:
            print(f"error occured : {e}")
            raise e

    if status:
        try:
            query = (
                db.session.query(Stock)
                .join(Alert, Stock.symbol == Alert.symbol)
                .filter(func.lower(Alert.status) == status.lower())
            )
        except Exception as e:
            print(f"error occured : {e}")
            raise e
    else:
        try:
            query = db.session.query(Stock)
        except Exception as e:
            print(f"error occured : {e}")
            raise e

    if possession == "in":
        try:
            query = query.filter(Stock.quantity > 0)
        except Exception as e:
            print(f"error occured : {e}")
    elif possession == "out":
        try:
            query = query.filter(Stock.quantity == 0)
        except Exception as e:
            print(f"error occured : {e}")
            raise e

    return query


def read_paginated_stocks(query, page: int, page_size=10) -> list[Stock]:
    offset = (page - 1) * page_size
    try:
        stocks = query.limit(page_size).offset(offset).all()
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


def get_total_count(query):
    return query.count()


def has_alert_status(symbol: str, status: Status) -> bool:
    result = db.session.query(
        exists().where(Alert.status == status).where(Alert.symbol == symbol)
    ).scalar()
    return result


def read_target_stocks(
    status: Status, possession: str, search_symbol: str, page: int, page_size=10
):
    query = get_filtered_query(status, possession, search_symbol)
    stocks = read_paginated_stocks(query, page, page_size)
    return stocks


def save_stock_data(symbol, start_date, end_date):
    # yfinanceでデータ取得
    # 前日までのデータ（yf.downloadは取引終了後のデータしか取得できない。現在価格は当日のデータを分間隔で取得して擬似的に得る。）
    data = yf.download(symbol + ".T", start=start_date, end=end_date)
    today_data = yf.download(symbol + ".T", period="1d", interval="1m")
    # pdb.set_trace()
    if today_data.empty:
        if data.empty:
            return False
        else:
            combined_data = data
    else:
        # カラムを確認して正しいカラム名を使用
        columns = today_data.columns.levels[0]  # MultiIndexの場合
        # pdb.set_trace()
        # 当日のデータを1日単位に集約
        current_data = today_data.resample("1D").agg(
            {
                # (columns[0], symbol + ".T"): "last",  # 'Adj Close'
                # (columns[1], symbol + ".T"): "last",  # 'Close'
                # (columns[2], symbol + ".T"): "max",  # 'High'
                # (columns[3], symbol + ".T"): "min",  # 'Low'
                # (columns[4], symbol + ".T"): "first",  # 'Open'
                # (columns[5], symbol + ".T"): "sum",  # 'Volume'
                # yfinanceのバージョン違い？取得できるデータが違う？以下はwindows機でやる場合。
                (columns[0], symbol + ".T"): "last",  # 'Close'
                (columns[1], symbol + ".T"): "max",  # 'High'
                (columns[2], symbol + ".T"): "min",  # 'Low'
                (columns[3], symbol + ".T"): "first",  # 'Open'
                (columns[4], symbol + ".T"): "sum",  # 'Volume'
            }
        )
        # インデックスの整合性をとるため、today_dailyのインデックスをhistorical_dataに合わせる
        current_data.index = current_data.index.normalize()

        target_date = current_data.index[-1].date()

        if data.empty:
            combined_data = current_data
        elif target_date in data.index.date:
            combined_data = data
        else:
            combined_data = pd.concat([data, current_data])

    # combined_datan.dropna(inplace=True)

    # データベースに保存
    for index, row in combined_data.iterrows():
        stock_price = StockPrice(
            symbol=symbol,
            date=index.date(),  # DateTimeIndexから日付部分を取得
            open_price=Decimal(row["Open"].item()),
            high_price=Decimal(row["High"].item()),
            low_price=Decimal(row["Low"].item()),
            close_price=Decimal(row["Close"].item()),
            volume=int(row["Volume"].item()),
        )

        # まず、同じ symbol と date のレコードを検索
        existing_record = (
            db.session.query(StockPrice)
            .filter_by(symbol=stock_price.symbol, date=stock_price.date)
            .first()
        )

        # 既存のレコードがあれば更新、なければ挿入
        if existing_record:
            existing_record.open_price = stock_price.open_price
            existing_record.high_price = stock_price.high_price
            existing_record.low_price = stock_price.low_price
            existing_record.close_price = stock_price.close_price
            existing_record.volume = stock_price.volume
            # 他のフィールドも更新
        else:
            db.session.add(stock_price)

    db.session.commit()
    print(f"Data for {symbol} saved successfully.")
    return True


def update_all_stock_data():
    # pdb.set_trace()
    symbols = db.session.query(Stock).with_entities(Stock.symbol).all()
    for symbol in symbols:
        # sqlalchemyのクエリ結果は、タプルのリストとして返されるので、symbol[0]として中の文字列を得る。
        update_stock_data(symbol[0])


def update_stock_data(symbol):
    # 最新の日付を取得
    latest_date = (
        db.session.query(StockPrice)
        .with_entities(StockPrice.date)
        .filter(StockPrice.symbol == symbol)
        .order_by(desc(StockPrice.date))
        .first()
    )

    if latest_date:
        start_date = latest_date[0].strftime("%Y-%m-%d")
    else:
        start_date = "2024-01-01"  # デフォルト開始日

    end_date = datetime.now().strftime("%Y-%m-%d")

    print(f"symbol:{symbol} update start")

    can_update = save_stock_data(symbol, start_date, end_date)
    # print("save stock data finished")
    # start_date<end_dateがTrueの場合でも、その間が土日祝日だったりすると、
    # yfinanceの値は無いので、移動平均の計算のとこで存在しない日付の分を計算しようとして
    # エラーが出るから、yfinanceからの取得結果が無いかどうかで以後の処理を行うかどうか決めている。
    if can_update:
        save_moving_average(
            symbol,
            datetime.strptime(start_date, "%Y-%m-%d"),
            datetime.strptime(end_date, "%Y-%m-%d"),
        )
        # print("save moving average finished")
        update_alert(symbol)
        # print("update alert finished")


def save_moving_average(symbol, start_date, end_date):
    days_ago = start_date - timedelta(days=200)
    query_data = (
        db.session.query(StockPrice)
        .filter(
            StockPrice.symbol == symbol,
            StockPrice.date.between(days_ago.date(), end_date.date()),
        )
        .all()
    )

    # dataframeに変換
    data = [
        {"id": row.id, "close_price": row.close_price, "date": row.date}
        for row in query_data
    ]
    df = pd.DataFrame(data)
    if df.empty:
        print("No data in the specified range")
    # 日付順にソート
    df = df.sort_values(by="date")
    # 移動平均を計算
    df["ma_5"] = df["close_price"].rolling(window=5).mean()
    df["ma_20"] = df["close_price"].rolling(window=20).mean()
    df["ma_60"] = df["close_price"].rolling(window=60).mean()
    df["ma_100"] = df["close_price"].rolling(window=100).mean()
    # 更新対象の範囲のみ抜き出す
    filtered_df = df[df["date"] >= start_date.date()]
    # 計算結果を元のテーブルに登録
    for _, row in filtered_df.iterrows():
        record = db.session.query(StockPrice).filter_by(id=row["id"]).first()
        if record:
            record.ma_5 = row["ma_5"]
            record.ma_20 = row["ma_20"]
            record.ma_60 = row["ma_60"]
            record.ma_100 = row["ma_100"]
    db.session.commit()


def update_alert(symbol):
    # 以前のデータを消す
    db.session.query(Alert).filter(Alert.symbol == symbol).delete()

    latest_entry = (
        db.session.query(StockPrice)
        .filter(StockPrice.symbol == symbol)
        .order_by(desc(StockPrice.date))
        .first()
    )
    previous_entry = (
        db.session.query(StockPrice)
        .filter(StockPrice.symbol == symbol)
        .order_by(desc(StockPrice.date))
        .offset(1)
        .limit(1)
        .first()
    )

    if is_buy(
        open=latest_entry.open_price,
        close=latest_entry.close_price,
        short_ma_yesterday=previous_entry.ma_5,
        short_ma=latest_entry.ma_5,
        very_long_ma=latest_entry.ma_100,
    ):
        db.session.add(Alert(symbol=symbol, status=Status.BUY))

    if is_sell(
        open=latest_entry.open_price,
        close=latest_entry.close_price,
        short_ma_yesterday=previous_entry.ma_5,
        short_ma=latest_entry.ma_5,
    ):
        db.session.add(Alert(symbol=symbol, status=Status.SELL))

    if is_exclusion(close=latest_entry.close_price, very_long_ma=latest_entry.ma_100):
        db.session.add(Alert(symbol=symbol, status=Status.EXCLUSION))

    db.session.commit()


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


def get_target_finance_data_dict(
    page: int, status: Status, possession: str, search_symbol: str, page_size=10
):
    # pdb.set_trace()
    return_data = []
    stocks = read_target_stocks(status, possession, search_symbol, page, page_size)
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

    bool_buy = has_alert_status(stock.symbol, Status.BUY)
    bool_sell = has_alert_status(stock.symbol, Status.SELL)
    bool_exclusion = has_alert_status(stock.symbol, Status.EXCLUSION)

    # 日付を datetime 型に変換して、降順にソート
    sorted_history = sorted(
        history, key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"), reverse=True
    )

    # 最近の行
    if len(sorted_history) > 0:
        latest_entry = sorted_history[0]
    else:
        latest_entry = None

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
        data = yf.download("9478.T", start="2025-01-07", end="2025-01-07")
        print(data)
        # update_all_stock_data()
        # stocks = read_all_stocks()
        # # stocks = [Stock.query.get(1)]
        # for stock in stocks:
        #     history = get_six_month_history(stock)

        #     # 日付を datetime 型に変換して、降順にソート
        #     sorted_history = sorted(
        #         history,
        #         key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"),
        #         reverse=True,
        #     )

        #     # 最近の行
        #     if len(sorted_history) > 0:
        #         latest_entry = sorted_history[0]
        #     else:
        #         latest_entry = None

        #     # 一つ前の日付の行
        #     if len(sorted_history) > 1:
        #         previous_entry = sorted_history[1]
        #     else:
        #         previous_entry = None

        #     bool_buy = is_buy(
        #         open=latest_entry["open_price"],
        #         close=latest_entry["close_price"],
        #         short_ma_yesterday=previous_entry["ma_5"],
        #         short_ma=latest_entry["ma_5"],
        #         very_long_ma=latest_entry["ma_100"],
        #     )

        #     bool_sell = is_sell(
        #         open=latest_entry["open_price"],
        #         close=latest_entry["close_price"],
        #         short_ma_yesterday=previous_entry["ma_5"],
        #         short_ma=latest_entry["ma_5"],
        #     )

        #     bool_exclusion = is_exclusion(
        #         close=latest_entry["close_price"], very_long_ma=latest_entry["ma_100"]
        #     )

        #     if bool_buy:
        #         db.session.add(Alert(symbol=stock.symbol, status=Status.BUY))
        #         db.session.commit()

        #     if bool_sell:
        #         db.session.add(Alert(symbol=stock.symbol, status=Status.SELL))
        #         db.session.commit()

        #     if bool_exclusion:
        #         db.session.add(Alert(symbol=stock.symbol, status=Status.EXCLUSION))
        #         db.session.commit()


# stock_dict = model_to_dict(stock)
# stock_dict = {"symbol": "7570"}
# print(stock.symbol)
# ohlc_list = get_six_month_ohlc_list_of_dict(stock)
# print(ohlc_list)
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
