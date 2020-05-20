import math
import unittest
from pathlib import Path

from scripts import skeleton


class UnitTests(unittest.TestCase):

    def setUp(self):
        self.unit_tests_directory = Path(__file__).parents[1].absolute() / 'unit_tests'
        self.neighbors_filename = 'neighbors_table.json'

    def test_middle(self):
        input_text = "XXX\n" \
                     "X1X\n" \
                     "XXX"
        expected_output_text = "XXX\n" \
                               "XYX\n" \
                               "XXX"
        self.a_tester(self.neighbors_filename, input_text, expected_output_text)

    def test_all_ones(self):
        input_text = "111\n" \
                     "111\n" \
                     "111"
        expected_output_text = "111\n" \
                               "111\n" \
                               "111"
        self.a_tester(self.neighbors_filename, input_text, expected_output_text)

    def test_dots(self):
        input_text = "...\n" \
                     "...\n" \
                     "..."
        expected_output_text = "...\n" \
                               "...\n" \
                               "..."
        self.a_tester(self.neighbors_filename, input_text, expected_output_text)

    def test_lonely_one_and_many_dots_bottom(self):
        input_text = "...\n" \
                     "...\n" \
                     "1.."
        expected_output_text = "...\n" \
                               "...\n" \
                               "1.."
        self.a_tester(self.neighbors_filename, input_text, expected_output_text)

    def test_lonely_one_and_many_dots_top(self):
        input_text = "..1\n" \
                     "...\n" \
                     "..."
        expected_output_text = "..1\n" \
                               "...\n" \
                               "..."
        self.a_tester(self.neighbors_filename, input_text, expected_output_text)

    def test_all_x(self):
        input_text = "XXX\n" \
                     "XXX\n" \
                     "XXX"
        expected_output_text = "XXX\n" \
                               "XXX\n" \
                               "XXX"
        self.a_tester(self.neighbors_filename, input_text, expected_output_text)

    def test_5_neighbors(self):
        input_text = "X11\n" \
                     "XX1\n" \
                     "XXX"
        expected_output_text = "XY1\n" \
                               "XXY\n" \
                               "XXX"
        self.a_tester(self.neighbors_filename, input_text, expected_output_text)

    def test_3_neighbors(self):
        input_text = ".1X\n" \
                     ".1X\n" \
                     "..."
        expected_output_text = ".YX\n" \
                               ".YX\n" \
                               "..."
        self.a_tester(self.neighbors_filename, input_text, expected_output_text)

    def test_1_neighbor(self):
        input_text = "...\n" \
                     ".1X\n" \
                     "..."
        expected_output_text = "...\n" \
                               ".YX\n" \
                               "..."
        self.a_tester(self.neighbors_filename, input_text, expected_output_text)

    def test_2_neighbors(self):
        input_text = "..1\n" \
                     ".1X\n" \
                     "..."
        expected_output_text = "..Y\n" \
                               ".YX\n" \
                               "..."
        self.a_tester(self.neighbors_filename, input_text, expected_output_text)

    def test_3_neighbors_under_threshold(self):
        input_text = ".11\n" \
                     ".1X\n" \
                     "..."
        expected_output_text = ".11\n" \
                               ".1X\n" \
                               "..."
        self.a_tester(self.neighbors_filename, input_text, expected_output_text)

    # Takes 2 seconds
    def test_no_less_xs_no_more_1s_no_more_dots_no_other_chars(self):

        neighbors_filename = 'neighbors_table.json'
        # TODO put here smaller numbers for fast running
        dim1, dim2 = 3, 3
        for input_text in UnitTests.input_generator(dim1, dim2):
            # no less xs
            number_of_xs_input = input_text.count('X')
            actual_result = self.calculate_output(neighbors_filename, input_text)
            number_of_xs_output = actual_result.count('X')
            self.assertTrue(number_of_xs_output >= number_of_xs_input)
            # no more 1s
            number_of_1s_input = input_text.count('1')
            number_of_1s_output = actual_result.count('1')
            self.assertTrue(number_of_1s_input <= number_of_1s_output)
            # no more dots
            number_of_dots_input = input_text.count('.')
            number_of_dots_output = actual_result.count('.')
            self.assertTrue(number_of_dots_input <= number_of_dots_output)
            # no other chars except Y
            other_chars = actual_result.replace('.', '').replace('X', '').replace('1', '')
            self.assertEqual(other_chars, '')

    @staticmethod
    def input_generator(dimension_1, dimension_2):
        translator = {0: 'X', 1: '.', 2: '1'}

        def make_input_from_number(represent_number):
            base = len(translator)
            wafer_grid = list()
            for row_index in range(dimension_1):
                wafer_grid.append([])
                for column_index in range(dimension_2):
                    residue = represent_number % base
                    chip_state = translator[residue]
                    wafer_grid[-1].append(chip_state)
                    represent_number = math.floor(represent_number / base)
            wafer_rows = [''.join(wafer_grid_row) for wafer_grid_row in wafer_grid]
            wafer_text = '\n'.join(wafer_rows)
            return wafer_text

        total_dimension = dimension_1 * dimension_2
        max_representing_number = pow(len(translator), total_dimension)
        for representing_number in range(max_representing_number):
            result_wafer_text = make_input_from_number(representing_number)
            yield result_wafer_text

    def test_on_file(self):
        path_for_input_file = self.unit_tests_directory / 'unit_test_1_input.txt'
        with open(path_for_input_file, 'r') as input_file:
            input_text = input_file.read()
        neighbors_filename = 'neighbors_table.json'
        path_for_output_file = self.unit_tests_directory / 'unit_test_1_expected_output.txt'
        with open(path_for_output_file, 'r') as output_file:
            output_text = output_file.read()
        self.a_tester(neighbors_filename, input_text, output_text)

    def calculate_output(self, neighbors_filename, input_text):
        path_for_neighbors_table = self.unit_tests_directory / neighbors_filename
        input_grid = skeleton.ChipsGrid(input_text)
        actual_output_text = skeleton.make_result_text(input_grid, path_for_neighbors_table)
        return actual_output_text

    def a_tester(self, neighbors_filename, input_text, expected_output_text):
        actual_output_text = self.calculate_output(neighbors_filename, input_text)
        self.assertEqual(actual_output_text, expected_output_text)

    # HERE UNIT TESTS FOR CLEAR GARBAGE METHOD

    def test_separate_un_relevant_lines_empty_file(self):
        un_relevant_text = """foooooo!?>>...XX11fooo!\n
        foooooo!?>>...XX11fooo!\n\n\n\n
        foooooo!?>>...XX11fooo!\n
        foooooo!?>>...XX11fooo!\n
        fo!?>>...XX11foo!\n
        """
        actual_result = skeleton.separate_un_relevant_lines(un_relevant_text)[0]
        expected_result = ''
        self.assertEqual(actual_result, expected_result)

    def test_separate_un_relevant_lines_one_dot_file(self):
        un_relevant_text = """foooooo!?>>...XX11fooo!\n
        foooooo!?>>...XX11fooo!\n\n\n\n
        .\n
        foooooo!?>>...XX11fooo!\n
        foooooo!?>>...XX11fooo!\n
        fo!?>>...XX11foo!\n
        """
        actual_result = skeleton.separate_un_relevant_lines(un_relevant_text)
        expected_result = '.'
        self.assertEqual(actual_result, expected_result)

    def test_separate_un_relevant_lines_choose_the_bigger(self):
        un_relevant_text = """foooooo!?>>...XX11fooo!
        foooooo!?>>...XX11fooo!\n\n\n\n
        ..
        XX
        ...
        X1X
        111
        foooooo!?>>...XX11fooo!
        foooooo!?>>...XX11fooo!
        fo!?>>...XX11foo!\n
        """
        actual_result = skeleton.separate_un_relevant_lines(un_relevant_text)
        expected_result = '...\n' \
                          'X1X\n' \
                          '111'
        self.assertEqual(actual_result, expected_result)

    def test_chip_grid(self):
        rows_dimension, column_dimension = 5, 5
        sample_size = 10_000
        for _, test_wafer in zip(range(sample_size), UnitTests.input_generator(rows_dimension, column_dimension)):
            wafer_grid = skeleton.ChipsGrid(test_wafer)
            wafer_text_result = str(wafer_grid)
            self.assertEqual(test_wafer, wafer_text_result)

    def test_find_longest_continuous_block_edges(self):
        input_set = set(range(1000))
        to_remove = {100, 500, 800}
        input_set_with_gaps = input_set.difference(to_remove)
        actual_result = skeleton.find_longest_continuous_block_edges(input_set_with_gaps)
        expected_result = (101, 499)
        self.assertTupleEqual(actual_result, expected_result)

    def test_find_longest_continuous_block_edges_parametrized(self):
        input_set = set(range(1000))
        for i in range(1, 500):
            input_set.remove(i)
            actual_result = skeleton.find_longest_continuous_block_edges(input_set)
            expected_result = (i + 1, 999)
            self.assertTupleEqual(actual_result, expected_result)
            input_set.add(i)

    def test_make_dict_of_neighbors_threshold(self):
        neighbors_filename = 'neighbors_table.json'
        neighbors_path = self.unit_tests_directory / neighbors_filename
        result_dict = skeleton.make_dict_of_neighbors_threshold(neighbors_path)
        expected_dict = {1: 1, 2: 1, 3: 2, 4: 3, 5: 3, 6: 4, 7: 5, 8: 6}
        self.assertDictEqual(result_dict, expected_dict)


if __name__ == '__main__':
    unittest.main()
