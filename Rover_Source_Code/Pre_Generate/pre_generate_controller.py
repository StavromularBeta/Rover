import pandas as pd
import sys
import os, sys, inspect
from pre_generate_data_manipulation import PreGenerateDataManipulation
from pre_generate_header_parsing import PreGenerateHeaderParsing
# below 3 lines add the parent directory to the path, so that SQL_functions can be found.
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir)


class PreGenerateController:
    """This class controls the methods in the pre_generate folder. It runs the data_manipulation routines, and then runs
     the header_parsing routines."""

    def __init__(self):
        self.target_file = r'T:\ANALYST WORK FILES\Peter\Rover\xml_data_files\data_7.xlsx'
        self.dm = PreGenerateDataManipulation(self.target_file)
        self.dm.data_manipulation_controller()
        self.hp = PreGenerateHeaderParsing(self.dm.samples_data_frame)
        self.hp.header_parsing_controller()


batch = PreGenerateController()
