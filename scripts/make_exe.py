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
    copy_neighbors_table_to_exe_dir()
