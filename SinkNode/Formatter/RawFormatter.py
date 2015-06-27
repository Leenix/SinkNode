import logging
from SinkNode.Formatter import Formatter

__author__ = 'Leenix'


class RawFormatter(Formatter):
    """
    RawFormatter does not change the format of the input entry.

    All entries that pass through are kept in the same JSON format in which they entered.
    Useful for when no formatting change is necessary
    """

    def __init__(self, outbox=None, logger_level=logging.FATAL, formatter_id="RawFormatter"):
        super(RawFormatter, self).__init__(outbox=outbox, logger_level=logger_level, formatter_id=formatter_id)

    def format_entry(self, entry):
        """
        Perform no formatting on the entry - pass it straight on
        :param entry:
        :return:
        """
        return entry
