import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from datetime import datetime

from stocks.stocks_controller import get_ticker_info_from_moex, get_tickers_from_moex
from strategies.strategies_controller import get_results_of_backtest

from forecasting.forecasting_controller import get_predictions_for_ticker

from chatbot.intents import IntentClassifier, GoogleNewsIntent


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    text: str


@app.get("/tickers")
def tickers():
    return get_tickers_from_moex()


@app.get("/stock_info/{ticker}")
def ticker_info_for_plot(ticker: str):
    data = get_ticker_info_from_moex(ticker)

    timestamps = data.ts.apply(lambda d: int(d.timestamp() * 1_000)).tolist()

    prices = data["pr_open"].tolist()
    prices = [{"price": price, "time": timestamp} for price, timestamp in zip(prices, timestamps)]

    predictions = get_predictions_for_ticker(data, ticker)

    time = prices[-1]["time"]
    
    preds = []
    for k in range(len(predictions)):
        preds.append({
            "price": predictions[k] - (predictions[0] - prices[-1]["price"]),
            "time": time + k * 1000 * 60 * 5
        })
    
    return {"actual": prices, "predicted": preds}


@app.get("/backtest/{ticker}")
def backtest(ticker: str, date: int, till_date: int, balance: int, strategy_type: str):
    date = datetime.fromtimestamp(int(date) // 1_000)
    date = date.strftime('%Y-%m-%d')

    till_date = datetime.fromtimestamp(int(till_date) // 1_000)
    till_date = till_date.strftime('%Y-%m-%d')
    
    return get_results_of_backtest(ticker, date, till_date, balance, strategy_type)


@app.post("/message")
def chat(user_message: Message):
    answer = IntentClassifier.get_answer(user_message.text)

    return {"text": answer}


@app.get("/news/{ticker}")
def news(ticker: str):
    return GoogleNewsIntent.get_news(company=ticker, news_section=True)
