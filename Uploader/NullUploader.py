from threading import Thread

__author__ = 'Leenix'

from ..Uploader import *

class NullUploader(Uploader):
    def __init__(self, logger_name=__name__):
        self.logger = logging.getLogger(logger_name)
        if self.logger.name == __name__:
            self.logger.addHandler(logging.StreamHandler())
            self.logger.setLevel(logging.INFO)

        self.upload_queue = Queue()

        self.upload_thread = Thread(name="uploader", target=self._uploader_loop)
        self.is_uploading = False

    def run(self):
        self.logger.debug("Starting upload thread")
        self.is_uploading = True
        self.upload_thread.start()

    def _uploader_loop(self):
        while self.is_uploading:
            entry = self.upload_queue.get()
            self.upload_queue.task_done()

    def stop(self):
        self.logger.debug("Stopping upload thread")
        self.is_uploading = False


