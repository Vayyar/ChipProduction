import copy
import enum
import json
import logging
import warnings
from collections import Counter
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from string import Template

import pandas
from gooey import GooeyParser, Gooey
from pystdf.IO import Parser
from pystdf.V4 import prr

import HtmlViewer
import utils

logger = logging.getLogger('ChipProductionLogger')
handler = RotatingFileHandler('ChipProductionLogger.log', maxBytes=100_000, backupCount=1)
logger.addHandler(handler)


def parse_file(path_to_read_from):
    type_of_file = path_to_read_from.suffix
    methods_dict = {'.txt': parse_text_file, '.stdf': parse_stdf_file}
    return methods_dict[type_of_file](path_to_read_from)


def parse_stdf_file(path_to_read_from):
    expected_grid = None

    class StdfToGrid:

        def after_begin(self):
            self.chips_set = set()

        def after_send(self, data):
            """
            prr: Contains the result information relating to each part tested by the test program.
            The PRR and the Part Information Record (PIR) bracket all the stored information
            pertaining to one tested part.
            i.e it contains the pass or fail data for each chip.
            link for documentation : http://www.kanwoda.com/wp-content/uploads/2015/05/std-spec.pdf
            see in the prr section page 41.
            ----------------------------------------------------------------------------------------
            X_COORD | are fields of prr Have legal values in the range -32767 to 32767.
            Y_COORD |  A missing value is indicated by the value -32768.
            ----------------------------------------------------------------------------------------
            PART_FLG | is also a field of prr, that contains several bits the three of them
                     | is indicating pass fail 0 = Part passed 1 = Part failed.
            """
            record_type, fields = data

            if record_type == prr:
                x_coordinate = fields[prr.X_COORD]
                y_coordinate = fields[prr.Y_COORD]
                is_fail = StdfToGrid.is_fail_prr(fields)
                state = 'X' if is_fail else '1'
                current_chip = Chip(y_coordinate, x_coordinate, state)
                if current_chip in self.chips_set and current_chip.state == ChipState.FAIL:
                    self.chips_set.remove(current_chip)
                self.chips_set.add(current_chip)

        @staticmethod
        def is_fail_prr(fields):
            return (fields[prr.PART_FLG] & 8) >> 3

        def after_complete(self):
            self.grid = StdfToGrid.partition_into_rows(self.chips_set)
            StdfToGrid.sort_each_chips_row(self.grid)
            self.grid = StdfToGrid.make_square_from_table(self.grid)
            self.grid = ChipsGrid.make_chips_grid_from_grid(self.grid)
            nonlocal expected_grid
            expected_grid = self.grid

        @staticmethod
        def partition_into_rows(chips_set):
            rows_dict = dict()
            for chip in chips_set:
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
    logger.info('Read the input wafer text file.')
    with open(path_to_read_from, 'r') as input_file:
        file_content = input_file.read()
    chips_map_as_string, rest_of_text_as_template = separate_un_relevant_text_lines(file_content)
    chips_map_as_grid = ChipsGrid(chips_map_as_string)
    return chips_map_as_grid, rest_of_text_as_template


def separate_un_relevant_text_lines(chips_map_as_str):
    """
    Get content of text file and separate it into the wafer
    part and the rest of the text.
    separate the text file into wafer and all the other stuff.
    :param chips_map_as_str: content of a wafer file as .txt
    :return: The wafer grid text that contains . X 1 only and template of all the other stuff.
    """
    logger.debug('In parse input wafer file: Starting extract wafer from text.')
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
    logger.debug('In parse input wafer file: Finish of separate wafer from text.')
    return chips_map_part_string, rest_of_text_as_template


def handle_two_wafers_case(relevant_indexes_set):
    if is_not_continuous_set(relevant_indexes_set):
        error_message = 'There are 2 wafers in the same file with same length.'
        logger.error(error_message)
        raise BadWaferFileException(error_message)


class BadWaferFileException(Exception):
    def __init__(self, message):
        self.message = message

    def __repr__(self):
        return f'BadWaferFileException!!!  {self.message}'


def is_not_continuous_set(int_set):
    is_continuous = max(int_set) - min(int_set) + 1 != len(int_set)
    return is_continuous


