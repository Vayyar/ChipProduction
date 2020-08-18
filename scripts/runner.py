from gooey import GooeyParser, Gooey

import algorithm


@Gooey(program_name='Mode chooser')
def mode_chooser():
    parser = GooeyParser()
    parser.add_argument("-d", '--directory', help='I want to process entire directory', action='store_true')
    arguments = parser.parse_args()
    return 'Dir' if arguments.directory else 'File'


if __name__ == '__main__':
    input_mode = mode_chooser()
    algorithm.main('Dir')
