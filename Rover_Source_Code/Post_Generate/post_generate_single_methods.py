class SingleMethods:

    def __init__(self,
                 finished_reports_dictionary,
                 single_reports_dictionary,
                 sample_data,
                 latex_header_and_sample_list_dictionary,
                 loq_dictionary
                 ):
        self.finished_reports_dictionary = finished_reports_dictionary
        self.single_reports_dictionary = single_reports_dictionary
        self.sample_data = sample_data
        self.latex_header_and_sample_list_dictionary = latex_header_and_sample_list_dictionary
        self.loq_dictionary = loq_dictionary

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
        return self.finished_reports_dictionary

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
        temporary_data = self.get_relevant_values_and_recoveries_for_single_reports_unit(temporary_data_frame,
                                                                                         'Basic',
                                                                                         'density')
        temporary_table = self.create_single_basic_table_unit(temporary_data, 'density')
        header = self.latex_header_and_sample_list_dictionary[sample_id[0:6]]
        footer = self.generate_footer()
        report = header + temporary_table + footer
        self.finished_reports_dictionary[sample_id] = report

    def generate_single_mg_ml_deluxe_report(self, sample_id):
        temporary_data_frame = self.sample_data.samples_data_frame[self.sample_data.samples_data_frame['sampleid']
                                                                   == sample_id]
        temporary_data = self.get_relevant_values_and_recoveries_for_single_reports_unit(temporary_data_frame,
                                                                                         'Deluxe',
                                                                                         'density')
        temporary_table = self.create_single_deluxe_table_unit(temporary_data, 'density')
        header = self.latex_header_and_sample_list_dictionary[sample_id[0:6]]
        footer = self.generate_footer()
        report = header + temporary_table + footer
        self.finished_reports_dictionary[sample_id] = report

    def generate_single_unit_basic_report(self, sample_id):
        temporary_data_frame = self.sample_data.samples_data_frame[self.sample_data.samples_data_frame['sampleid']
                                                                   == sample_id]
        temporary_data = self.get_relevant_values_and_recoveries_for_single_reports_unit(temporary_data_frame,
                                                                                         'Basic',
                                                                                         'unit')
        temporary_table = self.create_single_basic_table_unit(temporary_data, 'unit')
        header = self.latex_header_and_sample_list_dictionary[sample_id[0:6]]
        footer = self.generate_footer()
        report = header + temporary_table + footer
        self.finished_reports_dictionary[sample_id] = report

    def generate_single_unit_deluxe_report(self, sample_id):
        temporary_data_frame = self.sample_data.samples_data_frame[self.sample_data.samples_data_frame['sampleid']
                                                                   == sample_id]
        temporary_data = self.get_relevant_values_and_recoveries_for_single_reports_unit(temporary_data_frame,
                                                                                         'Deluxe',
                                                                                         'unit')
        temporary_table = self.create_single_deluxe_table_unit(temporary_data, 'unit')
        header = self.latex_header_and_sample_list_dictionary[sample_id[0:6]]
        footer = self.generate_footer()
        report = header + temporary_table + footer
        self.finished_reports_dictionary[sample_id] = report

    def get_standard_recovery_values(self, report_type):
        temporary_data_frame = self.sample_data.best_recovery_qc_data_frame
        ibu_recovery_value = str(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 1.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        cbdv_value = str(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 2.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        cbdva_value = str(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 3.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        thcv_value = str(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 4.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        cbgva_value = str(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 5.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        cbd_value = str(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 6.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        cbg_value = str(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 7.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        cbda_value = str(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 8.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        cbn_value = str(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 9.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        cbga_value = str(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 10.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        thcva_value = str(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 11.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        d9_thc_value = str(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 12.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        d8_thc_value = str(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 13.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        cbl_value = str(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 14.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        cbc_value = str(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 15.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        cbna_value = str(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 16.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        thca_value = str(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 17.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        cbla_value = str(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 18.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        cbca_value = str(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 19.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        if report_type == 'Deluxe':
            return [ibu_recovery_value, cbdv_value, cbdva_value, thcv_value, cbgva_value, cbd_value, cbg_value,
                    cbda_value, cbn_value, cbga_value, thcva_value, d9_thc_value, d8_thc_value, cbl_value, cbc_value,
                    cbna_value, thca_value, cbla_value, cbca_value]
        else:
            return [ibu_recovery_value, cbd_value, cbda_value, cbn_value, cbna_value, d9_thc_value, thca_value,
                    d8_thc_value]

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
            return [ibu_recovery_value, cbd_value, cbda_value, cbn_value, cbna_value, d9_thc_value, thca_value,
                    d8_thc_value]

    def get_relevant_values_and_recoveries_for_single_reports_unit(self, temporary_data_frame, report_type, unit_type):
        if unit_type == 'unit':
            column_1 = 'mg_g'
            column_2 = 'mg_unit'
        elif unit_type == 'density':
            column_1 = 'mg_ml'
            column_2 = 'percentage_concentration'
        else:
            column_1 = 'percentage_concentration'
            column_2 = 'percentage_concentration'
        ibu_recovery_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 1.0,
                                     ['percrecovery']].iloc[0]['percrecovery'])
        cbdv_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 2.0,
                                     [column_1]].iloc[0][column_1])
        cbdva_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 3.0,
                                     [column_1]].iloc[0][column_1])
        thcv_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 4.0,
                                     [column_1]].iloc[0][column_1])
        cbgva_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 5.0,
                                     [column_1]].iloc[0][column_1])
        cbd_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 6.0,
                                     [column_1]].iloc[0][column_1])
        cbg_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 7.0,
                                     [column_1]].iloc[0][column_1])
        cbda_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 8.0,
                                     [column_1]].iloc[0][column_1])
        cbn_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 9.0,
                                     [column_1]].iloc[0][column_1])
        cbga_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 10.0,
                                     [column_1]].iloc[0][column_1])
        thcva_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 11.0,
                                     [column_1]].iloc[0][column_1])
        d9_thc_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 12.0,
                                     [column_1]].iloc[0][column_1])
        d8_thc_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 13.0,
                                     [column_1]].iloc[0][column_1])
        cbl_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 14.0,
                                     [column_1]].iloc[0][column_1])
        cbc_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 15.0,
                                     [column_1]].iloc[0][column_1])
        cbna_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 16.0,
                                     [column_1]].iloc[0][column_1])
        thca_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 17.0,
                                     [column_1]].iloc[0][column_1])
        cbla_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 18.0,
                                     [column_1]].iloc[0][column_1])
        cbca_value = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 19.0,
                                     [column_1]].iloc[0][column_1])
        # UNITS
        cbdv_value_u = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 2.0,
                                     [column_2]].iloc[0][column_2])
        cbdva_value_u = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 3.0,
                                     [column_2]].iloc[0][column_2])
        thcv_value_u = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 4.0,
                                     [column_2]].iloc[0][column_2])
        cbgva_value_u = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 5.0,
                                     [column_2]].iloc[0][column_2])
        cbd_value_u = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 6.0,
                                     [column_2]].iloc[0][column_2])
        cbg_value_u = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 7.0,
                                     [column_2]].iloc[0][column_2])
        cbda_value_u = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 8.0,
                                     [column_2]].iloc[0][column_2])
        cbn_value_u = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 9.0,
                                     [column_2]].iloc[0][column_2])
        cbga_value_u = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 10.0,
                                     [column_2]].iloc[0][column_2])
        thcva_value_u = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 11.0,
                                     [column_2]].iloc[0][column_2])
        d9_thc_value_u = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 12.0,
                                     [column_2]].iloc[0][column_2])
        d8_thc_value_u = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 13.0,
                                     [column_2]].iloc[0][column_2])
        cbl_value_u = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 14.0,
                                     [column_2]].iloc[0][column_2])
        cbc_value_u = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 15.0,
                                     [column_2]].iloc[0][column_2])
        cbna_value_u = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 16.0,
                                     [column_2]].iloc[0][column_2])
        thca_value_u = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 17.0,
                                     [column_2]].iloc[0][column_2])
        cbla_value_u = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 18.0,
                                     [column_2]].iloc[0][column_2])
        cbca_value_u = "{0:.3f}".format(
            temporary_data_frame.loc[temporary_data_frame['id17'] == 19.0,
                                     [column_2]].iloc[0][column_2])
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
    $\Delta^{9}$-THC & """ + data[11] + r""" & ND & """ + recov_data[11] + r"""& """ + self.loq_dictionary[11] + r"""\\
    $\Delta^{9}$-THC Acid & """ + data[16] + r""" & ND & """ + recov_data[16] + r"""& """ + self.loq_dictionary[16] + r"""\\
    \hline
    \hline
    \textbf{Total THC*} &  \textbf{""" + str(float(data[11]) + (float(data[16]) * 0.877)) + r"""} & & &\\
    \hline
    \hline
    $\Delta^{8}$THC & """ + data[12] + r""" & ND & """ + recov_data[12] + r"""& """ + self.loq_dictionary[12] + r"""\\
    $\Delta^{8}$THC Acid & N/A & N/A & N/A & N/A \\
    \hline
    Cannabidiol (CBC) & """ + data[14] + r"""  & ND& """ + recov_data[14] + r"""& """ + self.loq_dictionary[14] + r"""\\
    Cannabidiol Acid & """ + data[18] + r"""  & ND & """ + recov_data[18] + r"""& """ + self.loq_dictionary[18] + r"""\\
    \hline
    Cannabidiol (CBD) &""" + data[5] + r""" &  ND & """ + recov_data[5] + r"""& """ + self.loq_dictionary[5] + r"""\\
    Cannabidiol Acid & """ + data[7] + r""" &  ND & """ + recov_data[7] + r"""& """ + self.loq_dictionary[7] + r"""\\
    \hline
    \hline
    \textbf{Total CBD**} &  \textbf{""" + str(float(data[5]) + (float(data[7]) * 0.877)) + r"""} & & &\\
    \hline
    \hline
    Cannabigerol (CBG) & """ + data[6] + r""" & ND & """ + recov_data[6] + r"""& """ + self.loq_dictionary[6] + r"""\\
    Cannabigerol Acid & """ + data[9] + r""" & ND & """ + recov_data[9] + r"""& """ + self.loq_dictionary[9] + r"""\\
    \hline
    Cannabicyclol (CBL) & """ + data[13] + r""" &  ND & """ + recov_data[13] + r"""& """ + self.loq_dictionary[13] + r"""\\
    Cannabicyclol Acid & """ + data[17] + r""" &  ND & """ + recov_data[17] + r"""& """ + self.loq_dictionary[17] + r"""\\
    \hline
    Cannabidivarin (CBDV) & """ + data[1] + r""" &  ND & """ + recov_data[1] + r"""& """ + self.loq_dictionary[1] + r"""\\
    Cannabidivarin Acid & """ + data[2] + r""" &  ND & """ + recov_data[2] + r"""&""" + self.loq_dictionary[2] + r"""\\
    \hline
    $\Delta^{9}$ THCV & """ + data[3] + r""" &  ND& """ + recov_data[3] + r"""& """ + self.loq_dictionary[3] + r"""\\
    $\Delta^{9}$ THCV Acid &  """ + data[10] + r""" &  ND & """ + recov_data[10] + r"""& """ + self.loq_dictionary[10] + r"""\\
    \hline
    Cannabinol (CBN) & """ + data[8] + r""" &   ND & """ + recov_data[8] + r"""& """ + self.loq_dictionary[8] + r"""\\
    Cannabinol Acid & """ + data[15] + r""" &  ND & """ + recov_data[15] + r"""& """ + self.loq_dictionary[15] + r""" \\
    \hline
    Cannabigerivarin Acid & """ + data[4] + r""" &  ND & """ + recov_data[4] + r"""& """ + self.loq_dictionary[4] + r""" \\
    \hline
    \hline
    \textbf{Moisture} & 0.00  &   &  &\\
    \hline
    \hline
    \end{tabular}
    \end{table}
    """
        return deluxe_potency_table_string

    def create_single_deluxe_table_unit(self, data, unit_type):
        recov_data = self.get_standard_recovery_values('Deluxe')
        if unit_type == 'unit':
            sample_type_1 = 'mg/g'
            sample_type_2 = 'mg/unit'
        elif unit_type == 'density':
            sample_type_1 = 'mg/mL'
            sample_type_2 = r'\%'
        else:
            sample_type_1 = r'\%'
            sample_type_2 = r'\%'
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
    \textbf{Cannabinoids} & \textbf{Sample 1} (""" + sample_type_1 + r""")  & \textbf{Sample 1} (""" + sample_type_2 + r""")  & \textbf{LB} (\%) & \textbf{RR} (\%) & \textbf{LOQ} (\%)\\
    \hline
    \hline
    $\Delta^{9}$-THC & """ + data[11][0] + r""" &  """ + data[11][1] + r""" & ND & """ + recov_data[11] + r"""&""" + \
                                      self.loq_dictionary[11] + r"""\\
    $\Delta^{9}$-THC Acid & """ + data[16][0] + r""" &  """ + data[16][1] + r""" & ND & """ + recov_data[16] + r"""& """ + self.loq_dictionary[16] + r"""\\
    \hline
    \hline
    \textbf{Total THC*} &  \textbf{""" + str(
            float(data[11][0]) + (float(data[16][0]) * 0.877)) + r"""} & \textbf{ """ + str(
            float(data[11][1]) + (float(data[16][1]) * 0.877)) + r"""} & & &\\
    \hline
    \hline
    $\Delta^{8}$THC & """ + data[12][0] + r""" &  """ + data[12][1] + r""" & ND & """ + recov_data[12] + r"""& """ + \
                                      self.loq_dictionary[12] + r"""\\
    $\Delta^{8}$THC Acid & ND & ND & 96.6 & 0.003\\
    \hline
    Cannabidiol (CBC) & """ + data[14][0] + r""" &  """ + data[14][1] + r"""  & ND & """ + recov_data[14] + r"""& """ + \
                                      self.loq_dictionary[14] + r"""\\
    Cannabidiol Acid & """ + data[18][0] + r""" &  """ + data[18][1] + r"""  & ND & """ + recov_data[18] + r"""& """ + \
                                      self.loq_dictionary[18] + r"""\\
    \hline
    Cannabidiol (CBD) &""" + data[5][0] + r""" &  """ + data[5][1] + r""" &  ND & """ + recov_data[5] + r"""& """ + \
                                      self.loq_dictionary[5] + r"""\\
    Cannabidiol Acid & """ + data[7][0] + r""" &  """ + data[7][1] + r""" &  ND & """ + recov_data[7] + r"""& """ + \
                                      self.loq_dictionary[7] + r"""\\
    \hline
    \hline
    \textbf{Total CBD**} &  \textbf{""" + str(
            float(data[5][0]) + (float(data[7][0]) * 0.877)) + r"""} & \textbf{ """ + str(
            float(data[5][0]) + (float(data[7][0]) * 0.877)) + r"""} & & &\\
    \hline
    \hline
    Cannabigerol (CBG) & """ + data[6][0] + r""" &  """ + data[6][1] + r""" & ND & """ + recov_data[6] + r"""& """ + \
                                      self.loq_dictionary[6] + r"""\\
    Cannabigerol Acid & """ + data[9][0] + r""" &  """ + data[9][1] + r""" & ND & """ + recov_data[9] + r"""& """ + \
                                      self.loq_dictionary[9] + r"""\\
    \hline
    Cannabicyclol (CBL) & """ + data[13][0] + r""" &  """ + data[13][1] + r""" &  ND & """ + recov_data[
                                          13] + r"""& """ + self.loq_dictionary[13] + r"""\\
    Cannabicyclol Acid & """ + data[17][0] + r""" &  """ + data[17][1] + r""" &  ND & """ + recov_data[17] + r"""& """ + \
                                      self.loq_dictionary[17] + r"""\\
    \hline
    Cannabidivarin (CBDV) & """ + data[1][0] + r""" &  """ + data[1][1] + r""" &  ND & """ + recov_data[1] + r"""& """ + \
                                      self.loq_dictionary[1] + r"""\\
    Cannabidivarin Acid & """ + data[2][0] + r""" &  """ + data[2][1] + r""" &  ND & """ + recov_data[2] + r"""& """ + \
                                      self.loq_dictionary[2] + r"""\\
    \hline
    $\Delta^{9}$ THCV & """ + data[3][0] + r""" &  """ + data[3][1] + r""" &  ND & """ + recov_data[3] + r"""& """ + \
                                      self.loq_dictionary[3] + r"""\\
    $\Delta^{9}$ THCV Acid &  """ + data[10][0] + r""" &  """ + data[10][1] + r""" &  ND & """ + recov_data[10] + r"""& """ + self.loq_dictionary[10] + r"""\\
    \hline
    Cannabinol (CBN) & """ + data[8][0] + r""" &  """ + data[8][1] + r""" &   ND & """ + recov_data[8] + r"""& """ + \
                                      self.loq_dictionary[8] + r"""\\
    Cannabinol Acid & """ + data[15][0] + r""" &  """ + data[15][1] + r""" &  ND & """ + recov_data[15] + r"""& """ + \
                                      self.loq_dictionary[15] + r""" \\
    \hline
    Cannabigerivarin Acid & """ + data[4][0] + r""" &  """ + data[4][1] + r""" &  ND & """ + recov_data[4] + r"""& """ + \
                                      self.loq_dictionary[4] + r""" \\
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
        elif sample_type == 'mg_ml':
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
    $\Delta^{9}$-THC & """ + data[5] + r""" & ND & """ + recov_data[5] + r"""& """ + self.loq_dictionary[5] + r"""\\
    $\Delta^{9}$-THC Acid & """ + data[6] + r""" & ND & """ + recov_data[6] + r"""& """ + self.loq_dictionary[6] + r"""\\
    \hline
    $\Delta^{8}$-THC & """ + data[7] + r""" & ND & """ + recov_data[7] + r"""& """ + self.loq_dictionary[7] + r"""\\
    $\Delta^{8}$-THC Acid & 0.00 & N/A & N/A & N/A \\
    \hline
    Cannabidiol (CBD) &""" + data[1] + r""" &  ND & """ + recov_data[1] + r"""& """ + self.loq_dictionary[1] + r"""\\
    Cannabidiol Acid &""" + data[2] + r""" &  ND & """ + recov_data[2] + r"""& """ + self.loq_dictionary[2] + r"""\\
    \hline
    \hline
    Cannabinol (CBN) & """ + data[3] + r""" &   ND & """ + recov_data[3] + r"""& """ + self.loq_dictionary[3] + r"""\\
    Cannabinol Acid & """ + data[4] + r""" &   ND & """ + recov_data[4] + r"""& """ + self.loq_dictionary[4] + r"""\\
    \hline
    \hline
    \textbf{Moisture} & 0.00  &   &  &\\
    \hline
    \hline
    \end{tabular}
    \end{table}
    """
        return basic_potency_table_string

    def create_single_basic_table_unit(self, data, unit_type):
        recov_data = self.get_standard_recovery_values('Basic')
        if unit_type == 'unit':
            sample_type_1 = 'mg/g'
            sample_type_2 = 'mg/unit'
        elif unit_type == 'density':
            sample_type_1 = 'mg/mL'
            sample_type_2 = r'\%'
        else:
            sample_type_1 = r'\%'
            sample_type_2 = r'\%'
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
    \textbf{Cannabinoids} & \textbf{Sample 1} (""" + sample_type_1 + r""") & \textbf{Sample 1} (""" + sample_type_2 + r""")  & \textbf{LB} (\%) & \textbf{RR} (\%) & \textbf{LOQ} (\%)\\
    \hline
    \hline
    $\Delta^{9}$ THC & """ + data[5][0] + r""" &  """ + data[5][1] + r""" &  ND & """ + recov_data[5] + r"""& """ + \
                                     self.loq_dictionary[5] + r"""\\
    $\Delta^{9}$ THC Acid &  """ + data[6][0] + r""" &  """ + data[6][1] + r""" &  ND & """ + recov_data[
                                         6] + r"""& """ + self.loq_dictionary[6] + r"""\\
    \hline
    $\Delta^{8}$ THC & """ + data[7][0] + r""" &  """ + data[7][1] + r""" &  ND & """ + recov_data[7] + r"""& """ + \
                                     self.loq_dictionary[7] + r"""\\
    $\Delta^{8}$ THC Acid &  0.00  &  0.00 &  ND & 100  & 0.003\\
    \hline
    Cannabidiol (CBD) &""" + data[1][0] + r""" &  """ + data[1][1] + r""" &  ND & """ + recov_data[1] + r"""& """ + \
                                     self.loq_dictionary[1] + r"""\\
    Cannabidiol Acid &""" + data[2][0] + r""" &  """ + data[2][1] + r""" &  ND & """ + recov_data[2] + r"""& """ + \
                                     self.loq_dictionary[2] + r"""\\
    \hline
    Cannabinol (CBN) & """ + data[3][0] + r""" &  """ + data[3][1] + r""" &   ND & """ + recov_data[3] + r"""& """ + \
                                     self.loq_dictionary[3] + r"""\\
    Cannabinol Acid & """ + data[4][0] + r""" &  """ + data[4][1] + r""" &   ND & """ + recov_data[4] + r"""& """ + \
                                     self.loq_dictionary[4] + r"""\\
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
