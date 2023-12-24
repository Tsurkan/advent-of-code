import unittest
from unittest.mock import patch
import script

class TestDay2(unittest.TestCase):

    file_path = '2023/day2/input.txt'

    text_input = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
                    Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
                    Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
                    Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
                    Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

    data = {
            'Game 1': {'blue': 6, 'red': 4, 'green': 2}, 
            'Game 2': {'blue': 4, 'green': 3, 'red': 1}, 
            'Game 3': {'green': 13, 'blue': 6, 'red': 20}, 
            'Game 4': {'green': 3, 'red': 14, 'blue': 15}, 
            'Game 5': {'red': 6, 'blue': 2, 'green': 3}
        }

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=text_input)
    def test_input_data_with_example_data(self, mock_open):
        self.assertEqual(script.input_data('some_file_path'), self.data)

    @patch('script.input_data')
    def test_task1_with_example_data(self, mock_input_data):
        mock_input_data.return_value = self.data

        self.assertEqual(script.task1('some_file_path'), 8)

    @patch('script.input_data')
    def test_task2_with_example_data(self, mock_input_data):
        mock_input_data.return_value = self.data

        self.assertEqual(script.task2('some_file_path'), 2286)

    def test_part1_with_puzzle_input(self):
        self.assertEqual(script.task1(self.file_path), 3099)

    def test_part2_with_puzzle_input(self):
        self.assertEqual(script.task2(self.file_path), 72970)

if __name__ == '__main__':
    unittest.main()