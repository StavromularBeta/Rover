import pandas as pd
import datetime
import re
import sys


class PreGenerateHeaderParsing:
    """This file finds the correct header information for the samples in the batch being processed and parses them.

    1. samples_data_frame = samples_data_frame created by pre_generate_data_manipulation.
    2. current_month_directory = the directory, in U drive, where header text files are stored for the current
    month.
    3. last_month_directory = the directory, in U drive, where header text files are stored for the previous
    month.
    4. jobs_in_batch = a list of the unique jobs in the batch. There can be multiple samples per job.
    5. header_contents_dictionary = a dictionary where the keys are the unique job numbers and the values are the
    parsed header information for the respective jobs, in list form. The list structure can be seen at the bottom
    of the header_parser method."""

    def __init__(self, samples_data_frame):
        self.samples_data_frame = samples_data_frame
        self.current_month_directory = ''
        self.last_month_directory = ''
        self.jobs_in_batch = ''
        self.header_contents_dictionary = {}

#       This is for development - allows me to see the full DataFrame when i print to the console, rather than a
#       truncated version. This is useful for debugging purposes and ensuring that methods are working as intended.
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', -1)

#       This is a list of the abbreviations given to the directories where the header files are stored for a given month
        self.date_dict = {1: 'JAN',
                          2: 'FEB',
                          3: 'MAR',
                          4: 'APR',
                          5: 'MAY',
                          6: 'JUN',
                          7: 'JUL',
                          8: 'AUG',
                          9: 'SEP',
                          10: 'OCT',
                          11: 'NOV',
                          12: 'DEC'}

    def header_parsing_controller(self):
        """The main controller function. To run the methods that make up this class, this function is called."""
        self.get_current_and_last_month_directory()
        self.create_unique_jobs_list()
        self.get_header_information_from_unique_jobs_list()

    def create_unique_jobs_list(self):
        """This method creates a list of all of the unique jobs in the batch. Each job may have multiple samples."""
        self.jobs_in_batch = self.samples_data_frame.sampleid.str.slice(0, 6).unique()

    def get_current_and_last_month_directory(self):
        """This method produces the address of the header folder for the current month and the previous month. Both are
        checked for relevant headers."""
        self.current_month_directory = 'U:\\TXT-' + self.date_dict[datetime.datetime.now().month] + "\\"
        try:
            self.last_month_directory = 'U:\\TXT-' + self.date_dict[int(datetime.datetime.now().month)-1] + "\\"
        except KeyError:
            self.last_month_directory = 'U:\\TXT-' + self.date_dict[12] + "\\"
            

    def get_header_information_from_unique_jobs_list(self):
        """This method gets the header information in its raw form (weirdly formatted text file from the LIMS system)
        from the jobs_in_batch list. It then passes these raw headers to the big, disgusting header parser function,
        which parses these headers to the best of it's ability. It does an alright job, but by no means a perfect one."""
        for item in self.jobs_in_batch:
            current_month_file_path = self.current_month_directory + 'W' + item + '.TXT'
            last_month_file_path = self.last_month_directory + 'W' + item + '.TXT'
            header_contents = ''
            print("HEADER INFORMATION")
            print("attempting to find header for " + item)
            try:
                header = open(current_month_file_path, 'r')
                header_contents = header.read()
                print(item + " header found.")
            except FileNotFoundError:
                try:
                    header = open(last_month_file_path, 'r')
                    header_contents = header.read()
                    print(item + " header found.")
                except FileNotFoundError:
                    print("ERROR: header not found. Dummy header made up in place.")
                    header_contents = "Header not found"
