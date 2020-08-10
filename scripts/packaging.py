import json
import shutil
import subprocess
import sys
import traceback
from pathlib import Path

import main


def make_config():
    """
    The json file should contains
    "temp_dir_path": "relative path for Byproducts",
    "artifacts_package_file_path": "relative path for artifacts",
    "neighbors_table_file_path":  "relative path for neighbors json file",
    "readme_file_path": "relative path for Readme file",
    "version_file_path": "relative path for version.txt",
    "exe_file_path": "where the exe initially will be created by packaging"
    """
    logger.debug('Starting load config into memory.')
    cwd = Path(__file__).parent
    config_path = f'{cwd}/packaging_config.json'
    with open(config_path) as config_json_file:
        config = json.load(config_json_file)
    logger.debug('End load config into memory.')
    return config


def validate_config(config):
    logger.debug('Start validate config arguments.')
    for key in config:
        path = Path(config[key])
        if key in {'temp_dir_path', 'artifacts_package_file_path', 'exe_file_path', 'requirements_file_path'}:
            continue
        if 'path' in key:
            if not Path.exists(path):
                raise Exception(f"The path {path} under name {key} in config doesn't exist")
        if 'file' in key and not Path.is_file(path):
            raise Exception(f"{path} isn't a file")
        if ('dir' in key or 'directory' in key) and not Path.is_dir(path):
            raise Exception(f"{path} isn't a dir")
    logger.debug('End validate config arguments.')


def make_list_of_files_to_copy(config):
    files_to_copy = [config["neighbors_table_file_path"], config["readme_file_path"],
                     config["version_file_path"], config["exe_file_path"], '.\\requirements.txt']
    return files_to_copy


def copy_files_into(copy_into_me, need_copy_paths):
    list(map(lambda path: shutil.copy(path, copy_into_me), need_copy_paths))


def create_exe_file():
    logger.info('Starting create 1 exe from the project')
    command = ['pyinstaller', '--windowed', '--name', 'DieCluster', '--onefile', 'main.py']
    try:
        with subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE) as process:
            output, err = process.communicate()
            print(output)
            if len(err) > 0:
                print(f'{err} error')
        logger.info('Ending create 1 exe from the project.')
    except Exception:
        logger.error('Failed creating 1 exe from the project.')
        line_length = 60
        line = '-' * line_length
        print("Exception in creating .exe file:")
        print(line)
        traceback.print_exc(file=sys.stdout)
        print(line)


def copy_all_files_into_one_dir(config):
    logger.info('Starting copy all files into 1 dir.')
    paths_of_files_to_copy = make_list_of_files_to_copy(config)
    directory_to_compress = Path(config['temp_dir_path'])
    if not Path.exists(directory_to_compress):
        Path.mkdir(directory_to_compress, parents=True)
    copy_files_into(directory_to_compress, paths_of_files_to_copy)
    logger.info('End copy all files into 1 dir.')
    return directory_to_compress


def make_archive(artifact_path, directory_to_compress):
    logger.info('Starting make zip from all files.')
    shutil.make_archive(artifact_path, 'zip', directory_to_compress)
    logger.info('End make zip from all files.')


def get_version(version_file_path):
    with open(version_file_path, 'r') as version_file:
        version = version_file.read()
    version_striped = version.strip()
    return version_striped


def is_invalid_value(value, options):
    return value not in options


class InvalidInputException(Exception):
    pass


def handle_invalid_answer(answer):
    logger.error(f'Your answer ({answer}) is invalid.')
    raise InvalidInputException()


def translate_place_from_str_to_int(place_to_update_str):
    translation_dict = {'h': 0, 'm': 1, 'l': 2}
    return translation_dict[place_to_update_str]


def calculate_new_version(current_version, place_to_update_str):
    version_list = current_version.split('.')
    place_to_update_int = translate_place_from_str_to_int(place_to_update_str)
    version_list_updated = version_list[0: place_to_update_int] + [str(int(version_list[place_to_update_int]) + 1)] \
                           + ['0' for _ in range(place_to_update_int + 1, 3)]
    version_list_updated_of_str = [str(element) for element in version_list_updated]
    version_as_str = '.'.join(version_list_updated_of_str)
    return version_as_str


def update_version(version_file_path, current_version, place_to_update_str):
    new_version = calculate_new_version(current_version, place_to_update_str)
    logger.info(f'The new version is {new_version}')
    with open(version_file_path, 'w') as version_file:
        version_file.write(new_version)


def input_validation(answer, options):
    if is_invalid_value(answer, options):
        handle_invalid_answer(answer)


def ask_for_version(config):
    version_file_path = config["version_file_path"]
    current_version = get_version(version_file_path)
    logger.info(f'The current version is {current_version} are you want to update version? (y \\ n).')
    is_want_to_update = input()
    input_validation(is_want_to_update, options={'y', 'n'})
    if is_want_to_update == 'n':
        return
    logger.info(f'Which of the 3 are you want to update (h/m/l)?.')
    place_to_update = input()
    input_validation(place_to_update, options={'h', 'm', 'l'})
    update_version(version_file_path, current_version, place_to_update)


def make_requirements_file():
    logger.info('Start creating requirements.txt file.')
    cwd = Path(__file__).parent
    command = ['pipreqs', str(cwd)]
    subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)
    logger.info('Finish creating requirements.txt file.')


if __name__ == '__main__':
    logger = main.create_logger(file_name='Packaging logger')
    config_dict = make_config()
    validate_config(config_dict)
    ask_for_version(config_dict)
    make_requirements_file()
    create_exe_file()
    dir_to_compress = copy_all_files_into_one_dir(config_dict)
    make_archive(config_dict['artifacts_package_file_path'], dir_to_compress)
