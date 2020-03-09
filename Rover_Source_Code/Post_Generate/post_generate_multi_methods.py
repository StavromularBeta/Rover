class MultiMethods:

    def __init__(self,
                 header_contents_dictionary,
                 multiple_reports_dictionary,
                 single_reports_dictionary,
                 latex_header_and_sample_list_dictionary,
                 sample_data,
                 cannabinoid_dictionary,
                 loq_dictionary
                 ):
        self.header_contents_dictionary = header_contents_dictionary
        self.multiple_reports_dictionary = multiple_reports_dictionary
        self.single_reports_dictionary = single_reports_dictionary
        self.latex_header_and_sample_list_dictionary = latex_header_and_sample_list_dictionary
        self.sample_data = sample_data
        self.cannabinoid_dictionary = cannabinoid_dictionary
        self.loq_dictionary = loq_dictionary
        self.finished_reports_dictionary = {}

    def generate_multi_sample_reports(self):
        multi_tuple_list = []
        for key in self.header_contents_dictionary.keys():
            matching = [(bob, marley) for bob, marley in self.multiple_reports_dictionary.items() if str(key)[0:6] in str(bob)]
            multi_tuple_list.append(matching)
        for item in multi_tuple_list:
            self.determine_number_of_pages_for_multi_reports(item)
        return self.single_reports_dictionary, self.finished_reports_dictionary

    def determine_number_of_pages_for_multi_reports(self, tuple_list):
        print(tuple_list)
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
            elif item[1][0] == 'per unit':
                unit = r"""mg/g) (mg/unit"""
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
            elif item[1][0] == 'per unit':
                data_column = r"""mg_unit"""
            else:
                data_column = 'percentage_concentration'
            if item[1][1] == 'Basic' and cannabinoid in [4, 5, 8, 9, 10, 11, 12, 13, 14, 15, 18]:
                data_value = '-'
            elif data_column == r"""mg_unit""":
                data_value_1 = "{0:.3f}".format(
                    self.sample_data.samples_data_frame.loc[
                        (self.sample_data.samples_data_frame['id17'] == cannabinoid_id_17)
                        & (self.sample_data.samples_data_frame['sampleid'] == sampleid),
                        ["mg_g"]].iloc[0]["mg_g"])
                data_value_2 = "{0:.3f}".format(
                    self.sample_data.samples_data_frame.loc[
                        (self.sample_data.samples_data_frame['id17'] == cannabinoid_id_17)
                        & (self.sample_data.samples_data_frame['sampleid'] == sampleid),
                        [data_column]].iloc[0][data_column])
                data_value = data_value_1 + r" / " + data_value_2
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
        loq_value = self.loq_dictionary[int(cannabinoid_id_17-1)]
        cannabinoid_latex_string += r"""ND & """ + cannabinoid_recovery_value + r"""&""" + loq_value + r"""\\"""
        return cannabinoid_latex_string

    def multiple_page_multi_table(self, tuple_list):
        pass

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