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
        added. """
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

    def deluxe_report_percentage_controller(self):
        """This is the controller function for the class. """
        self.generate_job_latex_headers()
        self.generate_samples_list()
        self.split_samples_into_single_or_multi()
        self.create_alternate_sample_type_columns()
        self.generate_multi_sample_reports()
        self.generate_single_sample_reports()
        self.generate_report_directories_and_files()
        print(self.sample_data.best_recovery_qc_data_frame)

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
            if item == 'Single':
                self.single_reports_dictionary[self.sample_data.unique_sample_id_list[counter]] = \
                    [self.updates['sample type'][counter],
                     self.updates['report type'][counter],
                     self.updates['density_unit'][counter],
                     self.updates['density_unit_option'][counter]]
            else:
                self.multiple_reports_dictionary[self.sample_data.unique_sample_id_list[counter]] = \
                    [self.updates['sample type'][counter],
                     self.updates['report type'][counter],
                     self.updates['density_unit'][counter],
                     self.updates['density_unit_option'][counter]]
            counter += 1

    def create_alternate_sample_type_columns(self):
        self.sample_data.samples_data_frame['mg_g'] =\
            self.sample_data.samples_data_frame['percentage_concentration'] * 10
        for key, value in self.single_reports_dictionary.items():
            sample_id = key
            if value[3] == 'density':
                self.sample_data.samples_data_frame.loc[self.sample_data.samples_data_frame['sampleid'] ==
                                                        sample_id,
                                                        'mg_ml'] = \
                    self.sample_data.samples_data_frame['mg_g'] * float(value[2])
            elif value[3] == 'unit':
                self.sample_data.samples_data_frame.loc[self.sample_data.samples_data_frame['sampleid'] ==
                                                        sample_id,
                                                        'mg_unit'] = \
                    self.sample_data.samples_data_frame['mg_g'] * \
                    float(value[2])
        for key, value in self.multiple_reports_dictionary.items():
            sample_id = key
            if value[3] == 'density':
                self.sample_data.samples_data_frame.loc[self.sample_data.samples_data_frame['sampleid'] ==
                                                        sample_id,
                                                        'mg_ml'] = \
                    self.sample_data.samples_data_frame['mg_g'] * float(value[2])
            elif value[3] == 'unit':
                self.sample_data.samples_data_frame.loc[self.sample_data.samples_data_frame['sampleid'] ==
                                                        sample_id,
                                                        'mg_unit'] = \
                    self.sample_data.samples_data_frame['mg_g'] * \
                    float(value[2])

# SINGLE SAMPLE PER PAGE CODE

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
            elif value[0] == 'mg/mL' and value[1] == 'Basic':
                self.generate_single_mg_ml_basic_report(key)
            elif value[0] == 'mg/mL' and value[1] == 'Deluxe':
                self.generate_single_mg_ml_deluxe_report(key)
            elif value[0] == 'per unit' and value[1] == 'Basic':
                self.generate_single_unit_basic_report(key)
            elif value[0] == 'per unit' and value[1] == 'Deluxe':
                self.generate_single_unit_deluxe_report(key)
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

    def generate_single_mg_ml_basic_report(self, sample_id):
        temporary_data_frame = self.sample_data.samples_data_frame[self.sample_data.samples_data_frame['sampleid']
                                                                   == sample_id]
        temporary_data = self.get_relevant_values_and_recoveries_for_single_reports(temporary_data_frame,
                                                                                    'mg_ml',
                                                                                    'Basic')
        temporary_table = self.create_single_basic_table(temporary_data, 'mg_ml')
        header = self.latex_header_and_sample_list_dictionary[sample_id[0:6]]
        footer = self.generate_footer()
        report = header + temporary_table + footer
        self.finished_reports_dictionary[sample_id] = report

    def generate_single_mg_ml_deluxe_report(self, sample_id):
        temporary_data_frame = self.sample_data.samples_data_frame[self.sample_data.samples_data_frame['sampleid']
                                                                   == sample_id]
        temporary_data = self.get_relevant_values_and_recoveries_for_single_reports(temporary_data_frame,
                                                                                    'mg_ml',
                                                                                    'Deluxe')
        temporary_table = self.create_single_deluxe_table(temporary_data, 'mg_ml')
        header = self.latex_header_and_sample_list_dictionary[sample_id[0:6]]
        footer = self.generate_footer()
        report = header + temporary_table + footer
        self.finished_reports_dictionary[sample_id] = report

    def generate_single_unit_basic_report(self, sample_id):
        temporary_data_frame = self.sample_data.samples_data_frame[self.sample_data.samples_data_frame['sampleid']
                                                                   == sample_id]
        temporary_data = self.get_relevant_values_and_recoveries_for_single_reports_unit(temporary_data_frame,
                                                                                         'Basic')
        temporary_table = self.create_single_basic_table_unit(temporary_data)
        header = self.latex_header_and_sample_list_dictionary[sample_id[0:6]]
        footer = self.generate_footer()
        report = header + temporary_table + footer
        self.finished_reports_dictionary[sample_id] = report

    def generate_single_unit_deluxe_report(self, sample_id):
        temporary_data_frame = self.sample_data.samples_data_frame[self.sample_data.samples_data_frame['sampleid']
                                                                   == sample_id]
        temporary_data = self.get_relevant_values_and_recoveries_for_single_reports_unit(temporary_data_frame,
                                                                                         'Deluxe')
        temporary_table = self.create_single_deluxe_table_unit(temporary_data)
        header = self.latex_header_and_sample_list_dictionary[sample_id[0:6]]
        footer = self.generate_footer()
        report = header + temporary_table + footer
        self.finished_reports_dictionary[sample_id] = report
        #####
    def get_standard_recovery_values(self, report_type):
        temporary_data_frame = self.sample_data.best_recovery_qc_data_frame
        ibu_recovery_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 1.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        cbdv_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 2.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        cbdva_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 3.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        thcv_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 4.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        cbgva_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 5.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        cbd_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 6.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        cbg_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 7.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        cbda_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 8.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        cbn_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 9.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        cbga_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 10.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        thcva_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 11.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        d9_thc_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 12.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        d8_thc_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 13.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        cbl_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 14.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        cbc_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 15.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        cbna_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 16.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        thca_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 17.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        cbla_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 18.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        cbca_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 19.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        if report_type == 'Deluxe':
            return [ibu_recovery_value, cbdv_value, cbdva_value, thcv_value, cbgva_value, cbd_value, cbg_value,
                    cbda_value, cbn_value, cbga_value, thcva_value, d9_thc_value, d8_thc_value, cbl_value, cbc_value,
                    cbna_value, thca_value, cbla_value, cbca_value]
        else:
            return [ibu_recovery_value, cbd_value, cbda_value, cbn_value, cbna_value, d9_thc_value, thca_value, d8_thc_value]

    def get_relevant_values_and_recoveries_for_single_reports(self, temporary_data_frame, sample_type, report_type):
        if sample_type == 'Percent':
            sample_column_type = 'percentage_concentration'
        elif sample_type == 'mg_g':
            sample_column_type = 'mg_g'
        elif sample_type == 'mg_ml':
            sample_column_type = 'mg_ml'
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
            return [ibu_recovery_value, cbd_value, cbda_value, cbn_value, cbna_value, d9_thc_value, thca_value, d8_thc_value]

    def get_relevant_values_and_recoveries_for_single_reports_unit(self, temporary_data_frame, report_type):
        ibu_recovery_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 1.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        cbdv_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 2.0,
                                     ['mg_g']].iloc[0]['mg_g'])
        cbdva_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 3.0,
                                     ['mg_g']].iloc[0]['mg_g'])
        thcv_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 4.0,
                                     ['mg_g']].iloc[0]['mg_g'])
        cbgva_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 5.0,
                                     ['mg_g']].iloc[0]['mg_g'])
        cbd_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 6.0,
                                     ['mg_g']].iloc[0]['mg_g'])
        cbg_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 7.0,
                                     ['mg_g']].iloc[0]['mg_g'])
        cbda_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 8.0,
                                     ['mg_g']].iloc[0]['mg_g'])
        cbn_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 9.0,
                                     ['mg_g']].iloc[0]['mg_g'])
        cbga_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 10.0,
                                     ['mg_g']].iloc[0]['mg_g'])
        thcva_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 11.0,
                                     ['mg_g']].iloc[0]['mg_g'])
        d9_thc_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 12.0,
                                     ['mg_g']].iloc[0]['mg_g'])
        d8_thc_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 13.0,
                                     ['mg_g']].iloc[0]['mg_g'])
        cbl_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 14.0,
                                     ['mg_g']].iloc[0]['mg_g'])
        cbc_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 15.0,
                                     ['mg_g']].iloc[0]['mg_g'])
        cbna_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 16.0,
                                     ['mg_g']].iloc[0]['mg_g'])
        thca_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 17.0,
                                     ['mg_g']].iloc[0]['mg_g'])
        cbla_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 18.0,
                                     ['mg_g']].iloc[0]['mg_g'])
        cbca_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 19.0,
                                     ['mg_g']].iloc[0]['mg_g'])
        #UNITS
        cbdv_value_u = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 2.0,
                                     ['mg_unit']].iloc[0]['mg_unit'])
        cbdva_value_u = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 3.0,
                                     ['mg_unit']].iloc[0]['mg_unit'])
        thcv_value_u = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 4.0,
                                     ['mg_unit']].iloc[0]['mg_unit'])
        cbgva_value_u = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 5.0,
                                     ['mg_unit']].iloc[0]['mg_unit'])
        cbd_value_u = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 6.0,
                                     ['mg_unit']].iloc[0]['mg_unit'])
        cbg_value_u = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 7.0,
                                     ['mg_unit']].iloc[0]['mg_unit'])
        cbda_value_u = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 8.0,
                                     ['mg_unit']].iloc[0]['mg_unit'])
        cbn_value_u = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 9.0,
                                     ['mg_unit']].iloc[0]['mg_unit'])
        cbga_value_u = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 10.0,
                                     ['mg_unit']].iloc[0]['mg_unit'])
        thcva_value_u = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 11.0,
                                     ['mg_unit']].iloc[0]['mg_unit'])
        d9_thc_value_u = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 12.0,
                                     ['mg_unit']].iloc[0]['mg_unit'])
        d8_thc_value_u = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 13.0,
                                     ['mg_unit']].iloc[0]['mg_unit'])
        cbl_value_u = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 14.0,
                                     ['mg_unit']].iloc[0]['mg_unit'])
        cbc_value_u = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 15.0,
                                     ['mg_unit']].iloc[0]['mg_unit'])
        cbna_value_u = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 16.0,
                                     ['mg_unit']].iloc[0]['mg_unit'])
        thca_value_u = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 17.0,
                                     ['mg_unit']].iloc[0]['mg_unit'])
        cbla_value_u = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 18.0,
                                     ['mg_unit']].iloc[0]['mg_unit'])
        cbca_value_u = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 19.0,
                                     ['mg_unit']].iloc[0]['mg_unit'])
        if report_type == 'Deluxe':
            return [ibu_recovery_value, [cbdv_value, cbdv_value_u], [cbdva_value, cbdva_value_u],
                    [thcv_value, thcv_value_u], [cbgva_value, cbgva_value_u], [cbd_value, cbd_value_u],
                    [cbg_value, cbg_value_u], [cbda_value, cbda_value_u], [cbn_value, cbn_value_u],
                    [cbga_value, cbga_value_u], [thcva_value, thcva_value_u], [d9_thc_value, d9_thc_value_u],
                    [d8_thc_value, d8_thc_value_u], [cbl_value, cbl_value_u], [cbc_value, cbc_value_u],
                    [cbna_value, cbna_value_u], [thca_value, thca_value_u], [cbla_value, cbla_value_u],
                    [cbca_value, cbca_value_u]]
        else:
            return [ibu_recovery_value, [cbd_value, cbd_value_u], [cbda_value, cbda_value_u], [cbn_value, cbn_value_u],
                    [cbna_value, cbna_value_u], [d9_thc_value, d9_thc_value_u], [thca_value, thca_value_u],
                    [d8_thc_value, d8_thc_value_u]]

    def create_single_deluxe_table(self, data, sample_type):
        recov_data = self.get_standard_recovery_values('Deluxe')
        if sample_type == 'Percent':
            sample_type = r'\%'
        elif sample_type == 'mg_g':
            sample_type = 'mg/g'
        elif sample_type == 'mg_ml':
            sample_type = 'mg/mL'
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
$\Delta^{9}$-THC & """ + data[11] + r""" & ND & """ + recov_data[11] + r"""& 0.003\\
$\Delta^{9}$-THC Acid & """ + data[16] + r""" & ND & """ + recov_data[16] + r"""& 0.003\\
\hline
\hline
\textbf{Total THC*} &  \textbf{""" + str(float(data[11]) + (float(data[16]) * 0.877)) + r"""} & & &\\
\hline
\hline
$\Delta^{8}$THC & """ + data[12] + r""" & ND & """ + recov_data[12] + r"""& 0.003\\
$\Delta^{8}$THC Acid & N/A & N/A & N/A & N/A \\
\hline
Cannabidiol (CBC) & """ + data[14] + r"""  & ND& """ + recov_data[14] + r"""& 0.003\\
Cannabidiol Acid & """ + data[18] + r"""  & ND & """ + recov_data[18] + r"""& 0.003\\
\hline
Cannabidiol (CBD) &""" + data[5] + r""" &  ND & """ + recov_data[5] + r"""& 0.003\\
Cannabidiol Acid & """ + data[7] + r""" &  ND & """ + recov_data[7] + r"""& 0.003\\
\hline
\hline
\textbf{Total CBD**} &  \textbf{""" + str(float(data[5]) + (float(data[7]) * 0.877)) + r"""} & & &\\
\hline
\hline
Cannabigerol (CBG) & """ + data[6] + r""" & ND & """ + recov_data[6] + r"""& 0.003\\
Cannabigerol Acid & """ + data[9] + r""" & ND & """ + recov_data[9] + r"""& 0.003\\
\hline
Cannabicyclol (CBL) & """ + data[13] + r""" &  ND & """ + recov_data[13] + r"""& 0.003\\
Cannabicyclol Acid & """ + data[17] + r""" &  ND & """ + recov_data[17] + r"""& 0.003\\
\hline
Cannabidivarin (CBDV) & """ + data[1] + r""" &  ND & """ + recov_data[1] + r"""& 0.003\\
Cannabidivarin Acid & """ + data[2] + r""" &  ND & """ + recov_data[2] + r"""& 0.003\\
\hline
$\Delta^{9}$ THCV & """ + data[3] + r""" &  ND& """ + recov_data[3] + r"""& 0.003\\
$\Delta^{9}$ THCV Acid &  """ + data[10] + r""" &  ND & """ + recov_data[10] + r"""& 0.003\\
\hline
Cannabinol (CBN) & """ + data[8] + r""" &   ND & """ + recov_data[8] + r"""& 0.003\\
Cannabinol Acid & """ + data[15] + r""" &  ND & """ + recov_data[15] + r"""& 0.003 \\
\hline
Cannabigerivarin Acid & """ + data[4] + r""" &  ND & """ + recov_data[4] + r"""& 0.003 \\
\hline
\hline
\textbf{Moisture} & 0.00  &   &  &\\
\hline
\hline
\end{tabular}
\end{table}
"""
        return deluxe_potency_table_string

    def create_single_deluxe_table_unit(self, data):
        recov_data = self.get_standard_recovery_values('Deluxe')
        sample_type = 'mg/unit'
        deluxe_potency_table_string = r"""
\newline
\renewcommand{\arraystretch}{1.2}
\begin{table}[h!]\centering
\begin{tabular}{p{\dimexpr0.270\textwidth-2\tabcolsep-\arrayrulewidth\relax}|
                p{\dimexpr0.245\textwidth-2\tabcolsep-\arrayrulewidth\relax}|
                p{\dimexpr0.245\textwidth-2\tabcolsep-\arrayrulewidth\relax}|
                p{\dimexpr0.08\textwidth-2\tabcolsep-\arrayrulewidth\relax}
                p{\dimexpr0.08\textwidth-2\tabcolsep-\arrayrulewidth\relax}
                p{\dimexpr0.08\textwidth-2\tabcolsep-\arrayrulewidth\relax}
                }
\textbf{Cannabinoids} & \textbf{Sample 1} (mg/g)  & \textbf{Sample 1} (""" + sample_type + r""")  & \textbf{LB} (\%) & \textbf{RR} (\%) & \textbf{LOQ} (\%)\\
\hline
\hline
$\Delta^{9}$-THC & """ + data[11][0] + r""" &  """ + data[11][1] + r""" & ND & """ + recov_data[11] + r"""& 0.003\\
$\Delta^{9}$-THC Acid & """ + data[16][0] + r""" &  """ + data[16][1] + r""" & ND & """ + recov_data[16] + r"""& 0.003\\
\hline
\hline
\textbf{Total THC*} &  \textbf{""" + str(float(data[11][0]) + (float(data[16][0]) * 0.877)) + r"""} & \textbf{ """ + str(float(data[11][1]) + (float(data[16][1]) * 0.877)) + r"""} & & &\\
\hline
\hline
$\Delta^{8}$THC & """ + data[12][0] + r""" &  """ + data[12][1] + r""" & ND & """ + recov_data[12] + r"""& 0.003\\
$\Delta^{8}$THC Acid & ND & ND & 96.6 & 0.003\\
\hline
Cannabidiol (CBC) & """ + data[14][0] + r""" &  """ + data[14][1] + r"""  & ND & """ + recov_data[14] + r"""& 0.003\\
Cannabidiol Acid & """ + data[18][0] + r""" &  """ + data[18][1] + r"""  & ND & """ + recov_data[18] + r"""& 0.003\\
\hline
Cannabidiol (CBD) &""" + data[5][0] + r""" &  """ + data[5][1] + r""" &  ND & """ + recov_data[5] + r"""& 0.003\\
Cannabidiol Acid & """ + data[7][0] + r""" &  """ + data[7][1] + r""" &  ND & """ + recov_data[7] + r"""& 0.003\\
\hline
\hline
\textbf{Total CBD**} &  \textbf{""" + str(float(data[5][0]) + (float(data[7][0]) * 0.877)) + r"""} & \textbf{ """ + str(float(data[5][0]) + (float(data[7][0]) * 0.877)) + r"""} & & &\\
\hline
\hline
Cannabigerol (CBG) & """ + data[6][0] + r""" &  """ + data[6][1] + r""" & ND & """ + recov_data[6] + r"""& 0.003\\
Cannabigerol Acid & """ + data[9][0] + r""" &  """ + data[9][1] + r""" & ND & """ + recov_data[9] + r"""& 0.003\\
\hline
Cannabicyclol (CBL) & """ + data[13][0] + r""" &  """ + data[13][1] + r""" &  ND & """ + recov_data[13] + r"""& 0.003\\
Cannabicyclol Acid & """ + data[17][0] + r""" &  """ + data[17][1] + r""" &  ND & """ + recov_data[17] + r"""& 0.003\\
\hline
Cannabidivarin (CBDV) & """ + data[1][0] + r""" &  """ + data[1][1] + r""" &  ND & """ + recov_data[1] + r"""& 0.003\\
Cannabidivarin Acid & """ + data[2][0] + r""" &  """ + data[2][1] + r""" &  ND & """ + recov_data[2] + r"""& 0.003\\
\hline
$\Delta^{9}$ THCV & """ + data[3][0] + r""" &  """ + data[3][1] + r""" &  ND & """ + recov_data[3] + r"""& 0.003\\
$\Delta^{9}$ THCV Acid &  """ + data[10][0] + r""" &  """ + data[10][1] + r""" &  ND & """ + recov_data[10] + r"""& 0.003\\
\hline
Cannabinol (CBN) & """ + data[8][0] + r""" &  """ + data[8][1] + r""" &   ND & """ + recov_data[8] + r"""& 0.003\\
Cannabinol Acid & """ + data[15][0] + r""" &  """ + data[15][1] + r""" &  ND & """ + recov_data[15] + r"""& 0.003 \\
\hline
Cannabigerivarin Acid & """ + data[4][0] + r""" &  """ + data[4][1] + r""" &  ND & """ + recov_data[4] + r"""& 0.003 \\
\hline
\hline
\textbf{Moisture} & 0.00  &   &  & \\
\hline
\hline
\end{tabular}
\end{table}
"""
        return deluxe_potency_table_string

    def create_single_basic_table(self, data, sample_type):
        recov_data = self.get_standard_recovery_values('Basic')
        if sample_type == 'Percent':
            sample_type = r'\%'
        elif sample_type == 'mg_g':
            sample_type = 'mg/g'
        elif sample_type == 'mg_mL':
            sample_type = 'mg/mL'
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
$\Delta^{9}$-THC & """ + data[5] + r""" & ND & """ + recov_data[5] + r"""& 0.003\\
$\Delta^{9}$-THC Acid & """ + data[6] + r""" & ND & """ + recov_data[6] + r"""& 0.003\\
\hline
$\Delta^{8}$-THC & """ + data[7] + r""" & ND & """ + recov_data[7] + r"""& 0.003\\
$\Delta^{8}$-THC Acid & 0.00 & N/A & N/A & N/A \\
\hline
Cannabidiol (CBD) &""" + data[1] + r""" &  ND & """ + recov_data[1] + r"""& 0.003\\
Cannabidiol Acid &""" + data[2] + r""" &  ND & """ + recov_data[2] + r"""& 0.003\\
\hline
\hline
Cannabinol (CBN) & """ + data[3] + r""" &   ND & """ + recov_data[3] + r"""& 0.003\\
Cannabinol Acid & """ + data[4] + r""" &   ND & """ + recov_data[4] + r"""& 0.003\\
\hline
\hline
\textbf{Moisture} & 0.00  &   &  &\\
\hline
\hline
\end{tabular}
\end{table}
"""
        return basic_potency_table_string

    def create_single_basic_table_unit(self, data):
        recov_data = self.get_standard_recovery_values('Basic')
        sample_type = 'mg/unit'
        basic_potency_table_string = r"""
