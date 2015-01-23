__author__ = 'Leenix'

from threading import Thread

from ..Processor import *



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

# Mapping between unit ID and Thingspeak channel
EXAMPLE_CHANNEL_MAP = {
    "<id_here>": "<API_KEY_HERE>",
}

# Thingspeak server address (change if using a custom server)
# default: "api.thingspeak.com:80"
SERVER_ADDRESS = "api.thingspeak.com:80"


class ThingspeakProcessor(Processor):
    def __init__(self, channel_map=EXAMPLE_CHANNEL_MAP, key_map=EXAMPLE_KEY_MAP, logger_name=__name__):
        self.channel_map = channel_map
        self.key_map = key_map

        self.logger = logging.getLogger(logger_name)

        self.in_queue = Queue()
        self.out_queue = Queue

        self.is_processing = False
        self.processor_thread = Thread(name="processor", target=self._process_loop())

    def _process_loop(self):
        """
        Processing loop for the processor
        :return: None
        """
        entry = self.in_queue.get()
        output = self.process_entry(entry)
        self.in_queue.task_done()

        self.out_queue.put(output)

    def run(self):
        """
        Process data from the incoming queue and output the processed data on the outgoing queue.

        :return: None
        """

        self.logger.debug("Processor starting")
        self.is_processing = True
        self.processor_thread.start()

    def stop(self):
        """
        Halt the processing of incoming packets.
        Data stored in the incoming and outgoing queues will not be affected.

        :return: None
        """
        self.logger.debug("Processor stopping")
        self.is_processing = False

    def process_entry(self, entry):
        """Process an incoming JSON entry into thingspeak format.

        Field mapping can be found in the settings.py file in the following format:
        date field name: thingspeak field name

        The CHANNEL_MAP list gives each ID the proper API key
        so the data is entered into the correct channel (assuming
        each unit has its own channel.

        :param entry: JSON format of sensor data = {
                        "id": unit_id,
                        "temperature": temp_data,
                        "humidity": humidity_data,...
                        }

        :return: JSON data in Thingspeak format = {
                        "key": API_KEY
                        "field1": field1_data
                        "field2": field2_data...
                        }
        """

        output = {}

        # Each entry must have an ID to be valid so we know where it's going
        if "id" in entry and entry["id"] in self.channel_map:
            channel_key = self.channel_map[entry["id"]]
            output["key"] = channel_key

            # Map the rest of the data into fields
            # Extra data will be ignored
            for k in entry:
                if k in self.key_map:
                    new_key = self.key_map[k]
                    output[new_key] = entry[k]

        self.logger.info("Processed packet: {}".format(output))
        return output