#                   sys.exit()
#                   uncommenting will allow user to exit upon a missing header, rather than adding a dummy header.
            self.header_contents_dictionary[item] = self.header_parser_V2(header_contents)

    def header_parser(self, header_contents):
        """I don't want to talk about it. It works, somehow."""
        if header_contents == "Header not found":
            parsed_header_contents = ['no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no',
                                      'no', 'no', 'no']
            return parsed_header_contents
        name1 = header_contents[0:55].strip()
        date = header_contents[55:66].strip()
        time = header_contents[66:84].strip()
        w_number = header_contents[84:98].strip()
        name2 = header_contents[98:150].strip()
        sample_type = header_contents[150:160].strip()
        sample_type_end = 160
        name3_end = 217
        if sample_type[0:3] == 'Hem':
            sample_type_end = 160
            sample_type = header_contents[150:sample_type_end].strip()
        elif sample_type[0:3] == 'Can':
            sample_type_end = 164
            sample_type = header_contents[150:sample_type_end].strip()
            name3_end = 221
        name3 = header_contents[sample_type_end:name3_end].strip()
        sample_subtype = header_contents[name3_end:228].strip()
        sample_subtype_end = 228
        if sample_subtype[0:3] == 'oil':
            sample_subtype = header_contents[name3_end:sample_subtype_end].strip()
        elif sample_subtype[0:3] == 'oth':
            sample_subtype = header_contents[name3_end:sample_subtype_end].strip()
        elif sample_subtype[0:3] == 'CAN':
            sample_subtype_end = 236
            sample_subtype = 'Flower'
        number_of_samples_start = sample_subtype_end + 58
        name4 = header_contents[sample_subtype_end:number_of_samples_start].strip()
        telstart = number_of_samples_start + 26
        number_of_samples = header_contents[number_of_samples_start:telstart].strip()
        arrival_temp_start = telstart + 23
        telephone = header_contents[telstart:arrival_temp_start].strip()
        end_info_1_start = arrival_temp_start + 56
        arrival_temp = header_contents[arrival_temp_start:end_info_1_start].strip()[-5:]
        end_info_2_start = end_info_1_start + 49
        end_info_1 = header_contents[end_info_1_start:end_info_2_start].strip()
        end_info_3_start = end_info_2_start + 35
        end_info_2 = header_contents[end_info_2_start:end_info_3_start].strip()
        end_info_3_end = end_info_3_start + 21
        end_info_3 = header_contents[end_info_3_start:end_info_3_end].strip()
        ###
        gross_list = header_contents[end_info_3_end:].split("  ")
        sample_information = [x for x in gross_list if "Sample:" not in x]
        sample_information = [x for x in sample_information if "MOISTURE" not in x]
        sample_information = [x for x in sample_information if "Quote" not in x]
        sample_information = [x for x in sample_information if "\n\n" not in x]
        sample_information = [x for x in sample_information if " \n" != x]
        sample_information = [i for i in sample_information if i]
        sample_info_counter = 0
        for item in sample_information:
            try:
                if isinstance(int(item[-2:]), int) & isinstance(int(item[0:2]), int) & (len(item) <= 8):
                    pass
            except ValueError:
                sample_information[sample_info_counter] = item[0] + ')' + item[1:]
            sample_info_counter += 1
        sample_information = ' '.join(sample_information)
        parsed_header_contents = [name1,
                                  date,
                                  time,
                                  w_number,
                                  name2,
                                  name3,
                                  name4,
                                  sample_type,
                                  sample_subtype,
                                  number_of_samples,
                                  arrival_temp,
                                  telephone,
                                  end_info_1,
                                  end_info_2,
                                  end_info_3,
                                  sample_information]
        return parsed_header_contents

    def header_parser_V2(self, header_contents):
        if header_contents == "Header not found":
            parsed_header_contents = ['no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no',
                                      'no', 'no', 'no']
            return parsed_header_contents
        name1 = header_contents[0:55].strip()
        date = header_contents[55:66].strip()
        time = header_contents[66:84].strip()
        w_number = header_contents[84:98].strip()
        remainder_of_header = header_contents[98:].strip().split("   ")
        remainder_of_header = [word for word in remainder_of_header if len(word) >= 1]
        if remainder_of_header[0][0] == "*":
            attn = remainder_of_header[0].strip()
            sample_type = re.sub('[\n]', '', remainder_of_header[1]).strip()
            address_1 = remainder_of_header[2].strip()
            sample_subtype = re.sub('[\n]', '', remainder_of_header[3]).strip()
            address_2 = remainder_of_header[4].strip()
            number_of_samples = re.sub('[\n]', '', remainder_of_header[5]).strip()
            postal_code = re.sub('[\n]', '', remainder_of_header[6]).strip()
        else:
            attn = "*"
            address_1 = remainder_of_header[0].strip()
            sample_type = re.sub('[\n]', '', remainder_of_header[1]).strip()
            address_2 = remainder_of_header[2].strip()
            sample_subtype = re.sub('[\n]', '', remainder_of_header[3]).strip()
            postal_code = re.sub('[\n]', '', remainder_of_header[4]).strip()
            number_of_samples = re.sub('[\n]', '', remainder_of_header[5]).strip()
        email = "can't find email"
        payment_information = "can't find payment information"
        arrival_temp = "can't find arrival temperature"
        sampler = "can't find sampler information"
        phone_number = "can't find phone number"
        for item in remainder_of_header:
            if "TEL:" in item:
                phone_number = re.sub('[\n]', '', item).strip()
            elif "@" in item:
                email = re.sub('[\n]', '', item).strip()
            elif "group" in item:
                email = re.sub('[\n]', '', item).strip()
            elif "Arrival temp" in item:
                arrival_temp = re.sub('[\n]', '', item).strip()[16:]
            elif "Pd" in item:
                payment_information = re.sub('[\n]', '', item).strip()
            elif "PD" in item:
                payment_information = re.sub('[\n]', '', item).strip()
        parsed_header_contents = [name1,
                                  date,
                                  time,
                                  w_number,
                                  address_1,
                                  address_2,
                                  postal_code,
                                  sample_type,
                                  sample_subtype,
                                  number_of_samples,
                                  arrival_temp,
                                  phone_number,
                                  email,
                                  'phantom{a}',
                                  payment_information,
                                  attn,
                                  'phantom{a}']
        return parsed_header_contents
