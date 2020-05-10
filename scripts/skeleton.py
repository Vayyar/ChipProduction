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
