import os.path
import errno


class FileWritingMethods:
    """The methods in this class create the files and file directories that make up the finished latex reports, and then
     write the reports to said files. """

    def __init__(self, finished_reports_dictionary, basic_reports_dictionary):
        """
        1. finished_reports_dictionary = finished reports ready to be written, at this point in the procedure.
        """
        self.finished_reports_dictionary = finished_reports_dictionary
        self.basic_reports_dictionary = basic_reports_dictionary

    def generate_report_directories_and_files(self):
        """creates a file at a given target and names it based on the key in finished_reports_dictionary - the key will
        be the 6 digit job number for multi sample reports, and the -XX number for single reports. The directory is
        always named using the 6 digit job number. """
        target = r'T:\ANALYST WORK FILES\Peter\Rover\reports\ '
        for key, value in self.finished_reports_dictionary.items():
            try:
                jobnumber = str(key)
                filename = target[:-1] + jobnumber[0:6] + '\\' + jobnumber + '_raw.tex'
                filename = filename.replace('/', '-')
                with self.safe_open_w(filename) as f:
                    f.write(value)
            except OSError:
                pass
        for key, value in self.basic_reports_dictionary.items():
            try:
                jobnumber = str(key)
                filename = target[:-1] + jobnumber + '\\' + jobnumber + '.txt'
                filename = filename.replace('/', '-')
                with self.safe_open_w(filename) as f:
                    for item in value:
                        f.write(item[0])
                        f.write(item[1].to_string())
                        f.write('\n\n')
            except OSError:
                pass

    def mkdir_p(self, path):
        """tries to make the directory."""
        try:
            os.makedirs(path)
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def safe_open_w(self, path):
        """ Open "path" for writing, creating any parent directories as needed. """
        self.mkdir_p(os.path.dirname(path))
        return open(path, 'w')