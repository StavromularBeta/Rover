import pandas as pd
import os, sys, inspect
import xlsxwriter
from math import floor, log10, isnan
# below 3 lines add the parent directory to the path, so that SQL_functions can be found.
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir)


class MushPreGenerateDataManipulation:
    """This file controls the data manipulation processes occurring prior to generating latex files.
     Raw data -> Processed data."""

    def __init__(self, data_xml_file):
        """The main init function.

        1. data_xml_file = the raw xml data file produced by TargetLynx. This must be manually placed in the datafiles
        2. folder to be read by Rover. The name of it is passed to init.
        3. raw_xml_data_frame = the first DataFrame produced from the xml file. At this point, the data is not
        manipulated in any way.
        4. percentage_data_frame = changes: analytical concentration converted to percentage concentration.
        5. blank_data_frame = changes: only information from blanks.
        6. qc_data_frame = changes: only information from standards.
        7. samples_and_dilutions_data_frame = changes: only information from samples and their dilutions.
        8. best_recovery_qc_data_frame = changes: all the standard data has been analyzed, and the best recoveries for
        each analyte have been selected for the new data frame, which consists of one samples' worth of rows.
        9. min_value_blank_data_frame = changes: one axis data frame with the minimum value of each analyte from the
        blank_data_frame.
        10. sample_dilutions_data_frame = changes: only information from dilutions
        11. samples_data_frame = changes: samples with out of range values switched out with the appropriate dil."""

        self.data_xml_file = data_xml_file
        self.raw_xml_data_frame = pd.DataFrame()
        self.unique_sample_id_list = []
        # Mushrooms
        self.trimmed_data_frame = pd.DataFrame()
        self.samples_data_frame = pd.DataFrame()

#       Range check dictionary - these are the high and low values for our curve. If area is smaller than the first
#       number, or larger than the second one, it is out of range. If that happens, the value needs to be swapped with
#       the corresponding value from the dilution.
        self.range_checker_dictionary = {1: [3065, 44880, 'ibuprofen'],
                                         2: [160, 170000, 'CBDV'],
                                         3: [150, 10000, 'CBDVA'],
                                         4: [259, 40000, 'THCV'],
                                         5: [25, 5000, 'CBGVA'],  # copying THCV for now
                                         6: [200, 200995, 'CBD'],
                                         7: [200, 100000, 'CBG'],
                                         8: [100, 50000, 'CBDA'],
                                         9: [100, 68050, 'CBN'],
                                         10: [100, 50000, 'CBGA'],
                                         11: [100, 15440, 'THCVA'],
                                         12: [200, 200000, 'd9_THC'],
                                         13: [200, 200000, 'd8_THC'],
                                         14: [250, 25000, 'CBL'],
                                         15: [100, 28000, 'CBC'],
                                         16: [100, 50000, 'CBNA'],
                                         17: [100, 200000, 'THCA'],
                                         18: [50, 5000, 'CBLA'],
                                         19: [50, 6000, 'CBCA']}

#       This DataFrame is so we can join the calibration curve data to the samples DataFrame in order to flag the
#       samples for being over the curve.
        self.over_curve_data = {'id17': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
                                'max_value': [44880, 170000, 10000, 40000, 5000, 200995, 100000, 50000, 68050,
                                              50000, 15440, 200000, 200000, 25000, 28000, 50000, 200000,
                                              5000, 6000]}
        self.over_curve_data_frame = pd.DataFrame(self.over_curve_data, columns=['id17', 'max_value'])

#       This is for development - allows me to see the full DataFrame when i print to the console, rather than a
#       truncated version. This is useful for debugging purposes and ensuring that methods are working as intended.
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', -1)

    def data_manipulation_controller(self):
        """The main controller function. To run the methods that make up this class, this function is called."""
        self.collect_data_from_xml_file()
        self.remove_unwanted_analytes_from_data_file()
        self.create_list_of_unique_samples()
        self.limit_sig_figs_in_dataframes()
        print(self.trimmed_data_frame)

    def collect_data_from_xml_file(self):
        """Reads the xml data, saves it to a Pandas DataFrame.

        1. id15: the id in the batch. First standard/blank/sample is 1, second is 2, etc.
        2. sampleid: the sample number, or the name of the standard/blank.
        3. id17: the id of the particular analyte for the row.
        4. name20: the name of the particular analyte for the row.
        5. initamount: the mass, in grams, of the sample.
        6. area: the peak area of the analyte from the chromatogram.
        7. analconc: the concentration calculated by TargetLynx. This will improve after analyst peak integration.
        8. percrecovery: the percentage recovery of ibuprofen.
        9. type: Blank, QC, or analyte.

        there is a try/except statement that will catch an incorrect path/filename."""

        try:
            raw_xml_data = pd.read_excel(self.data_xml_file,)
        except FileNotFoundError:
            print("ERROR: XML FILE NOT FOUND")
            print(str(self.data_xml_file) + " cannot be found. Either the path to the xml_data_files folder is " +
                  "wrong, or the file doesn't exist.")
            print("SCRIPT EXITING.")
            sys.exit()
        self.raw_xml_data_frame = pd.DataFrame(raw_xml_data,
                                               columns=['id15',
                                                        'sampleid',
                                                        'id17',
                                                        'name20',
                                                        'initamount',
                                                        'area',
                                                        'analconc',
                                                        'percrecovery',
                                                        'type']
                                               )

    def remove_unwanted_analytes_from_data_file(self):
        """Selects only the id17's that correspond to Psilocin, Psilocybin, and Baeocystin. Other analytes
         unnecessary."""
        self.trimmed_data_frame = self.raw_xml_data_frame[self.raw_xml_data_frame['id17'].isin([1.0, 2.0, 3.0])]
        search_for = ["CS4", "161", "162"]
        self.trimmed_data_frame = self.trimmed_data_frame[
            self.raw_xml_data_frame['sampleid'].str.contains('|'.join(search_for), na=False)]
        self.samples_data_frame = self.trimmed_data_frame[self.trimmed_data_frame.type != "QC"]

    def create_list_of_unique_samples(self):
        """This is a simple one line function that generates a list of unique samples in the samples_data_frame, for use
        at the GUI level."""
        self.unique_sample_id_list = self.samples_data_frame.sampleid.unique()

    def limit_sig_figs_in_dataframes(self):
        """This function rounds the values in the percentage recovery and percentage concentration columns of the
        standard recovery data frame and the samples data frame, respectively. """
        sig_figs = 4
        self.samples_data_frame['analconc'] = self.samples_data_frame.analconc.apply(
            lambda x: round(x, sig_figs - int(floor(log10(abs(x))))) if (1 > x > 0) else int(round(x)))
        self.samples_data_frame['percrecovery'] = self.samples_data_frame.percrecovery.apply(
            lambda x: round(x, sig_figs - int(floor(log10(abs(x))))) if (1 > x > 0) else int(round(x)))


