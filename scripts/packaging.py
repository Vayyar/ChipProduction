import json
import shutil
import subprocess
import sys
import traceback
from pathlib import Path


def make_config():
    cwd = Path(__file__).parent
    config_path = f'{cwd}/packaging_config.json'
    with open(config_path) as config_json_file:
        config = json.load(config_json_file)
    return config


def make_list_of_files_to_copy(config):
    files_to_copy = [config["neighbors_table_path"], config["readme_file_path"],
                     config["version_file_path"], config["exe_file_path"]]
    return files_to_copy


def copy_files_into(copy_into_me, need_copy_paths):
    list(map(lambda path: shutil.copy(path, copy_into_me), need_copy_paths))


def create_exe_file():
    command = ['pyinstaller', '--windowed', '--name', 'DieCluster', '--onefile', 'main.py']
    try:
        with subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE) as process:
            output, err = process.communicate()
            print(output)
            if len(err) > 0:
                print(f'{err} error')
    except Exception:
        line_length = 60
        line = '-' * line_length
        print("Exception in creating .exe file:")
        print(line)
        traceback.print_exc(file=sys.stdout)
        print(line)


def copy_all_files_into_exe_dir(config):
    paths_of_files_to_copy = make_list_of_files_to_copy(config)
    directory_to_compress = Path(config['.temp_path'])
    if not Path.exists(directory_to_compress):
        Path.mkdir(directory_to_compress)
    copy_files_into(directory_to_compress, paths_of_files_to_copy)
    return directory_to_compress


def make_archive(artifact_path, directory_to_compress):
    shutil.make_archive(artifact_path, 'zip', directory_to_compress)


if __name__ == '__main__':
    config_dict = make_config()
    create_exe_file()
    dir_to_compress = copy_all_files_into_exe_dir(config_dict)
    make_archive(config_dict['.artifacts_package_path'], dir_to_compress)
