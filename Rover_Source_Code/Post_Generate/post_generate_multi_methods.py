class MultiMethods:
    """This class contains the methods that make multi-sample reports - that is, jobs with more than one sample on the
    report. """

    def __init__(self,
                 header_contents_dictionary,
                 multiple_reports_dictionary,
                 single_reports_dictionary,
                 latex_header_and_sample_list_dictionary,
                 sample_data,
                 cannabinoid_dictionary,
                 loq_dictionary):
        """
        1. header_contents_dictionary = header contents for all of the jobs in the batch, updated and finalized.
        2. multiple_reports_dictionary = key: jobnumber (full number), value: list of modifiers like single/basic, the
        units and relevant unit/density values, single/multi status, etc.
        3. single_reports_dictionary = the same as above, but for one-sample reports.
        4. latex_header_and_sample_list_dictionary = finished latex headers and sample lists.
        5. sample_data = the actual sample data, with post_generate data columns added.
        6. cannabinoid_dictionary = a conversion dictionary necessary because the running order of the analytes is
        different to the reporting order, so id17 wont match up with table line number. This dict. has key: table order,
        value = [latex, id17].
        7. loq_dictionary = a dictionary for LOQ's, when we actually figure some out. S_o would work for this dict also.
        key: table order, value = LOQ. this dictionary will end up being the last column in the table.
        8 . finished_reports_dictionary = key:jobnumber, value: finished report.
        """
        self.header_contents_dictionary = header_contents_dictionary
        self.multiple_reports_dictionary = multiple_reports_dictionary
        self.single_reports_dictionary = single_reports_dictionary
        self.latex_header_and_sample_list_dictionary = latex_header_and_sample_list_dictionary
        self.sample_data = sample_data
        self.cannabinoid_dictionary = cannabinoid_dictionary
        self.loq_dictionary = loq_dictionary
        self.finished_reports_dictionary = {}

    def generate_multi_sample_reports(self):
        """groups all of the various subjobs together. the first for loop collects the various samples for a given job
        into a list and then appends that list to the multi_tuple_list. the multi_tuple_list is iterated through in the
        next loop and the jobs are sent to determine_number_of_pages_for_multi_reports. """
        multi_tuple_list = []
        for key in self.header_contents_dictionary.keys():
            matching = [(bob, marley) for bob, marley in self.multiple_reports_dictionary.items() if str(key)[0:6] in str(bob)]
            multi_tuple_list.append(matching)
        new_multi_tuple_list = []
        for item in multi_tuple_list:
            new_sub_list = []
            for subitem in item:
                if subitem[1][0] == 'per unit':
                    new_tuple_entry = (subitem[0], ['mg/g', subitem[1][1], subitem[1][2], subitem[1][3]])
                    new_sub_list.append(new_tuple_entry)
                    new_sub_list.append(subitem)
                elif subitem[1][0] == 'mg/mL':
                    new_tuple_entry = (subitem[0], ['Percent', subitem[1][1], subitem[1][2], subitem[1][3]])
                    new_sub_list.append(subitem)
                    new_sub_list.append(new_tuple_entry)
                elif subitem[1][0] == 'mg/g':
                    new_tuple_entry = (subitem[0], ['Percent', subitem[1][1], subitem[1][2], subitem[1][3]])
                    new_sub_list.append(subitem)
                    new_sub_list.append(new_tuple_entry)
                else:
                    new_sub_list.append(subitem)
            new_multi_tuple_list.append(new_sub_list)
        for item in new_multi_tuple_list:
            self.determine_number_of_pages_for_multi_reports(item)
        return self.single_reports_dictionary, self.finished_reports_dictionary

    def determine_number_of_pages_for_multi_reports(self, tuple_list):
        number_of_samples = len(tuple_list)
        if number_of_samples == 0:
            pass
        elif 5 >= number_of_samples > 0:
            sample_id = tuple_list[0][0][0:6]
            header = self.latex_header_and_sample_list_dictionary[sample_id]
            table_string = self.single_page_multi_table(tuple_list)
            footer = self.generate_footer()
            report = header + table_string + footer
            self.finished_reports_dictionary[sample_id] = report
        else:
            sample_id = tuple_list[0][0][0:6]
            header = self.latex_header_and_sample_list_dictionary[sample_id]
            table_strings = self.multiple_page_multi_table(tuple_list)
            footer = self.generate_footer()
            for item in table_strings:
                header += item
                header += r'\newpage'
            header = header[:-8]
            report = header + footer
            self.finished_reports_dictionary[sample_id] = report

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

    def multiple_page_multi_table(self, tuple_list):
        counter = 0
        tuple_list_list = []
        add_list = []
        for item in tuple_list:
            if counter >= 4:
                counter = 0
                tuple_list_list.append(add_list)
                add_list = []
            add_list.append(item)
            counter += 1
        tuple_list_list.append(add_list)
        latex_tables_list = []
        for item in tuple_list_list:
            table_header_string = self.generate_single_page_multi_table_header(item)
            main_table_string = self.generate_single_page_multi_table(item, table_header_string)
            end_string = r"""
\hline
\hline
\textbf{Moisture} & 0.00  &   &  &\\
\hline
\hline
\end{tabular}
\end{table}"""
            main_table_string += end_string
            latex_tables_list.append(main_table_string)
        return latex_tables_list

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
        unit_line_start = " & "
        for item in tuple_list:
            sampleid = item[0]
            if item[1][0] == 'Percent':
                unit = r"""\%"""
            elif item[1][0] == 'mg/g':
                unit = r"""mg/g"""
            elif item[1][0] == 'mg/mL':
                unit = r"""mg/mL"""
            elif item[1][0] == 'per unit':
                unit = r"""mg/unit"""
            else:
                unit = r"""\%"""
            sampleid_slot_line = r""" \textbf{Sample """ + sampleid[-1] + r"""}  &"""
            table_header_1 += sampleid_slot_line
            unit_line = r""" (""" + unit + r""")  &"""
            unit_line_start += unit_line
        table_header_3 = r"""\textbf{LB} & \textbf{RR} & \textbf{LOQ} \\"""
        table_header_1 += table_header_3
        table_header_1 += unit_line_start + r""" (\%) & (\%) & (\%) \\
\hline
\hline"""
        return table_header_1

    def generate_single_page_multi_table(self, tuple_list, table_header_string):
        table_header_string += self.generate_single_page_multi_table_line(1, tuple_list)
        table_header_string += self.generate_single_page_multi_table_line(2, tuple_list)
        table_header_string += r' \hline '
        table_header_string += r' \hline '
        table_header_string += self.generate_total_line(1, 2, tuple_list)
        table_header_string += r' \hline '
        table_header_string += r' \hline '
        table_header_string += self.generate_single_page_multi_table_line(3, tuple_list)
        table_header_string += r' \hline '
        table_header_string += self.generate_single_page_multi_table_line(4, tuple_list)
        table_header_string += self.generate_single_page_multi_table_line(5, tuple_list)
        table_header_string += r' \hline '
        table_header_string += self.generate_single_page_multi_table_line(6, tuple_list)
        table_header_string += self.generate_single_page_multi_table_line(7, tuple_list)
        table_header_string += r' \hline '
        table_header_string += r' \hline '
        table_header_string += self.generate_total_line(6, 7, tuple_list)
        table_header_string += r' \hline '
        table_header_string += r' \hline '
        table_header_string += self.generate_single_page_multi_table_line(8, tuple_list)
        table_header_string += self.generate_single_page_multi_table_line(9, tuple_list)
        table_header_string += r' \hline '
        table_header_string += self.generate_single_page_multi_table_line(10, tuple_list)
        table_header_string += self.generate_single_page_multi_table_line(11, tuple_list)
        table_header_string += r' \hline '
        table_header_string += self.generate_single_page_multi_table_line(12, tuple_list)
        table_header_string += self.generate_single_page_multi_table_line(13, tuple_list)
        table_header_string += r' \hline '
        table_header_string += self.generate_single_page_multi_table_line(14, tuple_list)
        table_header_string += self.generate_single_page_multi_table_line(15, tuple_list)
        table_header_string += r' \hline '
        table_header_string += self.generate_single_page_multi_table_line(16, tuple_list)
        table_header_string += self.generate_single_page_multi_table_line(17, tuple_list)
        table_header_string += r' \hline '
        table_header_string += self.generate_single_page_multi_table_line(18, tuple_list)
        return table_header_string

    def generate_total_line(self, cannabinoid, cannabinoid_acid, tuple_list):
        if cannabinoid == 1:
            cannabinoid_latex_string = r'\textbf{Total THC*} &'
        elif cannabinoid == 6:
            cannabinoid_latex_string = r'\textbf{Total CBD**} &'
        else:
            cannabinoid_latex_string = r'Something is wrong &'
        cannabinoid_id_17 = self.cannabinoid_dictionary[cannabinoid][1]
        cannabinoid_acid_id_17 = self.cannabinoid_dictionary[cannabinoid_acid][1]
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
            data_value = float(self.sample_data.samples_data_frame.loc[
                             (self.sample_data.samples_data_frame['id17'] == cannabinoid_id_17)
                             & (self.sample_data.samples_data_frame['sampleid'] == sampleid),
                             [data_column]].iloc[0][data_column]) + float(self.sample_data.samples_data_frame.loc[
                                (self.sample_data.samples_data_frame['id17'] == cannabinoid_acid_id_17)
                                & (self.sample_data.samples_data_frame['sampleid'] == sampleid),
                                [data_column]].iloc[0][data_column] * 0.877)
            if 100 > data_value >= 1:
                data_value = str(data_value)[0:4]
            elif 1 > data_value > 0:
                data_value = str(data_value)[0:5]
            elif data_value > 100:
                data_value = str(data_value)[0:3]
            else:
                data_value = 'ND'
            data_value = r"\textbf{" + data_value + "} &"
            cannabinoid_latex_string += data_value
        cannabinoid_latex_string += r"""\\"""
        return cannabinoid_latex_string

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
            data_value = self.sample_data.samples_data_frame.loc[
                        (self.sample_data.samples_data_frame['id17'] == cannabinoid_id_17)
                        & (self.sample_data.samples_data_frame['sampleid'] == sampleid),
                        [data_column]].iloc[0][data_column]
            if 100 > data_value >= 1:
                data_value = str(data_value)[0:4]
            elif 1 > data_value > 0:
                data_value = str(data_value)[0:5]
            else:
                data_value = 'ND'
            data_value = data_value + " &"
            cannabinoid_latex_string += data_value
        cannabinoid_recovery_value = str(self.sample_data.best_recovery_qc_data_frame.loc[
                                         self.sample_data.best_recovery_qc_data_frame['id17'] ==
                                         cannabinoid_id_17,
                                         ['percrecovery']].iloc[0]['percrecovery'])
        loq_value = self.loq_dictionary[int(cannabinoid_id_17-1)]
        cannabinoid_latex_string += r"""ND & """ + cannabinoid_recovery_value + r"""&""" + loq_value + r"""\\"""
        return cannabinoid_latex_string

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