import logging
from unittest import TestCase
from SinkNode.Formatter.CSVFormatter import CSVFormatter

__author__ = 'Leenix'


class TestCSVFormatter(TestCase):

    def setUp(self):
        self.test_formatter = CSVFormatter(logger_level=logging.DEBUG)

    def test_first_format(self):
        test_dict = {'This': 1, 'is': 2, 'a': 3, 'test': 4}
        first_run = self.test_formatter.format_entry(test_dict)

        self.assertEquals("'This','a','is','test'\n1,3,2,4", first_run)

    def test_second_format(self):
        test_dict = {'This': 1, 'is': 2, 'a': 3, 'test': 4}
        first_run = self.test_formatter.format_entry(test_dict.copy())
        second_run = self.test_formatter.format_entry(test_dict.copy())

        self.assertEquals("1,3,2,4", second_run)

    def test_extra_format(self):
        test_dict = {'This': 1, 'is': 2, 'a': 3, 'test': 4}
        test_dict_extra = {'This': 1, 'is': 2, 'a': 3, 'test': 4, 'thing': 5}

        first_run = self.test_formatter.format_entry(test_dict)
        second_run = self.test_formatter.format_entry(test_dict_extra)
        self.assertEquals("'This','a','is','test','thing'\n1,3,2,4,5", second_run)




