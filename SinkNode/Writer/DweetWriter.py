__author__ = 'Leenix'

from SinkNode.Writer import Writer
from SinkNode.Formatter.RawFormatter import RawFormatter
import requests
import logging

__author__ = 'Leenix'

SERVER_ADDRESS = "http://dweet.io/dweet/for/"


class DweetWriter(Writer):
    def __init__(self, writer_id, drop_failed_entries=True,
                 server_address=SERVER_ADDRESS,
                 logger_level=logging.FATAL):

        self.formatter = RawFormatter(outbox=None, logger_level=logger_level, formatter_id=writer_id+"Formatter")
        super(DweetWriter, self).__init__(formatter=self.formatter, logger_level=logger_level, writer_id=writer_id)

        self.id = writer_id
        self.server_address = "{0}{1}?".format(server_address, writer_id)
        self.drop_failed_entries = drop_failed_entries

    def write_entry(self, entry):
        """
        Upload the entry to Thingspeak
        :param entry: Processed entry
        :return:
        """
        packet_uploaded = False
        response = None

        while not packet_uploaded:

            try:
                self.logger.debug("Attempting upload...")
                response = requests.get(self.server_address, params=entry).json()

                packet_uploaded = True
                self.logger.info("Upload successful - Response {}".format(response))

            except Exception:
                self.logger.warning("Packet could not be uploaded")
                if self.drop_failed_entries:
                    packet_uploaded = True

        return response








