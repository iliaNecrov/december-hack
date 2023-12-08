import numpy as np
import pandas as pd

from datetime import datetime

from moexalgo import Ticker, Market

from .agent import Agent

from ..strategy.strategy import Decision

from typing import List, Tuple


MILISECONDS_IN_SECOND = 1_000


class Playground:

    def __init__(self, ticker: str, date: str, till_date: str):
        self.history = Ticker(ticker).tradestats(date=date, till_date=till_date)

        if not isinstance(self.history, pd.DataFrame):
            self.history = pd.DataFrame(self.history)

    def backtest(self, agent: Agent) -> Tuple[List[Decision], float]:
        actual_prices = []

        buy_decisions, sell_decisions = [], []

        for _, state in self.history.iterrows():
            price = agent.strategy.compute_price(state)
            
            timestamp = state.ts.timestamp() * MILISECONDS_IN_SECOND
            
            actual_prices.append({
                "price": price,
                "time": timestamp
            })

            decision = agent.action(state)

            if decision.code == "Buy":
                buy_decisions.append({
                    "price": price,
                    "time": timestamp
                })

            if decision.code == "Sell":
                sell_decisions.append({
                    "price": price,
                    "time": timestamp
                })

        final_balance = agent.balance + agent.n_stock * price

        return {
            "revenue": (final_balance - agent.starting_balance) / agent.starting_balance * 100,
            "actual": actual_prices,
            "buyDecisions": buy_decisions,
            "sellDecisions": sell_decisions
        }
