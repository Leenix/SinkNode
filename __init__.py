__author__ = 'Leenix'

from Reader import *
from Processor import *
from Uploader import *


class SinkNode:
    """
    Simple data ingestor made up of 3 processes: a reader, processor, and uploader.

    Reader      - Reads in data from a source and produces a JSON-format packet
    Processor   - Alters the data for uploading/storage
    Uploader    - Uploads the processed data to a server or file

    All processes use individual threads with data between transferred using data queues.
    """

    def __init__(self, reader, processor, uploader):
        self.read_queue = Queue()
        self.upload_queue = Queue()

        assert isinstance(reader, Reader)
        self.reader = reader
        self.reader.set_queue(self.read_queue)

        assert isinstance(processor, Processor)
        self.processor = processor
        self.processor.set_inbox(self.read_queue)
        self.processor.set_outbox(self.upload_queue)

        assert isinstance(uploader, Uploader)
        self.uploader = uploader
        self.uploader.set_queue(self.upload_queue)

    def run(self):
        self.reader.run()
        self.processor.run()
        self.uploader.run()

    def stop(self):
        self.reader.stop()
        self.processor.stop()
        self.uploader.stop()
