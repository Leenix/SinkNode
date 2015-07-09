import logging
from SinkNode.Writer import Writer
import datetime

__author__ = 'Leenix'


class LogFileWriter(Writer):
    def __init__(self, filename,
                 path="",
                 formatter=None,
                 timestamp=True,
                 monthly_files=True,
                 logger_level=logging.FATAL,
                 writer_id=__name__):

        super(LogFileWriter, self).__init__(formatter=formatter, logger_level=logger_level, writer_id=writer_id)
        self.logger.name = writer_id
        self.path = path
        self.filename = filename
        self.monthly_files = monthly_files
        self.timestamp_enabled = timestamp

    def write_entry(self, entry):
        """
        Append the entry to a logfile.
        Each entry is terminated by a newline character
        If 'monthly_files' is enabled, a new log file will be created every month to avoid gigantic files...
        :param entry:
        :return:
        """
        prefix = ""
        if self.monthly_files:
            prefix = datetime.datetime.now().strftime("%Y-%m ")

        logfile = open(self.path + prefix + self.filename, 'ab')

        # Add the entry line-by-line to include a timestamp on each line
        entry_lines = str(entry).split('\n')

        for line in entry_lines:
            if self.timestamp_enabled:
                logfile.write(datetime.datetime.now().strftime("%Y-%m-%d,%H:%M"))
                logfile.write(",")
            logfile.write(str(line))
            logfile.write('\n')
        logfile.close()


