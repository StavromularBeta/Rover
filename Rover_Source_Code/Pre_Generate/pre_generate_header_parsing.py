import pandas as pd
import datetime
import sys


class PreGenerateHeaderParsing:
    """This file finds the correct header information for the samples in the batch being processed and parses them."""

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
        self.last_month_directory = 'U:\\TXT-' + self.date_dict[int(datetime.datetime.now().month)-1] + "\\"

    def get_header_information_from_unique_jobs_list(self):
        """This method gets the header information in its raw form (weirdly formatted text file from the LIMS system)
        from the jobs_in_batch list. It then passes these raw headers to the big, disgusting header parser function,
        which parses these headers to the best of it's ability. It does an alright job, but by no means a perfect one."""
        for item in self.jobs_in_batch:
            current_month_file_path = self.current_month_directory + 'W' + item + '.TXT'
            last_month_file_path = self.last_month_directory + 'W' + item + '.TXT'
            header_contents = ''
            try:
                header = open(current_month_file_path, 'r')
                header_contents = header.read()
            except FileNotFoundError:
                try:
                    header = open(last_month_file_path, 'r')
                    header_contents = header.read()
                except FileNotFoundError:
                    print('shit dont be here')
                    print("ERROR: HEADER FOR AT LEAST ONE JOB CANNOT BE FOUND")
                    print("at least one header cannot be found for the current batch of jobs.")
                    print("SCRIPT EXITING.")
                    sys.exit()
            self.header_contents_dictionary[item] = self.header_parser(header_contents)

    def header_parser(self, header_contents):
        """I don't want to talk about it. It works, somehow."""
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
        datestring = "Date: " + date + " (" + time + ")"
        a_length = len(datestring)
        sourcestring = "Source: " + sample_type
        b_length = len(sourcestring)
        subtype_string = "Type: " + sample_subtype
        c_length = len(subtype_string)
        samplenumberstring = "No. of Samples: " + number_of_samples
        d_length = len(samplenumberstring)
        arrivaltempstring = "Arrival temp: " + arrival_temp
        e_length = len(arrivaltempstring)
        endinfo3string = end_info_3
        f_length = len(endinfo3string)
        lengthlist = [a_length, b_length, c_length, d_length, e_length, f_length]
        longest = max(lengthlist)
        counter = 0
        for item in lengthlist:
            if item != longest:
                offset = longest - item -1
                offset = "x" * offset
                offset = r'\phantom{' + offset + "}"
                lengthlist[counter] = offset
                counter += 1
            else:
                offset = r'\phantom{}'
                lengthlist[counter] = offset
                counter += 1
        parsed_header_contents = [name1,
                                  date,
                                  time,
                                  w_number,
                                  name2,
                                  sample_type,
                                  name3,
                                  sample_subtype,
                                  name4,
                                  number_of_samples,
                                  telephone,
                                  arrival_temp,
                                  end_info_1,
                                  end_info_2,
                                  end_info_3,
                                  lengthlist,
                                  sample_information]
        return parsed_header_contents

