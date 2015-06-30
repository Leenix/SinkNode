import Queue

__author__ = 'Leenix'

from SinkNode.Writer import Writer
from SinkNode.Formatter.RawFormatter import RawFormatter
import logging


class QueueWriter(Writer):
    """
    Pass the entry to an external queue
    """
    def __init__(self, outbox, writer_id='QueueWriter', logger_level=logging.FATAL):
        self.formatter = RawFormatter(outbox=None, logger_level=logger_level, formatter_id=writer_id+"Formatter")
        super(QueueWriter, self).__init__(formatter=self.formatter, logger_level=logger_level, writer_id=writer_id)

        self.outbox = outbox

    def write_entry(self, entry):
        self.outbox.put(entry)
