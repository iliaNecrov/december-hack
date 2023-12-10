import pandas as pd

from datetime import datetime, timedelta
from moexalgo import Market, Ticker

from typing import List, Dict


DEFAULT_PRICE_COLUMN = "pr_open"
DEFAULT_TIME_DELTA_IN_DAYS = 2
MILISECONDS_IN_SECOND = 1_000


def get_tickers_from_moex() -> List[str]:
    today = datetime.now().strftime('%Y-%m-%d')
    
    stocks = Market('stocks').obstats(date=today, latest=True) 

    if not isinstance(stocks, pd.DataFrame):
        stocks = pd.DataFrame(stocks)

    #return stocks.secid.unique().tolist()
    return ["SBER", "YNDX", "VKCO", "OZON", "TCSG"]


def get_ticker_info_from_moex(ticker: str, price_column: str = DEFAULT_PRICE_COLUMN) -> List[Dict[str, float]]:
    """Возвращает цену акци "price_columns" за последние "DEFAULT_TIME_DELTA_IN_DAYS" дня с текущего.
       Формат: [{"price": float, "time": int}]}.
    """
    
    today = datetime.now()
    days_ago = today - timedelta(days=DEFAULT_TIME_DELTA_IN_DAYS)

    today = today.strftime('%Y-%m-%d')
    days_ago = days_ago.strftime('%Y-%m-%d')
    
    ticker_data = Ticker(ticker).tradestats(date=days_ago, till_date=today)

    if not isinstance(ticker_data, pd.DataFrame):
        ticker_data = pd.DataFrame(ticker_data)

    return ticker_data