\newline
\renewcommand{\arraystretch}{1.2}
\begin{table}[h!]\centering
\begin{tabular}{p{\dimexpr0.270\textwidth-2\tabcolsep-\arrayrulewidth\relax}|
                p{\dimexpr0.245\textwidth-2\tabcolsep-\arrayrulewidth\relax}|
                p{\dimexpr0.245\textwidth-2\tabcolsep-\arrayrulewidth\relax}|
                p{\dimexpr0.08\textwidth-2\tabcolsep-\arrayrulewidth\relax}
                p{\dimexpr0.08\textwidth-2\tabcolsep-\arrayrulewidth\relax}
                p{\dimexpr0.08\textwidth-2\tabcolsep-\arrayrulewidth\relax}
                }
\textbf{Cannabinoids} & \textbf{Sample 1} (mg/g) & \textbf{Sample 1} (""" + sample_type + r""")  & \textbf{LB} (\%) & \textbf{RR} (\%) & \textbf{LOQ} (\%)\\
\hline
\hline
$\Delta^{9}$ THC & """ + data[5][0] + r""" &  """ + data[5][1] + r""" &  ND & """ + recov_data[5] + r"""& 0.003\\
$\Delta^{9}$ THC Acid &  """ + data[6][0] + r""" &  """ + data[6][1] + r""" &  ND & """ + recov_data[6] + r"""& 0.003\\
\hline
$\Delta^{8}$ THC & """ + data[7][0] + r""" &  """ + data[7][1] + r""" &  ND & """ + recov_data[7] + r"""& 0.003\\
$\Delta^{8}$ THC Acid &  0.00  &  0.00 &  ND & 100  & 0.003\\
\hline
Cannabidiol (CBD) &""" + data[1][0] + r""" &  """ + data[1][1] + r""" &  ND & """ + recov_data[1] + r"""& 0.003\\
Cannabidiol Acid &""" + data[2][0] + r""" &  """ + data[2][1] + r""" &  ND & """ + recov_data[2] + r"""& 0.003\\
\hline
Cannabinol (CBN) & """ + data[3][0] + r""" &  """ + data[3][1] + r""" &   ND & """ + recov_data[3] + r"""& 0.003\\
Cannabinol Acid & """ + data[4][0] + r""" &  """ + data[4][1] + r""" &   ND & """ + recov_data[4] + r"""& 0.003\\
\hline
\hline
\textbf{Moisture} & 0.00  &   &  &\\
\hline
\hline
\end{tabular}
\end{table}
"""
        return basic_potency_table_string

# MULTIPLE SAMPLES PER PAGE CODE

    def generate_multi_sample_reports(self):
        multi_tuple_list = []
        for key in self.header_data.header_contents_dictionary.keys():
            matching = [(bob, marley) for bob, marley in self.multiple_reports_dictionary.items() if str(key)[0:6] in str(bob)]
            multi_tuple_list.append(matching)
        for item in multi_tuple_list:
            self.determine_number_of_pages_for_multi_reports(item)

    def determine_number_of_pages_for_multi_reports(self, tuple_list):
        number_of_samples = len(tuple_list)
        if number_of_samples == 1:
            self.single_reports_dictionary[tuple_list[0][0]] = tuple_list[0][1]
        elif 5 >= number_of_samples > 1:
            sample_id = tuple_list[0][0][0:6]
            header = self.latex_header_and_sample_list_dictionary[sample_id]
            table_string = self.single_page_multi_table(tuple_list)
            footer = self.generate_footer()
            report = header + table_string + footer
            self.finished_reports_dictionary[sample_id] = report
        else:
            self.multiple_page_multi_table(tuple_list)

    def single_page_multi_table(self, tuple_list):
        table_header_string = self.generate_single_page_multi_table_header(tuple_list)
        main_table_string = self.generate_single_page_multi_table(tuple_list, table_header_string)
        end_string = r"""
