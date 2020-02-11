import os, sys, inspect
import pandas as pd
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir)
sys.path.insert(0, currentdir)
from pre_generate_data_manipulation import PreGenerateDataManipulation
from pre_generate_header_parsing import PreGenerateHeaderParsing


class PreGenerateController:
    """This class controls the methods in the pre_generate folder. It runs the data_manipulation routines, and then runs
     the header_parsing routines."""

    def __init__(self):
        self.target_file = r'T:\ANALYST WORK FILES\Peter\Rover\xml_data_files\data_7.xlsx'
        self.dm = PreGenerateDataManipulation(self.target_file)
        self.dm.data_manipulation_controller()
        self.hp = PreGenerateHeaderParsing(self.dm.samples_data_frame)
        self.hp.header_parsing_controller()

#       This is for development - allows me to see the full DataFrame when i print to the console, rather than a
#       truncated version. This is useful for debugging purposes and ensuring that methods are working as intended.
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', -1)
#       self.print_pre_generate_data_and_headers()

    def print_pre_generate_data_and_headers(self):
        print('RECOVERY')
        print(self.dm.best_recovery_qc_data_frame)
        print('BLANK')
        print(self.dm.min_value_blank_data_frame)
        print('HEADERS')
        for item in self.hp.header_contents_dictionary.values():
            print(item)
        print('SAMPLES')
        print(self.dm.samples_data_frame)


batch = PreGenerateController()
