from pathlib import Path
from typing import List, Dict

from command.command import Command, TransitionState
from util.configuration import Configuration
from util.direction import Direction


class ConfigReader:
    def __init__(self, path: Path):
        self.path = path

    @classmethod
    def init_from_str(cls, path: str):
        return cls(Path(path))

    def read_configuration(self) -> Configuration:
        alphabet = []

        with open(self.path, 'r', encoding='utf-8') as config:
            content = config.read().split('\n')
            alphabet: List
            commands: Dict
            start_command: str
            line: str
            start_cell_index: int
            i = 0
            while i < len(content):
                if '//' in content[i]:
                    i += 1
                    continue
                match (content[i]):
                    case 'А':
                        alphabet = self.__read_alphabet(content[i + 1])
                        i += 2
                    case 'П':
                        commands = self.__read_commands_dict(content[i + 1])
                        i += 2
                    case 'Р':
                        start_cell_index, start_command, line = self.__read_config(content[i + 1])
                        i += 2
                    case _:
                        self.__read_command(commands, content[i])
                        i += 1

        return Configuration(alphabet, [*line], commands[start_command], int(start_cell_index))

    @staticmethod
    def __read_alphabet(line):
        return [*line]

    @staticmethod
    def __read_commands_dict(line: str):
        line = line.split(' ')
        return {line[i].strip().lower(): Command(line[i].strip().lower(), dict(), i == len(line) - 1) for i in
                range(len(line))}

    @staticmethod
    def __read_command(commands: Dict[str, Command], line: str):
        line = line.lower().split(' ')
        commands[line[0].strip()].symbol_res[line[1].strip()] = TransitionState(
            line[3].strip(),
            commands[line[2].strip()],
            Direction.get_by_char(line[4])
        )

    @staticmethod
    def __read_config(line: str):
        line = line.split()
        return line[0].strip(), line[1].strip().lower(), line[2].strip()
