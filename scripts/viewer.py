import matplotlib.pyplot as plt


def plot_input_and_output(input_grid, output_grid):
    make_table(input_grid)
    make_table(output_grid)
    plt.show()


def make_table(grid_text):
    rows_text = grid_text.split('\n')
    cells_text = [[char for char in row] for row in rows_text]
    colors = [[get_color(char) for char in row] for row in cells_text]
    fig, ax = plt.subplots()
    ax.axis('tight')
    ax.axis('off')
    ax.table(cellText=cells_text, cellColours=colors, loc='center')


colors_dict = {'.': "w", "1": "g", "X": "r", "Y": "y"}


def get_color(char):
    return colors_dict[char]
