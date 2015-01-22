__author__ = 'Leenix'

from Queue import Queue


class Reader:
    """
    Parent class.
    Reads data from a source, which is specified by the child class.
    Data is converted into JSON format, then placed in a queue for processing.
    """
    def __init__(self):
        self.reader_queue = Queue()

    def stop(self):
        """
        Halt the reading process.
        Halting the read does not affect the read queue.
        :return:
        """
        raise Exception("Method [stop] not implemented")

    def run(self):
        """
        Read in packets of data and convert them to JSON format
        JSON packets are placed in the read queue to await further processing
        :return:
        """
        raise Exception("Method [run] not implemented")

    def convert_to_json(self, entry_line):
        """
        Convert the received entry to JSON format
        Actual format depends on child class method

        :param entry_line: Packetised entry line to be formatted
        :return: Entry in JSON format
        """
        raise Exception("Method [run] not implemented")

    def set_queue(self, queue):
        assert isinstance(queue, Queue)
        self.reader_queue = queue

