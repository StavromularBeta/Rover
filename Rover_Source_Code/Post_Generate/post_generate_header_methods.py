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
            print(item)
            header_string = r"""
% CLASS OF DOCUMENT
\documentclass{article}

% PACKAGES USED IN DOCUMENT
\usepackage[utf8]{inputenc}
\usepackage{natbib}
\usepackage{graphicx}
\usepackage[margin=1in]{geometry}
\usepackage{parskip}
\usepackage{siunitx}
\usepackage[dvipsnames]{xcolor}
\usepackage{fancyhdr}
\usepackage[includeheadfoot, margin=1in]{geometry}
\pagestyle{fancy}

% HEADER
\fancyhead[L]{
              """ + item[0] + r""" \\
              """ + item[16] + r""" \\
              """ + item[4] + r""" \\
              """ + item[5] + ', ' + item[6] + r"""\\
              \phantom{a} \\
              """ + item[11] + r""" \\
              """ + item[12] + r""" \\
              }
\fancyhead[C]{
              \textbf{Date:} """ + item[1] + r"""  (""" + item[2] + r""")""" + item[17][0] + r""" \\
              \textbf{Source:} """ + item[7] + item[17][1] + r""" \\
              \textbf{Type:} """ + item[8] + r"""""" + item[17][2] + r""" \\
              \textbf{No. of Samples:} """ + item[9] + r"""""" + item[17][3] + r"""\\
              \textbf{Arrival temp:} """ + item[10] + r"""""" + item[17][4] + r"""\\
              """ + item[14] + r"""""" + item[17][5] + r"""\\
              \phantom{a}\\
              }
\fancyhead[R]{
              \textbf{No.} """ + item[3] + r"""\\
              \phantom{a}\\
              \phantom{a}\\
              \phantom{a}\\
              \phantom{a}\\
              \phantom{a}\\
              \phantom{a}\\
               }

% FOOTER
\fancyfoot[C]{\textbf{MB Laboratories Ltd.}\\ \textbf{Web:} www.mblabs.com}
\fancyfoot[R]{\textbf{Mail:} PO Box 2103\\ Sidney, B.C., V8L 356}
\fancyfoot[L]{\textbf{T:} 250 656 1334\\ \textbf{E:} info@mblabs.com}

% SETS THE HEIGHT OF THE HEADER, INCLUDES HEADER AND FOOTER, REMOVES A LINE BELOW HEADER
\geometry{head=65pt, includehead=true, includefoot=true}
\renewcommand{\headrulewidth}{0pt}

\begin{document}"""
            self.latex_header_dictionary[key] = header_string
        return self.latex_header_dictionary

    def generate_samples_list(self):
        """iterates through the parsed header contents dictionary and produces the sample list for each job. """
        for key, item in self.header_data.header_contents_dictionary.items():
            samples_string = r"""

% SAMPLE LIST
\textbf{Samples:} """ + item[15] + r"""
\phantom{a}
\newline
\hline
"""
            self.latex_header_and_sample_list_dictionary[key] = self.latex_header_dictionary[key] + samples_string
        return self.latex_header_and_sample_list_dictionary
