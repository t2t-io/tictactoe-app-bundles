#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import os
import math
import traceback
from urllib.parse import urlparse

# Helper classes and functions
#
from base_sensor import BaseSensor, ConstantBaseSensor
from sensor_util import decouple_nested_list
from sys_util import execute_and_parse


# [todo] Replace `https://archives.t2t.io` with environment variable.
# [todo] Implement HTTP POST with 256 bytes of data body, and also download 256 bytes of response data.
#        (the related web-service in AWS also needs to be implemented)
#
HTTP_STAT_COMMAND = """
curl -w
'{\\n
    "time_namelookup": %{time_namelookup},\\n
    "time_connect": %{time_connect},\\n
    "time_appconnect": %{time_appconnect},\\n
    "time_pretransfer": %{time_pretransfer},\\n
    "time_redirect": %{time_redirect},\\n
    "time_starttransfer": %{time_starttransfer},\\n
    "time_total": %{time_total},\\n
    "remote_ip": "%{remote_ip}",\\n
    "remote_port": "%{remote_port}",\\n
    "speed_download": %{speed_download},\\n
    "speed_upload": %{speed_upload}\\n
}' -D /tmp/tgpbyHjg5 -o '/tmp/xmpcjffeM' -s -S """

HTTP_STAT_FIELDS = """
time_namelookup
time_connect
time_appconnect
time_pretransfer
time_redirect
time_starttransfer
time_total
remote_ip
"""

# Inspired by:
#   - http://www.cnx-software.com/2016/10/03/how-to-check-http-header-and-connection-stats-from-the-command-line/
#   - https://github.com/reorx/httpstat
#
#
# $  curl -w '{\n"time_namelookup": %{time_namelookup},\n"time_connect": %{time_connect},\n"time_appconnect": %{time_appconnect},\n"time_pretransfer": %{time_pretransfer},\n"time_redirect": %{time_redirect},\n"time_starttransfer": %{time_starttransfer},\n"time_total": %{time_total},\n"speed_download": %{speed_download},\n"speed_upload": %{speed_upload}\n}' -D /tmp/tmpbYHj0P -o '/tmp/tmpmjeMeW' -s -S 'https://archives.t2t.io' | jq .
#
# {
#   "time_namelookup": 0.005,
#   "time_connect": 0.058,
#   "time_appconnect": 0.285,
#   "time_pretransfer": 0.285,
#   "time_redirect": 0,
#   "time_starttransfer": 0.34,
#   "time_total": 0.341,
#   "speed_download": 38,
#   "speed_upload": 0
# }
#
# Execute CURL with time measurement, and output following sensor data:
# ----------------------------------------------------------------------------------
#
#   !   0002    F   internet    httpstat    archives.t2t.io   time_namelookup 255
#   !   000C    F   internet    httpstat    archives.t2t.io   time_connect    331
#   !   000A    F   internet    httpstat    archives.t2t.io   time_appconnect 539
#   !   0004    F   internet    httpstat    archives.t2t.io   time_pretransfer    539
#   !   0005    F   internet    httpstat    archives.t2t.io   time_starttransfer  597
#   !   0006    F   internet    httpstat    archives.t2t.io   time_redirect   0
#   !   0007    F   internet    httpstat    archives.t2t.io   time_total  598
#
#   !   0003    F   internet    httpstat    archives.t2t.io   range_dns   255
#   !   0009    F   internet    httpstat    archives.t2t.io   range_ssl   208
#   !   000B    F   internet    httpstat    archives.t2t.io   range_transfer  1
#   !   000D    F   internet    httpstat    archives.t2t.io   range_connection    76
#   !   000E    F   internet    httpstat    archives.t2t.io   range_server    58
#
#   !   0008    F   internet    httpstat    archives.t2t.io   speed_upload    0.0
#   !   000F    F   internet    httpstat    archives.t2t.io   speed_download  21.0
#
class CurlHttpStatSensor(BaseSensor):
    def __init__(self):
        super().__init__()
        self._url = "https://archives.t2t.io"
        if 'SYS_STATS_CURL_HTTP_STAT_SENSOR_URL' in os.environ:
            self._url = os.environ['SYS_STATS_CURL_HTTP_STAT_SENSOR_URL']
        self._command = "%s '%s'" % (HTTP_STAT_COMMAND, self._url)
        result = urlparse(self._url)
        self._hostname = result.netloc
        self._base.board_type = 'internet.httpstat'
        self._base.board_id = "_".join(self._hostname.split("."))
        self._base.sensor = "0.0.0.0"
        # print("hostname: %s, sensor: %s" % (self._hostname, self._base.sensor))
        # print("command: %s" % (self._command))
        self._preferred_period = 60
        self.time_fields = [ x for x in HTTP_STAT_FIELDS.split("\n") if x != "" ]

    def measure(self):
        (err, data) = execute_and_parse(self._command, 'json')
        if err is None:
            for f in self.time_fields:
                data[f] = data[f] if type(data[f]) is str else math.floor(data[f] * 1000)
            if "remote_ip" in data:
                self._base.sensor = data["remote_ip"]
            for f in ["remote_ip", "remote_port"]:
                if f in data:
                    del data[f]
            data.update(
                range_dns = data['time_namelookup'],
                range_connection = data['time_connect'] - data['time_namelookup'],
                range_ssl = data['time_pretransfer'] - data['time_connect'],
                range_server = data['time_starttransfer'] - data['time_pretransfer'],
                range_transfer = data['time_total'] - data['time_starttransfer']
            )
            return data
        else:
            # print(err)
            return None


    @property
    def data(self):
        data = self.measure()
        if not data:
            return []
        data_time = {k[5:]: v for k, v in data.items() if k[:4] == "time"}
        data_range = {k[6:]: v for k, v in data.items() if k[:5] == "range"}
        data_speed = {k[6:]: v for k, v in data.items() if k[:5] == "speed"}
        board_id = self._base.board_id
        sensor = self._base.sensor
        return [
            ConstantBaseSensor("%s.%s" % (self._base.board_type, "time"), board_id, sensor, data_time).data,
            ConstantBaseSensor("%s.%s" % (self._base.board_type, "range"), board_id, sensor, data_range).data,
            ConstantBaseSensor("%s.%s" % (self._base.board_type, "speed"), board_id, sensor, data_speed).data
        ]


SensorClasses = [
    CurlHttpStatSensor
]
