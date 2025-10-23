import unittest

from tape import Tape
from util.direction import Direction


class TestTapeModel(unittest.TestCase):
    def setUp(self):
        self.tape = Tape('0', ['1', '1', '0'])

    def test_move_left(self):
        self.tape.move(Direction.LEFT)
        self.assertEqual('0', self.tape.get_current_symbol())

    def test_move_right(self):
        self.tape.move(Direction.RIGHT)
        self.assertEqual('1', self.tape.get_current_symbol())

    def test_long_move(self):
        for i in range(10):
            self.tape.move(Direction.RIGHT)
        self.assertEqual('0', self.tape.get_current_symbol())
        for i in range(10):
            self.tape.move(Direction.LEFT)
        self.assertEqual('1', self.tape.get_current_symbol())

    def test_set_value(self):
        self.tape.set_value_in_current_cell('0')
        self.assertEqual('0', self.tape.get_current_symbol())

    def test_get_print_head_index(self):
        self.tape.move(Direction.RIGHT)
        self.assertEqual(1, self.tape.get_print_head_index())

    def test_get_line(self):
        self.tape.move(Direction.LEFT)
        self.assertEqual('0110', self.tape.get_line())
