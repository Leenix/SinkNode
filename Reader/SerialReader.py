import sys
import logging
from threading import Thread
import json

import serial
from serial import SerialException

from ..Reader import *


class SerialReader(Reader):
    """
    Serial reader that sorts the incoming stream into packets.
    """

    def __init__(self, port, baud_rate, start_delimiter=None, stop_delimiter='\n',
                 logger_level=logging.CRITICAL):

        self.start_delimiter = start_delimiter
        self.stop_delimiter = stop_delimiter

        self.port = port
        self.baud_rate = baud_rate
        self.ser = serial.Serial()

        self.is_reading = False
        self.read_thread = Thread(name="read_thread", target=self._read_loop())

        logging.basicConfig(level=logger_level)
        self.logger = logging.getLogger(__name__)

    def run(self):
        """
        Start the read loop for Serial input.
        Received packets are entered into the read_queue.

        :return: None
        """

        try:
            self.logger.info("Opening serial port [{}] with {} baud".format(self.port, self.baud_rate))
            self.ser.setBaudrate(self.baud_rate)
            self.ser.setPort(self.port)
            self.ser.open()

        except SerialException:
            self.logger.critical("Serial port [{}] cannot be opened :(".format(self.port))
            sys.exit()

        self.logger.info("Starting reader")
        self.is_reading = True
        self.read_thread.run()

    def stop(self):
        """
        Halt all reading operations
        The read queue is not cleared by stopping the reader

        :return: None
        """

        self.logger.info("Stopping reader")
        self.ser.close()
        self.is_reading = False

    def _read_loop(self):
        """
        Reading loop to be run by thread.
        Loop will run until manually stopped

        :return: None
        """
        recording_entry = False
        received = ""

        while self.is_reading:

            c = self.ser.read()

            # Don't record any incoming characters until a 'start' is received
            if not recording_entry:
                if c == self.start_delimiter:
                    recording_entry = True

            # Only stop recording when a 'stop' is received
            else:
                if not c == self.stop_delimiter:
                    received += c

                else:
                    entry = self.convert_to_json(received)
                    self.logger.debug("Incoming packet: {}".format(entry))
                    self.read_queue.put(entry)

    def convert_to_json(self, entry_line):
        """
        Convert the entry line to JSON
        Entry lines should already be in a JSON string; extract it.

        :param entry_line: JSON-formatted string
        :return: JSON object of the entry string
        """
        try:
            entry = json.loads(entry_line)

        except ValueError:
            pass

        return entry

