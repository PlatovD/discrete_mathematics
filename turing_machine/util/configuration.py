from dataclasses import dataclass
from typing import List

from command.command import Command


@dataclass
class Configuration:
    alphabet: List[str]
    line: List[str]
    command: Command
    start_cell_index: int

    def __to_numeric(self):
        if self.alphabet != ['0', '1']: return ''
        return f'\nnum_on_tape = {sum(int(num) for num in self.line) - 1}\n'

    def __str__(self):
        return ''.join(self.line[self.line.index('1'):self.start_cell_index]) + '[' + str(self.command) + ']' + ''.join(
            self.line[self.start_cell_index:]) + self.__to_numeric()
    # def __str__(self):
    #     return self.line
