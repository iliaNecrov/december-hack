import pandas as pd

from datetime import datetime, timedelta
from moexalgo import Market, Ticker

from typing import List, Dict


DEFAULT_PRICE_COLUMN = "pr_open"
DEFAULT_TIME_DELTA_IN_DAYS = 2


def get_tickers_from_moex() -> List[str]:
    today = datetime.now().strftime('%Y-%m-%d')
    
    stocks = Market('stocks').obstats(date=today, latest=True) 

    return stocks.ticker.unique().tolist()


def get_ticker_info_from_moex(ticker: str, price_column: str = DEFAULT_PRICE_COLUMN) -> List[Dict[str, float | int]]:
    """Возвращает цену акци "price_columns" за последние "DEFAULT_TIME_DELTA_IN_DAYS" дня с текущего.
       Формат: [{"price": float, "time": int}]}.
    """
    
    today = datetime.now()
    days_ago = today - timedelta(days=DEFAULT_TIME_DELTA_IN_DAYS)

    today = today.strftime('%Y-%m-%d')
    days_ago = days_ago.strftime('%Y-%m-%d')
    
    ticker_data = Ticker(ticker).tradestats(date=days_ago, till_date=today)

    timestamps = [datetime.combine(ticker_data.tradedate[k], ticker_data.tradetime[k]).timestamp() for k in range(len(ticker_data))]
    timestamps = list(map(lambda d: int(d), timestamps))

    prices = ticker_data[price_column].tolist()

    return [{"price": price, "time": timestamp} for price, timestamp in zip(prices, timestamps)]





