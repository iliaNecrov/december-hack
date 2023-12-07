import numpy as np
import pandas as pd

from moexalgo import Ticker, Market

from .agent import Agent

from ..strategy.strategy import Decision

from typing import List, Tuple


class Playground:

    def __init__(self, ticker: str, date: str, till_date: str):
        self.history = Ticker(ticker).tradestats(date=date, till_date=till_date)

        if not isinstance(self.history, pd.DataFrame):
            self.history = pd.DataFrame(self.history)

    def backtest(self, agent: Agent) -> Tuple[List[Decision], float]:
        decisions: List[Decision] = []
        
        for _, state in self.history.iterrows():
            decisions.append(
                agent.action(state)
            )

