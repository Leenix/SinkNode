from SinkNode.Formatter import Formatter
import logging
import datetime
from netaddr import *
import json


class WiFiFormatter(Formatter):
    def __init__(self, outbox=None, logger_level=logging.FATAL, entry_delimiter='|'):
        super(WiFiFormatter, self).__init__(outbox=outbox, logger_level=logger_level, formatter_id="WiFiFormatter")
        self.entry_delimiter = entry_delimiter

    def format_entry(self, entry):
        """
        Processes JSON entries into CSV format

        :param entry: JSON entry in 'column':'value' format
        :return: CSV entry in 'value','value','value' format
        """

        output = ""

        self.logger.debug("Received: {}".format(entry))

        data = entry["payload"]

        # Check if there is data to be read
        if len(data) > 0:
            # Extract the device info line-by-line
            lines = data.split(self.entry_delimiter)

            for i in xrange(0, len(lines)):
                self.logger.debug("Line: {}".format(lines[i]))

                if len(lines[i]) > 0:
                    try:
                        entry_line = json.loads(lines[i])

                        eui = entry_line["eui"]
                        vendor = entry_line["vendor"]
                        ssid = entry_line["ssid"]
                        last_seen = entry_line["last_seen"]

                        output += "{},{},{},{}\n".format(eui, vendor, ssid, last_seen)

                    except ValueError:
                        self.logger.error("Could not decode line: {}".format(lines[i]))

        return output[:-1]  # Lines are automatically terminated with a newline

