import math

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
                 mushrooms_dictionary,
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
        self.mushrooms_dictionary = mushrooms_dictionary
        self.loq_dictionary = loq_dictionary
        self.finished_reports_dictionary = {}

    def generate_multi_sample_reports(self, instrument_type):
        """groups all of the various subjobs together. the first for loop collects the various samples for a given job
        into a list and then appends that list to the multi_tuple_list. The second for loop adds the extra column in the
        table required if samples are to be reported in two different units. For example, a cannabis cookie needs to
        be reported in mg/g, and mg/cookie of analyte. The code to handle this is in the "if" part of the second for
        loop. the new_multi_tuple_list is iterated through in the last loop, and the jobs are sent to
        determine_number_of_pages_for_multi_reports. """
        multi_tuple_list = []
        for key in self.header_contents_dictionary.keys():
            matching = [(bob, marley) for bob, marley in self.multiple_reports_dictionary.items() if str(key)[0:6] in str(bob)]
            multi_tuple_list.append(matching)
        new_multi_tuple_list = []
        for item in multi_tuple_list:
            new_sub_list = []
            if instrument_type == "UPLCUV":
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
            else:
                for subitem in item:
                    if subitem[1][0] == 'per unit':
                        new_tuple_entry = (subitem[0], ['mg/g', subitem[1][1], subitem[1][2], subitem[1][3]])
                        new_sub_list.append(new_tuple_entry)
                        new_sub_list.append(subitem)
                    elif subitem[1][0] == 'mg/mL':
                        new_sub_list.append(subitem)
                    elif subitem[1][0] == 'mg/g':
                        new_sub_list.append(subitem)
                    else:
                        new_sub_list.append(subitem)
            new_multi_tuple_list.append(new_sub_list)
        for item in new_multi_tuple_list:
            self.determine_number_of_pages_for_multi_reports(item, instrument_type)
        return self.single_reports_dictionary, self.finished_reports_dictionary

    def determine_number_of_pages_for_multi_reports(self, tuple_list, instrument_type):
        """determines whether a given report can fit one one page/ has to be written on multiple pages. If there
        are no jobs requiring multiple samples per page, the first part of the if statement prevents the code from
        crashing. If there are more than 4 samples, we need multiple pages.
        This is pretty close to a 'controller' function for this class. If the job only needs one page, the code in
        the elif statement executes. a header, table, and footer are produced, combined, and added to the finished
        reports dictionary. If the job requires multiple pages, a header, multiple tables, and a footer are generated.
        each table is added to the header, along with a latex command that starts a new page after each table. When the
        footer is added, the last \newpage command is removed prior to its addition to the bulk of the report. This
        is then added to the finished reports dictionary.
        Note that if a job with one sample is selected as a 'multi' job at the GUI step, then it will be put through the
        multiple samples per job routine by default. It specifically has to be selected as a 'single' job to go through
        the single_methods class."""
        number_of_samples = len(tuple_list)
        if number_of_samples == 0:
            pass
        elif 4 >= number_of_samples > 0:
            sample_id = tuple_list[0][0][0:6]
            header = self.latex_header_and_sample_list_dictionary[sample_id]
            table_string = self.single_page_multi_table(tuple_list, instrument_type)
            footer = self.generate_footer(instrument_type)
            report = header + table_string + footer
            self.finished_reports_dictionary[sample_id] = report
        else:
            sample_id = tuple_list[0][0][0:6]
            header = self.latex_header_and_sample_list_dictionary[sample_id]
            table_strings = self.multiple_page_multi_table(tuple_list, instrument_type)
            footer = self.generate_footer(instrument_type)
            for item in table_strings:
                header += item
                header += r'\newpage\newgeometry{head=65pt, includehead=true, includefoot=true, margin=0.5in}'
            header = header[:-79]
            report = header + footer
            self.finished_reports_dictionary[sample_id] = report

    def single_page_multi_table(self, tuple_list, instrument_type):
        """combines the header of a table, to the main part of the table containing data. Then adds on the end string.
        returns the completed table."""
        table_header_string = self.generate_single_page_multi_table_header(tuple_list, instrument_type)
        main_table_string = self.generate_single_page_multi_table(tuple_list, table_header_string, instrument_type)
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

    def multiple_page_multi_table(self, tuple_list, instrument_type):
        """creates multiple tables. adds items in the tuple_list to the add_list. Every 4 items, it adds the add_list
        to the tuple_list_list and clears the add_list. Each add_list represents the samples going into one table. It
        then iterates through the tuple_list_list, and each list gets converted into a table, and added to
        latex_tables_list, which is a list of latex code. This list of latex tables is returned by the function."""
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
            table_header_string = self.generate_single_page_multi_table_header(item, instrument_type)
            main_table_string = self.generate_single_page_multi_table(item, table_header_string, instrument_type)
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

    def generate_single_page_multi_table_header(self, tuple_list, instrument_type):
        """creates the table headers. table_header_1 is the first part of the latex table, sets up the tabular
        environment. The width of the columns for cannabinoid names, blank, Recovery, and So are fixed. the remainder
        of the space of the table (49%) is divided between up to four sample columns. This is accomplished by dividing
        0.490 by the length of the list of samples, creating the appropriately spaced tabular entry, and then adding
        as many of these lines as there are samples. The second half of this function puts the units of each column
        below the name of each column. """
        table_header_1 = r"""
\renewcommand{\arraystretch}{1.2}
\begin{table}[h!]\centering
\small
\begin{tabular}{p{\dimexpr0.250\textwidth-2\tabcolsep-\arrayrulewidth\relax}|"""
        header_slot_modifier = 0.510 / len(tuple_list)
        header_slot_line = r"""p{\dimexpr""" +\
                           str(header_slot_modifier) +\
                           r"""\textwidth-2\tabcolsep-\arrayrulewidth\relax}|"""
        for i in range(len(tuple_list)):
            table_header_1 += header_slot_line
        table_header_2 = r"""
                p{\dimexpr0.07\textwidth-2\tabcolsep-\arrayrulewidth\relax}
                p{\dimexpr0.1\textwidth-2\tabcolsep-\arrayrulewidth\relax}
                p{\dimexpr0.07\textwidth-2\tabcolsep-\arrayrulewidth\relax}
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
        if instrument_type == "UPLCUV":
            table_header_3 = r"""\textbf{\small Blank} & \textbf{\small Recovery} & $\mathbf{\small S_{0}}$ \\"""
        else:
            table_header_3 = r"""\textbf{\small Blank} & \textbf{\small Recovery} & $\mathbf{\small MDL}$ \\"""
        table_header_1 += table_header_3
        table_header_1 += unit_line_start + r""" (mg/g) & (\%) & (mg/g) \\