\hline
\hline
\textbf{Moisture} & 0.00  &   &  &\\
\hline
\hline
\end{tabular}
\end{table}"""
        main_table_string += end_string
        return main_table_string

    def generate_single_page_multi_table_header(self, tuple_list):
        table_header_1 = r"""
\newline
\renewcommand{\arraystretch}{1.2}
\begin{table}[h!]\centering
\begin{tabular}{p{\dimexpr0.270\textwidth-2\tabcolsep-\arrayrulewidth\relax}|"""
        header_slot_modifier = 0.490 / len(tuple_list)
        header_slot_line = r"""p{\dimexpr""" +\
                           str(header_slot_modifier) +\
                           r"""\textwidth-2\tabcolsep-\arrayrulewidth\relax}|"""
        for i in range(len(tuple_list)):
            table_header_1 += header_slot_line
        table_header_2 = r"""
                p{\dimexpr0.08\textwidth-2\tabcolsep-\arrayrulewidth\relax}
                p{\dimexpr0.08\textwidth-2\tabcolsep-\arrayrulewidth\relax}
                p{\dimexpr0.08\textwidth-2\tabcolsep-\arrayrulewidth\relax}
                }
                \textbf{Cannabinoids} & """
        table_header_1 += table_header_2
        for item in tuple_list:
            sampleid = item[0]
            if item[1][0] == 'Percent':
                unit = r"""\%"""
            elif item[1][0] == 'mg/g':
                unit = r"""mg/g"""
            elif item[1][0] == 'mg/mL':
                unit = r"""mg/mL"""
            else:
                unit = r"""\%"""
            sampleid_slot_line = r""" \textbf{Sample """ + sampleid[-1] + r"""} (""" + unit + r""")  &"""
            table_header_1 += sampleid_slot_line
        table_header_3 = r"""\textbf{LB} (\%) & \textbf{RR} (\%) & \textbf{LOQ} (\%)\\
