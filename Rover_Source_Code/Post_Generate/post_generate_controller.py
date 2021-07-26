import os, sys, inspect
import pandas as pd
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir)
sys.path.insert(0, currentdir)
from post_generate_header_methods import HeaderMethods
from post_generate_organize_methods import OrganizeMethods
from post_generate_single_methods import SingleMethods
from post_generate_multi_methods import MultiMethods
from post_generate_file_writing_methods import FileWritingMethods
from post_generate_basic_text_report_methods import BasicTextReports


class ReportWriter:
    """This class controls the methods in the Post_Generate folder. It writes all of the reports once it is passed
    the data from the GUI."""

    def __init__(self, sample_data, header_data, updates):
        """The main init function.

        1. sample_data = the sample data, in dataframe format. Comes in without the columns for mg_g, mg_ml, and
        mg_unit - these are added to the sample_data by the organize methods.
        2. header_data = the header data with no modifications, the original headers parsed by Pre_Generate.
        3. updates = all the information updated or added on the GUI screen. contains updated headers and sample lists,
        sample type, report type, basic/deluxe info, and then unit masses/densities where relevant.
        4. single_reports_dictionary = key : sampleid, value : updates for single reports.
        5. multiple_reports_dictionary =  key : sampleid, value : updates for multiple reports.
        6. latex_header_dictionary = a dictionary of all the headers for each job in the batch. Key = jobnumber,
        value = latex headers, customer information only..
        7. Latex_header_and_sample_list_dictionary = the same as Latex_header_dictionary except with sample information
        added.
        8. finished_reports_dictionary = the finished reports as a string of Latex. key : sampleid, value : report.
        9. cannabinoid_dictionary = a conversion dictionary for converting between id17 (order in which analytes come
        off the HPLC) and report order (decided by wendy).
        10. LOQ dictionary = a dictionary for entering the LOQ's of various cannabinoids. Order corresponds to report
        order.
        11. header_methods = the HeaderMethods class. All code for creating Latex headers is in this class.
        12. organize_methods = the OrganizeMethods class. All code for creating extra data columns based on report type
        and splitting the samples into single or multi is in here.
        """

        self.sample_data = sample_data
        self.header_data = header_data
        self.updates = updates
        self.single_reports_dictionary = {}
        self.multiple_reports_dictionary = {}
        self.latex_header_dictionary = {}
        self.latex_header_and_sample_list_dictionary = {}
        self.finished_reports_dictionary = {}

#       This cannabinoid dictionary is used for making the multi-tables.
        self.cannabinoid_dictionary = {1: (r"$\Delta^{9}$-THC &", 12.0),
                                       2: (r"$\Delta^{9}$-THC Acid &", 17.0),
                                       3: (r"$\Delta^{8}$THC &", 13.0),
                                       4: (r"Cannabichromene (CBC) &", 15.0),
                                       5: (r"Cannabichromene Acid &", 19.0),
                                       6: (r"Cannabidiol (CBD) &", 6.0),
                                       7: (r"Cannabidiol Acid &", 8.0),
                                       8: (r"Cannabigerol (CBG) &", 7.0),
                                       9: (r"Cannabigerol Acid &", 10.0),
                                       10: (r"Cannabicyclol (CBL) &", 14.0),
                                       11: (r"Cannabicyclol Acid &", 18.0),
                                       12: (r"Cannabidivarin (CBDV) &", 2.0),
                                       13: (r"Cannabidivarin Acid &", 3.0),
                                       14: (r"$\Delta^{9}$ THCV &", 4.0),
                                       15: (r"$\Delta^{9}$ THCV Acid &", 11.0),
                                       16: (r"Cannabinol (CBN) &", 9.0),
                                       17: (r"Cannabinol Acid &", 16.0),
                                       18: (r"Cannabigerivarin Acid &", 5.0)
                                       }
        self.mushroom_dictionary = {1: (r"Psilocin &", 1.0),
                                    2: (r"Psilocybin &", 2.0),
                                    3: (r"Baeocystin * &", 3.0)}

#       This dictionary is for containing the LOQ's. keys match the list indices at the table writing step.
        self.loq_dictionary = {1: '0.001',
                               2: '0.001',
                               3: '0.001',
                               4: '0.001',
                               5: '0.001',
                               6: '0.001',
                               7: '0.001',
                               8: '0.001',
                               9: '0.001',
                               10: '0.001',
                               11: '0.001',
                               12: '0.001',
                               13: '0.001',
                               14: '0.001',
                               15: '0.001',
                               16: '0.001',
                               17: '0.001',
                               18: '0.001',
                               }
        # Helper classes
        self.header_methods = HeaderMethods(header_data)
        self.organize_methods = OrganizeMethods(updates, sample_data)

#       This is for development - allows me to see the full DataFrame when i print to the console, rather than a
#       truncated version. This is useful for debugging purposes and ensuring that methods are working as intended.
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', -1)

    def post_generate_controller(self, instrument_type):
        """This is the controller function for the class. First, the latex header dictionaries are produced. Then,
        the organizer methods are called. Multiple sample reports are handled first, because these methods will catch
        any solo reports that are mistakenly labeled multi and will add them to the dictionary of single reports.
        After that, single reports are handled. The single and multi classes have to be instantiated down here, and not
        in the init, because I haven't done proper class inheritance. """
        self.latex_header_dictionary = self.header_methods.generate_job_latex_headers()
        self.latex_header_and_sample_list_dictionary = self.header_methods.generate_samples_list()
        self.single_reports_dictionary, self.multiple_reports_dictionary = \
            self.organize_methods.split_samples_into_single_or_multi()
        self.sample_data = self.organize_methods.create_alternate_sample_type_columns(instrument_type)
        multi_methods = MultiMethods(self.header_data.header_contents_dictionary,
                                     self.multiple_reports_dictionary,
                                     self.single_reports_dictionary,
                                     self.latex_header_and_sample_list_dictionary,
                                     self.sample_data,
                                     self.cannabinoid_dictionary,
                                     self.mushroom_dictionary,
                                     self.loq_dictionary)
        self.single_reports_dictionary, self.finished_reports_dictionary = \
            multi_methods.generate_multi_sample_reports(instrument_type)
        single_methods = SingleMethods(self.finished_reports_dictionary,
                                       self.single_reports_dictionary,
                                       self.sample_data,
                                       self.latex_header_and_sample_list_dictionary,
                                       self.loq_dictionary)
        self.finished_reports_dictionary = single_methods.generate_single_sample_reports()
        if instrument_type == 'UPLCUV':
            basic_reports = BasicTextReports(self.multiple_reports_dictionary,
                                             self.single_reports_dictionary,
                                             self.sample_data)
            basic_reports_dictionary = basic_reports.basic_text_reports()
            file_writing_methods = FileWritingMethods(self.finished_reports_dictionary, basic_reports_dictionary)
            file_writing_methods.generate_report_directories_and_files()
        elif instrument_type == 'UPLCMS':
            file_writing_methods = FileWritingMethods(self.finished_reports_dictionary, 'MUSH')
            file_writing_methods.generate_report_directories_and_files()


