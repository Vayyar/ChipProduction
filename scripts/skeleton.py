import argparse

from typing import List, Set

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



def make_result_text(wafer_grid, neighbors_path: str) -> str:
    pass

def save_result_text(result: str, output_path: str):
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path', type=str, help='path for input file.')
    parser.add_argument('output_path', type=str, help='path for input file.')
    parser.add_argument('neighbors_path', type=str, help='path for table file.')
    args = parser.parse_args()
    chips_grid = parse_file(args.input_path)
    processed_text = make_result_text(chips_grid, args.neighbors_path)
    save_result_text(processed_text, args.output_path)
