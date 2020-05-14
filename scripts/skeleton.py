import argparse
import enum
import json
from pathlib import Path


def parse_file(path_to_read_from):
    with open(path_to_read_from, 'r') as input_file:
        file_content = input_file.read()
    chips_map_as_string = clear_un_relevant_lines(file_content)
    chips_map_as_grid = ChipsGrid(chips_map_as_string)
    return chips_map_as_grid


def clear_un_relevant_lines(chips_map_as_str):
    """
    :param chips_map_as_str: content of a wafer file as .txt
    :return: only the wafer grid text that contains . X 1 only.
    """
    chips_map_striped = chips_map_as_str.strip()
    file_lines_list = chips_map_striped.split('\n')
    file_lines_striped_list = [line.strip() for line in file_lines_list]
    max_relevant_line_length = max(
        [len(line) for line in file_lines_striped_list if is_contains_only_relevant_characters(line)])
    relevant_indexes_set = {index for index, line in enumerate(file_lines_striped_list)
                            if is_relevant(line, max_relevant_line_length)}
    max_lines_continuity_start, max_lines_continuity_end = find_longest_continuous_block_edges(relevant_indexes_set)
    chips_map_part_list = file_lines_striped_list[max_lines_continuity_start: max_lines_continuity_end + 1]
    chips_map_part_string = '\n'.join(chips_map_part_list)
    return chips_map_part_string


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


def is_relevant(line, max_not_garbage_line_length):
    """more severe check from 'is_not_garbage_characters' method"""
    return is_contains_only_relevant_characters(line) and len(line) == max_not_garbage_line_length and len(line) > 0


def find_longest_continuous_block_edges(set_of_ints):
    max_section_start, max_section_end = -1, -2
    set_of_ints_copy = set_of_ints.copy()
    for number in set_of_ints:
        if number not in set_of_ints_copy:
            continue
        current_section_start, current_section_end = \
            find_edges_of_section_centered_at(number, set_of_ints, set_of_ints_copy)
        if current_section_end - current_section_start > max_section_end - max_section_start:
            max_section_start, max_section_end = current_section_start, current_section_end
    return max_section_start, max_section_end


def find_edges_of_section_centered_at(number, set_of_ints, to_remove_from):
    start_index = number - 1
    end_index = number + 1
    while start_index in set_of_ints:
        to_remove_from.remove(start_index)
        start_index -= 1
    start_index += 1

    while end_index in set_of_ints:
        to_remove_from.remove(end_index)
        end_index += 1
    end_index -= 1
    return start_index, end_index


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
        number_of_x_neighbors = sum(1 for neighbor in self.neighbors_iterator(chip) if neighbor.state == ChipState.Die)
        return number_of_x_neighbors


class ChipState(enum.Enum):
    Live = 1
    Die = 2
    DieByPrediction = 3
    NotAChip = 4


class Chip:
    state_string_to_enum_translation_dict = {'X': ChipState.Die, '1': ChipState.Live,
                                             '.': ChipState.NotAChip, 'Y': ChipState.DieByPrediction}

    state_enum_to_string_translation_dict = {ChipState.Die: 'X', ChipState.Live: '1',
                                             ChipState.NotAChip: '.', ChipState.DieByPrediction: 'Y'}

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
        if grid_cell.state != ChipState.Live:
            continue
        total_number_of_cell_neighbors = wafer_grid.number_of_neighbors(grid_cell)
        total_number_of_x_neighbors = wafer_grid.number_of_x_neighbors(grid_cell)
        threshold = neighbors_table[total_number_of_cell_neighbors]
        new_state = ChipState.DieByPrediction if total_number_of_x_neighbors >= threshold else ChipState.Live
        grid_cell.state = new_state

    return wafer_grid


def make_dict_of_neighbors_threshold(neighbors_path):
    with open(neighbors_path) as neighbors_json_file:
        data_dict = json.load(neighbors_json_file)
    neighbors_dict = {int(key): value for key, value in data_dict.items()}
    return neighbors_dict


def save_result_text(result_grid, output_directory_path, input_path):
    grid_text = str(result_grid)
    output_file_name = choose_output_filename(input_path)
    output_file_path = output_directory_path / output_file_name
    with open(output_file_path, 'w') as output_file:
        output_file.write(grid_text)


def choose_output_filename(input_path):
    return f'result_of_{Path(input_path).stem}.txt'


def arguments_validation(arguments):
    for attribute, attribute_argument in vars(arguments).items():
        if 'path' not in attribute:
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


def process_args(arguments):
    for attribute, attribute_argument in vars(arguments).items():
        if 'path' in attribute:
            setattr(arguments, attribute, Path(attribute_argument))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file_path', type=str, help='path for input file.')
    parser.add_argument('output_dir_path', type=str, help='path for output directory.')
    parser.add_argument('neighbors_file_path', type=str, help='path for table file.')
    args = parser.parse_args()
    process_args(args)
    arguments_validation(args)
    chips_grid = parse_file(args.input_file_path)
    processed_grid = apply_algorithm_on_grid(chips_grid, args.neighbors_file_path)
    save_result_text(processed_grid, args.output_dir_path, args.input_file_path)
