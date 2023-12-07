import pandas as pd
import numpy as np

from ..strategy.strategy import Strategy, Decision


class Agent:

    def __init__(self, strategy: Strategy) -> None:
        self.strategy = strategy

        self.revenue = 0
        self.n_stock = 0

    def action(self, state: pd.DataFrame | np.ndarray) -> Decision:
        decision = self.strategy.make_decision(state)

        if decision.name == "Buy":
            self.n_stock += 1

        if decision.name == "Sell":
            self.n_stock -= 1

            self.revenue += self.strategy.compute_revenue(state)

        if decision.name == "Hold":
            pass

        if decision.name == "Short":
            pass

        return decision

