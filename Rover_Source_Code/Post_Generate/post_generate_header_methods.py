import pandas as pd


class HeaderMethods:

    def __init__(self, header_data):
        self.header_data = header_data
        self.latex_header_dictionary = {}
        self.latex_header_and_sample_list_dictionary = {}

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
\fancyhead[L]{""" + item[0] + r""" \\ """ + item[4] + r""" \\ """ + item[5] + r"""\\ """ + item[6] + r"""\\ """ + item[11] + r""" \\ """ + item[13] + r"""\\ \phantom{a}\\}
\fancyhead[C]{\textbf{Date:} """ + item[1] + r"""  (""" + item[2] + r""")""" + item[16][0] + r""" \\\textbf{Source:} """ + item[7] + item[16][1] + r""" \\\textbf{Type:} """ + item[8] + r"""""" + item[16][2] + r""" \\\textbf{No. of Samples:} """ + item[9] + r"""""" + item[16][3] + r"""\\\textbf{Arrival temp:} """ + item[10] + r"""""" + item[16][4] + r"""\\""" + item[14] + r"""""" + item[16][5] + r"""\\\phantom{a}\\}
\fancyhead[R]{\textbf{No.} """ + item[3] + r"""\\\phantom{a}\\\phantom{a}\\\phantom{a}\\\phantom{a}\\\phantom{a}\\\phantom{a}\\ }
\renewcommand{\headrulewidth}{0pt}
\setlength\headheight{60pt}
\begin{document}"""
            self.latex_header_dictionary[key] = header_string
        return self.latex_header_dictionary

    def generate_samples_list(self):
        """iterates through the parsed header contents dictionary and produces the sample list for each job. """
        for key, item in self.header_data.header_contents_dictionary.items():
            samples_string = r"""
\textbf{Samples:} """ + item[15] + r"""
\newline
\newline
\hline
"""
            self.latex_header_and_sample_list_dictionary[key] = self.latex_header_dictionary[key] + samples_string
        return self.latex_header_and_sample_list_dictionary
