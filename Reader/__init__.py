__author__ = 'Leenix'

from Queue import Queue
import json


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
        Convert the entry line to JSON
        Entry lines should already be in a JSON string; extract it.

        :param entry_line: JSON-formatted string
        :return: JSON object of the entry string
        """

        entry = ""
        try:
            entry = json.loads(entry_line)

        except ValueError:
            pass

        return entry

    def set_queue(self, queue):
        assert isinstance(queue, Queue)
        self.reader_queue = queue

