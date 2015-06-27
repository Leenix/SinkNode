import logging
from unittest import TestCase
from SinkNode.Formatter.ThingspeakFormatter import ThingspeakFormatter

__author__ = 'Leenix'

TEST_FIELD_MAP = {
    "value1": "field1",
    "value2": "field2",
}
class TestThingspeakFormatter(TestCase):

    def setUp(self):
        self.formatter = ThingspeakFormatter(formatter_id="test",
                                             api_key="TEST_API",
                                             key_map=TEST_FIELD_MAP,
                                             logger_level=logging.DEBUG)

        self.test_packet = {'id': 'test', 'value1': 1, 'value2': 2}

    def test_format_entry(self):
        processed_entry = self.formatter.format_entry(self.test_packet.copy())
        self.assertEquals({'key': 'TEST_API', 'field1': 1, 'field2': 2}, processed_entry)
