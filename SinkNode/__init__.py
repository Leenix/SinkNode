import datetime
from SinkNode.Writer import *
import json

LOGGER_FORMAT = "%(asctime)s - %(name)s - %(levelname)s: %(message)s"


class SinkNode:

    def __init__(self, reader=None, logger_level=logging.FATAL):

        # Set up logging stuff
        self.logger = logging.getLogger("Main")
        log_handler = logging.StreamHandler()
        log_handler.setFormatter(logging.Formatter(LOGGER_FORMAT))
        self.logger.addHandler(log_handler)
        self.logger.setLevel(logger_level)

        # Set up queues to pass the data between the different processes
        self.read_queue = Queue()

        self.writers = []
        self.readers = []

        if reader is not None:
            self.add_reader(reader)

        self.is_running = False
        self.process_thread = Thread(name="main", target=self._main_loop)

    def add_reader(self, reader):
        """
        Add a reader to the system
        :param reader:
        :return:
        """
        reader.set_outbox(self.read_queue)
        self.readers.append(reader)

    def add_writer(self, writer, condition=None):
        """
        Add a writer to output the formatted data
        Writers only accept packets conditionally, if their id matches the id of the incoming entry.
        :param writer: Writer object
        :return:
        """
        self.writers.append([writer, condition])
        self.logger.debug("Writer added [%s]", writer.get_id())

    def add_logger(self, logger, condition=None):
        """
        Add a logger to output the formatted data
        Loggers are non-conditional and will output every received entry.
        :param logger: Writer object
        :param condition: Filtering condition for the writer. The ID of incoming entries must match for the writer to
        record the entry. A condition of None removes the filter and makes the writer indiscriminate.
        :return:
        """
        assert isinstance(logger, Writer)
        self.writers.append([logger, None])
        self.logger.debug("Logger added [%s]", logger.get_id())

    def start(self):
        """
        Start the ingestor
        All the gears start turning over several threads.
        :return:
        """

        self.logger.debug("Starting readers...")
        for reader in self.readers:
            reader.start()

        # Fire up the writers
        self.logger.debug("Starting writers...")
        for writer in self.writers:
            writer[0].start()

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

        for reader in self.readers:
            reader.stop()

        for writer in self.writers:
            writer[0].stop()

        self.is_running = False

    def _main_loop(self):
        """
        Main loop of SinkNode
        Data is managed between read and write threads
        :return:
        """
        while self.is_running:
            try:

                entry = self.read_queue.get(block=True, timeout=2)
                self.logger.info("Entry received - %s", datetime.datetime.now().isoformat())

                try:
                    assert not isinstance(entry, basestring)
                    assert isinstance(entry, dict)

                    for writer in self.writers:
                        if writer[1] is None or entry["id"] == writer[1]:
                            self.logger.debug("Entry sent to writer [%s]", writer[0].get_id())
                            writer[0].add_entry(entry.copy())

                except AssertionError:
                    self.logger.error("Entry formatted incorrectly - Must be dictionary object")

                self.read_queue.task_done()

            except:
                pass
