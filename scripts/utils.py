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
