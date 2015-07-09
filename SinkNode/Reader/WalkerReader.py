
from SinkNode.Reader.XbeeReader import XBeeReader
import datetime
import struct


class WalkerReader(XBeeReader):
    UNIT_CLASS = "stalker"

    def __init__(self, port, baud_rate, logger_name=__name__):
        super(WalkerReader, self).__init__(self, port, baud_rate)

    def convert_to_json(self, entry_line):
        """
        Convert the Walker data packet into a readable format
        :param entry_line: Raw byte-encoded data from the unit
        :return: decoded data dictionary
        """
        if len(entry_line) == 23:

            offset = self.total_seconds((datetime.datetime(2000, 1, 1, 0, 0, 0, 0) - datetime.datetime(1970, 1, 1, 0, 0, 0, 0)))

            try:
                station_id, ts, air_temp, wall_temp, surface_temp, case_temp, humidity, lux, sound, current, \
                battery_percent, version = struct.unpack(">BIHHHHHHHHBB", entry_line)
                ts_time = datetime.datetime.utcfromtimestamp(ts + offset).strftime("%Y-%m-%d %H:%M")

                new_entry = {
                    'id': self.UNIT_CLASS + str(station_id),
                    'timestamp': ts_time,
                    'air_temp': float(air_temp) / 100,
                    'wall_temp': float(wall_temp) / 100,
                    'surface_temp': float(surface_temp) / 100,
                    'case_temp': float(case_temp) / 100,
                    'humidity': float(humidity) / 100,
                    'illuminance': lux,
                    'sound': sound,
                    'current': float(current) / 100,
                    'battery': battery_percent,
                    'version': version
                }
            except Exception:
                new_entry = 0
                pass

        self.logger.info("Received Data: {}".format(new_entry))
        return new_entry

    def total_seconds(deltatime):
        """
        Convert the date into the total number of seconds since the epoch
        :param deltatime: Date object to be converted
        :return: Total number of seconds from epoch to date.
        """
        return (deltatime.microseconds + (deltatime.seconds + deltatime.days * 24 * 3600) * 10 ** 6) / 10 ** 6


