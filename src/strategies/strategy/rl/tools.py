import torch

from typing import List, Tuple


class DiscreteAction:
    
    def __init__(self, name: str, number: int = None, value: float = None) -> None:
        super().__init__()

        self.name = name
        self.number = number
        self.value = value

    def __repr__(self) -> str:
        return f'Action "{self.name}"'
    

class State:

    def __init__(self, components: torch.Tensor, terminal: bool = False) -> None:
        self.components = components
        self.terminal = terminal

    def __repr__(self) -> str:
        return self.components.__repr__()
    

def concatenate_events(events: List[Tuple[State, DiscreteAction, float, State]], device: str = "cpu"):
    states, actions, rewards, new_states = [], [], [], []

    for event in events:
        states.append(event[0].components.reshape(1, -1))
        actions.append(event[1])
        rewards.append(event[2])
        new_states.append(event[3].components.reshape(1, -1))

    states, new_states = torch.cat(states).to(device), torch.cat(new_states).to(device)

    actions = list(map(lambda a: a.number, actions))
    actions = torch.tensor(actions).reshape(-1, 1).to(device)

    rewards = torch.tensor(rewards).reshape(-1, 1).to(device)

    return states, actions, rewards, new_states
