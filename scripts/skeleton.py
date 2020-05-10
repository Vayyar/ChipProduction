import argparse


def parse_file(path_to_read_from: str):
    with open(path_to_read_from, 'r') as input_file:
        file_content = input_file.read()
    chips_map_as_string = clear_from_garbage(file_content)
    chips_map_as_grid: ChipsGrid = ChipsGrid(chips_map_as_string)
    return chips_map_as_grid

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
