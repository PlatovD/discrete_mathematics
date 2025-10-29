from typing import List

from command.command import Command
from error.turing_machine_error import MachineIsNotApplicableError
from tape import Tape
from util.configuration import Configuration


class TuringMachine:
    def __init__(self, alphabet: List[str], start_command: Command, original_world: List[str],
                 start_cell_index: int = 0):
        self.alphabet = alphabet
        self.command = start_command
        self.tape = Tape(alphabet[0], original_world, start_cell_index)
        self.count_actions = 0

    @classmethod
    def init_from_config(cls, config: Configuration):
        return cls(config.alphabet, config.command, config.line, config.start_cell_index)

    def get_current_configuration(self):
        return Configuration(self.alphabet, self.tape.get_line(), self.command, self.tape.get_print_head_index())

    def execute(self) -> Configuration:
        while self.__step():
            self.count_actions += 1
            if self.count_actions > 1_000_000:
                raise MachineIsNotApplicableError("Машина не применима к данному слову при данной программе")

        return self.get_current_configuration()

    def __step(self) -> bool:
        if self.command.is_final_state: return False
        symbol = self.tape.get_current_symbol()
        if symbol not in self.command.symbol_res:
            return False

        transition_state = self.command.symbol_res[symbol]
        self.tape.set_value_in_current_cell(transition_state.symbol)
        self.command = transition_state.command
        self.tape.move(transition_state.direction)
        return True
