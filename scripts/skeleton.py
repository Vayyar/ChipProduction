import argparse
import enum
import json
from collections import Counter
from pathlib import Path
from string import Template

from pystdf.IO import Parser

def parse_file(path_to_read_from):
    type_of_file = path_to_read_from.suffix
    methods_dict = {'.txt': parse_text_file, '.stdf': parse_stdf_file}
    return methods_dict[type_of_file](path_to_read_from)


def parse_stdf_file(path_to_read_from):
    expected_grid = None

    class StdfToGrid:

        def after_begin(self):
            self.prev = 0
            self.text = ""
            self.pool = set()

        def after_send(self, dataSrc):
            rectype, fields = dataSrc

            if rectype == prr:
                x_coordinate = fields[prr.X_COORD]
                y_coordinate = fields[prr.Y_COORD]
                is_fail = (fields[prr.PART_FLG] & 8) >> 3
                state = 'X' if is_fail else '1'
                current_chip = Chip(y_coordinate, x_coordinate, state)
                if current_chip in self.pool and current_chip.state == ChipState.FAIL:
                    self.pool.remove(current_chip)
                self.pool.add(current_chip)

        def after_complete(self):
            self.grid = StdfToGrid.partition_into_rows(self.pool)
            StdfToGrid.sort_each_chips_row(self.grid)
            self.grid = StdfToGrid.make_square_from_table(self.grid)
            self.grid = ChipsGrid.make_chips_grid_from_grid(self.grid)
            # print(self.grid)
            nonlocal expected_grid
            expected_grid = self.grid

        @staticmethod
        def partition_into_rows(pool):
            rows_dict = dict()
            for chip in pool:
                if chip.row not in rows_dict:
                    rows_dict[chip.row] = list()
                rows_dict[chip.row].append(chip)
            # turn the dict into list
            number_of_rows = max(rows_dict.keys()) + 1
            grid = [rows_dict[index] for index in range(number_of_rows)]
            return grid

        @staticmethod
        def sort_each_chips_row(grid):
            for chips_row in grid:
                chips_row.sort(key=lambda chip: chip.column)

        @staticmethod
        def make_square_from_table(chips_table):
            max_row_length = max(len(chips_row) for chips_row in chips_table)
            square_grid = list()
            for chips_row in chips_table:
                filled_row = StdfToGrid.fill_row_edges(chips_row, max_row_length)
                square_grid.append(filled_row)
            return square_grid

        @staticmethod
        def fill_row_edges(chips_row, final_length):
            first_filled_column = chips_row[0].column
            last_filled_column = chips_row[-1].column
            row_number = chips_row[0].row
            row_start = [Chip(row_number, column, '.') for column in range(first_filled_column)]
            row_end = [Chip(row_number, column, '.') for column in range(last_filled_column + 1, final_length)]
            return row_start + chips_row + row_end

    with open(path_to_read_from, 'rb') as stdf_file:
        parser_object = Parser(inp=stdf_file)
        parser_object.addSink(StdfToGrid)
        parser_object.parse()

    return expected_grid, Template("$wafer")


def parse_text_file(path_to_read_from):
    with open(path_to_read_from, 'r') as input_file:
        file_content = input_file.read()
    chips_map_as_string, rest_of_text_as_template = separate_un_relevant_lines(file_content)
    chips_map_as_grid = ChipsGrid(chips_map_as_string)
    return chips_map_as_grid, rest_of_text_as_template


def separate_un_relevant_lines(chips_map_as_str):
    """
    :param chips_map_as_str: content of a wafer file as .txt
    :return: only the wafer grid text that contains . X 1 only.
    """
    chips_map_striped = chips_map_as_str.strip()
    file_lines_list = chips_map_striped.split('\n')
    file_lines_striped_list = [line.strip() for line in file_lines_list]
    most_common_relevant_line_length = find_most_common_relevant_line_length(file_lines_striped_list)
    relevant_indexes_set = {index for index, line in enumerate(file_lines_striped_list)
                            if is_relevant_wafer_line(line, most_common_relevant_line_length)}
    handle_two_wafers_case(relevant_indexes_set)
    wafer_start_index, wafer_end_index = min(relevant_indexes_set), max(relevant_indexes_set)
    chips_map_part_list = file_lines_striped_list[wafer_start_index: wafer_end_index + 1]
    chips_map_part_string = '\n'.join(chips_map_part_list)
    rest_of_the_text = chips_map_as_str.replace(chips_map_part_string, '$wafer')
    rest_of_text_as_template = Template(rest_of_the_text)
    return chips_map_part_string, rest_of_text_as_template