def find_most_common_relevant_line_length(file_lines_list):
    lengths_list = [len(line) for line in file_lines_list if
                    is_contains_only_relevant_characters(line) and len(line) != 0]
    if len(lengths_list) == 0:
        raise BadWaferFileException("The file contains no wafers!!!")
    counters = Counter(lengths_list)
    return counters.most_common()[0][0]


def is_contains_only_relevant_characters(line):
    """
    Checks if it possible that line is part of wafer.
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
    Make sure that line is indeed part of THE wafer in this file.
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
        logger.info('Starting save wafer into memory.')
        logger.debug('Starting save wafer text into memory.')
        map_as_list = map_as_string.split('\n')
        chips_grid_obj = list()
        for row_index, chips_row in enumerate(map_as_list):
            chips_grid_obj.append([])
            for column_index, chip_state in enumerate(chips_row):
                current_chip = Chip(row_index, column_index, chip_state)
                chips_grid_obj[-1].append(current_chip)
        logger.debug('Finish of save wafer text into memory.')
        logger.info('Wafer was saved into memory.')
        return chips_grid_obj

    def __deepcopy__(self, memodict={}):
        logger.info('Create wafer copy.')
        return ChipsGrid(str(self))

    @staticmethod
    def make_chips_grid_from_grid(chips_table):
        grid = ChipsGrid('')
        grid.__map_as_grid = chips_table
        return grid

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
        logger.info('Turn wafer into text representation.')
        representation_grid = [[str(chip) for chip in grid_row] for grid_row in self.map_as_grid]
        representation_lines_list = [''.join(representation_row) for representation_row in representation_grid]
        representation = '\n'.join(representation_lines_list)
        return representation

    def __iter__(self):
        """
        Iterate over all Chips in this grid.
        :return: Chips instances ordered by rows.
        """
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
        neighbors_number = sum(1 for neighbor in self.neighbors_iterator(chip)
                               if neighbor.state != ChipState.NOT_EXISTS)
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

    def __eq__(self, other):
        return all([self.row == other.row, self.column == other.column])

    def __hash__(self):
        return hash(self.column) + 1024 * hash(self.row)

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
    logger.debug('Starting apply the algorithm for predict who chips are failed.')
    wafer_grid_copy = copy.deepcopy(wafer_grid)
    neighbors_table = make_dict_of_neighbors_threshold(neighbors_path)
    for grid_cell in wafer_grid_copy:
        if grid_cell.state != ChipState.PASS:
            continue
        total_number_of_cell_neighbors = wafer_grid_copy.number_of_neighbors(grid_cell)
        total_number_of_x_neighbors = wafer_grid_copy.number_of_x_neighbors(grid_cell)
        threshold = neighbors_table[total_number_of_cell_neighbors]
        new_state = ChipState.FAIL_BY_PREDICTION if total_number_of_x_neighbors >= threshold else ChipState.PASS
        grid_cell.state = new_state
    logger.debug('Finish apply the algorithm for predict who chips are failed.')
    return wafer_grid_copy


def make_dict_of_neighbors_threshold(neighbors_path):
    logger.debug('Start reading input neighbors threshold file.')
    with open(neighbors_path) as neighbors_json_file:
        data_dict = json.load(neighbors_json_file)
    neighbors_dict = {int(key): value for key, value in data_dict.items()}
    logger.debug('Finish reading and processing input neighbors threshold file.')
    return neighbors_dict


def save_result_as_text(result_grid, output_directory_path, input_path):
    logger.debug('Saving result wafer as text file.')
    grid_text = str(result_grid)
    output_file_path = get_output_file_path(output_directory_path, input_path)
    with open(output_file_path, 'w') as output_file:
        output_file.write(grid_text)


def get_output_file_path(output_directory_path, input_path):
    output_file_name = choose_output_filename(input_path)
    output_file_path = output_directory_path / output_file_name
    return output_file_path


def choose_output_filename(input_path):
    return f'result_of_{input_path.stem}.txt'  # {input_path.suffix}'


def arguments_validation(arguments):
    logger.debug('Starting validating input arguments.')
    for attribute, attribute_argument in vars(arguments).items():
        if not isinstance(attribute_argument, Path):
            continue
        if not attribute_argument.exists():
            raise WrongArgumentsException(f"The path {attribute_argument} don't exist")
        if 'dir' in attribute and attribute_argument.is_file():
            raise WrongArgumentsException(f"The path {attribute_argument} is a file while we expect to a directory")
        if 'file' in attribute and attribute_argument.is_dir():
            raise WrongArgumentsException(f"The path {attribute_argument} is a directory while we expect a file")
        if 'file' in attribute and attribute_argument.is_dir():
            raise WrongArgumentsException(f"The path {attribute_argument} is a directory while we expect a file")
        if 'file' in attribute:
            if attribute_argument.is_dir():
                raise WrongArgumentsException(f"The path {attribute_argument} is a directory while we expect a file")
            supported_file_types = {'.txt', '.stdf'}
            if 'input' in attribute and attribute_argument.suffix not in supported_file_types:
                raise WrongArgumentsException(f"The type of the file {attribute_argument.name} is not supported"
                                              f" we support only .txt and .stdf file types.")
        logger.debug('Finish validating input arguments.')


class WrongArgumentsException(Exception):
    def __init__(self, *arguments):
        if arguments:
            self.message = arguments[0]
        else:
            self.message = None

    def __repr__(self):
        return f'WrongArgumentException!!!  {self.message if self.message is not None else ""}'


def create_logger(file_name='ChipProductionLogger.log'):
    warnings.filterwarnings("ignore")
    logger_inner_var = logging.getLogger('ChipProduction')
    logger_inner_var.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(file_name)
    file_handler_formatter = logging.Formatter(f'%(asctime)s - %(levelname)s - %(funcName)s - %(message)s\n')

    file_handler.setFormatter(file_handler_formatter)
    logger_inner_var.addHandler(file_handler)
    console_handler = logging.StreamHandler()
    console_handler_formatter = logging.Formatter(f'%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_handler_formatter)
    console_handler.setLevel(logging.INFO)
    logger_inner_var.addHandler(console_handler)
    return logger_inner_var


def change_all_log_levels_for_debug():
    for logger_handler in logger.handlers:
        logger_handler.setLevel(logging.DEBUG)


def combine_result_with_rest(wafer_grid, rest, type_of_file):
    methods_dict = {'.txt': combine_text_file_with_result_grid, '.stdf': combine_text_file_with_result_grid}
    return methods_dict[type_of_file](wafer_grid, rest)


def combine_text_file_with_result_grid(wafer_grid, rest_as_template):
    final_text = rest_as_template.substitute({'wafer': wafer_grid})
    return final_text


def get_version():
    version_file_path = Path(__file__).parent / 'version.txt'
    with open(version_file_path, 'r') as version_file:
        version_file_content = version_file.read()
    current_version = version_file_content.strip()
    return current_version


version = get_version()


def get_input_mode():
    with open(Path(__file__).parent / 'main_config.json') as config_json_file:
        config = json.load(config_json_file)
        return config['input_mode_Dir_or_File']


def enable_long_paths(args):
    enable_long_path = "\\\\?\\"
    for attribute, attribute_value in vars(args).items():
        if 'path' in attribute:
            setattr(args, attribute, Path(enable_long_path + str(attribute_value)))


@Gooey(navigation='TABBED', show_success_modal=False, program_name='Die Cluster', program_description=f'Version '
                                                                                                      f'{version}')
def get_argument():
    logger.debug('Starting of getting the input arguments.')
    input_mode = get_input_mode()
    parser = GooeyParser()
    default_paths_dict = get_default_paths()
    input_kind = 'file' if input_mode == 'File' else 'directory'
    parser.add_argument(f'input_wafer_path', metavar=f'input {input_kind} path',
                        widget=f'{input_mode}Chooser',
                        default=default_paths_dict[f'input_{input_kind}'],
                        type=Path, help=f'path for input {input_kind}.')
    parser.add_argument('output_dir_path', metavar='output dir path', widget='DirChooser',
                        default=default_paths_dict['output'], type=Path,
                        help='path for output directory.')
    parser.add_argument('neighbors_file_path', metavar='neighbors file path',
                        default=default_paths_dict['neighbors_table'], widget='FileChooser', type=Path,
                        help='path for table file.')
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")

    args = parser.parse_args()
    enable_long_paths(args)
    logger.debug('Finish of getting the input arguments.')
    return args, input_mode


def get_default_paths():
    cwd = Path(__file__).parents[1]
    default_paths = {'input_file': cwd / 'example.txt', 'output': cwd / 'results',
                     'neighbors_table': cwd / 'resources/neighbors_table.json',
                     'input_directory': cwd / r'resources\Folder_of_stdfs'}
    return default_paths


def get_date():
    return datetime.today().strftime("%Y_%m_%d_%H_%M_%S")


def arguments_modification(args):
    input_filename = args.input_wafer_path.stem
    args.output_dir_path /= f'results_of_{input_filename}_Date_{get_date()}'
    Path.mkdir(args.output_dir_path)
    utils.wait_for_path_to_exists(args.output_dir_path, maximum_time_to_wait=10)


def get_excel_file(directory: Path):
    for inode in directory.iterdir():
        if inode.suffix == '.xlsx':
            return inode


def find_excel_paths(args):
    output_directory = args.output_dir_path
    excels_paths = []
    for inode in output_directory.iterdir():
        if not inode.is_dir():
            continue
        else:
            excels_path = get_excel_file(inode)
            if excels_path is None:
                continue
            excels_paths.append(excels_path)
    return excels_paths


def merge_to_one_sheet(one_line_files, output_directory):
    data_frame = pandas.DataFrame()
    for file in one_line_files:
        if str(file).endswith('.xlsx'):
            data_frame = data_frame.append(pandas.read_excel(file), ignore_index=True)
    data_frame.head()
    result_file_path = output_directory / f'summary_merged_{str(one_line_files[0].stem)}.xlsx'
    utils.drop_un_named_columns(data_frame)
    data_frame.to_excel(result_file_path)
    return result_file_path


def merge_sheets(excel_files, output_directory):
    result_excel_path = output_directory.parent / f'summary_merged_{str(output_directory.stem)}.xlsx'
    with pandas.ExcelWriter(result_excel_path, engine='openpyxl') as writer:
        for excel_file in excel_files:
            data_frame = pandas.read_excel(excel_file)
            utils.drop_un_named_columns(data_frame)
            data_frame.to_excel(writer, sheet_name=excel_file.stem)
        writer.save()
    return result_excel_path


def create_one_excel(excel_paths, output_directory):
    one_line_files = list(filter(lambda path: 'merge' not in str(path), excel_paths))
    multi_line_files = list(filter(lambda path: 'merge' in str(path), excel_paths))
    if len(one_line_files) != 0:
        path_1_sheet_file = merge_to_one_sheet(one_line_files, output_directory)
        multi_line_files.insert(0, path_1_sheet_file)
    if len(multi_line_files) != 0:
        merge_sheets(multi_line_files, output_directory)


def merge_excels(args):
    excel_paths = find_excel_paths(args)
    create_one_excel(excel_paths, args.output_dir_path)


def handle_directory(args):
    arguments_modification(args)
    input_directory: Path = args.input_wafer_path
    for file in input_directory.iterdir():
        args_copy = copy.deepcopy(args)
        args_copy.input_wafer_path = file
        if file.is_dir():
            handle_directory(args_copy)
            continue
        if file.suffix not in {'.stdf', '.txt'}:
            continue
        handle_file(args_copy)
    merge_excels(args)


def handle_file(args):
    arguments_validation(args)
    arguments_modification(args)
    chips_grid, rest_of_file = parse_file(args.input_wafer_path)
    processed_grid = apply_algorithm_on_grid(chips_grid, args.neighbors_file_path)
    input_file_name = args.input_wafer_path.stem
    HtmlViewer.plot_input_and_output(str(chips_grid), str(processed_grid), args.output_dir_path, input_file_name)
    file_type = args.input_wafer_path.suffix
    result_text = combine_result_with_rest(processed_grid, rest_of_file, file_type)
    save_result_as_text(result_text, args.output_dir_path, args.input_wafer_path)
    logger.info('Finish of Die Cluster algorithm.')


if __name__ == '__main__':
    logger = create_logger()
    logger.info(f'Starting Die Cluster algorithm version {version}.')
    args, input_mode = get_argument()
    if args.verbose:
        change_all_log_levels_for_debug()
    if input_mode == 'Dir':
        handle_directory(args)
    else:
        handle_file(args)
