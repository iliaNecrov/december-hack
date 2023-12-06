import pandas as pd
import numpy as np

from typing import List
from dataclasses import dataclass


@dataclass
class Decision:
    """ code: "Buy", "Sell", "Hold", "Short" """
    
    code: str


class Strategy:

    def __init__(self, name: str) -> None:
        self.name = name

    def make_decision(self, data: pd.DataFrame) -> List[Decision]:
        """Принимает на вход набор данных за любой промежуток времени. 
           Для каждой точки возвращает список решений, принятых для каждой точки.
        """

        raise NotImplementedError
