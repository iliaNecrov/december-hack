import pandas as pd
import numpy as np

from typing import List
from dataclasses import dataclass

from abc import ABC


@dataclass
class Decision:
    """ code: "Buy", "Sell", "Hold", "Short" """
    
    code: str


class Strategy(ABC):

    def __init__(self, name: str) -> None:
        self.name = name

    def make_decision(self, state: pd.DataFrame | np.ndarray) -> Decision:
        """
        Принимает на вход состояние рынка в конкретный момент времени. 
        Для каждой точки возвращает список решений, принятых для каждой точки.
        """

        raise NotImplementedError
    
    def compute_revenue(self, state: pd.DataFrame | np.ndarray) -> float:
        """
        Принимает на вход состояние рынка в конкретный момент времени.
        Считает доход, который будет получен при продаже акции. 
        """

        raise NotImplementedError
    

class MockStrategy(Strategy):

    def __init__(self, name: str) -> None:
        super().__init__(name)

    def make_decision(self, state: pd.DataFrame | np.ndarray) -> Decision:
        pass
