__author__ = 'Leenix'
import datetime

__author__ = 'Leenix'

from SinkNode.Writer import *

LOGGER_FORMAT = "%(asctime)s - %(name)s - %(levelname)s: %(message)s"


class SinkNode:

    def __init__(self, reader, logger_level=logging.FATAL):

        # Set up logging stuff
        self.logger = logging.getLogger("Main")
        log_handler = logging.StreamHandler()
        log_handler.setFormatter(logging.Formatter(LOGGER_FORMAT))
        self.logger.addHandler(log_handler)
        self.logger.setLevel(logger_level)

        # Set up queues to pass the data between the different processes
        self.read_queue = Queue()

        # There are two write queues
        # The writers in the Logger queue will always attempt to write any entry read in
        # Writers in the Write queue will filter out entries based on entry 'id'
        self.logger_list = []
        self.writer_list = []

        # At this point, only one reader is allowed
        # TODO - Add the capacity for several readers (they just need to output to the same queue)
        self.reader = reader
        self.reader.set_outbox(self.read_queue)

        self.is_running = False
        self.process_thread = Thread(name="main", target=self._main_loop)

    def add_writer(self, writer):
        """
        Add a writer to output the formatted data
        Writers only accept packets conditionally, if their id matches the id of the incoming entry.
        :param writer: Writer object
        :return:
        """
        assert writer.get_id() is not ""
        self.writer_list.append(writer)
        self.logger.debug("Writer added [%s]", writer.get_id())

    def add_logger(self, logger):
        """
        Add a logger to output the formatted data
        Loggers are non-conditional and will output every received entry.
        :param logger: Writer object
        :return:
        """
        assert isinstance(logger, Writer)
        self.logger_list.append(logger)
        self.logger.debug("Logger added [%s]", logger.get_id())

    def start(self):
        """
        Start the ingestor
        All the gears start turning over several threads.
        :return:
        """

        self.logger.debug("Starting readers...")
        self.reader.start()

        # Fire up the logger list
        # TODO - start up writer threads on creation?
        self.logger.debug("Starting loggers...")
        for logger in self.logger_list:
            logger.start()

        # Fire up the conditional writers
        self.logger.debug("Starting writers...")
        for writer in self.writer_list:
            writer.start()

        self.is_running = True
        self.process_thread.start()
        self.logger.info("Main thread starting...")

    def stop(self):
        """
        Stop the ingestor
        Shut down all the threads and go home...
        :return:
        """
        self.logger.info("Main thread stopping..")
        self.reader.stop()

        for logger in self.logger_list:
            logger.stop()

        for writer in self.writer_list:
            writer.stop()

        self.is_running = False

    def _main_loop(self):
        """
        Main loop of SinkNode
        Data is managed between read and write threads
        :return:
        """
        while self.is_running:
            entry = self.read_queue.get()
            self.logger.info("Entry received - %s", datetime.datetime.now().isoformat())

            for logger in self.logger_list:
                self.logger.debug("Entry sent to logger [%s]", logger.get_id())
                logger.add_entry(entry.copy())

            for writer in self.writer_list:
                if entry["id"] == writer.get_id():
                    self.logger.debug("Entry sent to writer [%s]", writer.get_id())
                    writer.add_entry(entry.copy())

            self.read_queue.task_done()





