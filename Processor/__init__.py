__author__ = 'Leenix'

from Queue import Queue
import logging


class Processor:
    """
    Parent class.
    Transforms incoming JSON data packets to another format for uploading.
    Output format is dictated by the child class.
    Processed packets are placed into a queue for uploading.
    """
    def __init__(self):
        self.in_queue = Queue()
        self.out_queue = Queue()

        self.logger = logging.getLogger(__name__)

    def stop(self):
        """
        Stop processing incoming packets
        :return: None
        """
        raise Exception("Method [stop] not implemented")

    def run(self):
        """
        Start processing incoming packets
        :return: None
        """
        raise Exception("Method [run] not implemented")

    def process_entry(self, entry):
        """
        Transform the incoming entry
        :param entry: Incoming packet
        :return: Processed packet
        """
        raise Exception("Method [process_entry] not implemented")

    def set_inbox(self, in_queue):
        """
        Set the incoming packet queue
        :param in_queue: Queue of packets needing to be processed
        :return: None
        """
        assert isinstance(in_queue, Queue)
        self.in_queue = in_queue

    def set_outbox(self, out_queue):
        """
        Set the outgoing packet queue
        :param out_queue: Queue of packets that have been processed
        :return: None
        """
        assert isinstance(out_queue, Queue)
        self.out_queue = out_queue
