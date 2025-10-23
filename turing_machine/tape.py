from typing import List, Optional

from turing_machine.util.direction import Direction


class Tape:
    def __init__(self, blank_symbol: str, initial: Optional[List[str]] = None, start_cell_index: int = 0):
        self.blank_symbol = blank_symbol
        if initial is None:
            initial = []
        self.line = initial[:]
        self.print_head_index = start_cell_index

    def __move_print_head(self, direction: Direction):
        if direction == Direction.STAY:
            return

        if direction == Direction.LEFT:
            self.print_head_index -= 1
        else:
            self.print_head_index += 1

    def __prepare_line(self):
        if self.print_head_index == -1:
            self.print_head_index += 1
            self.line.insert(self.print_head_index, self.blank_symbol)
            return

        while self.print_head_index >= len(self.line):
            self.line.append(self.blank_symbol)

    def set_value_in_current_cell(self, value: str):
        self.__prepare_line()
        self.line[self.print_head_index] = value

    def move(self, direction: Direction):
        self.__move_print_head(direction)
        self.__prepare_line()

    def get_current_symbol(self):
        self.__prepare_line()
        return self.line[self.print_head_index]

    def get_print_head_index(self):
        return self.print_head_index

    def get_line(self):
        return ''.join(self.line)
