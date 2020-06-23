import tkinter as Tk
from tkinter import ttk
from tkinter import font as tkFont
import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir)
parentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir)
sys.path.insert(0, currentdir)
from Post_Generate.post_generate_controller import ReportWriter as report


class BatchWindow(Tk.Frame):
    def __init__(self, parent, **kwargs):
        Tk.Frame.__init__(self, parent, **kwargs)
        self.header_font = tkFont.Font(size=12, weight='bold')
        self.parent = parent
        self.master_display_frame = Tk.Frame(self)
        self.sub_display_frame = Tk.Frame(self)
        self.blank_data_frame = Tk.Frame(self.sub_display_frame)
        self.recovery_data_frame = Tk.Frame(self.sub_display_frame)
        self.headers_data_frame = Tk.Frame(self.sub_display_frame)
        self.samples_list_frame = Tk.Frame(self.sub_display_frame)
        self.samples_checklist_frame = Tk.Frame(self.sub_display_frame)
        self.display_sample_data_frame = Tk.Frame(self.sub_display_frame)
        self.sample_type_option_list = []
        self.updated_sample_type_option_list = []
        self.report_type_option_list = []
        self.updated_report_type_option_list = []
        self.single_or_multi_list = []
        self.updated_single_or_multi_list = []
        self.header_information_list = []
        self.update_header_information_list = []
        self.sample_information_list = []
        self.updated_sample_information_list = []
        self.density_unit_weight_list = []
        self.updated_density_unit_weight_list = []
        self.density_unit_weight_option_list = []
        self.updated_density_unit_weight_option_list = []
        self.sample_name_list = []
        self.updated_sample_name_list = []
        self.updated_dictionary = {}
        self.lengthlist = []

    def batch(self, data):
        self.create_scrollable_window()
        self.blank_data_frame.grid(row=0, column=0, sticky=Tk.W, padx=10, pady=10)
        self.recovery_data_frame.grid(row=0, column=1, sticky=Tk.W, padx=10, pady=10)
        self.headers_data_frame.grid(row=2, column=0, columnspan=2, sticky=Tk.W, padx=10, pady=10)
