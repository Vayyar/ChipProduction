import subprocess
from pathlib import Path
from shutil import copyfile


def copy_neighbors_table_to_exe_dir():
    current_file_path = Path(__file__)
    neighbors_table_filename = 'neighbors_table.json'
    exe_directory_path = current_file_path.parent / 'dist'
    neighbors_table_path = current_file_path.parents[1] / f'resources/{neighbors_table_filename}'
    neighbors_table_destination = exe_directory_path / neighbors_table_filename
    copyfile(neighbors_table_path, neighbors_table_destination)


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
