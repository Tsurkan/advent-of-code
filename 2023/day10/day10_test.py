import unittest
from unittest.mock import patch
import script

class TestDay10(unittest.TestCase):

    file_path = '2023/day10/input.txt'

    text_input_1 =   """.....
                        .S-7.
                        .|.|.
                        .L-J.
                        ....."""

    text_input_2 =   """..F7.
                        .FJ|.
                        SJ.L7
                        |F--J
                        LJ..."""

    text_input_3 =   """FF7FSF7F7F7F7F7F---7
                        L|LJ||||||||||||F--J
                        FL-7LJLJ||||||LJL-77
                        F--JF--7||LJLJ7F7FJ-
                        L---JF-JLJ.||-FJLJJ7
                        |F|F-JF---7F7-L7L|7|
                        |FFJF7L7F-JF7|JL---7
                        7-L-JL7||F7|L7F-7F7|
                        L.L7LFJ|||||FJL7||LJ
                        L7JLJL-JLJLJL--JLJ.L"""

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=text_input_1)
    def test_part1_with_example_data_1(self, mock_open):
        self.assertEqual(script.main('some_file_path')[0], 4)

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=text_input_1)
    def test_part2_with_example_data_1(self, mock_open):
        self.assertEqual(script.main('some_file_path')[1], 1)

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=text_input_2)
    def test_part1_with_example_data_2(self, mock_open):
        self.assertEqual(script.main('some_file_path')[0], 8)

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=text_input_2)
    def test_part2_with_example_data_2(self, mock_open):
        self.assertEqual(script.main('some_file_path')[1], 1)

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=text_input_3)
    def test_part1_with_example_data_3(self, mock_open):
        self.assertEqual(script.main('some_file_path')[0], 41)

    # @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=text_input_3)
    # def test_part2_with_example_data_3(self, mock_open):
    #     self.assertEqual(script.main('some_file_path')[1], 10)

    def test_part1_with_puzzle_input(self):
        self.assertEqual(script.main(self.file_path)[0], 6903)

    def test_part2_with_puzzle_input(self):
        self.assertEqual(script.main(self.file_path)[1], 265)

if __name__ == '__main__':
    unittest.main()