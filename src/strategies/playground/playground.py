import numpy as np
import pandas as pd

from moexalgo import Ticker, Market

from ..strategy.strategy import Strategy


class Playground:

    def __init__(self, ticker: str, date: str, till_date: str):
        self.history = Ticker(ticker).tradestats(date=date, till_date=till_date)

        self.history_iterator = iter(self.history)

    def init(self) -> None:
        self.history_iterator = iter(self.history)

    def validate(self, strategy: Strategy):
        pass
