#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import subprocess
import os
import shlex
import json
import traceback

# bash -c "cut -f1 -d ' ' /proc/uptime"
#
def get_uptime():
    try:
        with open('/proc/uptime') as f:
            lines = f.readlines()
        if lines is None:
            return -2
        elif len(lines) == 0:
            return -3
        else:
            l = lines[0]
            s = float(l.split(' ')[0])
            return s
    except Exception as e:
        print(e)
        return -1


def read_file_as_int(filepath):
    try:
        with open(filepath) as f:
            lines = f.readlines()
        return null if len(lines) == 0 else int(lines[0])
    except Exception as e:
        return None



def get_network_interface_statistics(name):
    path = "/sys/class/net/%s/statistics" % (name)
    xs = os.listdir(path)
    xs = [ [x, read_file_as_int("%s/%s" % (path, x))] for x in xs ]
    xs = [ x for x in xs if x[1] is not None ]
    xs = { x[0]: x[1] for x in xs }
    return xs


def execute_and_parse(command_line, data_format='csv', delimiter='\t'):
    command_line = "".join(command_line.split("\n"))
    try:
        if not (data_format in ['csv', 'json']):
            return (("unexpected data_format: %s" % data_format), None)

        cmd_and_args = shlex.split(command_line)
        cmd_env = os.environ.copy()
        cmd_env.update(
            LC_ALL='C',
        )
        p = subprocess.Popen(cmd_and_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=cmd_env)
        out, err = p.communicate()
        out, err = out.decode(), err.decode()

        if p.returncode != 0:
            return (("unexpected non-zero exit code: %d" % p.returncode), None)

        if data_format == 'csv':
            lines = out.split("\n")
            line_tokens = [ l.split(delimiter) for l in lines ]
            return (None, line_tokens)
        else:
            # print("out: %s" % (out))
            data = json.loads(out)
            return (None, data)
    except Exception as e:
        # traceback.print_tb(e.__traceback__)
        return (("%s" % (e)), None)





# Entry point
#
if __name__ == '__main__':
    print("system uptime: %.2f" % (get_uptime()))
    a = """
    curl -w
    '{\\n
        "time_namelookup": %{time_namelookup},\\n
        "time_connect": %{time_connect},\\n
        "time_appconnect": %{time_appconnect},\\n
        "time_pretransfer": %{time_pretransfer},\\n
        "time_redirect": %{time_redirect},\\n
        "time_starttransfer": %{time_starttransfer},\\n
        "time_total": %{time_total},\\n
        "speed_download": %{speed_download},\\n
        "speed_upload": %{speed_upload}\\n
    }' -D /tmp/tgpbyHjg5 -o '/tmp/xmpcjffeM' -s -S 'https://hub.cestec.jp'
    """
    (x, y) = execute_and_parse(a, 'json')
    print(x)
    print(y)

