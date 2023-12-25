import unittest
from unittest.mock import patch
import script

class TestDay4(unittest.TestCase):

    file_path = '2023/day4/input.txt'

    text_input_1 = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
                    Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
                    Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
                    Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
                    Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
                    Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

    text_input_2 = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
                    Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
                    Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
                    Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
                    Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
                    Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=text_input_1)
    def test_part1_with_example_data(self, mock_open):
        self.assertEqual(script.task1('some_file_path'), 13)

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=text_input_2)
    def test_part2_with_example_data(self, mock_open):
        self.assertEqual(script.task2('some_file_path'), 30)

    def test_part1_with_puzzle_input(self):
        self.assertEqual(script.task1(self.file_path), 25231)

    def test_part2_with_puzzle_input(self):
        self.assertEqual(script.task2(self.file_path), 9721255)

if __name__ == '__main__':
    unittest.main()