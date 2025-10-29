from machine import TuringMachine
from reader.reader import ConfigReader

reader = ConfigReader.init_from_str('../configurations/3')
machine = TuringMachine.init_from_config(reader.read_configuration())
print(machine.get_current_configuration())
print(machine.execute())
