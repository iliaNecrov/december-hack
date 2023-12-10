import torch

import pandas as pd
import numpy as np

from typing import List
from dataclasses import dataclass

from abc import ABC

from .rl.tools import DiscreteAction, State
from .rl.algorithms.q_learning import QNetwork, transform_q_network_to_policy


@dataclass
class Decision:
    """ code can be: "Buy", "Sell", "Hold", "Short" """
    
    code: str


class Strategy(ABC):

    def __init__(self, name: str) -> None:
        self.name = name

    def make_decision(self, state: np.ndarray, available_decisions: List[Decision], **kwargs) -> Decision:
        """
        Принимает на вход состояние рынка в конкретный момент времени. 
        Для каждой точки возвращает список решений, принятых для каждой точки.
        """

        raise NotImplementedError
    
    def compute_price(self, state: np.ndarray, **kwargs) -> float:
        """
        Принимает на вход состояние рынка в конкретный момент времени.
        Возвращает стоимость акции. 
        """

        raise NotImplementedError
    

class ReinforcementLearningStrategy(Strategy):

    def __init__(self, name: str, path_to_strategy: str) -> None:
        super().__init__(name)

        q = QNetwork(3, 21)
        q.load_state_dict(torch.load(path_to_strategy))

        self.q = transform_q_network_to_policy(q, actions=[
            DiscreteAction("Buy 1 ticker(s)", number=0), DiscreteAction("Sell 1 ticker(s)", number=1), DiscreteAction("Wait", number=2)
        ])

    def make_decision(self, state: np.ndarray, available_decisions: List[Decision], **kwargs) -> Decision:
        balance, n_stock = kwargs["balance"], kwargs["n_stock"]

        state = State(components=torch.tensor([balance, n_stock, self.compute_price(state)]))

        available_actions = self._transform_decisions_to_actions(available_decisions)

        action = self.q(state, available_actions)

        return self._transform_action_to_decision(action)
    
    def compute_price(self, state: np.ndarray) -> float:
        return state.pr_open
    
    def _transform_decisions_to_actions(self, decisions: List[Decision]) -> List[DiscreteAction]:
        actions = []

        for decision in decisions:
            if decision.code == "Buy":
                actions.append(DiscreteAction("Buy 1 ticker(s)", number=0))

            if decision.code == "Sell":
                actions.append(DiscreteAction("Sell 1 ticker(s)", number=1))

            if decision.code == "Hold":
                actions.append(DiscreteAction("Wait", number=2))

        return actions
    
    def _transform_action_to_decision(self, action: DiscreteAction) -> Decision:
        if "Buy" in action.name:
            return Decision("Buy")
        
        if "Sell" in action.name:
            return Decision("Sell")
        
        if "Wait" in action.name:
            return Decision("Hold")
    

class MockStrategy(Strategy):

    def __init__(self, name: str) -> None:
        super().__init__(name)

        self.sell_threshold = 251
        self.buy_threshold = 250

    def make_decision(self, state: np.ndarray, available_decisions: List[Decision]) -> Decision:
        if state.pr_open > self.sell_threshold:
            decision = Decision(code="Sell")
        
        if state.pr_open < self.buy_threshold:
            decision = Decision(code="Buy")
        
        if decision in available_decisions:
            return decision
            
        return Decision("Hold")
        
    def compute_price(self, state: np.ndarray) -> float:
        return state.pr_open
    

class ForecastingStrategy(Strategy):

    def __init__(self, name: str) -> None:
        super().__init__(name)

    def make_decision(self, state: np.ndarray, available_decisions: List[Decision]) -> Decision:
        return super().make_decision(state, available_decisions)
    
    def compute_price(self, state: np.ndarray) -> float:
        return super().compute_price(state)
