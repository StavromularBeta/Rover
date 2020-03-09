import os, sys, inspect
import pandas as pd
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentdir = os.path.dirname(parentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir)
sys.path.insert(0, currentdir)
import os.path
import errno
from post_generate_header_methods import HeaderMethods
from post_generate_organize_methods import OrganizeMethods
from post_generate_single_methods import SingleMethods
from post_generate_multi_methods import MultiMethods


class ReportWriter:
    """This file writes deluxe percentage reports. if multi=True, there will be multiple samples displayed per page. If
    multi=False, there will be only one sample displayed per page. """

    def __init__(self, sample_data, header_data, updates):
        """The main init function.

        1. cont = an initialization of the PreGenerateController class. All of the data for the report comes from here.
        2. latex_header_dictionary = a dictionary of all the headers for each job in the batch. Key = jobnumber,
        value = latex headers, customer information only..
        3. Latex_header_and_sample_list_dictionary = the same as Latex_header_dictionary except with sample information
        added. """
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
                                       4: (r"Cannabidiol (CBC) &", 15.0),
                                       5: (r"Cannabidiol Acid &", 19.0),
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

#       This dictionary is for containing the LOQ's. keys match the list indices at the table writing step.
        self.loq_dictionary = {1: '0.030',
                               2: '0.003',
                               3: '0.003',
                               4: '0.003',
                               5: '0.003',
                               6: '0.003',
                               7: '0.003',
                               8: '0.003',
                               9: '0.030',
                               10: '0.003',
                               11: '0.003',
                               12: '0.003',
                               13: '0.003',
                               14: '0.003',
                               15: '0.003',
                               16: '0.003',
                               17: '0.003',
                               18: '0.003',
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

    def deluxe_report_percentage_controller(self):
        """This is the controller function for the class. """
        self.latex_header_dictionary = self.header_methods.generate_job_latex_headers()
        self.latex_header_and_sample_list_dictionary = self.header_methods.generate_samples_list()
        self.single_reports_dictionary, self.multiple_reports_dictionary = \
            self.organize_methods.split_samples_into_single_or_multi()
        self.sample_data = self.organize_methods.create_alternate_sample_type_columns()
        self.multi_methods = MultiMethods(self.header_data.header_contents_dictionary,
                                          self.multiple_reports_dictionary,
                                          self.single_reports_dictionary,
                                          self.latex_header_and_sample_list_dictionary,
                                          self.sample_data,
                                          self.cannabinoid_dictionary,
                                          self.loq_dictionary)
        self.single_reports_dictionary, self.finished_reports_dictionary = \
            self.multi_methods.generate_multi_sample_reports()
        self.single_methods = SingleMethods(self.finished_reports_dictionary,
                                            self.single_reports_dictionary,
                                            self.sample_data,
                                            self.latex_header_and_sample_list_dictionary,
                                            self.loq_dictionary)
        self.finished_reports_dictionary = self.single_methods.generate_single_sample_reports()
        self.generate_report_directories_and_files()

    def generate_report_directories_and_files(self):
        target = r'T:\ANALYST WORK FILES\Peter\Rover\reports\ '
        for key, value in self.finished_reports_dictionary.items():
            try:
                jobnumber = str(key)
                filename = target + jobnumber[0:6] + '\\' + jobnumber + '_raw.tex'
                filename = filename.replace('/', '-')
                with self.safe_open_w(filename) as f:
                    f.write(value)
            except OSError:
                pass

    def mkdir_p(self, path):
        try:
            os.makedirs(path)
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def safe_open_w(self, path):
        """ Open "path" for writing, creating any parent directories as needed. """
        self.mkdir_p(os.path.dirname(path))
        return open(path, 'w')
