import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path', type=str, help='path for input file.')
    parser.add_argument('output_path', type=str, help='path for input file.')
    parser.add_argument('neighbors_path', type=str, help='path for table file.')
    args = parser.parse_args()
