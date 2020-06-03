import shutil
import subprocess
from pathlib import Path


def make_list_of_files_to_copy():
    files_to_copy = list()
    project_root_dir = current_file_path.parents[1]
    # add neighbors table path
    neighbors_table_filename = 'neighbors_table.json'
    neighbors_table_path = project_root_dir / f'resources/{neighbors_table_filename}'
    files_to_copy.append(neighbors_table_path)
    # Add readme path
    readme_file_name = 'README.md'
    readme_file_path = project_root_dir / readme_file_name
    files_to_copy.append(readme_file_path)
    # add version file path.
    version_file_name = 'version.txt'
    version_file_path = project_root_dir / version_file_name
    files_to_copy.append(version_file_path)
    return files_to_copy


def copy_files_into(copy_into_me, need_copy_paths):
    list(map(lambda path: shutil.copy(path, copy_into_me), need_copy_paths))


if __name__ == '__main__':
    command = ['pyinstaller', '--windowed', '--name', 'DieCluster', '--onefile', 'main.py']
    with subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE) as process:
        output, err = process.communicate()
        print(output)
        if len(err) > 0:
            print(f'{err} error')
    current_file_path = Path(__file__)
    paths_of_files_to_copy = make_list_of_files_to_copy()
    dir_to_compress = current_file_path.parent / 'dist'
    copy_files_into(dir_to_compress, paths_of_files_to_copy)
    zip_path = shutil.make_archive('DieCluster', 'zip', dir_to_compress)
    shutil.copy(zip_path, dir_to_compress)
