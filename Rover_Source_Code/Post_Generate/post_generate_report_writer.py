import pandas as pd
import os
import os.path
import errno


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
        self.finished_reports_dictionary = {}

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
        self.create_alternate_sample_type_columns()
        self.generate_single_sample_reports()
        self.generate_report_directories_and_files()

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

    def create_alternate_sample_type_columns(self):
        self.sample_data.samples_data_frame['mg_g'] =\
            self.sample_data.samples_data_frame['percentage_concentration'] * 10

    def generate_single_sample_reports(self):
        for key, value in self.single_reports_dictionary.items():
            if value[0] == 'Percent' and value[1] == 'Basic':
                self.generate_single_percent_basic_report(key)
            elif value[0] == 'Percent' and value[1] == 'Deluxe':
                self.generate_single_percent_deluxe_report(key)
            elif value[0] == 'mg/g' and value[1] == 'Basic':
                self.generate_single_mg_g_basic_report(key)
            elif value[0] == 'mg/g' and value[1] == 'Deluxe':
                self.generate_single_mg_g_deluxe_report(key)
            else:
                self.generate_single_percent_deluxe_report(key)

    def generate_single_percent_basic_report(self, sample_id):
        temporary_data_frame = self.sample_data.samples_data_frame[self.sample_data.samples_data_frame['sampleid']
                                                                   == sample_id]
        temporary_data = self.get_relevant_values_and_recoveries_for_single_reports(temporary_data_frame,
                                                                                    'Percent',
                                                                                    'Basic')
        temporary_table = self.create_single_basic_table(temporary_data, 'Percent')
        header = self.latex_header_and_sample_list_dictionary[sample_id[0:6]]
        footer = self.generate_footer()
        report = header + temporary_table + footer
        self.finished_reports_dictionary[sample_id] = report

    def generate_single_mg_g_basic_report(self, sample_id):
        temporary_data_frame = self.sample_data.samples_data_frame[self.sample_data.samples_data_frame['sampleid']
                                                                   == sample_id]
        temporary_data = self.get_relevant_values_and_recoveries_for_single_reports(temporary_data_frame,
                                                                                    'mg_g',
                                                                                    'Basic')
        temporary_table = self.create_single_basic_table(temporary_data, 'mg_g')
        header = self.latex_header_and_sample_list_dictionary[sample_id[0:6]]
        footer = self.generate_footer()
        report = header + temporary_table + footer
        self.finished_reports_dictionary[sample_id] = report

    def generate_single_percent_deluxe_report(self, sample_id):
        temporary_data_frame = self.sample_data.samples_data_frame[self.sample_data.samples_data_frame['sampleid']
                                                                   == sample_id]
        temporary_data = self.get_relevant_values_and_recoveries_for_single_reports(temporary_data_frame,
                                                                                    'Percent',
                                                                                    'Deluxe')
        temporary_table = self.create_single_deluxe_table(temporary_data, 'Percent')
        header = self.latex_header_and_sample_list_dictionary[sample_id[0:6]]
        footer = self.generate_footer()
        report = header + temporary_table + footer
        self.finished_reports_dictionary[sample_id] = report

    def generate_single_mg_g_deluxe_report(self, sample_id):
        temporary_data_frame = self.sample_data.samples_data_frame[self.sample_data.samples_data_frame['sampleid']
                                                                   == sample_id]
        temporary_data = self.get_relevant_values_and_recoveries_for_single_reports(temporary_data_frame,
                                                                                    'mg_g',
                                                                                    'Deluxe')
        temporary_table = self.create_single_deluxe_table(temporary_data, 'mg_g')
        header = self.latex_header_and_sample_list_dictionary[sample_id[0:6]]
        footer = self.generate_footer()
        report = header + temporary_table + footer
        self.finished_reports_dictionary[sample_id] = report

    def get_relevant_values_and_recoveries_for_single_reports(self, temporary_data_frame, sample_type, report_type):
        if sample_type == 'Percent':
            sample_column_type = 'percentage_concentration'
        elif sample_type == 'mg_g':
            sample_column_type = 'mg_g'
        else:
            sample_column_type = 'percentage_concentration'
        ibu_recovery_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 1.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        cbdv_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 2.0,
                                     [sample_column_type]].iloc[0][sample_column_type])
        cbdva_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 3.0,
                                     [sample_column_type]].iloc[0][sample_column_type])
        thcv_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 4.0,
                                     [sample_column_type]].iloc[0][sample_column_type])
        cbgva_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 5.0,
                                     [sample_column_type]].iloc[0][sample_column_type])
        cbd_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 6.0,
                                     [sample_column_type]].iloc[0][sample_column_type])
        cbg_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 7.0,
                                     [sample_column_type]].iloc[0][sample_column_type])
        cbda_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 8.0,
                                     [sample_column_type]].iloc[0][sample_column_type])
        cbn_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 9.0,
                                     [sample_column_type]].iloc[0][sample_column_type])
        cbga_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 10.0,
                                     [sample_column_type]].iloc[0][sample_column_type])
        thcva_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 11.0,
                                     [sample_column_type]].iloc[0][sample_column_type])
        d9_thc_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 12.0,
                                     [sample_column_type]].iloc[0][sample_column_type])
        d8_thc_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 13.0,
                                     [sample_column_type]].iloc[0][sample_column_type])
        cbl_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 14.0,
                                     [sample_column_type]].iloc[0][sample_column_type])
        cbc_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 15.0,
                                     [sample_column_type]].iloc[0][sample_column_type])
        cbna_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 16.0,
                                     [sample_column_type]].iloc[0][sample_column_type])
        thca_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 17.0,
                                     [sample_column_type]].iloc[0][sample_column_type])
        cbla_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 18.0,
                                     [sample_column_type]].iloc[0][sample_column_type])
        cbca_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 19.0,
                                     [sample_column_type]].iloc[0][sample_column_type])
        if report_type == 'Deluxe':
            return [ibu_recovery_value, cbdv_value, cbdva_value, thcv_value, cbgva_value, cbd_value, cbg_value,
                    cbda_value, cbn_value, cbga_value, thcva_value, d9_thc_value, d8_thc_value, cbl_value, cbc_value,
                    cbna_value, thca_value, cbla_value, cbca_value]
        else:
            return [ibu_recovery_value, cbd_value, cbn_value, d9_thc_value, thca_value]

    def create_single_deluxe_table(self, data, sample_type):
        if sample_type == 'Percent':
            sample_type = r'\%'
        elif sample_type == 'mg_g':
            sample_type = 'mg/g'
        else:
            sample_type = r'\%'
        deluxe_potency_table_string = r"""
\newline
\renewcommand{\arraystretch}{1.2}
\begin{table}[h!]\centering
\begin{tabular}{p{\dimexpr0.270\textwidth-2\tabcolsep-\arrayrulewidth\relax}|
                p{\dimexpr0.490\textwidth-2\tabcolsep-\arrayrulewidth\relax}|
                p{\dimexpr0.08\textwidth-2\tabcolsep-\arrayrulewidth\relax}
                p{\dimexpr0.08\textwidth-2\tabcolsep-\arrayrulewidth\relax}
                p{\dimexpr0.08\textwidth-2\tabcolsep-\arrayrulewidth\relax}
                }
\textbf{Cannabinoids} & \textbf{Sample 1} (""" + sample_type + r""")  & \textbf{LB} (\%) & \textbf{RR} (\%) & \textbf{LOQ} (\%)\\
\hline
\hline
$\Delta^{9}$-THC & """ + data[11] + r""" & ND & 94.4 & 0.003\\
$\Delta^{9}$-THC Acid & """ + data[16] + r""" & ND & 96.6& 0.003\\
\hline
\hline
\textbf{Total THC*} &  \textbf{""" + str(float(data[11]) + (float(data[16]) * 0.877)) + r"""} & & &\\
\hline
\hline
$\Delta^{8}$THC & """ + data[12] + r""" & ND & 72.5& 0.003\\
$\Delta^{8}$THC Acid & ND & ND & 96.6 & 0.003\\
\hline
Cannabidiol (CBC) & """ + data[14] + r"""  & ND & 65.7 & 0.003\\
Cannabidiol Acid & """ + data[18] + r"""  & ND & 97.6 & 0.003\\
\hline
Cannabidiol (CBD) &""" + data[5] + r""" &  ND & 92.3 & 0.003\\
Cannabidiol Acid & """ + data[7] + r""" &  ND & 112 & 0.003\\
\hline
\hline
\textbf{Total CBD**} &  \textbf{""" + str(float(data[5]) + (float(data[7]) * 0.877)) + r"""} & & &\\
\hline
\hline
Cannabigerol (CBG) & """ + data[6] + r""" & ND & 94.1 & 0.003\\
Cannabigerol Acid & """ + data[9] + r""" & ND & 96.8 & 0.003\\
\hline
Cannabicyclol (CBL) & """ + data[13] + r""" &  ND & 77.4 & 0.003\\
Cannabicyclol Acid & """ + data[17] + r""" &  ND & 91.6 & 0.003\\
\hline
Cannabidivarin (CBDV) & """ + data[1] + r""" &  ND & 93.2 & 0.003\\
Cannabidivarin Acid & """ + data[2] + r""" &  ND & 93.2  & 0.003\\
\hline
$\Delta^{9}$ THCV & """ + data[3] + r""" &  ND & 98.3 & 0.003\\
$\Delta^{9}$ THCV Acid &  """ + data[10] + r""" &  ND & 100  & 0.003\\
\hline
Cannabinol (CBN) & """ + data[8] + r""" &   ND & 101 & 0.003\\
Cannabinol Acid & """ + data[15] + r""" &  ND & 78.7 & 0.003 \\
\hline
Cannabigerivarin Acid & """ + data[4] + r""" &  ND & 92.0 & 0.003 \\
\hline
\hline
\textbf{Moisture} & 0.00  &   &  &\\
\hline
\hline
\end{tabular}
\end{table}
"""
        return deluxe_potency_table_string

    def create_single_basic_table(self, data, sample_type):
        if sample_type == 'Percent':
            sample_type = r'\%'
        elif sample_type == 'mg_g':
            sample_type = 'mg/g'
        else:
            sample_type = r'\%'
        basic_potency_table_string = r"""
\newline
\renewcommand{\arraystretch}{1.2}
\begin{table}[h!]\centering
\begin{tabular}{p{\dimexpr0.270\textwidth-2\tabcolsep-\arrayrulewidth\relax}|
                p{\dimexpr0.490\textwidth-2\tabcolsep-\arrayrulewidth\relax}|
                p{\dimexpr0.08\textwidth-2\tabcolsep-\arrayrulewidth\relax}
                p{\dimexpr0.08\textwidth-2\tabcolsep-\arrayrulewidth\relax}
                p{\dimexpr0.08\textwidth-2\tabcolsep-\arrayrulewidth\relax}
                }
\textbf{Cannabinoids} & \textbf{Sample 1} (""" + sample_type + r""")  & \textbf{LB} (\%) & \textbf{RR} (\%) & \textbf{LOQ} (\%)\\
\hline
\hline
$\Delta^{9}$-THC & """ + data[3] + r""" & ND & 94.4 & 0.003\\
$\Delta^{9}$-THC Acid & """ + data[4] + r""" & ND & 96.6& 0.003\\
\hline
Cannabidiol (CBD) &""" + data[1] + r""" &  ND & 92.3 & 0.003\\
\hline
Cannabinol (CBN) & """ + data[2] + r""" &   ND & 101 & 0.003\\
\hline
\hline
\textbf{Moisture} & 0.00  &   &  &\\
\hline
\hline
\end{tabular}
\end{table}
"""
        return basic_potency_table_string

    def generate_footer(self):
        footer_string = r"""
Methods: solvent extraction; measured by UPLC-UV. P.I. 1.14 \& based on USP monograph 29 \newline
$\si{S_{o}}$ (standard deviation at zero analyte concentration) = 0.001 \%. \% = percent (10mg/g = 1.0 \%). \newline\newline
ND = none detected. RR = Reference Recovery. LB = Lab Blank. THC = tetrahydrocannabinol.\newline 
\textbf{*Total THC} = $\Delta^{9}$-THC + (THCA x 0.877 ). \textbf{**Total CBD} = CBD + (CBDA x 0.877).\newline\newline
Material will be held for up to 3 weeks unless alternative arrangements have been made. Sample holding time may vary and is dependant on MBL license restrictions.
\newline\newline\newline
H. Hartmann \phantom{aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaasasssssssssssss}R. Bilodeau\\ Sr. Analytical Chemist: \underline{\hspace{2.1cm}}{ \hspace{4.1cm} Analytical Chemist: \underline{\hspace{3cm}}        
\end{document}
 """
        return footer_string

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


