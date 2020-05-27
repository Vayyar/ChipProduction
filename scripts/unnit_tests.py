import subprocess
import unittest
from pathlib import Path

from scripts import skeleton


class UnitTests(unittest.TestCase):
    def test_consistency(self):
        # read last .stdf running result
        # TODO change to Path(__file__)
        stdf_file_path = Path('../resources/N6W014_N6W014-19E5_WS_CP1_-40_20200313_110305.stdf')
        results_path = Path('../unit_tests')
        neighbors_file_path = Path('../resources/neighbors_table.json')
        command = ['python', f'{Path(__file__).parent / "skeleton.py"}', f'{stdf_file_path}', f'{results_path}',
                   f'{neighbors_file_path}']
        with subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE) as process:
            process.wait()
            # when merge remove comment from this section.
            # and make it a method.
            # output, err = process.communicate()
            # if len(err) > 0:
            #   logger.error(err)
        result_file_path = skeleton.get_output_file_path(results_path, stdf_file_path)
        with open(result_file_path, 'r') as result_file:
            result_wafer = result_file.read()
        # restore the original wafer
        test_wafer = result_wafer.replace('Y', '1')
        # make new .txt test file from the original wafer
        test_file_path = result_file_path.parents[1] / 'resources/test_wafer.txt'
        with open(test_file_path, 'w') as test_file:
            test_file.write(test_wafer)
        # run this python file on the new .txt file
        output_dir_path = Path(__file__).parents[1] / 'results'
        command = ['python', f'{__file__}', f'{test_file_path}', f'{output_dir_path}', f'{neighbors_file_path}']
        with subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE) as process:
            process.wait()
            # when merge remove comment from this section.
            # and make it a method
            # output, err = process.communicate()
            # if len(err) > 0:
            #   logger.error(err)
            #logger.error(err)
        output_file_path = skeleton.get_output_file_path(output_dir_path, test_file_path)
        with open(output_file_path, 'r') as result_from_text_file:
            result_from_text_file_wafer_str = result_from_text_file.read()
        # compare them.
        self.assertEqual(result_from_text_file_wafer_str, result_wafer)
