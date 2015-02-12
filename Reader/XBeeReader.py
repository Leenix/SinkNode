import sys
import logging
from threading import Thread
import json
from Queue import Queue
import serial
from serial import SerialException
from xbee import ZigBee
from SerialReader import *

# This if statement removes errors when building the documentation
if 'api_responses' in ZigBee.__dict__:
    ZigBee.api_responses[b'\xa1'] = {'name': 'route_record_indicator', 'structure': [{'name': 'data', 'len': None}]}
    ZigBee.api_responses[b'\xa2'] = {'name': 'device_authenticated_indicator', 'structure': [{'name': 'data', 'len': None}]}
    ZigBee.api_responses[b'\xa3'] = {'name': 'many_to_one_route_request_indicator', 'structure': [{'name': 'data', 'len': None}]}
    ZigBee.api_responses[b'\xa4'] = {'name': 'register_joining_device_indicator', 'structure': [{'name': 'data', 'len': None}]}
    ZigBee.api_responses[b'\xa5'] = {'name': 'join_notification_status', 'structure': [{'name': 'data', 'len': None}]}


class XBeeReader(SerialReader):
    def __init__(self, port, baud_rate, logger_name=__name__):
        super.__init__(self, port, baud_rate, logger_name=logger_name)
        self.xbee = ZigBee(self.ser)

    def _read_loop(self):
        while self.is_reading:
            frame = self.xbee.wait_read_frame()

            # Data packet - read in the data
            if frame['id'] == 'rx' or frame['id'] == 'rx_explicit':
                self.convert_to_json(frame['rf_data'])

