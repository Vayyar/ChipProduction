import math
import os
import unittest
from typing import List, Set, Dict

from scripts import skeleton


class UnitTests(unittest.TestCase):

    def setUp(self) -> None:
        self.unit_tests_directory: str = '../unit_tests'

    def test_middle(self):
        neighbors_filename = 'neighbors_table.json'
        input_text: str = "XXX\n" \
                          "X1X\n" \
                          "XXX"
        expected_output_text: str = "XXX\n" \
                                    "XYX\n" \
                                    "XXX"
        self.a_tester(neighbors_filename, input_text, expected_output_text)

    def test_all_ones(self):
        neighbors_filename = 'neighbors_table.json'
        input_text: str = "111\n" \
                          "111\n" \
                          "111"
        expected_output_text: str = "111\n" \
                                    "111\n" \
                                    "111"
        self.a_tester(neighbors_filename, input_text, expected_output_text)

    def test_dots(self):
        neighbors_filename = 'neighbors_table.json'
        input_text: str = "...\n" \
                          "...\n" \
                          "..."
        expected_output_text: str = "...\n" \
                                    "...\n" \
                                    "..."
        self.a_tester(neighbors_filename, input_text, expected_output_text)

    def test_lonely_one_and_many_dots_bottom(self):
        neighbors_filename = 'neighbors_table.json'
        input_text: str = "...\n" \
                          "...\n" \
                          "1.."
        expected_output_text: str = "...\n" \
                                    "...\n" \
                                    "1.."
        self.a_tester(neighbors_filename, input_text, expected_output_text)

    def test_lonely_one_and_many_dots_top(self):
        neighbors_filename = 'neighbors_table.json'
        input_text: str = "..1\n" \
                          "...\n" \
                          "..."
        expected_output_text: str = "..1\n" \
                                    "...\n" \
                                    "..."
        self.a_tester(neighbors_filename, input_text, expected_output_text)

    def test_all_x(self):
        neighbors_filename = 'neighbors_table.json'
        input_text: str = "XXX\n" \
                          "XXX\n" \
                          "XXX"
        expected_output_text: str = "XXX\n" \
                                    "XXX\n" \
                                    "XXX"
        self.a_tester(neighbors_filename, input_text, expected_output_text)

    # Takes 2 seconds
    def test_no_less_xs(self):

        neighbors_filename: str = 'neighbors_table.json'
        # TODO put here smaller numbers for fast running
        dim1, dim2 = 3, 3
        for input_text in UnitTests.input_generator(dim1, dim2):
            number_of_xs_input: int = input_text.count('X')
            actual_result: str = self.calculate_output(neighbors_filename, input_text)
            number_of_xs_output: int = actual_result.count('X')
            self.assertTrue(number_of_xs_output >= number_of_xs_input)

    @staticmethod
    def input_generator(dimension_1: int, dimension_2: int):
        translator = {0: 'X', 1: '.', 2: '1'}

        def make_input_from_number(represent_number: int):
            base: int = len(translator)
            wafer_grid: List[List[str]] = list()
            for row_index in range(dimension_1):
                wafer_grid.append([])
                for column_index in range(dimension_2):
                    residue: int = represent_number % base
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

    def calculate_output(self, neighbors_filename: str, input_text: str):
        path_for_neighbors_table: str = os.path.join(self.unit_tests_directory, neighbors_filename)
        input_grid: skeleton.ChipsGrid = skeleton.ChipsGrid(input_text)
        actual_output_text = skeleton.make_result_text(input_grid, path_for_neighbors_table)
        return actual_output_text

    def a_tester(self, neighbors_filename: str, input_text: str, expected_output_text: str):
        actual_output_text = self.calculate_output(neighbors_filename, input_text)
        self.assertEqual(actual_output_text, expected_output_text)

    # HERE UNIT TESTS FOR CLEAR GARBAGE METHOD

    def test_clear_garbage_empty_file(self):
        garbage_text = """foooooo!?>>...XX11fooo!\n
        foooooo!?>>...XX11fooo!\n\n\n\n
        foooooo!?>>...XX11fooo!\n
        foooooo!?>>...XX11fooo!\n
        fo!?>>...XX11foo!\n
        """
        actual_result: str = skeleton.clear_from_garbage(garbage_text)
        expected_result: str = ''
        self.assertEqual(actual_result, expected_result)

    def test_clear_garbage_one_dot_file(self):
        garbage_text = """foooooo!?>>...XX11fooo!\n
        foooooo!?>>...XX11fooo!\n\n\n\n
        .\n
        foooooo!?>>...XX11fooo!\n
        foooooo!?>>...XX11fooo!\n
        fo!?>>...XX11foo!\n
        """
        actual_result: str = skeleton.clear_from_garbage(garbage_text)
        expected_result: str = '.'
        self.assertEqual(actual_result, expected_result)

    def test_clear_garbage_choose_the_bigger(self):
        garbage_text = """foooooo!?>>...XX11fooo!
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
        actual_result: str = skeleton.clear_from_garbage(garbage_text)
        expected_result: str = '...\n' \
                               'X1X\n' \
                               '111'
        self.assertEqual(actual_result, expected_result)

