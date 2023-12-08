import torch

from .playground.playground import Playground
from .playground.agent import Agent
from .strategy.strategy import ReinforcementLearningStrategy


def get_results_of_backtest(ticker: str, date: str, till_date: str, balance: int, strategy_type: str):
    playground = Playground(ticker=ticker, date=date, till_date=till_date)

    if strategy_type == "rl":
        agent = Agent(strategy=ReinforcementLearningStrategy(name="RL", 
                                                             path_to_strategy="strategies/trained_strategies/baseline_rl_strategy"), 
                                                             starting_balance=balance)

    if strategy_type == "forecsating":
        pass

    if strategy_type == "algorithmic":
        pass

    backtest_results = playground.backtest(agent)

    return backtest_results

