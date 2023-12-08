import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from datetime import datetime

from stocks.stocks_controller import get_ticker_info_from_moex, get_tickers_from_moex
from strategies.strategies_controller import get_results_of_backtest

from ml.forecasting.forecasting_controller import get_predictions_for_ticker
from ml.anomaly_detection.anomaly_detection_controller import get_anomalies


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/tickers")
def tickers():
    return get_tickers_from_moex()


@app.get("/stock_info/{ticker}")
def ticker_info_for_plot(ticker: str):
    data = get_ticker_info_from_moex(ticker)

    #predictions = get_predictions_for_ticker(data, ticker)
    predictions = []

    price = data[-1]["price"]
    time = data[-1]["time"]
    
    for k in range(20):
        predictions.append({
            "price": price,
            "upper_price": price + 30,
            "lower_price": price - 30,
            "time": time + k * 1000 * 60 * 5
        })

    anomalies = [0] * len(predictions)

    for k, prediction in enumerate(predictions):
        prediction["anomaly"] = anomalies[k]

    return {"actual": data, "predicted": predictions}


@app.get("/backtest/{ticker}")
def backtest(ticker: str, date: int, till_date: int, balance: int, strategy_type: str):
    date = datetime.fromtimestamp(int(date) // 1_000)
    date = date.strftime('%Y-%m-%d')

    till_date = datetime.fromtimestamp(int(till_date) // 1_000)
    till_date = till_date.strftime('%Y-%m-%d')
    
    return get_results_of_backtest(ticker, date, till_date, balance, strategy_type)
