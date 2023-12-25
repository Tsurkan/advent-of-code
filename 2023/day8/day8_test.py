import unittest
from unittest.mock import patch
import script

class TestDay8(unittest.TestCase):

    file_path = '2023/day8/input.txt'

    text_input_1 = """RL

                    AAA = (BBB, CCC)
                    BBB = (DDD, EEE)
                    CCC = (ZZZ, GGG)
                    DDD = (DDD, DDD)
                    EEE = (EEE, EEE)
                    GGG = (GGG, GGG)
                    ZZZ = (ZZZ, ZZZ)"""

    text_input_2 = """LLR

                    AAA = (BBB, BBB)
                    BBB = (AAA, ZZZ)
                    ZZZ = (ZZZ, ZZZ)"""

    text_input_3 = """LR

                    11A = (11B, XXX)
                    11B = (XXX, 11Z)
                    11Z = (11B, XXX)
                    22A = (22B, XXX)
                    22B = (22C, 22C)
                    22C = (22Z, 22Z)
                    22Z = (22B, 22B)
                    XXX = (XXX, XXX)"""

    def test_preprocess_instructions_with_example_data(self):
        result1 = {'AAA': ('BBB', 'CCC'), 'BBB': ('DDD', 'EEE'), 'CCC': ('ZZZ', 'GGG'), 'DDD': ('DDD', 'DDD'), 'EEE': ('EEE', 'EEE'), 'GGG': ('GGG', 'GGG'), 'ZZZ': ('ZZZ', 'ZZZ')}
        self.assertEqual(script.preprocess_instructions(self.text_input_1.split('\n\n')), result1)

        result2 = {'AAA': ('BBB', 'BBB'), 'BBB': ('AAA', 'ZZZ'), 'ZZZ': ('ZZZ', 'ZZZ')}
        self.assertEqual(script.preprocess_instructions(self.text_input_2.split('\n\n')), result2)

        result3 = {'11A': ('11B', 'XXX'), '11B': ('XXX', '11Z'), '11Z': ('11B', 'XXX'), '22A': ('22B', 'XXX'), '22B': ('22C', '22C'), '22C': ('22Z', '22Z'), '22Z': ('22B', '22B'), 'XXX': ('XXX', 'XXX')}
        self.assertEqual(script.preprocess_instructions(self.text_input_3.split('\n\n')), result3)

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=text_input_1)
    def test_task_1_with_example_data_1(self, mock_open):
        self.assertEqual(script.task_1('some_file_path'), 2)
    
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=text_input_2)
    def test_task_1_with_example_data_2(self, mock_open):
        self.assertEqual(script.task_1('some_file_path'), 6)

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=text_input_3)
    def test_task_2_with_example_data(self, mock_open):
        self.assertEqual(script.task_2('some_file_path'), 6)

    def test_part1_with_puzzle_input(self):
        self.assertEqual(script.task_1(self.file_path), 16531)

    def test_part2_with_puzzle_input(self):
        self.assertEqual(script.task_2(self.file_path), 24035773251517)

if __name__ == '__main__':
    unittest.main()