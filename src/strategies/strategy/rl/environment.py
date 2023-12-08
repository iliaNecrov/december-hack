import torch
import pandas as pd

from .tools import DiscreteAction, State
from typing import Tuple, List


class Environment:

    def __init__(self, 
                 starting_balance: int, 
                 history: pd.DataFrame,
                 max_interactions_with_tickers: int = 10, 
                 column: str = "pr_open"):
        
        self.starting_balance = starting_balance

        self.balance = starting_balance
        self.history = history[column]

        self.history_iterator = iter(self.history)

        self.actions = [DiscreteAction(f"Buy {k} ticker(s)", value=k, number=k - 1) for k in range(1, max_interactions_with_tickers + 1)]
        
        self.actions = self.actions + [DiscreteAction(f"Sell {k} ticker(s)", value=k, number=max_interactions_with_tickers + k - 1) for k in range(1, max_interactions_with_tickers + 1)]
        self.actions = self.actions + [DiscreteAction("Wait", number=2 * max_interactions_with_tickers)]

    def init(self) -> State:
        self.balance = self.starting_balance
        self.history_iterator = iter(self.history)

        return State(components=torch.tensor([self.balance, 0, next(self.history_iterator)]), terminal=False)

    def step(self, state, action) -> Tuple[State, float]:
        current_balance, current_number_of_tickers, current_price = state.components

        current_capital = current_balance + current_number_of_tickers * current_price

        new_price = next(self.history_iterator)
        
        if "Buy" in action.name:
            number_of_tickers_to_buy = action.value

            new_balance = current_balance - number_of_tickers_to_buy * current_price
            
            new_number_of_tickers = current_number_of_tickers + number_of_tickers_to_buy

        if "Sell" in action.name:
            number_of_tickers_to_sell = action.value

            new_balance = current_balance + number_of_tickers_to_sell * current_price

            new_number_of_tickers = current_number_of_tickers - number_of_tickers_to_sell

        if "Wait" in action.name:
            new_balance = current_balance

            new_number_of_tickers = current_number_of_tickers

        new_capital = new_balance + new_number_of_tickers * new_price

        new_state = State(components=torch.tensor([new_balance, new_number_of_tickers, new_price]), terminal=False)
        reward = new_capital - current_capital
        
        return new_state, reward


    def get_available_actions(self, state: State) -> List[DiscreteAction]:
        current_balance, current_number_of_tickers, current_price = state.components

        available_actions = []
        for action in self.actions:
            if "Buy" in action.name:
                number_of_tickers_to_buy = action.value

                if current_balance - number_of_tickers_to_buy * current_price > 0:
                    available_actions.append(action)

            if "Sell" in action.name:
                number_of_tickers_to_sell = action.value

                if current_number_of_tickers >= number_of_tickers_to_sell:
                    available_actions.append(action)

            if "Wait" in action.name:
                available_actions.append(action)

        return available_actions
    

