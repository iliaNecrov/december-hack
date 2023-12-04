import pandas as pd

from .forecasters.forecaster import load_forecaster


def get_predictions_for_ticker(data: pd.DataFrame, ticker: str):
    forecaster = load_forecaster(ticker)

    return forecaster.predict(data)
