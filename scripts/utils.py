import time
from pathlib import Path


class PathDoesntExistsException(Exception):
    pass


def wait_for_path_to_exists(path, maximum_time_to_wait=2):
    counter = 0
    time_to_wait = 0.01
    while not Path.exists(path) and counter < maximum_time_to_wait:
        time.sleep(time_to_wait)
        counter += time_to_wait
    if counter >= maximum_time_to_wait:
        raise PathDoesntExistsException()


def get_inner_dir_path(directory_path: Path):
    for file in directory_path.iterdir():
        if file.is_dir():
            return file


def drop_un_named_columns(data_frame):
    un_named_columns = data_frame.columns.str.contains('unnamed', case=False)
    data_frame.drop(data_frame.columns[un_named_columns], axis=1, inplace=True)  # delete first indexing column


def short_the_path(path):
    path_as_str = str(path)
    path_as_str_reversed = path_as_str[::-1]
    if '..' not in path_as_str_reversed:
        return path
    first_backward_index = path_as_str_reversed.index('..')
    if first_backward_index >= len(path_as_str_reversed) - 2:
        return path
    last_index_to_remove = path_as_str_reversed[first_backward_index + 3:].index('\\') + first_backward_index + 3
    path_as_str_reversed_short = path_as_str_reversed[0:first_backward_index] + path_as_str_reversed[
                                                                                last_index_to_remove + 1:]
    short_path_as_str = path_as_str_reversed_short[::-1]
    short_path = Path(short_path_as_str)
    return short_the_path(short_path)
