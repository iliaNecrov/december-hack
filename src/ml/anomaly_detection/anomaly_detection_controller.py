import pandas as pd

from typing import List

from .anomaly_detector import AnomalyDetector

def get_anomalies(data: pd.DataFrame) -> List[bool]:
    """Для каждой точки в данных определяет аномальность"""
    pass