def handle_two_wafers_case(relevant_indexes_set):
    if is_not_continuous_set(relevant_indexes_set):
        raise TwoWafersException('There are 2 wafers in the same file with same length')


class TwoWafersException(Exception):
    def __init__(self, message):
        self.message = message

    def __repr__(self):
        return f'TwoWafersException!!!  {self.message}'


def is_not_continuous_set(int_set):
    is_continuous = max(int_set) - min(int_set) + 1 != len(int_set)
    return is_continuous


def find_most_common_relevant_line_length(file_lines_list):
    lengths_list = [len(line) for line in file_lines_list if is_contains_only_relevant_characters(line)]
    counters = Counter(lengths_list)
    return counters.most_common()[0][0]


def is_contains_only_relevant_characters(line):
    """
    assume line are striped
    :param line: a text line
    :return: True iff all characters are of chips map
            i.e the line composed from 1 X . only.
    """
    relevant_characters_set = {'X', '.', '1', 'Y'}
    is_all_relevant_characters = all([char in relevant_characters_set for char in line])
    is_not_garbage_line = is_all_relevant_characters
    return is_not_garbage_line


def is_relevant_wafer_line(line, most_common_not_garbage_line_length):
    """
    more severe check from 'is_not_garbage_characters' method
    :param line: line of text
    :param most_common_not_garbage_line_length: the expected len from not garbage line.
    :return: True iff line is part of the wafer grid.
    """
    return all([is_contains_only_relevant_characters(line), len(line) == most_common_not_garbage_line_length,
                len(line) > 0])


class ChipsGrid:
    def __init__(self, map_as_string):
        self.__map_as_grid = ChipsGrid.make_chips_grid(map_as_string)

    @staticmethod
    def make_chips_grid(map_as_string):
        map_as_list = map_as_string.split('\n')
        chips_grid_obj = list()
        for row_index, chips_row in enumerate(map_as_list):
            chips_grid_obj.append([])
            for column_index, chip_state in enumerate(chips_row):
                current_chip = Chip(row_index, column_index, chip_state)
                chips_grid_obj[-1].append(current_chip)
        return chips_grid_obj

    @property
    def map_as_grid(self):
        return self.__map_as_grid

    @property
    def rows_number(self):
        return len(self.map_as_grid)

    @property
    def columns_number(self):
        if self.rows_number == 0:
            return 0
        return len(self.map_as_grid[0])

    def __repr__(self):
        representation_grid = [[str(chip) for chip in grid_row] for grid_row in self.map_as_grid]
        representation_lines_list = [''.join(representation_row) for representation_row in representation_grid]
        representation = '\n'.join(representation_lines_list)
        return representation

    def __iter__(self):
        for chips_row in self.map_as_grid:
            for chip in chips_row:
                yield chip

    def neighbors_iterator(self, chip):
        for delta_rows in {-1, 0, 1}:
            for delta_columns in {-1, 0, 1}:
                if delta_rows == delta_columns == 0:
                    continue
                elif self.exist_place(chip, delta_rows, delta_columns):
                    result_row = chip.row + delta_rows
                    result_column = chip.column + delta_columns
                    current_neighbor = self.map_as_grid[result_row][result_column]
                    yield current_neighbor

    def exist_place(self, chip, delta_rows, delta_columns):
        result_row = chip.row + delta_rows
        result_column = chip.column + delta_columns
        is_existing_place = 0 <= result_row < self.rows_number and 0 <= result_column < self.columns_number
        return is_existing_place

    def number_of_neighbors(self, chip):
        neighbors_number = sum(1 for _ in self.neighbors_iterator(chip))
        return neighbors_number

    def number_of_x_neighbors(self, chip):
        number_of_x_neighbors = sum(1 for neighbor in self.neighbors_iterator(chip) if neighbor.state == ChipState.FAIL)
        return number_of_x_neighbors


