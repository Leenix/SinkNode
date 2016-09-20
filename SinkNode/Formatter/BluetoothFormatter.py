from SinkNode.Formatter import Formatter
import logging
import datetime
from netaddr import *


class BluetoothFormatter(Formatter):
    def __init__(self, outbox=None, logger_level=logging.FATAL):
        super(BluetoothFormatter, self).__init__(outbox=outbox, logger_level=logger_level, formatter_id="BluetoothFormatter")

    def format_entry(self, entry):
        """
        Processes JSON entries into CSV format

        :param entry: JSON entry in 'column':'value' format
        :return: CSV entry in 'value','value','value' format
        """

        output = ""

        self.logger.debug("Received: {}".format(entry))

        data = entry["data"]

        # Check if there is data to be read
        if len(data) > 0 and data.startswith("Found"):
            # Extract the device info line-by-line
            lines = entry["data"].split('|')

            for i in xrange(1, len(lines)-2):
                fields = lines[i].split(',')

                output += datetime.datetime.now().strftime("%Y-%m-%d,%H:%M:%S")
                for j in xrange(0, len(fields)):
                    output += ",{}".format(fields[j])

                    # Grab the MAC vendor while we're here
                    if j == 0:
                        try:
                            vendor = EUI(fields[j]).oui.registration().org

                        except NotRegisteredError:
                            vendor = 'Unregistered'
                        output += ",{}".format(vendor.replace(",", ""))

                output += '\n'
        return output[:-1]

