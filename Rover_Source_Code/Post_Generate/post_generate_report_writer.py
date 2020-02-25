#import os, sys, inspect
import pandas as pd

# below is disgusting, the author of this code needs to better understand how the python PATH works.
#currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
#parentdir = os.path.dirname(currentdir)
#sys.path.insert(0, parentdir)
#parentdir = os.path.dirname(parentdir)
#sys.path.insert(0, parentdir)
#parentdir = os.path.dirname(parentdir)
#sys.path.insert(0, parentdir)
#sys.path.insert(0, currentdir)


class ReportWriter:
    """This file writes deluxe percentage reports. if multi=True, there will be multiple samples displayed per page. If
    multi=False, there will be only one sample displayed per page. """

    def __init__(self, sample_data, header_data, updates):
        """The main init function.

        1. cont = an initialization of the PreGenerateController class. All of the data for the report comes from here.
        2. latex_header_dictionary = a dictionary of all the headers for each job in the batch. Key = jobnumber,
        value = latex headers, customer information only..
        3. Latex_header_and_sample_list_dictionary = the same as Latex_header_dictionary except with sample information
        added."""
        self.sample_data = sample_data
        self.header_data = header_data
        self.updates = updates
        self.latex_header_dictionary = {}
        self.latex_header_and_sample_list_dictionary = {}
        self.single_reports_dictionary = {}
        self.multiple_reports_dictionary = {}

#       This is for development - allows me to see the full DataFrame when i print to the console, rather than a
#       truncated version. This is useful for debugging purposes and ensuring that methods are working as intended.
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', -1)

    def deluxe_report_percentage_controller(self):
        """This is the controller function for the class. """
        self.generate_job_latex_headers()
        self.generate_samples_list()
        self.split_samples_into_single_or_multi()
        self.create_mg_g_column()

    def generate_job_latex_headers(self):
        """Iterates through the parsed header contents dictionary and produces the latex header for each job. Note that
        there will be fewer headers than samples if jobs contain more than one sample."""
        for key, item in self.header_data.header_contents_dictionary.items():
            header_string = r"""
\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{natbib}
\usepackage{graphicx}
\usepackage[margin=1in]{geometry}
\usepackage{parskip}
\usepackage{siunitx}
\usepackage[dvipsnames]{xcolor}
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhead[L]{""" + item[0] + r""" \\ """ + item[4] + r""" \\ """ + item[6] + r"""\\ """ + item[8] + r"""\\ """ + item[10] + r""" \\ """ + item[13] + r"""\\ \phantom{a}\\}
\fancyhead[C]{\textbf{Date:} """ + item[1] + r"""  (""" + item[2] + r""")""" + item[15][0] + r""" \\\textbf{Source:} """ + item[5] + item[15][1] + r""" \\\textbf{Type:} """ + item[7] + r"""""" + item[15][2] + r""" \\\textbf{No. of Samples:} """ + item[9] + r"""""" + item[15][3] + r"""\\\textbf{Arrival temp:} """ + item[11] + r"""""" + item[15][4] + r"""\\""" + item[14] + r"""""" + item[15][5] + r"""\\\phantom{a}\\}
\fancyhead[R]{\textbf{No.} """ + item[3] + r"""\\\phantom{a}\\\phantom{a}\\\phantom{a}\\\phantom{a}\\\phantom{a}\\\phantom{a}\\ }
\renewcommand{\headrulewidth}{0pt}
\setlength\headheight{60pt}
\begin{document}"""
            self.latex_header_dictionary[key] = header_string

    def generate_samples_list(self):
        """iterates through the parsed header contents dictionary and produces the sample list for each job. """
        for key, item in self.header_data.header_contents_dictionary.items():
            samples_string = r"""
\textbf{Samples:} """ + item[16] + r"""
\newline
\newline
\hline
"""
            self.latex_header_and_sample_list_dictionary[key] = self.latex_header_dictionary[key] + samples_string

    def split_samples_into_single_or_multi(self):
        counter = 0
        for item in self.updates['single multi']:
            print(item)
            if item == 'Single':
                self.single_reports_dictionary[self.sample_data.unique_sample_id_list[counter]] = \
                    [self.updates['sample type'][counter],
                     self.updates['report type'][counter]]
            else:
                self.multiple_reports_dictionary[self.sample_data.unique_sample_id_list[counter]] = \
                    [self.updates['sample type'][counter],
                     self.updates['report type'][counter]]
            counter += 1
        for x, y in self.single_reports_dictionary.items():
            print(x, y)
        for x, y in self.multiple_reports_dictionary.items():
            print(x, y)

    def create_mg_g_column(self):
        self.sample_data.samples_data_frame['mg_g'] =\
            self.sample_data.samples_data_frame['percentage_concentration'] * 10







