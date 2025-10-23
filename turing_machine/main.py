from machine import TuringMachine
from reader.reader import ConfigReader

reader = ConfigReader.init_from_str('../configurations/11.4a')
machine = TuringMachine.init_from_config(reader.read_configuration())

print(machine.execute())