class ChipState(enum.Enum):
    PASS = 1
    FAIL = 2
    FAIL_BY_PREDICTION = 3
    NOT_EXISTS = 4


class Chip:
    state_string_to_enum_translation_dict = {'X': ChipState.FAIL, '1': ChipState.PASS,
                                             '.': ChipState.NOT_EXISTS, 'Y': ChipState.FAIL_BY_PREDICTION}

    state_enum_to_string_translation_dict = {ChipState.FAIL: 'X', ChipState.PASS: '1',
                                             ChipState.NOT_EXISTS: '.', ChipState.FAIL_BY_PREDICTION: 'Y'}

    def __init__(self, row, column, state):
        self.__row = row
        self.__column = column
        self.__state = Chip.translate_state_from_string_to_enum(state)

    @staticmethod
    def translate_state_from_string_to_enum(state_as_str):
        chip_state = Chip.state_string_to_enum_translation_dict[state_as_str]
        return chip_state

    def __repr__(self):
        return Chip.translate_state_from_enum_to_string(self.state)

    @staticmethod
    def translate_state_from_enum_to_string(chip_state_enum):
        state = Chip.state_enum_to_string_translation_dict[chip_state_enum]
        return state

    @property
    def row(self):
        return self.__row

    @property
    def column(self):
        return self.__column

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, new_state):
        self.__state = new_state


def apply_algorithm_on_grid(wafer_grid, neighbors_path):
    neighbors_table = make_dict_of_neighbors_threshold(neighbors_path)
    for grid_cell in wafer_grid:
        if grid_cell.state != ChipState.PASS:
            continue
        total_number_of_cell_neighbors = wafer_grid.number_of_neighbors(grid_cell)
        total_number_of_x_neighbors = wafer_grid.number_of_x_neighbors(grid_cell)
        threshold = neighbors_table[total_number_of_cell_neighbors]
        new_state = ChipState.FAIL_BY_PREDICTION if total_number_of_x_neighbors >= threshold else ChipState.PASS
        grid_cell.state = new_state

    return wafer_grid


def make_dict_of_neighbors_threshold(neighbors_path):
    with open(neighbors_path) as neighbors_json_file:
        data_dict = json.load(neighbors_json_file)
    neighbors_dict = {int(key): value for key, value in data_dict.items()}
    return neighbors_dict


def save_result_text(result_grid, output_directory_path, input_path):
def save_result_as_text(result_grid, output_directory_path, input_path):
    grid_text = str(result_grid)
    output_file_name = choose_output_filename(input_path)
    output_file_path = output_directory_path / output_file_name
    with open(output_file_path, 'w') as output_file:
        output_file.write(grid_text)


def choose_output_filename(input_path):
    return f'result_of_{Path(input_path).stem}.txt'


def arguments_validation(arguments):
    for attribute, attribute_argument in vars(arguments).items():
        if not isinstance(attribute_argument, Path):
            continue
        if not attribute_argument.exists():
            raise WrongArgumentsException(f"The path {attribute_argument} don't exist")
        if 'dir' in attribute and attribute_argument.is_file():
            raise WrongArgumentsException(f"The path {attribute_argument} is a file while we expect to a directory")
        if 'file' in attribute and attribute_argument.is_dir():
            raise WrongArgumentsException(f"The path {attribute_argument} is a directory while we expect a file")


class WrongArgumentsException(Exception):
    def __init__(self, *arguments):
        if arguments:
            self.message = arguments[0]
        else:
            self.message = None

    def __repr__(self):
        return f'WrongArgumentException!!!  {self.message if self.message is not None else ""}'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file_path', type=lambda p: Path(p), help='path for input file.')
    parser.add_argument('output_dir_path', type=lambda p: Path(p), help='path for output directory.')
    parser.add_argument('neighbors_file_path', type=lambda p: Path(p), help='path for table file.')
    args = parser.parse_args()
    arguments_validation(args)
    chips_grid, rest_of_the_text_as_template = parse_text_file(args.input_file_path)
    processed_grid = apply_algorithm_on_grid(chips_grid, args.neighbors_file_path)
    result_text = rest_of_the_text_as_template.substitute({'wafer': processed_grid})
    save_result_as_text(result_text, args.output_dir_path, args.input_file_path)
