import logging

__author__ = 'Leenix'

from Queue import Queue


class Uploader:
    def __init__(self):
        self.upload_queue = Queue()
        self.logger = logging.getLogger(__name__)

    def stop(self):
        """
        Stop the uploading
        :return: None
        """
        raise Exception("Method [stop] not implemented")

    def run(self):
        """
        Start uploading packets
        :return: None
        """
        raise Exception("Method [run] not implemented")

    def upload_entry(self, entry):
        """
        Upload the entry to its destination
        :param entry: Entry to be uploaded
        :return: None
        """
        raise Exception("Method [upload_entry] not implemented")

    def set_queue(self, queue):
        assert isinstance(queue, Queue)
        self.upload_queue = queue