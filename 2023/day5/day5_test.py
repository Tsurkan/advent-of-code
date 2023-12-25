import unittest
from unittest.mock import patch
import script

class TestDay5(unittest.TestCase):

    file_path = '2023/day5/input.txt'

    text_input = """seeds: 79 14 55 13

                    seed-to-soil map:
                    50 98 2
                    52 50 48

                    soil-to-fertilizer map:
                    0 15 37
                    37 52 2
                    39 0 15

                    fertilizer-to-water map:
                    49 53 8
                    0 11 42
                    42 0 7
                    57 7 4

                    water-to-light map:
                    88 18 7
                    18 25 70

                    light-to-temperature map:
                    45 77 23
                    81 45 19
                    68 64 13

                    temperature-to-humidity map:
                    0 69 1
                    1 0 69

                    humidity-to-location map:
                    60 56 37
                    56 93 4"""

    def test_convert_with_example_data(self):
        all_maps = [[[50, 98, 2], [52, 50, 48]], [[0, 15, 37], [37, 52, 2], [39, 0, 15]], 
        [[49, 53, 8], [0, 11, 42], [42, 0, 7], [57, 7, 4]], [[88, 18, 7], [18, 25, 70]], 
        [[45, 77, 23], [81, 45, 19], [68, 64, 13]], [[0, 69, 1], [1, 0, 69]], [[60, 56, 37], [56, 93, 4]]]

        self.assertEqual(script.convert(79, all_maps), 82)
        self.assertEqual(script.convert(14, all_maps), 43)
        self.assertEqual(script.convert(55, all_maps), 86)
        self.assertEqual(script.convert(13, all_maps), 35)

    def test_card_announcement(self):
        result = [[], [], [], [], [], [], []]
        self.assertEqual(script.card_announcement(), result)

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=text_input)
    def test_part1_with_example_data(self, mock_open):
        self.assertEqual(script.task1('some_file_path'), 35)

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=text_input)
    def test_part2_with_example_data(self, mock_open):
        self.assertEqual(script.task2('some_file_path'), 46)

    def test_part1_with_puzzle_input(self):
        self.assertEqual(script.task1(self.file_path), 282277027)

    def test_part2_with_puzzle_input(self):
        self.assertEqual(script.task2(self.file_path), 11554135)

if __name__ == '__main__':
    unittest.main()