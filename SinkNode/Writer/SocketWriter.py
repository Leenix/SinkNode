__author__ = 'Leenix'

from SinkNode.Writer import Writer
from SinkNode.Formatter.RawFormatter import RawFormatter
import socket
import logging


class SocketWriter(Writer):
    def __init__(self, writer_id, server_address='http://localhost', server_port=8888, logger_level=logging.FATAL):

        self.formatter = RawFormatter(outbox=None, logger_level=logger_level, formatter_id=writer_id + "Formatter")
        super(SocketWriter, self).__init__(formatter=self.formatter, logger_level=logger_level, writer_id=writer_id)

        self.id = writer_id
        self.server_address = server_address
        self.server_port = server_port

    def write_entry(self, entry):
        """
        Send the data entry to the specified socket
        :param entry: The string formatted data entry to send
        """

        # Establish a TCP socket connection and send the data
        client_socket = socket.socket()

        self.logger.debug("Connecting to server: {}:{}".format(self.server_address, self.server_port))
        client_socket.connect((self.server_address, self.server_port))

        self.logger.debug("Sending: [{}]".format(str(entry)))
        client_socket.send(str(entry) + '\n')
        client_socket.close()

