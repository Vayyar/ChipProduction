from itertools import product
from pathlib import Path
from string import Template

import matplotlib.pyplot as plt
import pandas
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def plot_input_and_output(input_grid, output_grid, output_dir, input_file_name):
    images_paths = [output_dir / f'image_{idx}.jpg' for idx in range(2)]
    make_and_save_table(images_paths[0], input_grid)
    make_and_save_table(images_paths[1], output_grid)
    short_summary = make_summary(input_grid, output_grid, output_dir, input_file_name)
    result_file_path = output_dir / f'result_of_{input_file_name}.html'
    make_final_page(images_paths, result_file_path, short_summary)


def make_text_figure(text, image_path):
    img = Image.new('RGB', (500, 500), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 25)
    draw.text((0, 0), text, (0, 0, 0), font=font)
    img.save(image_path)


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
    difference_coordinates_str = ":".join(difference_coordinates)
    short_summary = f'Original: {number_of_chips} chips.<br>' \
                    f'Pass/ fail: {number_of_pass_chips} / {number_of_fail_chips}.<br>' \
                    f'After Process:<br>' \
                    f'Pass/ fail: {pass_at_the_end} / {fail_at_the_end} ({failed_by_prediction} new fails).<br>'

    fieldnames = ['File_name', 'Total_chips', 'Initially_failed', 'Initially_passed', 'Failed_by_prediction',
                  'Total_failed',
                  'Total_passed', 'Difference_coordinates']
    row_values = [input_file_name, number_of_chips, number_of_fail_chips, number_of_pass_chips,
                  failed_by_prediction, fail_at_the_end, pass_at_the_end, difference_coordinates_str]
    data_frame_dict = {field_name: [row_value] for field_name, row_value in zip(fieldnames, row_values)}
    data_frame = pandas.DataFrame.from_dict(data_frame_dict)
    summary_file_path = output_dir / f'{input_file_name}_summary.xlsx'
    with pandas.ExcelWriter(summary_file_path) as writer:
        data_frame.to_excel(writer, sheet_name=input_file_name)
    return short_summary


def make_grid_of_chars(grid_text):
    rows_text = grid_text.split('\n')
    return [[char for char in row] for row in rows_text]


def add_demo_axis(table):
    table_with_y_axis = [list(range(0, len(table[0])))] + table
    table_with_demo_axis = [[idx] + row for row, idx in
                            zip(table_with_y_axis, list(range(-1, len(table_with_y_axis))))]
    table_with_demo_axis[0][0] = '\\ '  # Origin
    return table_with_demo_axis


def make_and_save_table(figure_path, grid_text):
    cells_text = make_grid_of_chars(grid_text)
    cells_text_with_demo_axis = add_demo_axis(cells_text)
    colors = [[get_color(char) for char in row] for row in cells_text_with_demo_axis]
    figure, ax = plt.subplots()
    ax.axis("off")
    ax.table(cellText=cells_text_with_demo_axis, cellColours=colors, loc='center')
    plt.savefig(figure_path, bbox_inches="tight")


def make_final_page(images_paths, path_for_result, short_summary):
    with open('figures_union_template.html', 'r') as skeleton:
        skeleton_page = skeleton.read()
    page_template = Template(skeleton_page)
    relative_images_path = [Path('.') / Path(image_path).name for image_path in images_paths]
    html_page = page_template.substitute(
        {'wafer_before': relative_images_path[0], 'wafer_summary': short_summary,
         'wafer_after': relative_images_path[1]})
    with open(path_for_result, 'w') as final_page:
        final_page.write(html_page)


colors_dict = {'.': "w", "1": "g", "X": "r", "Y": "y"}


def get_color(char):
    return colors_dict[char] if char in colors_dict else "pink"
