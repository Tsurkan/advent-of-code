import unittest
from unittest.mock import patch
import script

class TestDay6(unittest.TestCase):

    file_path = '2023/day6/input.txt'

    text_input = """Time:      7  15   30
                    Distance:  9  40  200"""

    def test_count_ways_to_beat_record_with_example_data(self):
        self.assertEqual(script.count_ways_to_beat_record(7, 9), 4)
        self.assertEqual(script.count_ways_to_beat_record(15, 40), 8)
        self.assertEqual(script.count_ways_to_beat_record(30, 200), 9)

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=text_input)
    def test_task1_with_example_data(self, mock_open):
        self.assertEqual(script.task1('some_file_path'), 288)

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=text_input)
    def test_task2_with_example_data(self, mock_open):
        self.assertEqual(script.task2('some_file_path'), 71503)

    def test_part1_with_puzzle_input(self):
        self.assertEqual(script.task1(self.file_path), 800280)

    def test_part2_with_puzzle_input(self):
        self.assertEqual(script.task2(self.file_path), 45128024)

if __name__ == '__main__':
    unittest.main()