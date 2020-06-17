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


def make_list_of_files_to_copy(config):
    files_to_copy = [config["neighbors_table_file_path"], config["readme_file_path"],
                     config["version_file_path"], config["exe_file_path"]]
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


if __name__ == '__main__':
    logger = main.create_logger(file_name='Packaging logger')
    config_dict = make_config()
    validate_config(config_dict)
    create_exe_file()
    dir_to_compress = copy_all_files_into_one_dir(config_dict)
    make_archive(config_dict['artifacts_package_file_path'], dir_to_compress)
