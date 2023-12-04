import pandas as pd

from datetime import datetime
from moexalgo import Market, Ticker

from typing import List, Dict


DEFAULT_PRICE_COLUMN = "pr_open"
DEFAULT_TIME_DELTA_IN_DAYS = 2


def get_tickers_from_moex() -> List[str]:
    today = datetime.now().strftime('%Y-%m-%d')
    
    stocks = Market('stocks').obstats(date=today, latest=True) 

    return stocks.ticker.unique().tolist()


def get_ticker_info_from_moex(ticker: str, price_column: str = DEFAULT_PRICE_COLUMN) -> List[float]:
    """Возвращает цену акци "price_columns" за последние "DEFAULT_TIME_DELTA_IN_DAYS" дня с текущего."""
    
    today = datetime.now()
    days_ago = today - datetime.timedelta(days=DEFAULT_TIME_DELTA_IN_DAYS)

    today = today.strftime('%Y-%m-%d')
    days_ago = days_ago.strftime('%Y-%m-%d')
    
    ticker_data = Ticker(ticker).tradestats(date=days_ago, till_date=today)

    return ticker_data[price_column].tolist()





