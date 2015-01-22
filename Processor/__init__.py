__author__ = 'Leenix'

from Queue import Queue


class Processor:
    def __init__(self):
        self.in_queue = Queue()
        self.out_queue = Queue()

    def stop(self):
        raise Exception("Method [stop] not implemented")

    def run(self):
        raise Exception("Method [run] not implemented")

    def process_entry(self):
        raise Exception("Method [process_entry] not implemented")

    def set_inbox(self, in_queue):
        assert isinstance(in_queue, Queue)
        self.in_queue = in_queue

    def set_outbox(self, out_queue):
        assert isinstance(out_queue, Queue)
        self.out_queue = out_queue
