import csv
from itertools import product

import matplotlib.pyplot as plt
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def plot_input_and_output(input_grid, output_grid, output_dir, input_file_name):
    images_paths = [output_dir / f'image_{idx}.jpg' for idx in range(3)]
    make_and_save_table(images_paths[0], input_grid, title=f'Wafer before calling the program')
    make_and_save_table(images_paths[2], output_grid, title=f'Wafer after calling the program')
    short_summary = make_summary(input_grid, output_grid, output_dir, input_file_name)
    make_text_figure(short_summary, images_paths[1])
    result_image_path = output_dir / f'result_of_{input_file_name}.jpg'
    merge_images(images_paths, result_image_path)


def make_text_figure(text, image_path):
    img = Image.new('RGB', (500, 500), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 25)
    draw.text((0, 0), text, (0, 0, 0), font=font)
    img.save(image_path)


def merge_images(images_paths, path_for_result):
    images = [Image.open(x) for x in images_paths]
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]

    new_im.save(path_for_result)


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


def make_summary(input_grid, output_grid, output_dir, input_file_name):
    number_of_fail_chips = input_grid.count('X')
    number_of_pass_chips = input_grid.count('1')
    number_of_chips = number_of_fail_chips + number_of_pass_chips
    failed_by_prediction = output_grid.count('Y')
    pass_at_the_end = output_grid.count('1')
    fail_at_the_end = output_grid.count('X') + output_grid.count('Y')
    difference_coordinates = find_difference_coordinates(input_grid, output_grid)
    difference_coordinates_str = " ".join(difference_coordinates)
    short_summary = f'The wafer contains {number_of_chips} chips.\n' \
                    f'From them {number_of_fail_chips} was failed\n' \
                    f'And {number_of_pass_chips} was pass.\n' \
                    f'We mark as fails some more {failed_by_prediction} chips.\n' \
                    f'Total {fail_at_the_end} was failed.\n' \
                    f'And {pass_at_the_end} was passed.\n'
    summary_file_path = output_dir / f'{input_file_name}_summary.csv'
    with open(summary_file_path, mode='w', newline='') as csv_file:
        fieldnames = ['File name', 'Total chips', 'Initially failed', 'Initially passed', 'Failed by prediction',
                      'Total failed',
                      'Total passed', 'Difference coordinates']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        row_values = [input_file_name, number_of_chips, number_of_fail_chips, number_of_pass_chips,
                      failed_by_prediction, fail_at_the_end, pass_at_the_end, difference_coordinates_str]
        rows_dict = {header: value for header, value in zip(fieldnames, row_values)}
        writer.writerow(rows_dict)

    return short_summary


def make_grid_of_chars(grid_text):
    rows_text = grid_text.split('\n')
    return [[char for char in row] for row in rows_text]


def make_and_save_table(figure_path, grid_text, title, additional_text=''):
    cells_text = make_grid_of_chars(grid_text)
    colors = [[get_color(char) for char in row] for row in cells_text]
    figure, ax = plt.subplots()
    figure.text(0.05, 0.95, title, size=24)
    ax.axis('tight')
    ax.axis('off')
    ax.text(100, 100, additional_text)
    ax.table(cellText=cells_text, cellColours=colors, loc='center')
    plt.savefig(figure_path)


colors_dict = {'.': "w", "1": "g", "X": "r", "Y": "y"}


def get_color(char):
    return colors_dict[char]
