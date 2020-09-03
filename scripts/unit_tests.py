import math
import subprocess
import unittest
from datetime import datetime
from pathlib import Path
from random import choice

import utils
from scripts import main


class UnitTests(unittest.TestCase):

    def setUp(self):
        self.unit_tests_directory = Path(__file__).parents[1].absolute() / 'unit_tests'
        self.neighbors_filename = 'neighbors_table.json'
        self.wafer_initial_states = ['X', '1', '.']

    def test_consistency(self):
        # read last .stdf running result
        cwd = Path(__file__).parent
        main_script_path = cwd / "main.py"
        stdf_file_path = cwd / '../resources/N6W014_N6W014-19E5_WS_CP1_-40_20200313_110305.stdf'
        results_path = cwd / f'../unit_tests/consistency_test__Date_{datetime.today().strftime("%Y_%m_%d_%H_%M_%S")}'
        neighbors_file_path = cwd / '../resources/neighbors_table.json'
        Path.mkdir(results_path)
        utils.wait_for_path_to_exists(results_path)
        command = ['python', '-u', f'{main_script_path}', '--ignore-gooey', f'{stdf_file_path}',
                   f'{results_path}',
                   f'{neighbors_file_path}']
        print(' '.join(command))
        subprocess.run(command, input='File\n', stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, encoding='ascii')

        result_file_path = utils.get_inner_dir_path(results_path) / main.choose_output_filename(stdf_file_path)
        utils.wait_for_path_to_exists(result_file_path, maximum_time_to_wait=60)
        with open(result_file_path, 'r') as result_file:
            result_wafer = result_file.read()
        # restore the original wafer
        test_wafer = result_wafer.replace('Y', '1')
        # make new .txt test file from the original wafer
        test_file_path = cwd.parent / 'resources/test_wafer.txt'
        with open(test_file_path, 'w') as test_file:
            test_file.write(test_wafer)
        # run this python file on the new .txt file
        output_dir_path = cwd.parent / 'results'
        command = ['python', '-u', f'{main_script_path}', '--ignore-gooey', f'{test_file_path}',
                   f'{output_dir_path}', f'{neighbors_file_path}']
        subprocess.run(command, input='File\n', stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, encoding='ascii')
        output_file_path = utils.get_inner_dir_path(results_path) / main.choose_output_filename(stdf_file_path)
        utils.wait_for_path_to_exists(output_file_path, maximum_time_to_wait=60)
        with open(output_file_path, 'r') as result_from_text_file:
            result_from_text_file_wafer_str = result_from_text_file.read()
        # compare them.
        self.assertEqual(result_from_text_file_wafer_str, result_wafer)

    def test_is_y_exchange_its_neighbor_to_y(self):
        input_text = "...\n" \
                     "X11\n" \
                     "..."
        expected_wafer_text_first_option = "...\n" \
                                           "XY1\n" \
                                           "..."
        expected_wafer_text_second_option = "...\n" \
                                            "XYY\n" \
                                            "..."
        self.a_tester(self.neighbors_filename, input_text, expected_wafer_text_first_option)

    def test_ignore_small_noises(self):
        input_text = ".\n" \
                     "XXX\n" \
                     "XXX\n" \
                     "XXX\n" \
                     "."
        expected_wafer_text = "XXX\n" \
                              "XXX\n" \
                              "XXX"
        actual_wafer_text, _ = main.separate_un_relevant_text_lines(input_text)
        self.assertEqual(actual_wafer_text, expected_wafer_text)

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
    def test_same_amount_xs_no_more_1s_same_amount_of_dots_no_other_chars(self):
        dim1, dim2 = 3, 3
        for input_text in UnitTests.input_generator(dim1, dim2):
            self.assert_that_algorithm_return_making_sense_result(input_text)

    def test_amount_of_x_y_1_dots_in_result_on_random_samples(self):
        dimensions = [(1, 1), (3, 5), (37, 25), (44, 12), (15, 1)]
        sample_size = 50
        for dimension in dimensions:
            self.check_algorithm_on_samples(dimension, sample_size)

    def check_algorithm_on_samples(self, dimension, sample_size):
        for random_wafer in self.get_random_sample_points(dimension, sample_size):
            self.assert_that_algorithm_return_making_sense_result(random_wafer)

    def get_random_sample_points(self, dimension, sample_size):
        for _ in range(sample_size):
            yield self.get_random_sample_point(dimension)

    def get_random_sample_point(self, dimension):
        x_dimension, y_dimension = dimension
        states_list = [[self.get_random_wafer_state() for _ in range(x_dimension)] for _ in range(y_dimension)]
        lines_list = [''.join(states_row) for states_row in states_list]
        wafer_as_str = '\n'.join(lines_list)
        return wafer_as_str

    def get_random_wafer_state(self):
        return choice(self.wafer_initial_states)

    def assert_that_algorithm_return_making_sense_result(self, input_text):
        neighbors_filename = 'neighbors_table.json'
        # no less xs
        number_of_xs_input = input_text.count('X')
        actual_result = self.calculate_output(neighbors_filename, input_text)
        number_of_xs_output = actual_result.count('X')
        self.assertTrue(number_of_xs_output == number_of_xs_input)
        # no more 1s
        number_of_1s_input = input_text.count('1')
        number_of_1s_output = actual_result.count('1')
        self.assertTrue(number_of_1s_output <= number_of_1s_input)
        # (#Y + #1) in output == (#1) in input.
        number_of_ys_output = actual_result.count('Y')
        self.assertTrue(number_of_1s_output + number_of_ys_output == number_of_1s_input)
        # no more dots
        number_of_dots_input = input_text.count('.')
        number_of_dots_output = actual_result.count('.')
        self.assertTrue(number_of_dots_input == number_of_dots_output)
        # no other chars except Y
        other_chars = actual_result.replace('.', '').replace('X', '').replace('1', '').replace('\n', ''). \
            replace('Y', '')
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
        input_grid = main.ChipsGrid(input_text)
        actual_output_as_greed = main.apply_algorithm_on_grid(input_grid, path_for_neighbors_table)
        actual_output_text = str(actual_output_as_greed)
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
        try:
            _, __ = main.separate_un_relevant_text_lines(un_relevant_text)
            self.assertTrue(False)
        except Exception as e:
            self.assertEqual(type(e), main.BadWaferFileException)

    def test_separate_un_relevant_lines_one_dot_file(self):
        un_relevant_text = """foooooo!?>>...XX11fooo!\n
        foooooo!?>>...XX11fooo!\n\n\n\n
        .\n
        foooooo!?>>...XX11fooo!\n
        foooooo!?>>...XX11fooo!\n
        fo!?>>...XX11foo!\n
        """

        actual_result, _ = main.separate_un_relevant_text_lines(un_relevant_text)
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
        actual_result, _ = main.separate_un_relevant_text_lines(un_relevant_text)
        expected_result = '...\n' \
                          'X1X\n' \
                          '111'
        self.assertEqual(actual_result, expected_result)

    def test_chip_grid(self):
        rows_dimension, column_dimension = 5, 5
        sample_size = 10_000
        for _, test_wafer in zip(range(sample_size), UnitTests.input_generator(rows_dimension, column_dimension)):
            wafer_grid = main.ChipsGrid(test_wafer)
            wafer_text_result = str(wafer_grid)
            self.assertEqual(test_wafer, wafer_text_result)

    def test_make_dict_of_neighbors_threshold(self):
        neighbors_filename = 'neighbors_table.json'
        neighbors_path = self.unit_tests_directory / neighbors_filename
        result_dict = main.make_dict_of_neighbors_threshold(neighbors_path)
        expected_dict = {0: 1, 1: 1, 2: 1, 3: 2, 4: 3, 5: 3, 6: 4, 7: 5, 8: 6}
        self.assertDictEqual(result_dict, expected_dict)


if __name__ == '__main__':
    unittest.main()
