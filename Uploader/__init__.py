__author__ = 'Leenix'

from Queue import Queue


class Uploader:
    def __init__(self):
        self.upload_queue = Queue()

    def stop(self):
        raise Exception("Method [stop] not implemented")

    def run(self):
        raise Exception("Method [run] not implemented")

    def upload_entry(self, entry):
        raise Exception("Method [upload_entry] not implemented")

    def set_queue(self, queue):
        assert isinstance(queue, Queue)
        self.upload_queue = queue