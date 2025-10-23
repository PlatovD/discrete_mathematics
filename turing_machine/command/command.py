from dataclasses import dataclass

from util.direction import Direction


@dataclass
class Command:
    name: str
    symbol_res: dict[str, 'TransitionState']
    is_final_state: bool = False

    def __str__(self):
        return self.name


@dataclass
class TransitionState:
    symbol: str
    command: Command
    direction: Direction