\hline
\hline
"""
        table_header_1 += table_header_3
        return table_header_1

    def generate_single_page_multi_table(self, tuple_list, table_header_string):
        table_header_string += self.generate_single_page_multi_table_line(1, tuple_list)
        table_header_string += self.generate_single_page_multi_table_line(2, tuple_list)
        table_header_string += self.generate_single_page_multi_table_line(3, tuple_list)
        table_header_string += self.generate_single_page_multi_table_line(4, tuple_list)
        table_header_string += self.generate_single_page_multi_table_line(5, tuple_list)
        table_header_string += self.generate_single_page_multi_table_line(6, tuple_list)
        table_header_string += self.generate_single_page_multi_table_line(7, tuple_list)
        table_header_string += self.generate_single_page_multi_table_line(8, tuple_list)
        table_header_string += self.generate_single_page_multi_table_line(9, tuple_list)
        table_header_string += self.generate_single_page_multi_table_line(10, tuple_list)
        table_header_string += self.generate_single_page_multi_table_line(11, tuple_list)
        table_header_string += self.generate_single_page_multi_table_line(12, tuple_list)
        table_header_string += self.generate_single_page_multi_table_line(13, tuple_list)
        table_header_string += self.generate_single_page_multi_table_line(14, tuple_list)
        table_header_string += self.generate_single_page_multi_table_line(15, tuple_list)
        table_header_string += self.generate_single_page_multi_table_line(16, tuple_list)
        table_header_string += self.generate_single_page_multi_table_line(17, tuple_list)
        table_header_string += self.generate_single_page_multi_table_line(18, tuple_list)
        return table_header_string

    def generate_single_page_multi_table_line(self, cannabinoid, tuple_list):
        cannabinoid_latex_string = self.cannabinoid_dictionary[cannabinoid][0]
        cannabinoid_id_17 = self.cannabinoid_dictionary[cannabinoid][1]
        for item in tuple_list:
            sampleid = item[0]
            if item[1][0] == 'Percent':
                data_column = 'percentage_concentration'
            elif item[1][0] == 'mg/g':
                data_column = r"""mg_g"""
            elif item[1][0] == 'mg/mL':
                data_column = r"""mg_ml"""
            else:
                data_column = 'percentage_concentration'
            if item[1][1] == 'Basic' and cannabinoid in [4, 5, 8, 9, 10, 11, 12, 13, 14, 15, 18]:
                data_value = '-'
            else:
                data_value = "{0:.3f}".format(
                    self.sample_data.samples_data_frame.loc[
                        (self.sample_data.samples_data_frame['id17'] == cannabinoid_id_17)
                        & (self.sample_data.samples_data_frame['sampleid'] == sampleid),
                        [data_column]].iloc[0][data_column])
            data_value = data_value + " &"
            cannabinoid_latex_string += data_value
        cannabinoid_recovery_value = "{0:.3f}".format(self.sample_data.best_recovery_qc_data_frame.loc[
                                                      self.sample_data.best_recovery_qc_data_frame['id17'] ==
                                                      cannabinoid_id_17,
                                                      ['percrecovery']].iloc[0]['percrecovery'])
        cannabinoid_latex_string += r"""ND & """ + cannabinoid_recovery_value + r"""& 0.003\\"""
        return cannabinoid_latex_string

    def multiple_page_multi_table(self, tuple_list):
        pass

# FOOTER AND WRITING TO FILE CODE

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
