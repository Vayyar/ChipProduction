import shutil
import subprocess
import sys
import traceback
from pathlib import Path


def make_list_of_files_to_copy(cwd):
    files_to_copy = list()
    project_root_dir = cwd.parent
    # add neighbors table path
    neighbors_table_filename = 'neighbors_table.json'
    neighbors_table_path = project_root_dir / 'resources' / f'{neighbors_table_filename}'
    files_to_copy.append(neighbors_table_path)
    # Add readme path
    readme_file_name = 'README.md'
    readme_file_path = project_root_dir / readme_file_name
    files_to_copy.append(readme_file_path)
    # add version file path.
    version_file_name = 'version.txt'
    version_file_path = cwd / version_file_name
    files_to_copy.append(version_file_path)
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


def copy_all_files_into_exe_dir(cwd):
    paths_of_files_to_copy = make_list_of_files_to_copy(cwd)
    directory_to_compress = cwd / 'dist'
    copy_files_into(directory_to_compress, paths_of_files_to_copy)
    return directory_to_compress


def make_archive(cwd, directory_to_compress):
    print(cwd)
    print(directory_to_compress)
    shutil.make_archive(cwd / 'DieCluster', 'zip', directory_to_compress)


if __name__ == '__main__':
    create_exe_file()
    cwd = Path(__file__).parent
    dir_to_compress = copy_all_files_into_exe_dir(cwd)
    make_archive(cwd, dir_to_compress)
