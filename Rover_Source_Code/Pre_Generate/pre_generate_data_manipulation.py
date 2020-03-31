import pandas as pd
import os, sys, inspect
from math import floor, log10
# below 3 lines add the parent directory to the path, so that SQL_functions can be found.
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir)


class PreGenerateDataManipulation:
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
        self.percentage_data_frame = pd.DataFrame()
        self.blank_data_frame = pd.DataFrame()
        self.qc_data_frame = pd.DataFrame()
        self.samples_and_dilutions_data_frame = pd.DataFrame()
        self.best_recovery_qc_data_frame = pd.DataFrame()
        self.min_value_blank_data_frame = pd.DataFrame()
        self.sample_dilutions_data_frame = pd.DataFrame()
        self.samples_data_frame = pd.DataFrame()
        self.condensed_samples_data_frame = pd.DataFrame()
        self.samples_list_data_frame = pd.DataFrame()
        self.unique_sample_id_list = []

#       Range check dictionary - these are the high and low values for our curve. If area is smaller than the first
#       number, or larger than the second one, it is out of range. If that happens, the value needs to be swapped with
#       the corresponding value from the dilution.
        self.range_checker_dictionary = {1: [3065, 44880, 'ibuprofen'],
                                         2: [127, 94400, 'CBDV'],
                                         3: [64, 16896, 'CBDVA'],
                                         4: [259, 103785, 'THCV'],
                                         5: [259, 103785, 'CBGVA'],  # copying THCV for now
                                         6: [100, 160995, 'CBD'],
                                         7: [117, 80956, 'CBG'],
                                         8: [100, 170668, 'CBDA'],
                                         9: [100, 27050, 'CBN'],
                                         10: [100, 22440, 'CBGA'],
                                         11: [100, 15440, 'THCVA'],
                                         12: [133.9, 203125, 'd9_THC'],
                                         13: [163, 84959, 'd8_THC'],
                                         14: [86.4, 82725, 'CBL'],
                                         15: [100, 14365, 'CBC'],
                                         16: [131, 24365, 'CBNA'],
                                         17: [100, 170391, 'THCA'],
                                         18: [110, 20391, 'CBLA'],
                                         19: [100, 12482, 'CBCA']}