#       self.samples_list_frame.grid(row=4, column=0, columnspan=2, sticky=Tk.W, padx=10, pady=10)
#       above line is now obsolete. Will keep for a bit.
        self.display_sample_data_frame.grid(row=1, column=0, columnspan=2, sticky=Tk.W, padx=10, pady=10)
        self.samples_checklist_frame.grid(row=3, column=0, columnspan=2, sticky=Tk.W, padx=10, pady=10)
        self.create_blank_frame(data)
        self.create_recovery_frame(data)
        self.create_header_frames(data)
        self.create_sample_list_frame(data)
        self.create_samples_checklist_option_frame(data)
        self.display_sample_data(data)

    def create_scrollable_window(self):
        display_all_jobs_canvas = Tk.Canvas(self.master_display_frame,
                                            width=1280,
                                            height=700,
                                            scrollregion=(0, 0, 0, 15000))
        all_entries_scroll = Tk.Scrollbar(self.master_display_frame,
                                          orient="vertical",
                                          command=display_all_jobs_canvas.yview)
        display_all_jobs_canvas.configure(yscrollcommand=all_entries_scroll.set)
        all_entries_scroll.pack(side='right',
                                fill='y')
        display_all_jobs_canvas.pack(side="left",
                                     fill='y')
        display_all_jobs_canvas.create_window((0, 0),
                                              window=self.sub_display_frame,
                                              anchor='nw')
        self.master_display_frame.grid()

    def create_blank_frame(self, data):
        blank_label = Tk.Label(self.blank_data_frame, text="Blank Data", font=self.header_font)
        blank_label.grid(row=0, column=0, sticky=Tk.W)
        blank_text = Tk.Text(self.blank_data_frame, width=18, height=20)
        blank_text.insert(Tk.END, data.dm.min_value_blank_data_frame.to_string())
        blank_text.config(state="disabled")
        blank_text.grid(row=1, column=0)

    def create_recovery_frame(self, data):
        recovery_label = Tk.Label(self.recovery_data_frame, text="Standard Recovery Data", font=self.header_font)
        recovery_label.grid(row=0, column=0, sticky=Tk.W)
        recovery_text = Tk.Text(self.recovery_data_frame, width=70, height=20)
        recovery_text.insert(Tk.END, data.dm.best_recovery_qc_data_frame.to_string())
        recovery_text.config(state="disabled")
        recovery_text.grid(row=1, column=0)

    def create_header_frames(self, data):
        counter = 0
        column_counter = 1
        Tk.Label(self.headers_data_frame, text="Client Name", font=self.header_font).grid(row=1, column=0, sticky=Tk.W)
        Tk.Label(self.headers_data_frame, text="Date", font=self.header_font).grid(row=2, column=0, sticky=Tk.W)
        Tk.Label(self.headers_data_frame, text="Time", font=self.header_font).grid(row=3, column=0, sticky=Tk.W)
        Tk.Label(self.headers_data_frame, text="Job Number", font=self.header_font).grid(row=4, column=0, sticky=Tk.W)
        Tk.Label(self.headers_data_frame, text="Attention", font=self.header_font).grid(row=5, column=0, sticky=Tk.W)
        Tk.Label(self.headers_data_frame, text="Address 1", font=self.header_font).grid(row=6, column=0, sticky=Tk.W)
        Tk.Label(self.headers_data_frame, text="Address 2", font=self.header_font).grid(row=7, column=0, sticky=Tk.W)
        Tk.Label(self.headers_data_frame, text="Address 3", font=self.header_font).grid(row=8, column=0, sticky=Tk.W)
        Tk.Label(self.headers_data_frame, text="Sample Type 1", font=self.header_font).grid(row=9, column=0, sticky=Tk.W)
        Tk.Label(self.headers_data_frame, text="Sample Type 2", font=self.header_font).grid(row=10, column=0, sticky=Tk.W)
        Tk.Label(self.headers_data_frame, text="Number of Samples", font=self.header_font).grid(row=11, column=0, sticky=Tk.W)
        Tk.Label(self.headers_data_frame, text="Receive Temp.", font=self.header_font).grid(row=12, column=0, sticky=Tk.W)
        Tk.Label(self.headers_data_frame, text="Additional Info 1", font=self.header_font).grid(row=13, column=0, sticky=Tk.W)
        Tk.Label(self.headers_data_frame, text="Additional Info 2", font=self.header_font).grid(row=14, column=0, sticky=Tk.W)
        Tk.Label(self.headers_data_frame, text="Additional Info 3", font=self.header_font).grid(row=15, column=0, sticky=Tk.W)
        Tk.Label(self.headers_data_frame, text="Payment Info", font=self.header_font).grid(row=16, column=0, sticky=Tk.W)
        for key, value in data.hp.header_contents_dictionary.items():
            header_frame_label = Tk.Label(self.headers_data_frame, text=key, font=self.header_font)
            header_frame_label.grid(row=counter, column=column_counter)
            counter += 1
            header_name_entry = Tk.Entry(self.headers_data_frame)
            header_name_entry.insert(Tk.END, value[0])
            header_name_entry.grid(row=counter, column=column_counter)
            counter += 1
            date_entry = Tk.Entry(self.headers_data_frame)
            date_entry.insert(Tk.END, value[1])
            date_entry.grid(row=counter, column=column_counter)
            counter += 1
            time_entry = Tk.Entry(self.headers_data_frame)
            time_entry.insert(Tk.END, value[2])
            time_entry.grid(row=counter, column=column_counter)
            counter += 1
            job_entry = Tk.Entry(self.headers_data_frame)
            job_entry.insert(Tk.END, value[3])
            job_entry.grid(row=counter, column=column_counter)
            counter += 1
            attention_entry = Tk.Entry(self.headers_data_frame)
            attention_entry.insert(Tk.END, value[15])
            attention_entry.grid(row=counter, column=column_counter)
            counter += 1
            address_entry = Tk.Entry(self.headers_data_frame)
            address_entry.insert(Tk.END, value[4])
            address_entry.grid(row=counter, column=column_counter)
            counter += 1
            address_entry_2 = Tk.Entry(self.headers_data_frame)
            address_entry_2.insert(Tk.END, value[5])
            address_entry_2.grid(row=counter, column=column_counter)
            counter += 1
            address_entry_3 = Tk.Entry(self.headers_data_frame)
            address_entry_3.insert(Tk.END, value[6])
            address_entry_3.grid(row=counter, column=column_counter)
            counter += 1
            sample_type_entry_1 = Tk.Entry(self.headers_data_frame)
            sample_type_entry_1.insert(Tk.END, value[7])
            sample_type_entry_1.grid(row=counter, column=column_counter)
            counter += 1
            sample_type_entry_2 = Tk.Entry(self.headers_data_frame)
            sample_type_entry_2.insert(Tk.END, value[8])
            sample_type_entry_2.grid(row=counter, column=column_counter)
            counter += 1
            number_of_samples_entry = Tk.Entry(self.headers_data_frame)
            number_of_samples_entry.insert(Tk.END, value[9])
            number_of_samples_entry.grid(row=counter, column=column_counter)
            counter += 1
            receive_temp = Tk.Entry(self.headers_data_frame)
            receive_temp.insert(Tk.END, value[10])
            receive_temp.grid(row=counter, column=column_counter)
            counter += 1
            additional_info_1 = Tk.Entry(self.headers_data_frame)
            additional_info_1.insert(Tk.END, value[11])
            additional_info_1.grid(row=counter, column=column_counter)
            counter += 1
            additional_info_2 = Tk.Entry(self.headers_data_frame)
            additional_info_2.insert(Tk.END, value[12])
            additional_info_2.grid(row=counter, column=column_counter)
            counter += 1
            additional_info_3 = Tk.Entry(self.headers_data_frame)
            additional_info_3.insert(Tk.END, value[13])
            additional_info_3.grid(row=counter, column=column_counter)
            counter += 1
            payment_info = Tk.Entry(self.headers_data_frame)
            payment_info.insert(Tk.END, value[14])
            payment_info.grid(row=counter, column=column_counter)
            counter += 1
            counter = 0
            column_counter += 1
            self.header_information_list.append((key, [header_name_entry,
                                                       date_entry,
                                                       time_entry,
                                                       job_entry,
                                                       address_entry,
                                                       address_entry_2,
                                                       address_entry_3,
                                                       sample_type_entry_1,
                                                       sample_type_entry_2,
                                                       number_of_samples_entry,
                                                       receive_temp,
                                                       additional_info_1,
                                                       additional_info_2,
                                                       additional_info_3,
                                                       payment_info,
                                                       attention_entry,
                                                       attention_entry,]))

    def create_sample_list_frame(self, data):
        counter = 0
        for key, value in data.hp.header_contents_dictionary.items():
            Tk.Label(self.samples_list_frame, text=key + " samples list", font=self.header_font).grid(row=counter,
                                                                                                      column=0,
                                                                                                      sticky=Tk.W)
            samples_list_text = Tk.Text(self.samples_list_frame, width=80, height=10)
            samples_list_text.insert(Tk.END, value[15])
            counter += 1
            samples_list_text.grid(row=counter, column=0)
            counter += 1
            self.sample_information_list.append((key, samples_list_text))

    def create_samples_checklist_option_frame(self, data):
        counter = 1
        Tk.Label(self.samples_checklist_frame, text="Samples", font=self.header_font).grid(row=0, column=0)
        Tk.Label(self.samples_checklist_frame, text="Units", font=self.header_font).grid(row=0, column=1)
        Tk.Label(self.samples_checklist_frame, text="Basic/Deluxe", font=self.header_font).grid(row=0, column=2)
        Tk.Label(self.samples_checklist_frame, text="single/multi", font=self.header_font).grid(row=0, column=3)
        Tk.Label(self.samples_checklist_frame,
                 text="density or unit mass input",
                 font=self.header_font).grid(row=0, column=4, columnspan=2)
        for item in data.dm.unique_sample_id_list:
            Tk.Label(self.samples_checklist_frame, text=item).grid(row=counter, column=0)
            sample_type_string_variable = Tk.StringVar(self.samples_checklist_frame)
            sample_type_choices = {'Percent', 'mg/mL', 'mg/g', 'per unit'}
            sample_type_string_variable.set('Percent')
            sample_type_menu = Tk.OptionMenu(self.samples_checklist_frame,
                                             sample_type_string_variable,
                                             *sample_type_choices)
            sample_type_menu.grid(row=counter, column=1)
            self.sample_type_option_list.append((item, sample_type_menu, sample_type_string_variable))
            report_type_string_variable = Tk.StringVar(self.samples_checklist_frame)
            report_type_choices = {'Basic', 'Deluxe'}
            report_type_string_variable.set('Basic')
            report_type_menu = Tk.OptionMenu(self.samples_checklist_frame,
                                             report_type_string_variable,
                                             *report_type_choices)
            report_type_menu.grid(row=counter, column=2)
            self.report_type_option_list.append((item, report_type_menu, report_type_string_variable))
            multi_or_single_variable = Tk.StringVar(self.samples_checklist_frame)
            multi_or_single_choices = {'Multi', 'Single'}
            multi_or_single_variable.set('Multi')
            multi_single_menu = Tk.OptionMenu(self.samples_checklist_frame,
                                              multi_or_single_variable,
                                              *multi_or_single_choices)
            multi_single_menu.grid(row=counter, column=3)
            self.single_or_multi_list.append((item, multi_single_menu, multi_or_single_variable))
            unit_or_density_entry = Tk.Entry(self.samples_checklist_frame)
            unit_or_density_entry.insert(Tk.END, 1.0)
            unit_or_density_entry.grid(row=counter, column=4)
            self.density_unit_weight_list.append((item, unit_or_density_entry))
            density_or_unit_variable = Tk.StringVar(self.samples_checklist_frame)
            density_or_unit_choices = {'density', 'unit'}
            density_or_unit_variable.set('density')
            density_unit_menu = Tk.OptionMenu(self.samples_checklist_frame,
                                              density_or_unit_variable,
                                              *density_or_unit_choices)
            density_unit_menu.grid(row=counter, column=5)
            self.density_unit_weight_option_list.append((item, density_unit_menu, density_or_unit_variable))
            sample_name_entry = Tk.Entry(self.samples_checklist_frame)
            Tk.Label(self.samples_checklist_frame, text="   Sample name: ").grid(row=counter, column=6)
            sample_name_entry.grid(row=counter, column=7)
            self.sample_name_list.append((item, sample_name_entry))
            counter += 1
        Tk.Button(self.samples_checklist_frame,
                  text="Generate Batch",
                  command=lambda x=data: self.generate_batch(x), font=self.header_font).grid(row=counter,
                                                                                             column=0,
                                                                                             padx=10,
                                                                                             pady=20,
                                                                                             sticky=Tk.W,
                                                                                             columnspan=2)

    def display_sample_data(self, data):
        samples_label = Tk.Label(self.display_sample_data_frame, text="Raw Data - All Samples",
                                 font=self.header_font)
        samples_label.grid(row=0, column=0, sticky=Tk.W)
        samples_text = Tk.Text(self.display_sample_data_frame, width=100, height=100)
        samples_text.insert(Tk.END, data.dm.condensed_samples_data_frame.to_string())
        samples_text.config(state="disabled")
        samples_text.grid(row=1, column=0)

    def generate_batch(self, data):
        self.updated_sample_type_option_list = [var.get() for item, menu, var in self.sample_type_option_list]
        self.updated_report_type_option_list = [var.get() for item, menu, var in self.report_type_option_list]
        self.updated_single_or_multi_list = [var.get() for item, menu, var in self.single_or_multi_list]
        self.update_header_information_list = [var.get()
                                               for key, variables in self.header_information_list for var in variables]
        self.updated_sample_information_list = [var.get("1.0", Tk.END) for item, var in self.sample_information_list]
        self.updated_density_unit_weight_list = [float(var.get()) for item, var in self.density_unit_weight_list]
        self.updated_density_unit_weight_option_list =\
            [var.get() for item, menu, var in self.density_unit_weight_option_list]
        self.updated_sample_name_list = [[item, var.get()] for item, var in self.sample_name_list]
        self.updated_dictionary['sample type'] = self.updated_sample_type_option_list
        self.updated_dictionary['report type'] = self.updated_report_type_option_list
        self.updated_dictionary['single multi'] = self.updated_single_or_multi_list
        self.updated_dictionary['headers'] = self.update_header_information_list
        self.updated_dictionary['samples'] = self.updated_sample_information_list
        self.updated_dictionary['density_unit'] = self.updated_density_unit_weight_list
        self.updated_dictionary['density_unit_option'] = self.updated_density_unit_weight_option_list
        self.updated_dictionary['sample names'] = self.updated_sample_name_list
        self.post_generate_controller(data.dm, data.hp)

    def post_generate_controller(self, sample_data, header_data):
        counter = 0
        for key, value in header_data.header_contents_dictionary.items():
            for item in range(0, 17):
                header_data.header_contents_dictionary[key][item] = \
                    self.updated_dictionary['headers'][counter]
                counter += 1
            datestring = "Date: " + header_data.header_contents_dictionary[key][1] + " (" + header_data.header_contents_dictionary[key][2] + ")"
            sourcestring = "Source: " + header_data.header_contents_dictionary[key][7]
            subtype_string = "Type: " + header_data.header_contents_dictionary[key][8]
            samplenumberstring = "No. of Samples: " + header_data.header_contents_dictionary[key][9]
            arrivaltempstring = "Arrival temp: " + header_data.header_contents_dictionary[key][10]
            endinfo3string = header_data.header_contents_dictionary[key][14]
            self.lengthlist = [len(datestring),
                               len(sourcestring),
                               len(subtype_string),
                               len(samplenumberstring),
                               len(arrivaltempstring),
                               len(endinfo3string)]
            longest = max(self.lengthlist)
            lengthlist_counter = 0
            for item in self.lengthlist:
                if item != longest:
                    offset = longest - item - 1
                    offset = "x" * offset
                    offset = r'\phantom{' + offset + "}"
                    self.lengthlist[lengthlist_counter] = offset
                    lengthlist_counter += 1
                else:
                    offset = r'\phantom{}'
                    self.lengthlist[lengthlist_counter] = offset
                    lengthlist_counter += 1
            header_data.header_contents_dictionary[key].append(self.lengthlist)
        header_counter = 15
        counter = 0
        sample_names_master_list = []
        for key, value in header_data.header_contents_dictionary.items():
            jobnumber_to_match = value[3][1:]
            print(jobnumber_to_match)
            empty_list_for_matching = []
            print(self.updated_dictionary['sample names'])
            for item in self.updated_dictionary['sample names']:
                if int(item[0][0:6]) == int(jobnumber_to_match):
                    if len(str(item[0])) == 8:
                        string = r'\textbf{' + item[0][-1] + r')} ' + item[1]
                        empty_list_for_matching.append(string)
                    else:
                        string = r'\textbf{' + item[0][-2:] + r')} ' + item[1]
                        empty_list_for_matching.append(string)
                else:
                    pass
            sample_names_master_list.append(' '.join([i for i in empty_list_for_matching]))
        for key, value in header_data.header_contents_dictionary.items():
            header_data.header_contents_dictionary[key][header_counter] = sample_names_master_list[counter]
            counter += 1
        batch_report = report(sample_data, header_data, self.updated_dictionary)
        batch_report.post_generate_controller()


