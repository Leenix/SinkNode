from SinkNode.Formatter import Formatter
import logging

__author__ = 'Leenix'


class CSVFormatter(Formatter):
    def __init__(self, outbox=None, logger_level=logging.FATAL):
        super(CSVFormatter, self).__init__(outbox=outbox, logger_level=logger_level, formatter_id="CSVFormatter")

        self.columns = []

    def format_entry(self, entry):
        """
        Processes JSON entries into CSV format

        :param entry: JSON entry in 'column':'value' format
        :return: CSV entry in 'value','value','value' format
        """

        output = ""

        new_columns = len(self.columns) > 0

        # See if a column order has been established
        if new_columns:
            # Order already established - put values into columns
            for key in self.columns:
                if key in entry.keys():
                    output += str(entry.pop(key))
                else:
                    output += "-"
                output += ","

        # Check for any left-over columns that need to be added
        new_columns = len(entry) > 0

        if new_columns:
            self.logger.info("New columns added - %s", entry.keys())
            keys = entry.keys()
            for key in keys:

                self.columns.append(key)
                output += str(entry.pop(key))
                output += ","

            # Prepend the headings
            output = "{0}\n{1}".format(str(self.columns).strip('[]').replace(" ", ""), output)

        # Trim the extra comma at the end
        return output[:-1]
