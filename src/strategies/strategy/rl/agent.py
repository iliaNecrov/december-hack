from typing import Callable, List

from .tools import *


class Agent:

    def __init__(self, policy: Callable[[State, List[DiscreteAction]], DiscreteAction]) -> None:
        self.policy = policy

    def action(self, state: State, available_actions: List[DiscreteAction]) -> DiscreteAction:
        return self.policy(state, available_actions)
    
    def change_policy(self, new_policy: Callable[[State, List[DiscreteAction]], DiscreteAction]) -> None:
        self.policy = new_policy