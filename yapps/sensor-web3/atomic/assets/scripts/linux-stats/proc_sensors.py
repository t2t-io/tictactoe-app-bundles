#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import os
import traceback

# Helper classes and functions
#
from base_sensor import BaseSensor
from sensor_util import SensorData, decouple_nested_list


class ConstantWirelessStatSensor(BaseSensor):
    def __init__(self, adapter, sensor, constant_data, unit_length_defs=None):
        super().__init__()
        self._base.board_type = 'wireless'
        self._base.board_id = adapter
        self._base.sensor = sensor
        self._unit_length_defs['signal'] = 'db'
        self._unit_length_defs['noise'] = 'db'
        self._unit_length_defs['link'] = '%'
        self._unit_length_defs['nwid'] = ''
        self._unit_length_defs['crypt'] = ''
        self._unit_length_defs['frag'] = ''
        self._unit_length_defs['retry'] = ''
        self._unit_length_defs['misc'] = ''
        self._constant_data = constant_data
        if unit_length_defs is not None:
            self._unit_length_defs.update(unit_length_defs)

    def measure(self):
        return self._constant_data


# Monitor wireless adapter status by watching /proc/net/wireless
# process file.
#
# `/proc/net/wireless` looks like this:
#
#   $ cat /proc/net/wireless
#   Inter-| sta-|   Quality        |   Discarded packets               | Missed | WE
#    face | tus | link level noise |  nwid  crypt   frag  retry   misc | beacon | 22
#    wlan0: 0000  100.  -45.  -256.       0      0      0      0      0        0
#
#
# Here are output examples after parsing
#
#   !   0002    F   wireless    wlan0   quality link    100 %
#   !   0003    F   wireless    wlan0   quality signal  -45 db
#   !   0004    F   wireless    wlan0   quality noise   -256    db
#   !   0005    F   wireless    wlan0   connectivity    status  0
#
class WirelessSensor(BaseSensor):
    def __init__(self):
        super().__init__()
        self._preferred_period = 5

    def value_to_int(self, value):
        return int(value[0:-1]) if value[-1] == '.' else int(value)


    def parse_wireless_stat_line(self, line):
        try:
            MAX_LINK_QUALITY = 70
            line = line.rstrip()
            xs = line.split(" ")
            xs = [ x for x in xs if x != "" ]
            results = []
            adapter = xs[0]
            adapter = adapter[0:-1] if adapter[-1] == ":" else adapter
            _fields = {}
            _fields['link'] = (self.value_to_int(xs[2]) / MAX_LINK_QUALITY) * 100
            _fields['signal'] = self.value_to_int(xs[3])
            _fields['noise'] = self.value_to_int(xs[4])
            results.append([adapter, "quality", _fields])
            _fields = {}
            _fields['status'] = int(xs[1])
            results.append([adapter, "connectivity", _fields])
            _fields = {}
            _fields['nwid'] = int(xs[5])
            _fields['crypt'] = int(xs[6])
            _fields['frag'] = int(xs[7])
            _fields['retry'] = int(xs[8])
            _fields['misc'] = int(xs[9])
            results.append([adapter, "discarded", _fields])
            return results
        except Exception as e:
            # print(e)
            # traceback.print_tb(e.__traceback__)
            return []


    def read_wireless_quality(self, stat_file=None):
        stat_file = os.environ["WIRELESS_STAT_FILE"] if stat_file is None and "WIRELESS_STAT_FILE" in os.environ else stat_file
        stat_file = "/proc/net/wireless" if stat_file is None else stat_file
        if os.path.exists(stat_file):
            xs = None
            with open(stat_file) as f:
                xs = f.readlines()
            xs = xs[2:]
            xs = [ self.parse_wireless_stat_line(x) for x in xs ]
            return xs
        else:
            return None


    @property
    def data(self):
        xs = self.read_wireless_quality()
        data_list = [ ConstantWirelessStatSensor(y[0], y[1], y[2]).data for x in xs for y in x ]
        return decouple_nested_list(data_list)


SensorClasses = [
    WirelessSensor
]
