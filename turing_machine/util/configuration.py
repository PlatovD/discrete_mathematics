from dataclasses import dataclass
from typing import List

from command.command import Command


@dataclass
class Configuration:
    alphabet: List[str]
    line: List[str]
    command: Command
    start_cell_index: int

    def __str__(self):
        return ''.join(self.line[:self.start_cell_index]) + '[' + str(self.command) + ']' + ''.join(
            self.line[self.start_cell_index:])
