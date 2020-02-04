import pandas as pd


class PreGenerateHeaderParsing:
    """This file finds the correct header information for the samples in the batch being processed and parses them."""

    def __init__(self, samples_data_frame):
        self.samples_data_frame = samples_data_frame

#       This is for development - allows me to see the full DataFrame when i print to the console, rather than a
#       truncated version. This is useful for debugging purposes and ensuring that methods are working as intended.
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', -1)

    def header_parsing_controller(self):
        self.test_function()

    def test_function(self):
        print(self.samples_data_frame)
