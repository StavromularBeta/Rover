import tkinter as Tk
from tkinter import ttk


class BatchWindow(Tk.Frame):
    def __init__(self, parent, **kwargs):
        Tk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.master_display_frame = Tk.Frame(self)
        self.sub_display_frame = Tk.Frame(self)
        self.blank_data_frame = Tk.Frame(self.sub_display_frame)
        self.recovery_data_frame = Tk.Frame(self.sub_display_frame)
        self.headers_data_frame = Tk.Frame(self.sub_display_frame)
        self.samples_list_frame = Tk.Frame(self.sub_display_frame)

    def batch(self, data):
        self.create_scrollable_window()
        self.blank_data_frame.grid(row=0, column=0)
        self.recovery_data_frame.grid(row=0, column=1)
        self.headers_data_frame.grid(row=1, column=0, columnspan=2)
        self.samples_list_frame.grid(row=2, column=0, columnspan=2)
        self.create_blank_frame(data)
        self.create_recovery_frame(data)
        self.create_header_frames(data)
        self.create_sample_list_frame(data)

    def create_scrollable_window(self):
        display_all_jobs_canvas = Tk.Canvas(self.master_display_frame,
                                            width=1080,
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
        blank_label = Tk.Label(self.blank_data_frame, text="Blank Data")
        blank_label.grid(row=0, column=0)
        blank_text = Tk.Text(self.blank_data_frame, width=18, height=20)
        blank_text.insert(Tk.END, data.dm.min_value_blank_data_frame.to_string())
        blank_text.config(state="disabled")
        blank_text.grid(row=1, column=0)

    def create_recovery_frame(self, data):
        recovery_label = Tk.Label(self.recovery_data_frame, text="Standard Recovery Data")
        recovery_label.grid(row=0, column=0)
        recovery_text = Tk.Text(self.recovery_data_frame, width=60, height=20)
        recovery_text.insert(Tk.END, data.dm.best_recovery_qc_data_frame.to_string())
        recovery_text.config(state="disabled")
        recovery_text.grid(row=1, column=0)

    def create_header_frames(self, data):
        counter = 0
        column_counter = 1
        Tk.Label(self.headers_data_frame, text="Client Name").grid(row=1, column=0)
        Tk.Label(self.headers_data_frame, text="Date").grid(row=2, column=0)
        Tk.Label(self.headers_data_frame, text="Time").grid(row=3, column=0)
        Tk.Label(self.headers_data_frame, text="Job Number").grid(row=4, column=0)
        Tk.Label(self.headers_data_frame, text="Address 1").grid(row=5, column=0)
        Tk.Label(self.headers_data_frame, text="Address 2").grid(row=6, column=0)
        Tk.Label(self.headers_data_frame, text="Address 3").grid(row=7, column=0)
        Tk.Label(self.headers_data_frame, text="Sample Type 1").grid(row=8, column=0)
        Tk.Label(self.headers_data_frame, text="Sample Type 2").grid(row=9, column=0)
        Tk.Label(self.headers_data_frame, text="Number of Samples").grid(row=10, column=0)
        Tk.Label(self.headers_data_frame, text="Receive Temp.").grid(row=11, column=0)
        Tk.Label(self.headers_data_frame, text="Additional Info 1").grid(row=12, column=0)
        Tk.Label(self.headers_data_frame, text="Additional Info 2").grid(row=13, column=0)
        Tk.Label(self.headers_data_frame, text="Additional Info 3").grid(row=14, column=0)
        Tk.Label(self.headers_data_frame, text="Payment Info").grid(row=15, column=0)
        for key, value in data.hp.header_contents_dictionary.items():
            header_frame_label = Tk.Label(self.headers_data_frame, text=key)
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
            address_entry = Tk.Entry(self.headers_data_frame)
            address_entry.insert(Tk.END, value[4])
            address_entry.grid(row=counter, column=column_counter)
            counter += 1
            address_entry_2 = Tk.Entry(self.headers_data_frame)
            address_entry_2.insert(Tk.END, value[6])
            address_entry_2.grid(row=counter, column=column_counter)
            counter += 1
            address_entry_3 = Tk.Entry(self.headers_data_frame)
            address_entry_3.insert(Tk.END, value[8])
            address_entry_3.grid(row=counter, column=column_counter)
            counter += 1
            sample_type_entry_1 = Tk.Entry(self.headers_data_frame)
            sample_type_entry_1.insert(Tk.END, value[5])
            sample_type_entry_1.grid(row=counter, column=column_counter)
            counter += 1
            sample_type_entry_2 = Tk.Entry(self.headers_data_frame)
            sample_type_entry_2.insert(Tk.END, value[7])
            sample_type_entry_2.grid(row=counter, column=column_counter)
            counter += 1
            number_of_samples_entry = Tk.Entry(self.headers_data_frame)
            number_of_samples_entry.insert(Tk.END, value[9])
            number_of_samples_entry.grid(row=counter, column=column_counter)
            counter += 1
            receive_temp = Tk.Entry(self.headers_data_frame)
            receive_temp.insert(Tk.END, value[11])
            receive_temp.grid(row=counter, column=column_counter)
            counter += 1
            additional_info_1 = Tk.Entry(self.headers_data_frame)
            additional_info_1.insert(Tk.END, value[10])
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

    def create_sample_list_frame(self, data):
        counter = 0
        for key, value in data.hp.header_contents_dictionary.items():
            Tk.Label(self.samples_list_frame, text=key + " samples list").grid(row=counter, column=0)
            samples_list_text = Tk.Text(self.samples_list_frame, width=80, height=10)
            samples_list_text.insert(Tk.END, value[16])
            counter += 1
            samples_list_text.grid(row=counter, column=0)
            counter += 1


