import pandas as pd


class OrganizeMethods:

    def __init__(self, updates, sample_data):
        self.updates = updates
        self.sample_data = sample_data
        self.single_reports_dictionary = {}
        self.multiple_reports_dictionary = {}

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
        return self.single_reports_dictionary, self.multiple_reports_dictionary

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
        return self.sample_data
