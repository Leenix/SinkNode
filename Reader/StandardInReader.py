import sys
import logging
from threading import Thread


from SinkNode.Reader import *


class StandardInReader(Reader):
    """
    Serial reader that sorts the incoming stream into packets.
    """

    def __init__(self, start_delimiter=" ", stop_delimiter='\n', logger_name=__name__):
        self.start_delimiter = start_delimiter
        self.stop_delimiter = stop_delimiter

        self.logger = logging.getLogger(logger_name)
        if self.logger.name == __name__:
            self.logger.addHandler(logging.StreamHandler())
            self.logger.setLevel(logging.INFO)

        self.reader_queue = Queue()

        self.is_reading = False
        self.read_thread = Thread(name="read_thread", target=self._read_loop)

    def start(self):
        """
        Start the read loop for Serial input.
        Received packets are entered into the read_queue.

        :return: None
        """

        self.logger.debug("Starting reader thread")
        self.is_reading = True
        self.read_thread.start()

    def stop(self):
        """
        Halt all reading operations
        The read queue is not cleared by stopping the reader

        :return: None
        """

        self.logger.debug("Stopping reader thread")
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

            c = sys.stdin.read(1);

            # Don't record any incoming characters until a 'start' is received
            if not recording_entry:
                if c == self.start_delimiter:
                    recording_entry = True

            # Only stop recording when a 'stop' is received
            else:
                if not c == self.stop_delimiter:
                    received += c

                else:
                    recording_entry = False
                    entry = self.convert_to_json(received)
                    self.logger.info("Incoming packet: {}".format(entry))
                    self.reader_queue.put(entry)
                    received = ""


if __name__ == '__main__':
    read_queue = Queue()
    logger = logging.getLogger("StandardInReader")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    reader = StandardInReader(logger_name=logger.name)

    reader.set_queue(read_queue)
    reader.start()

    while True:
        packet = read_queue.get()
        logger.info("Packet: {}".format(packet))
        read_queue.task_done()


