class BasicTextReports:

    def __init__(self, multiple_reports_dictionary, single_reports_dictionary, sample_data):
        self.multiple_reports_dictionary = multiple_reports_dictionary
        self.single_reports_dictionary = single_reports_dictionary
        self.sample_data = sample_data
        self.basic_text_reports_dictionary = {}

    def basic_text_reports(self):
        self.create_basic_reports(self.multiple_reports_dictionary, 'Multi')
        self.create_basic_reports(self.single_reports_dictionary, 'Single')
        return self.basic_text_reports_dictionary

    def create_basic_reports(self, dictionary, dictionary_type):
        for key, value in dictionary.items():
            jobnumber = key[0:6]
            jobnumber_with_sample_designation = key
            unit_type = value[0]
            basic_deluxe_status = value[1]
            unit_density_modifier = value[2]
            head_string = "JOB: " + jobnumber + '\n'
            head_string += "SAMPLE: " + jobnumber_with_sample_designation + '\n'
            head_string += "UNITS REPORTED: " + unit_type + '\n'
            if unit_type == 'mg/mL':
                head_string += 'DENSITY: ' + str(unit_density_modifier) + " g/mL" + '\n'
            elif unit_type == 'per unit':
                head_string += 'ONE UNIT: ' + str(unit_density_modifier) + " g" + '\n'
            head_string += "BASIC/DELUXE STATUS: " + basic_deluxe_status + '\n'
            if dictionary_type == 'Multi':
                head_string += "SINGLE/MULTIPLE SAMPLES PER REPORT: Multiple" + '\n\n'
            else:
                head_string += "SINGLE/MULTIPLE SAMPLES PER REPORT: Single" + '\n\n'
            temporary_data_frame = self.sample_data.samples_data_frame[self.sample_data.samples_data_frame['sampleid']
                                                                       == jobnumber_with_sample_designation]
            head_string += "SAMPLE DATA" + '\n'
            head_string += "Ibuprofen Recovery: " + str(temporary_data_frame.iloc[0, 7])[0:5] + ' Percent \n'
            head_string += "Sample Mass: " + str(temporary_data_frame.iloc[0, 4]) + ' g \n\n'
            if unit_type == 'mg/mL':
                condensed_temporary_data_frame = temporary_data_frame[['sampleid',
                                                                       'name20',
                                                                       'percentage_concentration',
                                                                       'mg_ml',
                                                                       'over_curve']]
            elif unit_type == 'per unit':
                condensed_temporary_data_frame = temporary_data_frame[['sampleid',
                                                                       'name20',
                                                                       'percentage_concentration',
                                                                       'mg_g',
                                                                       'mg_unit',
                                                                       'over_curve']]
            elif unit_type == 'mg/g':
                condensed_temporary_data_frame = temporary_data_frame[['sampleid',
                                                                       'name20',
                                                                       'percentage_concentration',
                                                                       'mg_g',
                                                                       'over_curve']]
            else:
                condensed_temporary_data_frame = temporary_data_frame[['sampleid',
                                                                       'name20',
                                                                       'percentage_concentration',
                                                                       'over_curve']]
            condensed_temporary_data_frame.rename(columns={'percentage_concentration': r'%'}, inplace=True)
            if jobnumber in self.basic_text_reports_dictionary:
                self.basic_text_reports_dictionary[jobnumber].append([head_string, condensed_temporary_data_frame])
            else:
                self.basic_text_reports_dictionary[jobnumber] = [[head_string, condensed_temporary_data_frame]]

