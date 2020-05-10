import unittest

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

    def calculate_output(self, neighbors_filename: str, input_text: str):
        path_for_neighbors_table: str = os.path.join(self.unit_tests_directory, neighbors_filename)
        input_grid: skeleton.ChipsGrid = skeleton.ChipsGrid(input_text)
        actual_output_text = skeleton.make_result_text(input_grid, path_for_neighbors_table)
        return actual_output_text

    def a_tester(self, neighbors_filename: str, input_text: str, expected_output_text: str):
        actual_output_text = self.calculate_output(neighbors_filename, input_text)
        self.assertEqual(actual_output_text, expected_output_text)
