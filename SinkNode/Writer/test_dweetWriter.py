import logging
from unittest import TestCase
from SinkNode.Writer.DweetWriter import DweetWriter

__author__ = 'Leenix'


class TestDweetWriter(TestCase):

    def setUp(self):
        self.test_writer = DweetWriter("dickhouse", logger_level=logging.DEBUG)

    def test_write_entry(self):
        test_entry = {'dick': 'whale', 'lovable': 'fawn', 'what': 28}
        response = self.test_writer.write_entry(test_entry)
        self.assertEquals('succeeded', response['this'])