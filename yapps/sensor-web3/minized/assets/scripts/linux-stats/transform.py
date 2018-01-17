import json
import re

LINUX = "linux"
LINUX_PROCESS = "linux_process"
CONNECTIVITY = "connectivity"
HTTPSTAT = "httpstat"
LOCALHOST = "7F000001"
ANY = "_"
CPU_X_PATTERN = re.compile('^cpu[0-9]+$')
DISK_X_PATTERN = re.compile('^disk[0-9]+$')
NET_IO_COUNTERS_X_PATTERN = re.compile('net_io_counters\..*$')
NET_IO_STATS_X_PATTERN = re.compile('net_io_stats\..*$')
HTTPSTATS_PATTERN = re.compile('^internet\.httpstat\..*$')

def convert_process_name(name):
    return "_".join(name.split("-"))


def encode_toe3_packet(sd_list, p_type, p_id, s_type, s_id):
    points = [ [s.data_type, s.value] for s in sd_list ]
    return [p_type, p_id, s_type, s_id, points]


def toe3_transform(data_list):
    if len(data_list) == 0:
        return (None, None)
    first = data_list[0]
    category = "measurements"
    if type(first) is list:
        board_type = first[0].board_type
        board_id = first[0].board_id
        sensor = first[0].sensor
        data_type = first[0].data_type
        if board_type == "process":
            xs = [ encode_toe3_packet(ss, LINUX_PROCESS, convert_process_name(ss[0].sensor), ss[0].board_id, ANY)  for ss in data_list ]
        elif DISK_X_PATTERN.match(sensor):
            if data_type in ["percentage", "used", "free", "total"]:
                xs = [ encode_toe3_packet(ss, LINUX, LOCALHOST, "disk", ss[0].sensor[4:])  for ss in data_list ]
            else:
                xs = [ encode_toe3_packet(ss, LINUX, LOCALHOST, "disk", ss[0].sensor[4:])  for ss in data_list ]
                category = "metadata"
        elif NET_IO_COUNTERS_X_PATTERN.match(sensor):
            xs = [ encode_toe3_packet(ss, LINUX, LOCALHOST, "net_io_counters", ss[0].sensor.split('.')[1])  for ss in data_list ]
        elif NET_IO_STATS_X_PATTERN.match(sensor):
            xs = [ encode_toe3_packet(ss, LINUX, LOCALHOST, "net_io_stats", ss[0].sensor.split('.')[1])  for ss in data_list ]
        elif HTTPSTATS_PATTERN.match(board_type):
            xs = [ encode_toe3_packet(ss, CONNECTIVITY, ss[0].board_id, "%s.%s" % (HTTPSTAT, ss[0].board_type.split('.')[2]), ss[0].sensor)  for ss in data_list ]
        else:
            return ("error", "unexpected board_type/board_id/sensor %s/%s/%s for list of SensorData\n" % (board_type, board_id, sensor))
    else:
        (board_type, board_id, sensor, data_type, value, unit_length) = first.to_tuple()
        if sensor == "cpu":
            xs = [ encode_toe3_packet(data_list, LINUX, LOCALHOST, sensor, ANY) ]
        elif sensor == "system" and data_type == "uptime":
            xs = [ encode_toe3_packet(data_list, LINUX, LOCALHOST, "stats", ANY) ]
        elif CPU_X_PATTERN.match(sensor):
            xs = [ [LINUX, LOCALHOST, "cpu_loads", d.sensor[3:], [[d.data_type, d.value]]] for d in data_list ]
        elif sensor in ["cpu_times", "cpu_freq", "virtual_memory", "swap_memory", "diskio"]:
            xs = [ encode_toe3_packet(data_list, LINUX, LOCALHOST, sensor, ANY) ]
        elif board_type == "wireless":
            qs = [ d for d in data_list if d.sensor == "quality" ]
            qs = encode_toe3_packet(qs, LINUX, LOCALHOST, "wireless_quality", qs[0].board_id)
            ds = [ d for d in data_list if d.sensor == "discarded" ]
            ds = encode_toe3_packet(ds, LINUX, LOCALHOST, "wireless_discarded", ds[0].board_id)
            xs = [qs, ds]
        else:
            return (board_type, "%s" % (data_list))
    return (category, json.dumps(xs))


def toe3_serializer(data_list):
    (category, payload) = toe3_transform(data_list)
    if category:
        return "%s\t%s\n" % (category, payload)
    else:
        return None
