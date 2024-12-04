from app.model import Stock
from app.database import get_db
from decimal import Decimal
import yfinance as yf
import pdb

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

def read_all_stocks() -> list[Stock]:
    try:
        with get_db() as db:
            stocks = db.query(Stock).all()
            return stocks
    except Exception as e:
        print(f'error occured : {e}')
        raise e

def get_current_price_and_company_name(symbol):
    # yfinanceでデータを取得
    ticker = yf.Ticker(symbol + '.T')
    try:
        current_price = ticker.info.get('currentPrice', '情報がありません')
        company_name = ticker.info.get('longName', '情報がありません')
        return {'currentPrice': current_price, 'companyName': company_name}
    except Exception as e:
        print(f"データ取得中にエラーが発生しました: {e}")

def get_finance_data_list():
    # pdb.set_trace()
    return_data = []
    stocks = read_all_stocks()
    for stock in stocks:
        stock_dict = stock.to_camel_case_dict()
        finance_data = get_current_price_and_company_name(stock.symbol)
        current_price = Decimal(finance_data['currentPrice'])
        digits = Decimal('0.01')
        return_data.append({
            **stock_dict,
            **finance_data,
            'reachTargetPrice': Decimal(stock_dict['targetPrice'] - current_price).quantize(digits),
            'leftCutlossPrice': Decimal(current_price - stock_dict['cutlossPrice']).quantize(digits),
            'profitAndLoss': Decimal((current_price - stock_dict['purchasePrice']) * stock_dict['quantity']).quantize(digits)
            })
    return return_data