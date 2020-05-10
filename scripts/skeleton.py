import argparse
import enum

from typing import List, Set, Dict

def parse_file(path_to_read_from: str):
    with open(path_to_read_from, 'r') as input_file:
        file_content = input_file.read()
    chips_map_as_string = clear_from_garbage(file_content)
    chips_map_as_grid: ChipsGrid = ChipsGrid(chips_map_as_string)
    return chips_map_as_grid


def clear_from_garbage(chips_map: str) -> str:
    chips_map_striped: str = chips_map.strip()
    file_lines: List[str] = chips_map_striped.split('\n')
    file_lines_striped: List[str] = [line.strip() for line in file_lines]
    max_not_garbage_line_length = max([len(line) for line in file_lines_striped if is_not_garbage_characters(line)])
    not_garbage_indexes: Set[int] = {index for index, line in enumerate(file_lines_striped)
                                     if is_not_garbage(line, max_not_garbage_line_length)}
    max_lines_continuity_start, max_lines_continuity_end = find_longest_continuous_block_edges(not_garbage_indexes)
    chips_map_part_list: List[str] = file_lines_striped[max_lines_continuity_start: max_lines_continuity_end + 1]
    chips_map_part_string: str = '\n'.join(chips_map_part_list)
    return chips_map_part_string


def is_not_garbage_characters(line: str) -> bool:
    """@pre: assume all line are striped
       check that all characters are of chips map
    """
    relevant_characters: Set[str] = {'X', '.', '1'}
    is_all_relevant_characters: bool = all([char in relevant_characters for char in line])
    is_not_garbage_line: bool = is_all_relevant_characters
    return is_not_garbage_line


def is_not_garbage(line: str, max_not_garbage_line_length: int):
    """more severe check from 'is_not_garbage_characters' method"""
    return is_not_garbage_characters(line) and len(line) == max_not_garbage_line_length and len(line) > 0


def find_longest_continuous_block_edges(set_of_ints: Set[int]):
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
    start_index: int = number - 1
    end_index: int = number + 1
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
    def __init__(self, map_as_string: str):
        self.__map_as_grid: List[List[Chip]] = ChipsGrid.make_chips_grid(map_as_string)

    @staticmethod
    def make_chips_grid(map_as_string: str):
        map_as_list: List[str] = map_as_string.split('\n')
        chips_grid_obj: List[List[Chip]] = list()
        for row_index, chips_row in enumerate(map_as_list):
            chips_grid_obj.append([])
            for column_index, chip_state in enumerate(chips_row):
                current_chip: Chip = Chip(row_index, column_index, chip_state)
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
        representation_grid: List[List[str]] = [[str(chip) for chip in grid_row] for grid_row in self.map_as_grid]
        representation_lines: List[str] = [''.join(representation_row) for representation_row in representation_grid]
        representation: str = '\n'.join(representation_lines)
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
                    result_row: int = chip.row + delta_rows
                    result_column: int = chip.column + delta_columns
                    current_neighbor: Chip = self.map_as_grid[result_row][result_column]
                    yield current_neighbor

    def exist_place(self, chip, delta_rows, delta_columns):
        result_row: int = chip.row + delta_rows
        result_column: int = chip.column + delta_columns
        is_existing_place: bool = 0 <= result_row < self.rows_number and 0 <= result_column < self.columns_number
        return is_existing_place

    def number_of_neighbors(self, chip):
        neighbors_number: int = sum(1 for _ in self.neighbors_iterator(chip))
        return neighbors_number

    def number_of_x_neighbors(self, chip):
        number_of_x_neighbors = sum(1 for neighbor in self.neighbors_iterator(chip) if neighbor.state == ChipState.Die)
        return number_of_x_neighbors



class Chip:
    def __init__(self, row, column, state):
        self.__row = row
        self.__column = column
        self.__state = Chip.translate_state_from_string_to_enum(state)

    @staticmethod
    def translate_state_from_string_to_enum(state: str):
        state_translation_dict: Dict[str, ChipState] = {'X': ChipState.Die, '1': ChipState.Live,
                                                        '.': ChipState.NotAChip, 'Y': ChipState.DieByPrediction}
        chip_state: ChipState = state_translation_dict[state]
        return chip_state

    def __repr__(self):
        return Chip.translate_state_from_enum_to_string(self.state)

    @staticmethod
    def translate_state_from_enum_to_string(chip_state: 'ChipState'):
        state_translation_dict: Dict[ChipState, str] = {ChipState.Die: 'X', ChipState.Live: '1',
                                                        ChipState.NotAChip: '.', ChipState.DieByPrediction: 'Y'}
        state: str = state_translation_dict[chip_state]
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





def make_result_text(wafer_grid, neighbors_path: str) -> str:
    pass

def save_result_text(result: str, output_path: str):
    pass


class ChipState(enum.Enum):
    Live = 1
    Die = 2
    DieByPrediction = 3
    NotAChip = 4


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path', type=str, help='path for input file.')
    parser.add_argument('output_path', type=str, help='path for input file.')
    parser.add_argument('neighbors_path', type=str, help='path for table file.')
    args = parser.parse_args()
    chips_grid = parse_file(args.input_path)
    processed_text = make_result_text(chips_grid, args.neighbors_path)
    save_result_text(processed_text, args.output_path)
