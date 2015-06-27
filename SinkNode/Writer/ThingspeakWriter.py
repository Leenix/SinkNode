import httplib
import urllib
import time
import logging
from SinkNode.Formatter.ThingspeakFormatter import ThingspeakFormatter
from SinkNode.Writer import Writer

__author__ = 'Leenix'

SERVER_ADDRESS = "api.thingspeak.com:80"
THINGSPEAK_DELAY = 15

HEADERS = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}


class ThingspeakWriter(Writer):
    def __init__(self,
                 writer_id,
                 api_key,
                 key_map,
                 drop_failed_entries=True,
                 server_address=SERVER_ADDRESS,
                 upload_delay=THINGSPEAK_DELAY,
                 logger_level=logging.FATAL):

        self.formatter = ThingspeakFormatter(api_key,
                                             key_map,
                                             outbox=None,
                                             logger_level=logger_level,
                                             formatter_id=writer_id+"Formatter")

        super(ThingspeakWriter, self).__init__(formatter=self.formatter, logger_level=logger_level, writer_id=writer_id)

        self.id = writer_id
        self.api_key = api_key
        self.server_address = server_address
        self.upload_delay = upload_delay
        self.drop_failed_entries = drop_failed_entries

    def write_entry(self, entry):
        """
        Upload the entry to Thingspeak
        :param entry: Processed entry
        :return:
        """
        packet_uploaded = False

        while not packet_uploaded:

            try:
                self.logger.debug("Attempting upload...")

                # TODO - Switch to 'requests' library instead of httplib/urllib
                params = urllib.urlencode(entry)
                conn = httplib.HTTPConnection(self.server_address)
                conn.request("POST", "/update", params, HEADERS)
                response = conn.getresponse()
                self.logger.info("Response: %s", response)
                conn.close()

                packet_uploaded = True
                self.logger.info("Upload successful")

                # Thingspeak can only accept a packet every 15 seconds
                time.sleep(self.upload_delay)

            except Exception:
                self.logger.warning("Packet could not be uploaded")
                if self.drop_failed_entries:
                    packet_uploaded = True
                time.sleep(2)