\hline
\hline"""
        return table_header_1

    def generate_single_page_multi_table(self, tuple_list, table_header_string, instrument_type):
        """creates the bulk of the table. The tables appearance is analogous to the way this function is laid out.
        each line is either a regular line, or total THC/CBD. Each of the two types of lines has its own function."""
        if instrument_type == "UPLCMS":
            table_header_string += '\n'
            table_header_string += self.generate_single_page_multi_table_line(1, tuple_list, True) + '\n'
            table_header_string += self.generate_single_page_multi_table_line(2, tuple_list, True) + '\n'
            table_header_string += self.generate_single_page_multi_table_line(3, tuple_list, True) + '\n'
        else:
            table_header_string += self.generate_single_page_multi_table_line(1, tuple_list) + '\n'
            table_header_string += self.generate_single_page_multi_table_line(2, tuple_list) + '\n'
            table_header_string += r' \hline ' + '\n'
            table_header_string += r' \hline ' + '\n'
            table_header_string += self.generate_total_line(1, 2, tuple_list) + '\n'
            table_header_string += r' \hline ' + '\n'
            table_header_string += r' \hline ' + '\n'
            table_header_string += self.generate_single_page_multi_table_line(3, tuple_list) + '\n'
            table_header_string += self.generate_single_page_multi_table_line("Delta8Acid", tuple_list) + '\n'
            table_header_string += r' \hline ' + '\n'
            table_header_string += self.generate_single_page_multi_table_line(4, tuple_list) + '\n'
            table_header_string += self.generate_single_page_multi_table_line(5, tuple_list) + '\n'
            table_header_string += r' \hline ' + '\n'
            table_header_string += self.generate_single_page_multi_table_line(6, tuple_list) + '\n'
            table_header_string += self.generate_single_page_multi_table_line(7, tuple_list) + '\n'
            table_header_string += r' \hline ' + '\n'
            table_header_string += r' \hline ' + '\n'
            table_header_string += self.generate_total_line(6, 7, tuple_list) + '\n'
            table_header_string += r' \hline ' + '\n'
            table_header_string += r' \hline ' + '\n'
            table_header_string += self.generate_single_page_multi_table_line(8, tuple_list) + '\n'
            table_header_string += self.generate_single_page_multi_table_line(9, tuple_list) + '\n'
            table_header_string += r' \hline ' + '\n'
            table_header_string += self.generate_single_page_multi_table_line(10, tuple_list) + '\n'
            table_header_string += self.generate_single_page_multi_table_line(11, tuple_list) + '\n'
            table_header_string += r' \hline ' + '\n'
            table_header_string += self.generate_single_page_multi_table_line(12, tuple_list) + '\n'
            table_header_string += self.generate_single_page_multi_table_line(13, tuple_list) + '\n'
            table_header_string += r' \hline ' + '\n'
            table_header_string += self.generate_single_page_multi_table_line(14, tuple_list) + '\n'
            table_header_string += self.generate_single_page_multi_table_line(15, tuple_list) + '\n'
            table_header_string += r' \hline ' + '\n'
            table_header_string += self.generate_single_page_multi_table_line(16, tuple_list) + '\n'
            table_header_string += self.generate_single_page_multi_table_line(17, tuple_list) + '\n'
            table_header_string += r' \hline ' + '\n'
            table_header_string += self.generate_single_page_multi_table_line("Cannabigerivarin_Acid", tuple_list) + '\n'
        return table_header_string

    def generate_total_line(self, cannabinoid, cannabinoid_acid, tuple_list):
        """there are two types of total lines, one for THC, and one for CBD. The first if statement determines which
        cannabinoid we want, and generates the latex name of the cannabinoid for the table. It then uses the
        cannabinoid dictionary to find the id17 of the cannabinoids we want. The next for loop determines which data
        columns to access, depending on the units- these data columns are generated by organize_methods.py, after the
        GUI step. The magic happens immediately below on line 272: the function grabs the data values with the correct
        sample ids and id17s from the samples_data_frame, and uses them in the total THC/CBD equation to generate the
        total value. The final if/elif statement gets the sigfigs/decimal places correct (mostly at this point,
        struggling with values between 10 and 1 and not sure why), and creates the latex line for the table. """
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
            data_value = self.sig_fig_and_rounding_for_values(data_value)
            data_value = r"\textbf{" + data_value + "} &"
            cannabinoid_latex_string += data_value
        cannabinoid_latex_string += r"""\\"""
        return cannabinoid_latex_string

    def generate_single_page_multi_table_line(self, cannabinoid, tuple_list, mushroom_report=False):
        """The first if statement deals with Delta8Acid, which we don't have a standard for. After that, the function
        essentially mirrors generate_total_line. Differences are that basic/deluxe has to be handled - on line 318,
        any cannabinoids that aren't required for a given sample are represented as a dash. The data value required is
        selected the same way as generate_total_line, except there is no need to add two values together, we just have
        to get one value. The last part of the function grabs the cannabinoid recovery value from the standard used by
        the batch. """
        if cannabinoid == "Delta8Acid":
            start = r"""$\Delta^{8}$THC Acid & """
            for item in tuple_list:
                start += r"""ND &"""
            start += r"""ND & N/A & N/A \\ """
            return start
        elif cannabinoid == "Cannabigerivarin_Acid":
            start = r"""Cannabigerivarin Acid & """
            for item in tuple_list:
                start += r"""ND &"""
            start += r"""ND & N/A & N/A \\ """
            return start
        elif cannabinoid == "Baeocystin":
            start = r"""Baeocystin * & """
            for item in tuple_list:
                start += r"""ND &"""
            start += r"""ND & N/A & 0.0003 \\ """
            return start
        if mushroom_report:
            cannabinoid_latex_string = self.mushrooms_dictionary[cannabinoid][0]
            cannabinoid_id_17 = self.mushrooms_dictionary[cannabinoid][1]
        else:
            cannabinoid_latex_string = self.cannabinoid_dictionary[cannabinoid][0]
            cannabinoid_id_17 = self.cannabinoid_dictionary[cannabinoid][1]
        for item in tuple_list:
            sampleid = item[0]
            if item[1][0] == 'Percent':
                if mushroom_report:
                    data_column = 'analconc'
                else:
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
            else:
                try:
                    data_value = self.sample_data.samples_data_frame.loc[
                                (self.sample_data.samples_data_frame['id17'] == cannabinoid_id_17)
                                & (self.sample_data.samples_data_frame['sampleid'].str.contains(sampleid)),
                                [data_column]].iloc[0][data_column]
                except IndexError:
                    data_value = "ND"
            data_value = self.sig_fig_and_rounding_for_values(data_value)
            data_value = data_value + " &"
            cannabinoid_latex_string += data_value
        if mushroom_report:
            cannabinoid_recovery_value = self.sample_data.recovery_data_frame.loc[
                                         self.sample_data.recovery_data_frame['id17'] ==
                                         cannabinoid_id_17,
                                         ['percrecovery']].iloc[0]['percrecovery']
        else:
            cannabinoid_recovery_value = self.sample_data.best_recovery_qc_data_frame.loc[
                                         self.sample_data.best_recovery_qc_data_frame['id17'] ==
                                         cannabinoid_id_17,
                                         ['percrecovery']].iloc[0]['percrecovery']
        cannabinoid_recovery_value = self.sig_fig_and_rounding_for_values(cannabinoid_recovery_value)
        if mushroom_report:
            loq_value = "0.0003"
        else:
            loq_value = self.loq_dictionary[int(cannabinoid_id_17-1)]
        cannabinoid_latex_string += r"""ND & """ + cannabinoid_recovery_value + r"""&""" + loq_value + r"""\\"""
        return cannabinoid_latex_string

    def generate_footer(self, instrument_type):
        """This function generates the latex footer that goes on the bottom of the reports. Contains information about
        the procedure and the variables in the table, liability stuff for the company, the footer for the company
        with the business name and the contact information, and also the spots for the senior chemist signatures
        on the reports. """
        if instrument_type == "UPLCUV":
            footer_string = r"""
