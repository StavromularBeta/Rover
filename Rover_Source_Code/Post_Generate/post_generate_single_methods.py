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
        ibu_recovery_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 1.0,
                                                      ['percrecovery']].iloc[0]['percrecovery']
        ibu_recovery_value = self.round_down_to_correct_decimal_point(ibu_recovery_value)
        cbdv_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 2.0,
                                              ['percrecovery']].iloc[0]['percrecovery']
        cbdv_value = self.round_down_to_correct_decimal_point(cbdv_value)
        cbdva_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 3.0,
                                               ['percrecovery']].iloc[0]['percrecovery']
        cbdva_value = self.round_down_to_correct_decimal_point(cbdva_value)
        thcv_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 4.0,
                                              ['percrecovery']].iloc[0]['percrecovery']
        thcv_value = self.round_down_to_correct_decimal_point(thcv_value)
        cbgva_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 5.0,
                                               ['percrecovery']].iloc[0]['percrecovery']
        cbgva_value = self.round_down_to_correct_decimal_point(cbgva_value)
        cbd_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 6.0,
                                             ['percrecovery']].iloc[0]['percrecovery']
        cbd_value = self.round_down_to_correct_decimal_point(cbd_value)
        cbg_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 7.0,
                                             ['percrecovery']].iloc[0]['percrecovery']
        cbg_value = self.round_down_to_correct_decimal_point(cbg_value)
        cbda_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 8.0,
                                              ['percrecovery']].iloc[0]['percrecovery']
        cbda_value = self.round_down_to_correct_decimal_point(cbda_value)
        cbn_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 9.0,
                                             ['percrecovery']].iloc[0]['percrecovery']
        cbn_value = self.round_down_to_correct_decimal_point(cbn_value)
        cbga_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 10.0,
                                              ['percrecovery']].iloc[0]['percrecovery']
        cbga_value = self.round_down_to_correct_decimal_point(cbga_value)
        thcva_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 11.0,
                                               ['percrecovery']].iloc[0]['percrecovery']
        thcva_value = self.round_down_to_correct_decimal_point(thcva_value)
        d9_thc_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 12.0,
                                                ['percrecovery']].iloc[0]['percrecovery']
        d9_thc_value = self.round_down_to_correct_decimal_point(d9_thc_value)
        d8_thc_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 13.0,
                                                ['percrecovery']].iloc[0]['percrecovery']
        d8_thc_value = self.round_down_to_correct_decimal_point(d8_thc_value)
        cbl_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 14.0,
                                             ['percrecovery']].iloc[0]['percrecovery']
        cbl_value = self.round_down_to_correct_decimal_point(cbl_value)
        cbc_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 15.0,
                                             ['percrecovery']].iloc[0]['percrecovery']
        cbc_value = self.round_down_to_correct_decimal_point(cbc_value)
        cbna_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 16.0,
                                              ['percrecovery']].iloc[0]['percrecovery']
        cbna_value = self.round_down_to_correct_decimal_point(cbna_value)
        thca_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 17.0,
                                              ['percrecovery']].iloc[0]['percrecovery']
        thca_value = self.round_down_to_correct_decimal_point(thca_value)
        cbla_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 18.0,
                                              ['percrecovery']].iloc[0]['percrecovery']
        cbla_value = self.round_down_to_correct_decimal_point(cbla_value)
        cbca_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 19.0,
                                              ['percrecovery']].iloc[0]['percrecovery']
        cbca_value = self.round_down_to_correct_decimal_point(cbca_value)
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
        ibu_recovery_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 1.0,
                                                      ['percrecovery']].iloc[0]['percrecovery']
        ibu_recovery_value = self.round_down_to_correct_decimal_point(ibu_recovery_value)
        cbdv_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 2.0,
                                              [sample_column_type]].iloc[0][sample_column_type]
        cbdv_value = self.round_down_to_correct_decimal_point(cbdv_value)
        cbdva_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 3.0,
                                               [sample_column_type]].iloc[0][sample_column_type]
        cbdva_value = self.round_down_to_correct_decimal_point(cbdva_value)
        thcv_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 4.0,
                                              [sample_column_type]].iloc[0][sample_column_type]
        thcv_value = self.round_down_to_correct_decimal_point(thcv_value)
        cbgva_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 5.0,
                                               [sample_column_type]].iloc[0][sample_column_type]
        cbgva_value = self.round_down_to_correct_decimal_point(cbgva_value)
        cbd_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 6.0,
                                             [sample_column_type]].iloc[0][sample_column_type]
        cbd_value = self.round_down_to_correct_decimal_point(cbd_value)
        cbg_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 7.0,
                                             [sample_column_type]].iloc[0][sample_column_type]
        cbg_value = self.round_down_to_correct_decimal_point(cbg_value)
        cbda_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 8.0,
                                              [sample_column_type]].iloc[0][sample_column_type]
        cbda_value = self.round_down_to_correct_decimal_point(cbda_value)
        cbn_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 9.0,
                                             [sample_column_type]].iloc[0][sample_column_type]
        cbn_value = self.round_down_to_correct_decimal_point(cbn_value)
        cbga_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 10.0,
                                              [sample_column_type]].iloc[0][sample_column_type]
        cbga_value = self.round_down_to_correct_decimal_point(cbga_value)
        thcva_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 11.0,
                                               [sample_column_type]].iloc[0][sample_column_type]
        thcva_value = self.round_down_to_correct_decimal_point(thcva_value)
        d9_thc_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 12.0,
                                                [sample_column_type]].iloc[0][sample_column_type]
        d9_thc_value = self.round_down_to_correct_decimal_point(d9_thc_value)
        d8_thc_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 13.0,
                                                [sample_column_type]].iloc[0][sample_column_type]
        d8_thc_value = self.round_down_to_correct_decimal_point(d8_thc_value)
        cbl_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 14.0,
                                             [sample_column_type]].iloc[0][sample_column_type]
        cbl_value = self.round_down_to_correct_decimal_point(cbl_value)
        cbc_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 15.0,
                                             [sample_column_type]].iloc[0][sample_column_type]
        cbc_value = self.round_down_to_correct_decimal_point(cbc_value)
        cbna_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 16.0,
                                              [sample_column_type]].iloc[0][sample_column_type]
        cbna_value = self.round_down_to_correct_decimal_point(cbna_value)
        thca_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 17.0,
                                              [sample_column_type]].iloc[0][sample_column_type]
        thca_value = self.round_down_to_correct_decimal_point(thca_value)
        cbla_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 18.0,
                                              [sample_column_type]].iloc[0][sample_column_type]
        cbla_value = self.round_down_to_correct_decimal_point(cbla_value)
        cbca_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 19.0,
                                              [sample_column_type]].iloc[0][sample_column_type]
        cbca_value = self.round_down_to_correct_decimal_point(cbca_value)
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
        ibu_recovery_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 1.0,
                                                      ['percrecovery']].iloc[0]['percrecovery']
        ibu_recovery_value = self.round_down_to_correct_decimal_point(ibu_recovery_value)
        cbdv_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 2.0,
                                              [column_1]].iloc[0][column_1]
        cbdv_value = self.round_down_to_correct_decimal_point(cbdv_value)
        cbdva_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 3.0,
                                               [column_1]].iloc[0][column_1]
        cbdva_value = self.round_down_to_correct_decimal_point(cbdva_value)
        thcv_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 4.0,
                                              [column_1]].iloc[0][column_1]
        thcv_value = self.round_down_to_correct_decimal_point(thcv_value)
        cbgva_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 5.0,
                                               [column_1]].iloc[0][column_1]
        cbgva_value = self.round_down_to_correct_decimal_point(cbgva_value)
        cbd_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 6.0,
                                             [column_1]].iloc[0][column_1]
        cbd_value = self.round_down_to_correct_decimal_point(cbd_value)
        cbg_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 7.0,
                                             [column_1]].iloc[0][column_1]
        cbg_value = self.round_down_to_correct_decimal_point(cbg_value)
        cbda_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 8.0,
                                              [column_1]].iloc[0][column_1]
        cbda_value = self.round_down_to_correct_decimal_point(cbda_value)
        cbn_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 9.0,
                                             [column_1]].iloc[0][column_1]
        cbn_value = self.round_down_to_correct_decimal_point(cbn_value)
        cbga_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 10.0,
                                              [column_1]].iloc[0][column_1]
        cbga_value = self.round_down_to_correct_decimal_point(cbga_value)
        thcva_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 11.0,
                                               [column_1]].iloc[0][column_1]
        thcva_value = self.round_down_to_correct_decimal_point(thcva_value)
        d9_thc_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 12.0,
                                                [column_1]].iloc[0][column_1]
        d9_thc_value = self.round_down_to_correct_decimal_point(d9_thc_value)
        d8_thc_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 13.0,
                                                [column_1]].iloc[0][column_1]
        d8_thc_value = self.round_down_to_correct_decimal_point(d8_thc_value)
        cbl_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 14.0,
                                             [column_1]].iloc[0][column_1]
        cbl_value = self.round_down_to_correct_decimal_point(cbl_value)
        cbc_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 15.0,
                                             [column_1]].iloc[0][column_1]
        cbc_value = self.round_down_to_correct_decimal_point(cbc_value)
        cbna_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 16.0,
                                              [column_1]].iloc[0][column_1]
        cbna_value = self.round_down_to_correct_decimal_point(cbna_value)
        thca_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 17.0,
                                              [column_1]].iloc[0][column_1]
        thca_value = self.round_down_to_correct_decimal_point(thca_value)
        cbla_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 18.0,
                                              [column_1]].iloc[0][column_1]
        cbla_value = self.round_down_to_correct_decimal_point(cbla_value)
        cbca_value = temporary_data_frame.loc[temporary_data_frame['id17'] == 19.0,
                                              [column_1]].iloc[0][column_1]
        cbca_value = self.round_down_to_correct_decimal_point(cbca_value)
        # UNITS
        cbdv_value_u = temporary_data_frame.loc[temporary_data_frame['id17'] == 2.0,
                                                [column_2]].iloc[0][column_2]
        cbdv_value_u = self.round_down_to_correct_decimal_point(cbdv_value_u)
        cbdva_value_u = temporary_data_frame.loc[temporary_data_frame['id17'] == 3.0,
                                                 [column_2]].iloc[0][column_2]
        cbdva_value_u = self.round_down_to_correct_decimal_point(cbdva_value_u)
        thcv_value_u = temporary_data_frame.loc[temporary_data_frame['id17'] == 4.0,
                                                [column_2]].iloc[0][column_2]
        thcv_value_u = self.round_down_to_correct_decimal_point(thcv_value_u)
        cbgva_value_u = temporary_data_frame.loc[temporary_data_frame['id17'] == 5.0,
                                                 [column_2]].iloc[0][column_2]
        cbgva_value_u = self.round_down_to_correct_decimal_point(cbgva_value_u)
        cbd_value_u = temporary_data_frame.loc[temporary_data_frame['id17'] == 6.0,
                                               [column_2]].iloc[0][column_2]
        cbd_value_u = self.round_down_to_correct_decimal_point(cbd_value_u)
        cbg_value_u = temporary_data_frame.loc[temporary_data_frame['id17'] == 7.0,
                                               [column_2]].iloc[0][column_2]
        cbg_value_u = self.round_down_to_correct_decimal_point(cbg_value_u)
        cbda_value_u = temporary_data_frame.loc[temporary_data_frame['id17'] == 8.0,
                                                [column_2]].iloc[0][column_2]
        cbda_value_u = self.round_down_to_correct_decimal_point(cbda_value_u)
        cbn_value_u = temporary_data_frame.loc[temporary_data_frame['id17'] == 9.0,
                                               [column_2]].iloc[0][column_2]
        cbn_value_u = self.round_down_to_correct_decimal_point(cbn_value_u)
        cbga_value_u = temporary_data_frame.loc[temporary_data_frame['id17'] == 10.0,
                                                [column_2]].iloc[0][column_2]
        cbga_value_u = self.round_down_to_correct_decimal_point(cbga_value_u)
        thcva_value_u = temporary_data_frame.loc[temporary_data_frame['id17'] == 11.0,
                                                 [column_2]].iloc[0][column_2]
        thcva_value_u = self.round_down_to_correct_decimal_point(thcva_value_u)
        d9_thc_value_u = temporary_data_frame.loc[temporary_data_frame['id17'] == 12.0,
                                                  [column_2]].iloc[0][column_2]
        d9_thc_value_u = self.round_down_to_correct_decimal_point(d9_thc_value_u)
        d8_thc_value_u = temporary_data_frame.loc[temporary_data_frame['id17'] == 13.0,
                                                  [column_2]].iloc[0][column_2]
        d8_thc_value_u = self.round_down_to_correct_decimal_point(d8_thc_value_u)
        cbl_value_u = temporary_data_frame.loc[temporary_data_frame['id17'] == 14.0,
                                               [column_2]].iloc[0][column_2]
        cbl_value_u = self.round_down_to_correct_decimal_point(cbl_value_u)
        cbc_value_u = temporary_data_frame.loc[temporary_data_frame['id17'] == 15.0,
                                               [column_2]].iloc[0][column_2]
        cbc_value_u = self.round_down_to_correct_decimal_point(cbc_value_u)
        cbna_value_u = temporary_data_frame.loc[temporary_data_frame['id17'] == 16.0,
                                                [column_2]].iloc[0][column_2]
        cbna_value_u = self.round_down_to_correct_decimal_point(cbna_value_u)
        thca_value_u = temporary_data_frame.loc[temporary_data_frame['id17'] == 17.0,
                                                [column_2]].iloc[0][column_2]
        thca_value_u = self.round_down_to_correct_decimal_point(thca_value_u)
        cbla_value_u = temporary_data_frame.loc[temporary_data_frame['id17'] == 18.0,
                                                [column_2]].iloc[0][column_2]
        cbla_value_u = self.round_down_to_correct_decimal_point(cbla_value_u)
        cbca_value_u = temporary_data_frame.loc[temporary_data_frame['id17'] == 19.0,
                                                [column_2]].iloc[0][column_2]
        cbca_value_u = self.round_down_to_correct_decimal_point(cbca_value_u)
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
        thc_total = self.create_total_line('regular', 'deluxe', 'THC', data)
        cbd_total = self.create_total_line('regular', 'deluxe', 'CBD', data)
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
                    p{\dimexpr0.07\textwidth-2\tabcolsep-\arrayrulewidth\relax}
                    p{\dimexpr0.1\textwidth-2\tabcolsep-\arrayrulewidth\relax}
                    p{\dimexpr0.07\textwidth-2\tabcolsep-\arrayrulewidth\relax}
                    }
    \textbf{Cannabinoids} & \textbf{Sample 1}  & \textbf{\small Blank} & \textbf{\small Recovery} & $\mathbf{\small S_{0}}$\\
    & (""" + sample_type + r""") & (\%) & (\%) & (\%) \\
    \hline
    \hline
    $\Delta^{9}$-THC & """ + data[11] + r""" & ND & """ + recov_data[11] + r"""& """ + self.loq_dictionary[11] + r"""\\
    $\Delta^{9}$-THC Acid & """ + data[16] + r""" & ND & """ + recov_data[16] + r"""& """ + self.loq_dictionary[16] + r"""\\
    \hline
    \hline
    \textbf{Total THC*} &  \textbf{""" + thc_total + r"""} & & &\\
    \hline
    \hline
    $\Delta^{8}$THC & """ + data[12] + r""" & ND & """ + recov_data[12] + r"""& """ + self.loq_dictionary[12] + r"""\\
    $\Delta^{8}$THC Acid & ND & ND & N/A & N/A \\
    \hline
    Cannabichromene (CBC) & """ + data[14] + r"""  & ND& """ + recov_data[14] + r"""& """ + self.loq_dictionary[14] + r"""\\
    Cannabichromene Acid & """ + data[18] + r"""  & ND & """ + recov_data[18] + r"""& """ + self.loq_dictionary[18] + r"""\\
    \hline
    Cannabidiol (CBD) &""" + data[5] + r""" &  ND & """ + recov_data[5] + r"""& """ + self.loq_dictionary[5] + r"""\\
    Cannabidiol Acid & """ + data[7] + r""" &  ND & """ + recov_data[7] + r"""& """ + self.loq_dictionary[7] + r"""\\
    \hline
    \hline
    \textbf{Total CBD**} &  \textbf{""" + cbd_total + r"""} & & &\\
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
        thc_total = self.create_total_line('unit', 'deluxe', 'THC', data)
        cbd_total = self.create_total_line('unit', 'deluxe', 'CBD', data)
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
                    p{\dimexpr0.07\textwidth-2\tabcolsep-\arrayrulewidth\relax}
                    p{\dimexpr0.1\textwidth-2\tabcolsep-\arrayrulewidth\relax}
                    p{\dimexpr0.07\textwidth-2\tabcolsep-\arrayrulewidth\relax}
                    }
    \textbf{Cannabinoids} & \textbf{Sample 1} & \textbf{Sample 1}  & \textbf{\small Blank} & \textbf{\small Recovery} & $\mathbf{\small S_{0}}$ \\
    & (""" + sample_type_1 + r""") & (""" + sample_type_2 + r""") & (\%) & (\%) & (\%) \\
    \hline
    \hline
    $\Delta^{9}$-THC & """ + data[11][0] + r""" &  """ + data[11][1] + r""" & ND & """ + recov_data[11] + r"""&""" + \
                                      self.loq_dictionary[11] + r"""\\
    $\Delta^{9}$-THC Acid & """ + data[16][0] + r""" &  """ + data[16][1] + r""" & ND & """ + recov_data[
                                          16] + r"""& """ + self.loq_dictionary[16] + r"""\\
    \hline
    \hline
    \textbf{Total THC*} &  \textbf{""" + thc_total[0] + r"""} & \textbf{""" + thc_total[1] + r"""} & & &\\
    \hline
    \hline
    $\Delta^{8}$THC & """ + data[12][0] + r""" &  """ + data[12][1] + r""" & ND & """ + recov_data[12] + r"""& """ + \
                                      self.loq_dictionary[12] + r"""\\
    $\Delta^{8}$THC Acid & ND & ND & ND & N/A & N/A\\
    \hline
    Cannabichromene (CBC) & """ + data[14][0] + r""" &  """ + data[14][1] + r"""  & ND & """ + recov_data[14] + r"""& """ + \
                                      self.loq_dictionary[14] + r"""\\
    Cannabichromene Acid & """ + data[18][0] + r""" &  """ + data[18][1] + r"""  & ND & """ + recov_data[18] + r"""& """ + \
                                      self.loq_dictionary[18] + r"""\\
    \hline
    Cannabidiol (CBD) &""" + data[5][0] + r""" &  """ + data[5][1] + r""" &  ND & """ + recov_data[5] + r"""& """ + \
                                      self.loq_dictionary[5] + r"""\\
    Cannabidiol Acid & """ + data[7][0] + r""" &  """ + data[7][1] + r""" &  ND & """ + recov_data[7] + r"""& """ + \
                                      self.loq_dictionary[7] + r"""\\
    \hline
    \hline
    \textbf{Total CBD**} &  \textbf{""" + cbd_total[0] + r"""} & \textbf{""" + cbd_total[1] + r"""} & & &\\
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
    $\Delta^{9}$ THCV Acid &  """ + data[10][0] + r""" &  """ + data[10][1] + r""" &  ND & """ + recov_data[
                                          10] + r"""& """ + self.loq_dictionary[10] + r"""\\
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
        thc_total = self.create_total_line('regular', 'basic', 'THC', data)
        cbd_total = self.create_total_line('regular', 'basic', 'CBD', data)
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
                    p{\dimexpr0.07\textwidth-2\tabcolsep-\arrayrulewidth\relax}
                    p{\dimexpr0.1\textwidth-2\tabcolsep-\arrayrulewidth\relax}
                    p{\dimexpr0.07\textwidth-2\tabcolsep-\arrayrulewidth\relax}
                    }
    \textbf{Cannabinoids} & \textbf{Sample 1}  & \textbf{\small Blank} & \textbf{\small Recovery} & $\mathbf{\small S_{0}}$\\
    & (""" + sample_type + r""") & (\%) & (\%) & (\%) \\
    \hline
    \hline
    $\Delta^{9}$-THC & """ + data[5] + r""" & ND & """ + recov_data[5] + r"""& """ + self.loq_dictionary[5] + r"""\\
    $\Delta^{9}$-THC Acid & """ + data[6] + r""" & ND & """ + recov_data[6] + r"""& """ + self.loq_dictionary[6] + r"""\\
    \hline
    \hline
    \textbf{Total THC*} &  \textbf{""" + thc_total + r"""} & & &\\
    \hline
    \hline
    $\Delta^{8}$-THC & """ + data[7] + r""" & ND & """ + recov_data[7] + r"""& """ + self.loq_dictionary[7] + r"""\\
    $\Delta^{8}$THC Acid & ND & ND & N/A & N/A \\
    \hline
    Cannabidiol (CBD) &""" + data[1] + r""" &  ND & """ + recov_data[1] + r"""& """ + self.loq_dictionary[1] + r"""\\
    Cannabidiol Acid &""" + data[2] + r""" &  ND & """ + recov_data[2] + r"""& """ + self.loq_dictionary[2] + r"""\\
    \hline
    \hline
    \textbf{Total CBD**} &  \textbf{""" + cbd_total + r"""} & & &\\
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
        thc_total = self.create_total_line('unit', 'basic', 'THC', data)
        cbd_total = self.create_total_line('unit', 'basic', 'CBD', data)
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
                    p{\dimexpr0.07\textwidth-2\tabcolsep-\arrayrulewidth\relax}
                    p{\dimexpr0.1\textwidth-2\tabcolsep-\arrayrulewidth\relax}
                    p{\dimexpr0.07\textwidth-2\tabcolsep-\arrayrulewidth\relax}
                    }
    \textbf{Cannabinoids} & \textbf{Sample 1} & \textbf{Sample 1}  & \textbf{\small Blank} & \textbf{\small Recovery} & $\mathbf{\small S_{0}}$ \\
    & (""" + sample_type_1 + r""") & (""" + sample_type_2 + r""") & (\%) & (\%) & (\%) \\
    \hline
    \hline
    $\Delta^{9}$ THC & """ + data[5][0] + r""" &  """ + data[5][1] + r""" &  ND & """ + recov_data[5] + r"""& """ + \
                                     self.loq_dictionary[5] + r"""\\
    $\Delta^{9}$ THC Acid &  """ + data[6][0] + r""" &  """ + data[6][1] + r""" &  ND & """ + recov_data[
                                         6] + r"""& """ + self.loq_dictionary[6] + r"""\\
    \hline
    \hline
    \textbf{Total THC*} &  \textbf{""" + thc_total[0] + r"""} & \textbf{""" + thc_total[1] + r"""} & & &\\
    \hline
    \hline
    $\Delta^{8}$ THC & """ + data[7][0] + r""" &  """ + data[7][1] + r""" &  ND & """ + recov_data[7] + r"""& """ + \
                                     self.loq_dictionary[7] + r"""\\
    $\Delta^{8}$THC Acid & ND & ND & ND & N/A & N/A \\
    \hline
    Cannabidiol (CBD) &""" + data[1][0] + r""" &  """ + data[1][1] + r""" &  ND & """ + recov_data[1] + r"""& """ + \
                                     self.loq_dictionary[1] + r"""\\
    Cannabidiol Acid &""" + data[2][0] + r""" &  """ + data[2][1] + r""" &  ND & """ + recov_data[2] + r"""& """ + \
                                     self.loq_dictionary[2] + r"""\\
    \hline
    \hline
    \textbf{Total CBD**} &  \textbf{""" + cbd_total[0] + r"""} & \textbf{""" + cbd_total[1] + r"""} & & &\\
    \hline
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
    Methods: solvent extraction; measured by UPLC-UV, tandem MS, P.I. 1.14 \& based on USP monograph 29 \newline
    $\si{S_{o}}$ = standard deviation at zero analyte concentration. MDL generally considered to be 3x $\si{S_{o}}$ value. \newline\newline
    ND = none detected. N/A = not applicable. THC = tetrahydrocannabinol.\newline 
    \textbf{*Total THC} = $\Delta^{9}$-THC + (THCA x 0.877 ). \textbf{**Total CBD} = CBD + (CBDA x 0.877).\newline\newline
    Material will be held for up to 3 weeks unless alternative arrangements have been made. Sample holding time may vary and is dependant on MBL license restrictions.
    \newline\newline\newline
    R. Bilodeau \phantom{aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaasasssssssssssss}H. Hartmann\\ Analytical Chemist: \underline{\hspace{3cm}}{ \hspace{3.2cm} Sr. Analytical Chemist: \underline{\hspace{3cm}}       
    \fancyfoot[C]{\textbf{MB Laboratories Ltd.}\\ \textbf{Web:} www.mblabs.com}
    \fancyfoot[R]{\textbf{Mail:} PO Box 2103\\ Sidney, B.C., V8L 356}
    \fancyfoot[L]{\textbf{T:} 250 656 1334\\ \textbf{E:} info@mblabs.com}
    \end{document}
     """
        return footer_string

    def round_down_to_correct_decimal_point(self, data_value):
        if 100 > data_value >= 1:
            data_value = str(data_value)[0:4]
        elif 1 > data_value > 0:
            data_value = str(data_value)[0:5]
        elif data_value >= 100:
            data_value = str(data_value)[0:3]
        else:
            data_value = 'ND'
        return data_value

    def create_total_line(self, total_line_type, report_type, cannabinoid, data):
        if total_line_type == "unit":
            if cannabinoid == 'THC':
                if report_type == 'basic':
                    delta9 = data[5][0]
                    acid = data[6][0]
                    delta9_unit = data[5][1]
                    acid_unit = data[6][1]
                else:
                    delta9 = data[11][0]
                    acid = data[16][0]
                    delta9_unit = data[11][1]
                    acid_unit = data[16][1]
                if delta9 == 'ND':
                    delta9 = 0
                if acid == 'ND':
                    acid = 0
                if delta9_unit == 'ND':
                    delta9_unit = 0
                if acid_unit == 'ND':
                    acid_unit = 0
                total1 = float(delta9) + (float(acid) * 0.877)
                total2 = float(delta9_unit) + (float(acid_unit) * 0.877)
                if 100 > total1 >= 1:
                    total1 = str(total1)[0:4]
                elif 1 > total1 > 0:
                    total1 = str(total1)[0:5]
                elif total1 >= 100:
                    total1 = str(total1)[0:3]
                else:
                    total1 = 'ND'
                if 100 > total2 >= 1:
                    total2 = str(total2)[0:4]
                elif 1 > total2 > 0:
                    total2 = str(total2)[0:5]
                elif total2 >= 100:
                    total2 = str(total2)[0:3]
                else:
                    total2 = 'ND'
                return [total1, total2]
            else:
                if report_type == 'basic':
                    cbd = data[1][0]
                    acid = data[2][0]
                    cbd_unit = data[1][1]
                    acid_unit = data[2][1]
                else:
                    cbd = data[5][0]
                    acid = data[7][0]
                    cbd_unit = data[5][1]
                    acid_unit = data[7][1]
                if cbd == 'ND':
                    cbd = 0
                if acid == 'ND':
                    acid = 0
                if cbd_unit == 'ND':
                    cbd_unit = 0
                if acid_unit == 'ND':
                    acid_unit = 0
                total1 = float(cbd) + (float(acid) * 0.877)
                total2 = float(cbd_unit) + (float(acid_unit) * 0.877)
                if 100 > total1 >= 1:
                    total1 = str(total1)[0:4]
                elif 1 > total1 > 0:
                    total1 = str(total1)[0:5]
                elif total1 >= 100:
                    total1 = str(total1)[0:3]
                else:
                    total1 = 'ND'
                if 100 > total2 >= 1:
                    total2 = str(total2)[0:4]
                elif 1 > total2 > 0:
                    total2 = str(total2)[0:5]
                elif total2 >= 100:
                    total2 = str(total2)[0:3]
                else:
                    total2 = 'ND'
                return [total1, total2]
        elif total_line_type == "regular":
            if cannabinoid == 'THC':
                if report_type == 'basic':
                    delta9 = data[5]
                    acid = data[6]
                else:
                    delta9 = data[11]
                    acid = data[16]
                if delta9 == 'ND':
                    delta9 = 0
                if acid == 'ND':
                    acid = 0
                total = float(delta9) + (float(acid) * 0.877)
                if 100 > total >= 1:
                    total = str(total)[0:4]
                elif 1 > total > 0:
                    total = str(total)[0:5]
                elif total >= 100:
                    total = str(total)[0:3]
                else:
                    total = 'ND'
                return total
            else:
                if report_type == "basic":
                    cbd = data[1]
                    acid = data[2]
                else:
                    cbd = data[5]
                    acid = data[7]
                if cbd == 'ND':
                    cbd = 0
                if acid == 'ND':
                    acid = 0
                total = float(cbd) + (float(acid) * 0.877)
                if 100 > total >= 1:
                    total = str(total)[0:4]
                elif 1 > total > 0:
                    total = str(total)[0:5]
                elif total >= 100:
                    total = str(total)[0:3]
                else:
                    total = 'ND'
                return total

