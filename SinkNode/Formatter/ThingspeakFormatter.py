__author__ = 'Leenix'

from SinkNode.Formatter import Formatter
import logging

# Mapping between data id keys and Thingspeak fields
EXAMPLE_KEY_MAP = {
    "air_temp": "field1",
    "wall_temp": "field2",
    "surface_temp": "field3",
    "case_temp": "field4",
    "humidity": "field5",
    "illuminance": "field6",
    "sound": "field7",
    "battery": "field8"
}

# Thingspeak server address (change if using a custom server)
# default: "api.thingspeak.com:80"
SERVER_ADDRESS = "api.thingspeak.com:80"


class ThingspeakFormatter(Formatter):
    """
    The ThingspeakFormatter translates JSON data into a Thingspeak-compatible format by replacing the JSON keys
    with thingspeak field labels. The key-field mapping requires a map to be specified on creation.

    Each formatter should handle one thingspeak channel each. Therefore, API keys are matched to each channel.
    """
    def __init__(self, api_key, key_map, outbox=None, formatter_id=__name__, logger_level=logging.FATAL):
        super(ThingspeakFormatter, self).__init__(self, logger_level=logger_level, formatter_id=formatter_id)
        self.outbox = outbox
        self.api_key = api_key
        self.key_map = key_map

    def format_entry(self, entry):
        """Process an incoming JSON entry into thingspeak format.

        Field mapping can be found in the settings.py file in the following format:
        date field name: thingspeak field name
        date field name: thingspeak field name

        :param entry: JSON format of sensor data = {
                        "id": unit_id,
                        "temperature": temp_data,
                        "humidity": humidity_data,...
                        }
        """
        output = {}

        # Each entry must have an ID to be valid so we know where it's going
        if 'id' in entry.keys() and len(entry["id"]) > 0:
            output["key"] = self.api_key

            # Map the rest of the data into fields
            # Extra data will be ignored
            for k in entry:
                if k in self.key_map:
                    new_key = self.key_map[k]
                    output[new_key] = entry[k]

        return output