Methods: solvent extraction; measured by UPLC-UV, tandem MS, P.I. 1.14 \& based on USP monograph 29 \newline
$\si{S_{o}}$ = standard deviation at zero analyte concentration. MDL generally considered to be 3x $\si{S_{o}}$ value. \newline\newline
ND = none detected. N/A = not applicable. THC = tetrahydrocannabinol.\newline 
\textbf{*Total THC} = $\Delta^{9}$-THC + (THCA x 0.877 ). \textbf{**Total CBD} = CBD + (CBDA x 0.877).\newline\newline
Material will be held for up to 3 weeks unless alternative arrangements have been made. Sample holding time may vary and is dependent on MBL license restrictions.
\newline\newline\newline
R. Bilodeau \phantom{aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaasasssssssssssss}H. Hartmann\\ Analytical Chemist: \underline{\hspace{3cm}}{ \hspace{3.2cm} Sr. Analytical Chemist: \underline{\hspace{3cm}}       
\end{document}
 """
        else:
            footer_string = r"""* Compound estimated based on psilocybin response; no standard available.\newline
Methods: solvent extraction; measured by UHPLC-ESI - tandem MSMS\newline\newline
\textbf{MDL} = Method Detection Limit.\phantom{aaaaaaaaaaaaaaaaaaaaalaaaaaa}\textbf{ND} = None Detected.\newline
\textbf{mg/g} = milligrams per gram (10 mg/g = 1.0\%)\phantom{aaaaaaaaaaaaaaa}\textbf{N/A} = Not Applicable.\newline\newline
Material will be held for up to 3 weeks unless alternate arrangements have been made.
\newline\newline\newline
R. Bilodeau \phantom{aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaasasssssssssssss}H. Hartmann\\ Analytical Chemist: \underline{\hspace{3cm}}{ \hspace{3.2cm} Sr. Analytical Chemist: \underline{\hspace{3cm}}    \end{document}
 """
        return footer_string

    def sig_fig_and_rounding_for_values(self, value):
        print(value)
        if value == '-':
            return value
        elif value == "ND":
            return value
        elif math.isnan(value):
            return "ND"
        string_value = str(value)
        split_string = string_value.split('.')
        pre_decimal = split_string[0]
        if len(pre_decimal) >= 3:
            value = int(round(value))
        elif len(pre_decimal) >= 2:
            value = round(value, 1)
        elif len(pre_decimal) == 1:
            if int(pre_decimal[0]) == 0:
                value = round(value, 3)
                if len(str(value)) == 4:
                    value = str(value) + '0'
            else:
                value = round(value, 2)
                if len(str(value)) == 3:
                    value = str(value) + '0'
        if value == 0.0:
            value = 'ND'
        return str(value)




