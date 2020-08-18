import subprocess
from pathlib import Path

from gooey import GooeyParser, Gooey


@Gooey(program_name='Mode chooser', navigation='TABBED', show_success_modal=False)
def mode_chooser():
    parser = GooeyParser()
    parser.add_argument("-d", '--directory', help='I want to process entire directory', action='store_true')
    arguments = parser.parse_args()
    return 'Dir' if arguments.directory else 'File'


def runner():
    input_mode = mode_chooser()
    main_path = Path(__file__).parent / 'main.py'
    command = ['python', f'{main_path}']
    subprocess.run(command, stdout=subprocess.PIPE,
                   input=input_mode, encoding='ascii')


if __name__ == '__main__':
    runner()
