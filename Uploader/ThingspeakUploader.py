import httplib
from threading import Thread
import urllib

__author__ = 'Leenix'

from ..Uploader import *
import time

SERVER_ADDRESS = "api.thingspeak.com:80"
THINGSPEAK_DELAY = 15

HEADERS = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}


class ThingspeakUploader(Uploader):
    def __init__(self, server_address=SERVER_ADDRESS, upload_delay=THINGSPEAK_DELAY):
        self.server_address = server_address
        self.upload_delay = upload_delay

        self.uploader = Thread(name="uploader", target=self._upload_loop())
        self.is_uploading = False

    def run(self):
        self.is_uploading = True
        self.uploader.start()

    def _uploader_loop(self):
        while self.is_uploading:
            entry = self.upload_queue.get()

            try:
                self.upload_entry(entry)
                self.upload_queue.task_done()
                time.sleep(self.upload_delay)
            except Exception:
                time.sleep(2)

    def stop(self):
        self.is_uploading = False

    def upload_entry(self, entry):
        params = urllib.urlencode(entry)
        conn = httplib.HTTPConnection(self.server_address)
        conn.request("POST", "/update", params, HEADERS)
        response = conn.getresponse()
        conn.close()
        return response

