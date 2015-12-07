from xbee import ZigBee
from SinkNode.Reader.SerialReader import *
import json


# This if statement removes errors when building the documentation
if 'api_responses' in ZigBee.__dict__:
    ZigBee.api_responses[b'\xa1'] = {'name': 'route_record_indicator', 'structure': [{'name': 'data', 'len': None}]}
    ZigBee.api_responses[b'\xa2'] = {'name': 'device_authenticated_indicator',
                                     'structure': [{'name': 'data', 'len': None}]}
    ZigBee.api_responses[b'\xa3'] = {'name': 'many_to_one_route_request_indicator',
                                     'structure': [{'name': 'data', 'len': None}]}
    ZigBee.api_responses[b'\xa4'] = {'name': 'register_joining_device_indicator',
                                     'structure': [{'name': 'data', 'len': None}]}
    ZigBee.api_responses[b'\xa5'] = {'name': 'join_notification_status', 'structure': [{'name': 'data', 'len': None}]}


class XBeeReader(SerialReader):
    """
    XBeeReader listens for incoming packets on an XBee running in API mode.
    Individual packets parsed over serial port.
    """
    def __init__(self, port, baud_rate, logger_level=logging.FATAL):
        super(XBeeReader, self).__init__(port, baud_rate, logger_level=logger_level)
        self.xbee = ZigBee(self.ser, escaped=True)
        self.logger.name = "XBeeReader"

    def read_entry(self):
        """
        Read in a packet from the XBee
        :return: Received data payload from XBee packet
        """
        frame = self.xbee.wait_read_frame()  # Data packet - read in the data
        if frame['id'] == 'rx' or frame['id'] == 'rx_explicit':
            return json.dumps({"data": str(frame['rf_data']).encode('hex')})