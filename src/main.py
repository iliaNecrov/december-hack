import uvicorn

from fastapi import FastAPI

from stocks.stocks_controller import get_ticker_info_from_moex, get_tickers_from_moex

from ml.forecasting.forecasting_controller import get_predictions_for_ticker
from ml.anomaly_detection.anomaly_detection_controller import get_anomalies


app = FastAPI()


@app.get("/tickers")
def get_tickers():
    return get_tickers_from_moex()


@app.get("/stock_info/{ticker}")
def get_ticker_info_for_plot(ticker: str):
    data = get_ticker_info_from_moex(ticker)

    predictions = get_predictions_for_ticker(data, ticker)
    anomalies = [0, 0, 0, 0, 1, 0, 0, 0, 1, 0]

    for k, prediction in enumerate(predictions):
        prediction["anomaly"] = anomalies[k]

    return {"actual": data, "predicted": predictions}

