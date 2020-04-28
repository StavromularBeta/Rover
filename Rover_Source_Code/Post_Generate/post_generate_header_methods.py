import pandas as pd


class HeaderMethods:
    """This class contains the methods that create the latex headers for all of the reports."""

    def __init__(self, header_data):
        """
        1. header_data = the header data from pre_generate with GUI modifications - specifically, any changes made on
        the GUI have replaced the parsed attempts at the correct information, and the spacing has been added.
        2. latex_header_dictionary = the dictionary of finished latex headers only.
        3. latex_header_and_sample_list_dictionary = the dictionary of finished latex headers and sample lists.
        """
        self.header_data = header_data
        self.latex_header_dictionary = {}
        self.latex_header_and_sample_list_dictionary = {}

    def generate_job_latex_headers(self):
        """Iterates through the parsed header contents dictionary and produces the latex header for each job. the 16th
        list item is a list of padding, which gets applied to the center column of the header so that the center column
        is properly aligned (the one downfall of this latex header package, no alignment on the center column). """
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
\usepackage[includeheadfoot, margin=1in, headheight=100pt]{geometry}
\pagestyle{fancy}
\fancyhead[L]{""" + item[0] + r""" \\ """ + item[4] + r""" \\ """ + item[5] + ', ' + item[6] + r"""\\ \phantom{a} \\ """ + item[11] + r""" \\ """ + item[13] + r"""\\ \phantom{a}\\}
\fancyhead[C]{\textbf{Date:} """ + item[1] + r"""  (""" + item[2] + r""")""" + item[16][0] + r""" \\\textbf{Source:} """ + item[7] + item[16][1] + r""" \\\textbf{Type:} """ + item[8] + r"""""" + item[16][2] + r""" \\\textbf{No. of Samples:} """ + item[9] + r"""""" + item[16][3] + r"""\\\textbf{Arrival temp:} """ + item[10] + r"""""" + item[16][4] + r"""\\""" + item[14] + r"""""" + item[16][5] + r"""\\\phantom{a}\\}
\fancyhead[R]{\textbf{No.} """ + item[3] + r"""\\\phantom{a}\\\phantom{a}\\\phantom{a}\\\phantom{a}\\\phantom{a}\\\phantom{a}\\ }
\renewcommand{\headrulewidth}{0pt}
\begin{document}"""
            self.latex_header_dictionary[key] = header_string
        return self.latex_header_dictionary

    def generate_samples_list(self):
        """iterates through the parsed header contents dictionary and produces the sample list for each job. """
        for key, item in self.header_data.header_contents_dictionary.items():
            samples_string = r"""
\phantom{a}
\newline
\newline
\newline
\newline
\textbf{Samples:} """ + item[15] + r"""
\phantom{a}
\newline
\newline
\hline
"""
            self.latex_header_and_sample_list_dictionary[key] = self.latex_header_dictionary[key] + samples_string
        return self.latex_header_and_sample_list_dictionary
