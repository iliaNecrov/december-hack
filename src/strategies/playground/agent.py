import pandas as pd
import numpy as np

from ..strategy.strategy import Strategy, Decision

from typing import List


class Agent:

    def __init__(self, strategy: Strategy, starting_balance: int) -> None:
        self.strategy = strategy

        self.n_stock = 0
        
        self.starting_balance = starting_balance

        self.balance = starting_balance

    def action(self, state: pd.DataFrame | np.ndarray) -> Decision:
        """
        По входному состоянию системы принимает решение согласно стратегии.
        """
        decision = self.strategy.make_decision(state, self.get_available_decisions(state), balance=self.balance, n_stock=self.n_stock)

        if decision.code == "Buy":
            self.n_stock += 1

            self.balance -= self.strategy.compute_price(state)

        if decision.code == "Sell":
            self.n_stock -= 1

            self.balance += self.strategy.compute_price(state)

        if decision.code == "Hold":
            pass

        if decision.code == "Short":
            pass

        return decision
    
    def get_available_decisions(self, state: pd.DataFrame | np.ndarray) -> List[Decision]:
        """
        По входному состоянию системы возвращает список доступных решений в данный момент времени.
        """
        available_decisions: List[Decision] = [Decision("Hold"), Decision("Short")]
        
        if self.n_stock > 0:
            available_decisions.append(Decision("Sell"))
        
        if self.balance > self.strategy.compute_price(state):
            available_decisions.append(Decision("Buy"))
        
        return available_decisions

