import sys
import logging

from SinkNode.Reader import Reader


class StandardInReader(Reader):
    """
    Serial reader that sorts the incoming stream into packets.
    """

    def __init__(self, start_delimiter=None, stop_delimiter='\n', logger_level=logging.FATAL):
        self.start_delimiter = start_delimiter
        self.stop_delimiter = stop_delimiter

        super(StandardInReader, self).__init__(logger_level=logger_level)

        self.logger.name = 'StandardInReader'

    def read_entry(self):
        """
        Read in an entry from the console
        :return:
        """

        is_recording = False

        if self.start_delimiter is None:
            is_recording = True

        output = ""

        # Wait for the entry to start...
        while not is_recording:
            c = sys.stdin.read(1)
            if c == self.start_delimiter:
                is_recording = True

        # Read the entry until we get a stop character
        c = sys.stdin.read(1)
        while c != self.stop_delimiter:
            output += c
            c = sys.stdin.read(1)

        return str(output)