#       This DataFrame is so we can join the calibration curve data to the samples DataFrame in order to flag the
#       samples for being over the curve.
        self.over_curve_data = {'id17': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
                                'max_value': [44880, 94400, 16896, 103785, 103785, 160995, 80956, 170668,
                                              27050, 22440, 15440, 203125, 84959, 82725, 14365, 24365,
                                              170391, 20391, 12482]}
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
        self.convert_analytical_concentration_to_percentage_concentration()
        self.split_into_blank_qc_and_sample_data_frame()
        self.combine_qc_into_one_data_set_with_highest_recovery_values()
        self.combine_blanks_into_one_data_set_with_lowest_percentage_concentration_values()
        self.join_over_curve_df_to_samples_df()
        self.assign_high_flag_to_sample_data()
        self.split_samples_data_frame_into_dilutions_and_samples()
        self.swap_out_out_of_range_values()
        self.create_list_of_unique_samples()
        self.create_condensed_sample_list_data_frame_for_gui()
        self.limit_sig_figs_in_dataframes()

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

    def convert_analytical_concentration_to_percentage_concentration(self):
        """converts the analytical concentration to a percent concentration. Saves as a new DataFrame."""

        self.percentage_data_frame = self.raw_xml_data_frame
        self.percentage_data_frame['percentage_concentration'] = self.percentage_data_frame['analconc']/10000

    def split_into_blank_qc_and_sample_data_frame(self):
        """splits the percentage DataFrame into blank, qc, and sample DataFrames, based on the 'type' column."""

        self.blank_data_frame = self.percentage_data_frame[self.percentage_data_frame.type == "Blank"]
        self.qc_data_frame = self.percentage_data_frame[self.percentage_data_frame.type == "QC"]
        self.samples_and_dilutions_data_frame = self.percentage_data_frame[self.percentage_data_frame.type == "Analyte"]

    def combine_qc_into_one_data_set_with_highest_recovery_values(self):
        """groups the qc_data_frame and creates a new DataFrame with only the best recoveries for each analyte.

        This code was taken from the following StackOverflow question: https://stackoverflow.com/questions/31361599.
        Specifically, the answer given by Padraic Cunningham. Some modifications were made.

        first, a new column is created in the qc_data_frame that measures the distance from 100 (%) in absolute terms
        for each recovery value. Then, we do the groupby and transformation based on the indexes with the smallest
        distance from 100 %. We make our 'best recovery' DataFrame based on that. The final DataFrame that is spat out
        has unnecessary columns removed.

        Note: almost how we want this function. Initially, we had max recovery. Now, we have closest recovery to 100.
        What we want in the end is closest recovery to 100, but not over 100. """

        self.qc_data_frame['distance_from_100'] = abs(self.percentage_data_frame['percrecovery']-100)
        tem = self.qc_data_frame.groupby(['id17'])['distance_from_100'].transform(min) == self.qc_data_frame['distance_from_100']
        self.best_recovery_qc_data_frame = self.qc_data_frame[tem]
        self.best_recovery_qc_data_frame.reset_index(drop=True, inplace=True)
        self.best_recovery_qc_data_frame = self.best_recovery_qc_data_frame[['id15',
                                                                             'id17',
                                                                             'sampleid',
                                                                             'name20',
                                                                             'area',
                                                                             'percrecovery']].copy()

    def combine_blanks_into_one_data_set_with_lowest_percentage_concentration_values(self):
        """ produces a single axis data frame with one min value for each analyte, with the analytes being identified by
        id17 (could also do name20 here). To access the min value for each analyte, use df.iloc[n], with n= row. """

        self.min_value_blank_data_frame = self.blank_data_frame.groupby(['name20'])['percentage_concentration'].min()

    def join_over_curve_df_to_samples_df(self):
        """ joins the upper limits on areas for given analytes (based on calibration curve) to the samples DataFrame.
        These values are used to assign flags that indicate whether a given peak area is out of calibration range."""
        self.samples_and_dilutions_data_frame = pd.merge(left=self.samples_and_dilutions_data_frame,
                                                         right=self.over_curve_data_frame,
                                                         how='left',
                                                         left_on='id17',
                                                         right_on='id17')

    def assign_high_flag_to_sample_data(self):
        """assigns a flag to indicate whether a peak area is over the calibration curve range. the over_curve column
        will have a blank string if the area is not over, and will say 'over' if the area is over."""
        self.samples_and_dilutions_data_frame = self.samples_and_dilutions_data_frame.assign(over_curve='')
        self.samples_and_dilutions_data_frame.loc[self.samples_and_dilutions_data_frame['area'] >
                                                  self.samples_and_dilutions_data_frame['max_value'],
                                                  'over_curve'] = 'over'

    def split_samples_data_frame_into_dilutions_and_samples(self):
        """Splits the samples DataFrame into two - one containing the dilutions, and one containing the undiluted
        samples. This allows us to swap out the out of calibration range values by joining the two DataFrames together
        conditional on the over_curve field. Works by assuming that any sample id with a length larger than 9 is a dil,
        (xxxxxx-xx x/xx) and any with a length less than or equal to nine (xxxxxx-xx) is a sample"""
        self.sample_dilutions_data_frame = self.samples_and_dilutions_data_frame[self.samples_and_dilutions_data_frame.sampleid.str.len() > 9]
        self.samples_data_frame = self.samples_and_dilutions_data_frame[self.samples_and_dilutions_data_frame.sampleid.str.len() <= 9]

    def swap_out_out_of_range_values(self):
        """swaps the out of range values in samples_data_frame with in range ones from sample_dilutions_data_frame.
        Looks for the 'over' flag, and then gets the row that has the sampleid from the sample contained in its
        sampleid (if that makes sense) and the correct id17. It then replaces percentage_concentration, and changes
         the flag from 'over' to 'Corrected: new area = (area from dilution)'. """
        for index, row in self.samples_data_frame.iterrows():
            if row['over_curve'] == 'over':
                dilution = self.sample_dilutions_data_frame.loc[(self.sample_dilutions_data_frame['id17'] == row['id17'])
                                                                & (self.sample_dilutions_data_frame['sampleid'].str.contains(row['sampleid']))]
                try:
                    self.samples_data_frame.loc[index, 'percentage_concentration'] = dilution.iloc[0, 9]
                    self.samples_data_frame.loc[index, 'over_curve'] = 'Corrected: new area = ' + str(dilution.iloc[0, 5])
                except IndexError:
                    self.samples_data_frame.loc[index, 'over_curve'] = 'Out of range, no dil. '
        self.samples_data_frame.fillna(0, inplace=True)

    def create_condensed_sample_list_data_frame_for_gui(self):
        self.condensed_samples_data_frame = self.samples_data_frame[['sampleid',
                                                                     'name20',
                                                                     'percentage_concentration',
                                                                     'area',
                                                                     'over_curve']]

    def create_list_of_unique_samples(self):
        """This is a simple one line function that generates a list of unique samples in the samples_data_frame, for use
        at the GUI level."""
        self.unique_sample_id_list = self.samples_data_frame.sampleid.unique()

    def limit_sig_figs_in_dataframes(self):
        """This function rounds the values in the percentage recovery and percentage concentration columns of the
        standard recovery data frame and the samples data frame, respectively. """
        sig_figs = 2
        self.best_recovery_qc_data_frame.fillna(0, inplace=True)
        self.best_recovery_qc_data_frame['percrecovery'] = self.best_recovery_qc_data_frame.percrecovery.apply(
            lambda x: round(x, sig_figs - int(floor(log10(abs(x))))) if (100 > x > 0) else int(round(x)))
        self.samples_data_frame['percentage_concentration'] = self.samples_data_frame.percentage_concentration.apply(
            lambda x: round(x, sig_figs - int(floor(log10(abs(x))))) if (1 > x > 0) else int(round(x)))
