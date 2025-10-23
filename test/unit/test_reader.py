from unittest import TestCase

from reader.reader import ConfigReader


class TestReader(TestCase):
    def setUp(self):
        self.reader = ConfigReader.init_from_str('unit/testutil/test.txt')

    def test_get_alphabet(self):
        config = self.reader.read_configuration()
        self.assertEqual(0, config.start_cell_index)
        self.assertEqual(['0', '1'], config.alphabet)
        self.assertEqual('111', config.line)
        self.assertEqual('[q1]111', str(config))
