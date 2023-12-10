import torch
import torch.nn as nn

import numpy as np
import pandas as pd
import joblib


class Model(nn.Module):

    def __init__(self, 
                 input_size: int, 
                 hidden_size: int, 
                 output_size: int, 
                 num_layers: int) -> None:
        
        super().__init__()

        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size, num_layers=num_layers, batch_first=True)

        self.linear = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        outputs, (hn, cn) = self.lstm(x)
        
        return self.linear(outputs)


def make_predictions(model: Model, last_features: torch.Tensor, n_iter: int):
    x = last_features

    predictions = []
    for _ in range(n_iter):
        y = model(x)

        predictions.append(y[-1].detach().numpy())
        
        x = torch.cat([x[1:], y[-1].reshape(1, -1)])

    return np.array(predictions)


def get_predictions_for_ticker(data: pd.DataFrame, ticker: str):    
    scaler = joblib.load(f"forecasting/forecasters/{ticker}/scaler_{ticker}")

    model = Model(input_size=19, hidden_size=50, output_size=19, num_layers=1)
    model.load_state_dict(torch.load(f"forecasting/forecasters/{ticker}/model_{ticker}"))

    values = data.drop(columns=["secid", "ts"])[-3:].values
    values = scaler.transform(values)
    values = torch.from_numpy(values).float()
    
    predictions = make_predictions(model, values, n_iter=20)
    predictions = scaler.inverse_transform(predictions)
    predictions = predictions[:, 0]

    return predictions.tolist()
