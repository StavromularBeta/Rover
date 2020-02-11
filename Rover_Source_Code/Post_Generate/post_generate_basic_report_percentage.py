import os, sys, inspect
import pandas as pd

# below is disgusting, the author of this code needs to better understand how the python PATH works.
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir)
sys.path.insert(0, currentdir)

from Pre_Generate.pre_generate_controller import PreGenerateController as cont


class PostGenerateDeluxeReportPercentage:
    """This file writes deluxe percentage reports. if multi=True, there will be multiple samples displayed per page. If
    multi=False, there will be only one sample displayed per page. """

    def __init__(self, multi=True):
        """The main init function.

        1. cont = an initialization of the PreGenerateController class. All of the data for the report comes from here.
        2. latex_header_dictionary = a dictionary of all the headers for each job in the batch. Key = jobnumber,
        value = latex headers, customer information only..
        3. Latex_header_and_sample_list_dictionary = the same as Latex_header_dictionary except with sample information
        added."""
        self.cont = cont()
        self.latex_header_dictionary = {}
        self.latex_header_and_sample_list_dictionary = {}

    def deluxe_report_percentage_controller(self):
        """This is the controller function for the class. """
        self.generate_job_latex_headers()
        self.generate_samples_list()

    def generate_job_latex_headers(self):
        """Iterates through the parsed header contents dictionary and produces the latex header for each job. Note that
        there will be fewer headers than samples if jobs contain more than one sample."""
        for key, item in self.cont.hp.header_contents_dictionary.items():
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
        for key, item in self.cont.hp.header_contents_dictionary.items():
            samples_string = r"""
\textbf{Samples:} """ + item[16] + r"""
\newline
\newline
\hline
"""
            self.latex_header_and_sample_list_dictionary[key] = self.latex_header_dictionary[key] + samples_string


latex = PostGenerateDeluxeReportPercentage()
latex.deluxe_report_percentage_controller()