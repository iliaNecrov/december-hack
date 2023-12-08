import random

from ..tools import State, DiscreteAction

from typing import Tuple, List


DEFAULT_VOLUME = 10_000


class ExperienceReplayMemory:
    
    def __init__(self, volume: int = DEFAULT_VOLUME):
        self.volume = volume
        self.memory = []

    def store(self, events: List[Tuple[State, DiscreteAction, float, State]]):
        if len(self.memory) == self.volume:
            self.memory = []

        self.memory.extend(events)

    def sample(self, batch_size: int):
        return random.sample(self.memory, batch_size)