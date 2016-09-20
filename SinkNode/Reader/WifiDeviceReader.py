import sys
from datetime import datetime

sys.path.append('/mnt/sda1/netaddr')

import json
from threading import Thread
from time import sleep
from netaddr import *
from scapy.all import *
import logging
from Queue import Queue
from SinkNode.Reader import Reader


PROBE_REQUEST_SUBTYPE = 4
PROBE_RESPONSE_SUBTYPE = 5
SSID_BEACON_FRAME = 8
ASSOCIATION_REQUEST = 0
ASSOCIATION_RESPONSE = 1
DATA = 0x00


class WifiDeviceReader(Reader):
    """
    Read in WiFi-enabled devices using a monitor-mode transceiver
    """

    def __init__(self, interface='wlan0', entry_separator='|', dump_period=None, include_access_points=False, id='WiFi',
                 cumulative_list=False, logger_level=logging.FATAL, outbox=None):
        """
        Make a WiFi scanner object to search for surrounding WiFi-enabled devices.
        Your wireless interface needs to be in monitor mode for this class to function properly.

        :param interface: Wireless interface to listen to. Must be in monitor mode.
        Ubuntu: sudo ifconfig wlan0 down
        Ubuntu: sudo iwconfig wlan0 mode monitor
        Ubuntu: sudo ifconfig wlan0 up

        :param entry_separator: Separator character between devices when dumping device list
        :param dump_period: Amount of time between device list dumps (in seconds)
        :param include_access_points: Include fixed AP in the device scan (true == yes)
        :param id: Data tag for the device dump (important for SinkNode logging later on)
        :param cumulative_list: Keep the device list after every dump or scrap. (true == keep; false == scrap)
        :param logger_level: Logger level for class debugging and information
        :param outbox: Queue where processed device lists will be dumped
        :return:
        """
        self.interface = interface
        self.entry_separator = entry_separator
        self.dump_period = dump_period
        self.include_access_points = include_access_points
        self.id = id
        self.cumulative_list = cumulative_list

        self.listener_thread = Thread(target=self.start_wifi_scan)
        self.listener_thread.setDaemon(True)
        self.packet_queue = Queue()

        self.process_thread = Thread(target=self.process_packets)
        self.process_thread.setDaemon(True)

        self.device_list = {}
        self.outbox = outbox

        super(WifiDeviceReader, self).__init__(outbox=outbox, logger_level=logger_level, reader_id=self.id)

    def start(self):
        """
        Start scanning for WiFi-enabled devices
        :return:
        """
        super(WifiDeviceReader, self).start()
        self.logger.info("Started Wifi listener")

        self.listener_thread.start()
        self.process_thread.start()

    def stop(self):
        """
        Stop scanning for wireless devices
        :return:
        """
        super(WifiDeviceReader, self).stop()
        self.logger.info("Stopping Wifi listener")

    def read_entry(self):
        """
        Periodically dump the device list.
        If no dump period is specified, devices information will be transmitted as soon as it comes in.

        :return: List of keys(MAC addresses) of collected devices. Can be used to pull Device data from the list.
        """

        # Set up a periodic write if specified
        if self.dump_period is not None:
            self.logger.debug("Sleeping for {} seconds...".format(self.dump_period))
            sleep(self.dump_period)

        # Waiting time is over - send whatever you got. If there's nothing, wait until there's something
        while len(self.device_list) < 1:
            sleep(0.5)

        self.logger.info("Found {} device(s)".format(len(self.device_list)))
        return self.device_list.keys()

    def convert_to_json(self, entry_line):
        """
        Convert the device list into a transmissible JSON string

        :param entry_line: List of device MAC addresses. Can be used to pull data from the device list
        :return: JSON string containing all current device information.
        The device list is contained under the 'payload' key as a separated string.
        """
        s = ""
        for d in entry_line:

            # Get the device info from the list, either destructively or cumulatively
            if self.cumulative_list:
                entry = self.device_list[d]
            else:
                entry = self.device_list.pop(d).to_json()

            entry.replace(self.entry_separator, '')
            s += entry + self.entry_separator
        payload = json.dumps({"id": self.id, "payload": s})

        self.logger.debug("Dumping: {}".format(payload))
        return payload

    def start_wifi_scan(self):
        """
        Start listening to surrounding wifi signals to identify APs and devices.
        Received packets are processed in the 'handle_packet' callback function.
        No packets are stored so the scan can run continuously.

        :return: None
        """
        try:
            sniff(iface=self.interface, prn=self.handle_packet, store=0)
        except KeyboardInterrupt:
            sys.exit(0)

    def handle_packet(self, pkt):
        """
        Callback function for wifi scanning.
        Probe packets are examined for device information.
        Only 802.11 Packets are passed into the packet queue for examination.

        :param pkt: Packet to be examined
        :return: None
        """
        if pkt.haslayer(Dot11):
            self.packet_queue.put(pkt)
            self.logger.debug("Packet received")

    def process_packets(self):
        """
        Extract relevant information from incoming packets.
        Device/AP information is added to the related list.

        Device information will only be saved if the device or ap tags are not null.
        I.e. self.ap_id_tag = 'foo' will save AP information and output it with the 'foo' tag.
        :return:
        """
        while self.is_running:
            new_packet = self.packet_queue.get()

            ssid = self.get_ssid(new_packet)
            eui = self.get_device_address(new_packet)
            is_ap = self.is_access_point(new_packet)

            # Only accept devices with valid addresses that are not already in the device list
            if eui is not None and eui not in self.device_list:

                if is_ap:
                    if self.include_access_points:
                        ssid += " (AP)"
                        self.device_list[eui] = self.Device(eui, ssid)

                else:
                    self.device_list[eui] = self.Device(eui, ssid)

            self.packet_queue.task_done()

    @staticmethod
    def get_ssid(pkt):
        """
        Extract the SSID related to the specified packet if available
        :param pkt: Captured WLAN packet or management frame
        :return: SSID of the related access point
        """
        ssid = None

        if pkt.haslayer(Dot11Elt):
            p = pkt[Dot11Elt]

            while isinstance(p, Dot11Elt):
                if p.ID == 0:
                    ssid = p.info
                p = p.payload

        return ssid

    @staticmethod
    def is_access_point(pkt):
        is_ap = False
        if pkt.subtype == SSID_BEACON_FRAME:
            is_ap = True
        return is_ap

    @staticmethod
    def get_device_address(pkt):
        address = None
        subtype = pkt.subtype

        # Grab address from frame. Different frame types change the location of the device address (src/dst).
        if subtype == PROBE_REQUEST_SUBTYPE or subtype == SSID_BEACON_FRAME:
            address = pkt.addr2
        elif subtype == PROBE_RESPONSE_SUBTYPE:
            address = pkt.addr1

        # Put MAC address in standard format
        if address is not None and len(address) > 0:
            address = str(EUI(address))

        return address

    class Device:
        """
        Data model object for wireless devices or access points
        """

        def __init__(self, mac_address, ssid=None, packet_type=None):
            """
            Create a new device.
            Vendor ID is determined based on the first three octets of the MAC address

            :param mac_address: Mac address of device in "xx-xx-xx-xx-xx-xx" format
            :param ssid: Network ID associated with the device
            :param packet_type: Subtype of the 802.11 packet that the device was discovered
            :return:
            """
            self.mac_address = EUI(mac_address)
            self.time_last_seen = datetime.now()

            self.ssid = None
            self.set_ssid(ssid)

            self.packet_type = packet_type

            # Attempt to find the MAC address; Not all devices have registered vendor IDs
            try:
                self.vendor = self.mac_address.oui.registration().org
                if len(self.vendor) > 20:
                    self.vendor = self.vendor[0:20]
            except NotRegisteredError:
                self.vendor = 'Unregistered'
            self.vendor.replace(',', '')  # Sanitise commas

        def __str__(self):
            return "eui: {}, vendor: {}, last_seen: {}, ssid: {}".format(str(self.mac_address),
                                                                         self.vendor,
                                                                         self.time_last_seen.isoformat(),
                                                                         self.ssid)

        def to_json(self):
            """
            Output the device entry in JSON format
            :return: JSON formatted string of the device entry
            """
            output = {'eui': str(self.mac_address),
                      'vendor': self.vendor,
                      'last_seen': self.time_last_seen.strftime("%Y-%m-%d %H:%M:%S"),
                      'ssid': self.ssid
                      }

            json_string = ""
            try:
                json_string = json.dumps(output)
            except UnicodeDecodeError as err:
                print("\n\nUnicode error: {}\n\n".format(str(self)))

            return json_string

        def update_last_seen(self, dt=None):
            if dt is not None:
                self.time_last_seen = dt
            else:
                self.time_last_seen = datetime.now()

        def get_time_last_seen(self):
            return self.time_last_seen

        def set_ssid(self, ssid):
            """
            Set a new SSID associated with a device
            :param ssid: The SSID associated with the device
            :return:
            """
            if ssid is not None and len(ssid) > 0:
                new_ssid = unicode(ssid, errors="ignore")
                self.ssid = new_ssid

            else:
                self.ssid = None


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding("utf8")
    read_queue = Queue()
    reader = WifiDeviceReader(interface='wlan0', dump_period=5, id='wifi', logger_level=logging.DEBUG, include_access_points=True)
    reader.set_outbox(read_queue)
    reader.start()

    while True:
        try:
            packet = read_queue.get()
            print("Packet: {}\n".format(packet))
            read_queue.task_done()
        except KeyboardInterrupt:
            reader.stop()
            sys.exit(0)
