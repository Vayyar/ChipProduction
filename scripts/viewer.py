from itertools import product

import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def plot_input_and_output(input_grid, output_grid, output_dir, input_file_name):
    images_paths = [output_dir / f'image_{idx}.jpg' for idx in range(3)]
    make_and_save_table(images_paths[0], input_grid, title=f'Wafer before calling the program')
    make_and_save_table(images_paths[2], output_grid, title=f'Wafer after calling the program')
    short_summary = make_summary_file(input_grid, output_grid, output_dir, input_file_name)
    make_text_figure(short_summary, images_paths[1])
    result_image_path = output_dir / f'result_of_{input_file_name}.jpg'
    merge_images(images_paths, result_image_path)


def find_difference_coordinates(input_grid, output_grid):
    grid_of_chars_input = make_grid_of_chars(input_grid)
    grid_of_chars_output = make_grid_of_chars(output_grid)
    number_of_rows = len(grid_of_chars_input)
    number_of_columns = len(grid_of_chars_input[0])
    coordinates_of_difference_list = list()
    for x_coordinate, y_coordinate in product(range(number_of_rows), range(number_of_columns)):
        input_cell = grid_of_chars_input[x_coordinate][y_coordinate]
        output_cell = grid_of_chars_output[x_coordinate][y_coordinate]
        if input_cell != output_cell:
            coordinates_of_difference_list.append(f'({x_coordinate},{y_coordinate})')
    return coordinates_of_difference_list


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


def make_grid_of_chars(grid_text):
    rows_text = grid_text.split('\n')
    return [[char for char in row] for row in rows_text]


def make_and_save_table(grid_text, pdf, title, additional_text=''):
    cells_text = make_grid_of_chars(grid_text)
    colors = [[get_color(char) for char in row] for row in cells_text]
    figure, ax = plt.subplots()
    figure.text(0.05, 0.95, title, size=24)
    ax.axis('tight')
    ax.axis('off')
    ax.text(100, 100, additional_text)
    ax.table(cellText=cells_text, cellColours=colors, loc='center')
    pdf.savefig(figure)


def make_text_figure(pdf, text):
    figure, ax = plt.subplots()
    figure.text(.1, .1, text, size=20)
    ax.axis('tight')
    ax.axis('off')
    pdf.savefig(figure)


colors_dict = {'.': "w", "1": "g", "X": "r", "Y": "y"}


def get_color(char):
    return colors_dict[char]
