import pandas as pd


class PreGenerateMainScript:
    """This file controls the processes occurring prior to generating latex files. Raw data -> Processed data."""

    def __init__(self, data_xml_file):
        """The main init function.

            data_xml_file = the raw xml data file produced by TargetLynx. This must be manually placed in the datafiles
        folder to be read by Rover. The name of it is passed to init.
            raw_xml_data_frame = the first DataFrame produced from the xml file. At this point, the data is not
        manipulated in any way.
            percentage_data_frame = changes: analytical concentration converted to percentage concentration."""

        self.data_xml_file = data_xml_file
        self.raw_xml_data_frame = pd.DataFrame()
        self.percentage_data_frame = pd.DataFrame()
        self.blank_data_frame = pd.DataFrame()
        self.qc_data_frame = pd.DataFrame()
        self.samples_data_frame = pd.DataFrame()

    def pre_generate_controller(self):
        """The main controller function. To run the methods that make up this class, this function is called."""
        self.collect_data_from_xml_file()
        self.convert_analytical_concentration_to_percentage_concentration()
        self.split_into_blank_qc_and_sample_data_frame()
        print(self.blank_data_frame)
        print(self.qc_data_frame)
        print(self.samples_data_frame)

    def collect_data_from_xml_file(self):
        """Reads the xml data, saves it to a Pandas DataFrame.

        the columns of the raw DataFrame are as follows:
            1) id15: the id in the batch. First standard/blank/sample is 1, second is 2, etc.
            2) sampleid: the sample number, or the name of the standard/blank.
            3) id17: the id of the particular analyte for the row.
            4) name20: the name of the particular analyte for the row.
            5) initamount: the mass, in grams, of the sample.
            6) area: the peak area of the analyte from the chromatogram.
            7) analconc: the concentration calculated by TargetLynx. This will improve after analyst peak integration.
            8) percrecovery: the percentage recovery of ibuprofen.
            9) type: Blank, QC, or analyte.
            """
        raw_xml_data = pd.read_excel(self.data_xml_file,)
        self.raw_xml_data_frame = pd.DataFrame(raw_xml_data,
                                               columns=['id15',
                                                        'sampleid',
                                                        'id17',
                                                        'name20',
                                                        'initamount',
                                                        'area',
                                                        'analconc',
                                                        'percrecovery',
                                                        'type']
                                               )

    def convert_analytical_concentration_to_percentage_concentration(self):
        """converts the analytical concentration to a percent concentration. Saves as a new DataFrame."""
        self.percentage_data_frame = self.raw_xml_data_frame
        self.percentage_data_frame['percentage_concentration'] = self.percentage_data_frame['analconc']/10000

    def split_into_blank_qc_and_sample_data_frame(self):
        """splits the percentage DataFrame into blank, qc, and sample DataFrames, based on the 'type' column."""
        self.blank_data_frame = self.percentage_data_frame[self.percentage_data_frame.type == "Blank"]
        self.qc_data_frame = self.percentage_data_frame[self.percentage_data_frame.type == "QC"]
        self.samples_data_frame = self.percentage_data_frame[self.percentage_data_frame.type == "Analyte"]


pre_generate = PreGenerateMainScript(r'T:\ANALYST WORK FILES\Peter\Rover\xml_data_files\data_6.xlsx')
pre_generate.pre_generate_controller()
