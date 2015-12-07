import logging
from SinkNode.Writer import Writer
import datetime

__author__ = 'Leenix'


class LogFileWriter(Writer):
    def __init__(self, filename,
                 path="",
                 formatter=None,
                 file_time_prefix=None,
                 logger_level=logging.FATAL,
                 writer_id=__name__,
                 timestamp_format=None):

        super(LogFileWriter, self).__init__(formatter=formatter, logger_level=logger_level, writer_id=writer_id)
        self.logger.name = writer_id
        self.path = path
        self.filename = filename
        self.file_time_prefix = file_time_prefix
        self.timestamp_format = timestamp_format

    def write_entry(self, entry):
        """
        Append the entry to a logfile.
        Each entry is terminated by a newline character
        If 'file_time_prefix' is enabled, a new log file will be created every month to avoid gigantic files...
        :param entry:
        :return:
        """
        prefix = ""
        if self.file_time_prefix is not None:
            prefix = datetime.datetime.now().strftime(self.file_time_prefix)

        logfile = open(self.path + prefix + self.filename, 'ab')

        # Add the entry line-by-line to include a timestamp on each line
        entry_lines = str(entry).split('\n')

        for line in entry_lines:
            if self.timestamp_format is not None:
                logfile.write(datetime.datetime.now().strftime(self.timestamp_format))
                logfile.write(",")
            logfile.write(str(line))
            logfile.write('\n')
        logfile.close()


