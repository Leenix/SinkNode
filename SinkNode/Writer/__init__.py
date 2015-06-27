import logging
from threading import Thread

from SinkNode import Formatter
from SinkNode.Formatter import RawFormatter


LOGGER_FORMAT = "%(asctime)s - %(name)s - %(levelname)s: %(message)s"

__author__ = 'Leenix'

from Queue import Queue


class Writer(object):
    def __init__(self, formatter=None, writer_id=__name__, logger_level=logging.FATAL, logger_format=LOGGER_FORMAT):
        self.id = writer_id

        if formatter is None:
            formatter = RawFormatter()
        self.formatter = formatter

        # Incoming entries are passed to the format queue, which are processed and passed to the write queue
        self.format_queue = Queue()
        self.write_queue = Queue()
        self.formatter.set_inbox(self.format_queue)
        self.formatter.set_outbox(self.write_queue)

        # Set up logging stuff...
        self.logger = logging.getLogger(writer_id)
        log_handler = logging.StreamHandler()
        log_handler.setFormatter(logging.Formatter(logger_format))
        self.logger.addHandler(log_handler)
        self.logger.setLevel(logger_level)

        self.is_running = False
        self.write_thread = Thread(name=writer_id, target=self._write_loop)

    def stop(self):
        """
        Stop the press!
        :return: None
        """
        self.is_running = False
        self.formatter.stop()

    def start(self):
        """
        Start writing packets
        :return: None
        """
        self.logger.info("Starting writer [%s]", self.get_id())
        self.is_running = True
        self.write_thread.start()
        self.formatter.start()

    def add_entry(self, entry):
        """
        Add an entry to the writer's formatting queue
        :param entry: JSON formatted string
        :return:
        """
        self.formatter.add_to_inbox(entry)

    def write_entry(self, entry):
        """
        Write the formatted entry to its destination
        - This method must be overridden by child classes
        :param entry: Entry to be uploaded
        :return: None
        """
        raise Exception("Method [write_entry] not implemented")

    def _write_loop(self):
        """
        Write any formatted entries to their appropriate destination
        :return:
        """
        while self.is_running:
            formatted_entry = self.write_queue.get()
            self.write_entry(formatted_entry)
            self.write_queue.task_done()
            self.logger.info("Entry written")

    def get_id(self):
        """
        Get the id of the writer
        :return: id of the writer object
        """
        return self.id

    def set_formatter(self, formatter):
        """
        Set the formatter for the writer
        :param formatter: Formatter object
        :return:
        """
        assert isinstance(formatter, Formatter)
        self.formatter = formatter
        self.formatter.set_inbox(self.format_queue)
        self.formatter.set_outbox(self.write_queue)