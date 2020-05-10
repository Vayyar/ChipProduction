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

    def calculate_output(self, neighbors_filename: str, input_text: str):
        path_for_neighbors_table: str = os.path.join(self.unit_tests_directory, neighbors_filename)
        input_grid: skeleton.ChipsGrid = skeleton.ChipsGrid(input_text)
        actual_output_text = skeleton.make_result_text(input_grid, path_for_neighbors_table)
        return actual_output_text

    def a_tester(self, neighbors_filename: str, input_text: str, expected_output_text: str):
        actual_output_text = self.calculate_output(neighbors_filename, input_text)
        self.assertEqual(actual_output_text, expected_output_text)
