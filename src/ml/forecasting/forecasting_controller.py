import pandas as pd

from .forecasters.forecaster import load_forecaster


def get_predictions_for_ticker(data: pd.DataFrame, ticker: str):
    forecaster = load_forecaster(ticker)

    
    return [{"price": 10, 
             "upper_price": 15,
             "lower_price": 5,
             "time": 1701884745 + k * 1000 * 60} for k in range(10)]
