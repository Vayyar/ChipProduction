from itertools import product

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def plot_input_and_output(input_grid, output_grid, output_dir, input_file_name):
    with PdfPages(output_dir / f'{input_file_name}_summary.pdf') as pdf:
        make_summary_file(input_grid, output_grid, output_dir, input_file_name)
        make_and_save_table(input_grid, pdf, title=f'{short_summary} Wafer before calling the program')
        make_and_save_table(output_grid, pdf, title=f'Wafer after calling the program')


def make_table(grid_text):

def make_summary_file(input_grid, output_grid, output_dir, input_file_name):
    number_of_fail_chips = input_grid.count('X')
    number_of_pass_chips = input_grid.count('1')
    number_of_chips = number_of_fail_chips + number_of_pass_chips
    failed_by_prediction = output_grid.count('Y')
    pass_at_the_end = output_grid.count('1')
    fail_at_the_end = output_grid.count('X') + output_grid.count('Y')
    difference_coordinates = find_difference_coordinates(input_grid, output_grid)
    short_summary = f'The wafer contains {number_of_chips} chips.\n' \
                    f'From them {number_of_fail_chips} was failed\n' \
                    f'And {number_of_pass_chips} was pass.\n' \
                    f'We mark as fails some more {failed_by_prediction} chips.\n' \
                    f'Total {fail_at_the_end} was failed.\n' \
                    f'And {pass_at_the_end} was passed.\n'
    summary = short_summary + \
              f'The coordinates of chips we mark as failed even they was pass initially are:' \
              f' {",".join(difference_coordinates)}'
    summary_text_file_path = output_dir / f'{input_file_name}_summary.txt'
    with open(summary_text_file_path, 'w') as summary_text_file:
        summary_text_file.write(summary)
    return short_summary
    rows_text = grid_text.split('\n')
    cells_text = [[char for char in row] for row in rows_text]

def make_and_save_table(grid_text, pdf, title):
    cells_text = make_grid_of_chars(grid_text)
    colors = [[get_color(char) for char in row] for row in cells_text]
    figure, ax = plt.subplots()
    figure.text(0.05, 0.95, title, size=24)
    ax.axis('tight')
    ax.axis('off')
    ax.table(cellText=cells_text, cellColours=colors, loc='center')
    pdf.savefig(figure)


colors_dict = {'.': "w", "1": "g", "X": "r", "Y": "y"}


def get_color(char):
    return colors_dict[char]
