import torch
import torch.nn as nn

from torch.optim import Adam
from torch.nn import MSELoss

from typing import List, Tuple, Callable

from ..tools import State, DiscreteAction, concatenate_events
from .experience_replay_memory import ExperienceReplayMemory


class QNetwork(nn.Module):

    def __init__(self, space_dim: int, action_dim: int) -> None:
        super().__init__()

        self.space_dim = space_dim
        self.action_dim = action_dim

        self.network = nn.Sequential(
            nn.Linear(space_dim, 120),
            nn.ReLU(),
            nn.Linear(120, 84),
            nn.ReLU(),
            nn.Linear(84, action_dim),
        )

    def forward(self, x):
        return self.network(x)
    

def deep_q_learning(q: QNetwork,
                    events: List[Tuple[State, DiscreteAction, float, State]], 
                    gamma: float = 0.99,
                    device: str = "cpu") -> Tuple[torch.Tensor, torch.Tensor]:
    
    states, actions, rewards, new_states = concatenate_events(events, device)

    values = q(states).gather(1, actions)

    target = rewards + gamma * q(new_states).max(dim=1)[0].detach().unsqueeze(1)

    return values, target


def double_deep_q_learning(q1: QNetwork,
                           q2: QNetwork,
                           update_q2_weights: bool,
                           events: List[Tuple[State, DiscreteAction, float, State]],
                           gamma: float = 0.99,
                           device: str = "cpu") -> Tuple[torch.Tensor, torch.Tensor]:
    
    states, actions, rewards, new_states = concatenate_events(events, device)

    values = q1(states).gather(1, actions)

    target = rewards + gamma * q2(new_states).max(dim=1)[0].detach().unsqueeze(1)

    if update_q2_weights:
        q2.load_state_dict(q1.state_dict())

    return values, target


def transform_q_network_to_policy(q: QNetwork, actions: List[DiscreteAction]) -> Callable[[State, List[DiscreteAction]], DiscreteAction]:
    def policy(state: State, available_actions: List[DiscreteAction]):
        available_actions_ids = list(map(lambda a: a.number, available_actions))
        
        unavailable_actions_ids = list(set(range(q.action_dim)) - set(available_actions_ids))
        
        values = q(state.components)
        values[unavailable_actions_ids] = -torch.inf

        best_action_idx = torch.argmax(values)

        return actions[best_action_idx]
    
    return policy