from threading import Thread

__author__ = 'Leenix'

LOGGER_FORMAT = "%(asctime)s - %(name)s - %(levelname)s: %(message)s"

from Queue import Queue
import logging


class Formatter(object):
    """
    Parent class.
    Transforms incoming JSON data packets to another format for writing or uploading.
    Output format is dictated by the child class.
    """
    def __init__(self, outbox=None, logger_level=logging.FATAL, formatter_id=__name__, logger_format=LOGGER_FORMAT):
        self.logger = logging.getLogger(__name__)

        # The inbox queue can be either internal or externally passed in. The outbox must be specified
        self.inbox = Queue()
        self.outbox = outbox

        # Set up logging stuff...
        self.logger = logging.getLogger(formatter_id)
        log_handler = logging.StreamHandler()
        log_handler.setFormatter(logging.Formatter(logger_format))
        self.logger.addHandler(log_handler)
        self.logger.setLevel(logger_level)

        self.is_running = True
        self.format_thread = Thread(target=self._format_loop)

    def stop(self):
        """
        Stop processing incoming packets
        :return: None
        """
        self.logger.fatal("Stopping formatter")
        self.is_running = False

    def start(self):
        """
        Start processing incoming packets
        :return: None
        """
        self.logger.debug("Starting formatter")
        # Ensure that the queues have been defined before continuing
        assert isinstance(self.inbox, Queue)
        assert isinstance(self.outbox, Queue)

        # On with the show
        self.is_running = True
        self.format_thread.start()

    def _format_loop(self):
        """
        Format incoming entries and pass them on
        JSON entries come in via the inbox queue and formatted entries are placed in the outbox queue
        :return:
        """
        while self.is_running:
            # Process away and pass the entry to the out pile
            raw_entry = self.inbox.get()
            formatted_entry = self.format_entry(raw_entry)
            self.logger.debug("Formatted entry: [%s]", str(formatted_entry))
            self.outbox.put(formatted_entry)

            # Job done; cross it off the inbox to-do list
            self.inbox.task_done()

    def format_entry(self, entry):
        """
        Transform the incoming entry
        - Must be overridden in child classes
        :param entry: Incoming packet
        :return: Processed packet
        """
        raise Exception("Method [process_entry] not implemented")

    def add_to_inbox(self, entry):
        """
        Manually add an entry to the formatter queue.
        Use this instead of tying the inbox to an external queue

        :param entry: JSON entry to be formatted
        :return:
        """
        self.inbox.put(entry)

    def set_inbox(self, in_queue):
        """
        Set the incoming packet queue
        :param in_queue: Queue of packets needing to be processed
        :return: None
        """
        assert isinstance(in_queue, Queue)
        self.inbox = in_queue

    def set_outbox(self, out_queue):
        """
        Set the outgoing packet queue
        :param out_queue: Queue of packets that have been processed
        :return: None
        """
        assert isinstance(out_queue, Queue)
        self.outbox = out_queue
