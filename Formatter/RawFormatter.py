
from Formatter import Formatter
__author__ = 'Leenix'


class RawFormatter(Formatter):
    """
    RawFormatter does not change the format of the input entry.

    All entries that pass through are kept in the same JSON format in which they entered.
    Useful for when no formatting change is necessary
    """

    def format_entry(self, entry):
        """
        Perform no formatting on the entry - pass it straight on
        :param entry:
        :return:
        """
        return entry
