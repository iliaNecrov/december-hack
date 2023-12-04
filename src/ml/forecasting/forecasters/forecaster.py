import pandas as pd

from abc import ABC
from typing import List, Dict


class Forecaster(ABC):

    def __init__(self, name: str) -> None:
        self.name = name

    def train(self, data: pd.DataFrame):
        """Обучение модели."""
        raise NotImplementedError
    
    def predict(self, data: pd.DataFrame) -> List[Dict[str, float | int]]:
        """Должен возвращать список объектов в формате: [{"price": [...], 
                                                          "upper_price": [...],
                                                          "lower_price": [...],
                                                          "time": int}]
        Делаем прогноз на один день вперед.
        """
        raise NotImplementedError
    
    def serialize(self, path: str):
        """Сериализует модель в папку по пути path."""
        raise NotImplementedError


def load_forecaster(path: str) -> Forecaster:
    """Загружает модель из папки по пути."""
    pass