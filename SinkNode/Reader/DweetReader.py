from SinkNode.Reader import *
import dweepy
from requests import ConnectionError


class DweetReader(Reader):
    def __init__(self, thing_name=None, outbox=None, logger_level=logging.FATAL, logger_format=LOGGER_FORMAT, reader_name="DweetReader"):
        super(DweetReader, self).__init__(outbox=outbox, logger_level=logger_level, logger_format=logger_format, reader_id=reader_name)
        self.thing_name = thing_name

        self.listener_thread = Thread(target=self.listener_loop)
        self.listener_thread.setDaemon(True)

        self.dweet_queue = Queue()

    def start(self):
        self.listener_thread.start()
        super(DweetReader, self).start()

    def read_entry(self):
        raw_dweet = self.dweet_queue.get()
        self.dweet_queue.task_done()

        self.logger.debug("Raw Dweet: {}".format(raw_dweet))

        entry = json.dumps(raw_dweet["content"])

        return entry

    def listener_loop(self):
        self.logger.debug("Starting listener thread")
        while self.is_running:
            try:
                for dweet in dweepy.listen_for_dweets_from(thing_name=self.thing_name):
                    self.dweet_queue.put(dweet)

            except ConnectionError:
                self.logger.debug("Listener timed out. Restarting...")

