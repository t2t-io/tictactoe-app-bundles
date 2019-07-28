#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import psutil
import os
import time
import traceback


# Helper classes and functions
#
from base_sensor import BaseSensor, DataTypeTransformSensor
from sensor_util import SensorData, decouple_nested_list
import sys_util


PYTHON_EXECUTABLES = ["python", "python3", "Python", "python3.4", "python2.7"]


class ConstantSysProcessSensor(DataTypeTransformSensor):
    def __init__(self, executable, name, constant_data, unit_length_defs=None):
        super().__init__()
        self._base.board_type = 'process'
        self._base.board_id = executable
        self._base.sensor = name
        self._unit_length_defs['cpu'] = '%'
        self._unit_length_defs['memory'] = '%'
        self._constant_data = constant_data
        if unit_length_defs is not None:
            self._unit_length_defs.update(unit_length_defs)

    def measure(self):
        return self._constant_data


class AppProcess:
    disabled_fields = None
    children = []
    @staticmethod
    def createInstance(pid, keywords):
        if pid == 0:
            return None
        try:
            process = psutil.Process(pid)
            exe = process.exe()
            name = os.path.basename(exe)
            ret = None
            ret = AppProcess(pid, process, exe) if name in ["node"] else ret
            ret = AppProcess(pid, process, exe) if name in PYTHON_EXECUTABLES else ret
            if ret is None:
                ks = [ (1 if k in name else 0) for k in keywords ]
                ret = AppProcess(pid, process, exe) if sum(ks) > 0 else ret
            '''
            print("ret => %s" % (ret))
            if ret is None:
                print("%s is not target" % (name))
            else:
                print("found %s" % (exe))
            '''
            return ret
            # return AppProcess(pid, process, exe) if os.path.basename(exe) in ["node"] + PYTHON_EXECUTABLES else None
        except Exception as e:
            # print(traceback.format_exc())
            # print("e => %s" % (e))
            return None

    def set_field(self, excluded_fields, name, value, negative_checking=False):
        if negative_checking and value < 0:
            return
        if excluded_fields is None:
            self._fields[name] = value
        elif name in excluded_fields:
            return
        else:
            self._fields[name] = value

    def __init__(self, pid, process, exe, child=False):
        self.pid = pid
        self.process = process
        self.exe = exe
        self.executable = os.path.basename(exe)
        self.cmdline = process.cmdline()
        self._fields = {}
        self.set_field(None, "uptime", time.time() - process.create_time(), True)
        self.set_field(AppProcess.disabled_fields, "num_threads", process.num_threads())
        self.set_field(AppProcess.disabled_fields, "num_fds", process.num_fds())
        self.set_field(AppProcess.disabled_fields, "cpu", process.cpu_percent(interval=0.1))
        self.set_field(AppProcess.disabled_fields, "memory", process.memory_percent())
        if self.executable == "node":
            # print("cmdline(): %s" % (self.cmdline))
            xs = [ x for x in self.cmdline if x[0] is not "-" ]
            # print("xs(): %s" % (xs))
            js = xs[1]
            if os.path.basename(js) == "lsc":
                js = xs[2]
                yapps = os.path.basename(js) == "app.ls"
                self.script = "livescript"
            else:
                yapps = os.path.basename(js) == "index.js"
                self.script = "javascript"
            dirname = os.path.dirname(js)
            dirname = process.cwd() if dirname == "." else dirname
            dirname = process.cwd() if dirname == "" else dirname
            dirname = os.path.abspath(dirname)
            # print("dirname = %s, cwd = %s" % (dirname, process.cwd()))
            self.name = os.path.basename(dirname) if yapps else os.path.basename(js)
        elif self.executable in PYTHON_EXECUTABLES:
            self.script = "python"
            self.executable = "python"
            name, ext = os.path.splitext(os.path.basename(self.cmdline[1]))
            self.name = name
            if name == "jarvis":
                children = process.children()
                if len(children) > 0:
                    app = children[0]
                    tokens = os.path.dirname(app.exe()).split('/')
                    self.executable = 'ironman'
                    self.name = tokens[-1]
                    AppProcess.children.append(AppProcess(app.pid, app, app.exe(), True))
        elif child:
            tokens = os.path.dirname(exe).split('/')
            self.name = tokens[-1]
            self.executable = "iapp"
            self.script = None
        else:
            self.name = self.executable
            self.executable = "native"
            self.script = None


# ProcessSensor monitors all processes in the system, and filter out those
# interesting processes, e.g. node-js process, python process.
#
#!   003C    F   process python  stats   cpu 0.0 %
#!   003D    F   process python  stats   num_threads 10
#!   003E    F   process python  stats   num_fds 7
#!   003F    F   process python  stats   pid 67853
#!   0040    F   process python  stats   memory  0.05564689636230469 %
#!   0041    F   process node    sensor-web  cpu 0.1 %
#!   0042    F   process node    sensor-web  num_threads 11
#!   0043    F   process node    sensor-web  num_fds 23
#!   0044    F   process node    sensor-web  pid 67829
#!   0045    F   process node    sensor-web  memory  0.6449222564697266  %
#
class ProcessSensor(BaseSensor):
    def __init__(self):
        super().__init__()
        self._preferred_period = 2
        self._keywords = []
        self._disabled_fields = []
        if 'SYS_STATS_PROCESS_SENSOR_EXTRA_KEYWORDS' in os.environ:
            keywords = os.environ['SYS_STATS_PROCESS_SENSOR_EXTRA_KEYWORDS']
            self._keywords = keywords.split(',') if keywords is not None and keywords != '' else self._keywords
        if 'SYS_STATS_PROCESS_SENSOR_DISABLED_FIELDS' in os.environ:
            fields = os.environ['SYS_STATS_PROCESS_SENSOR_DISABLED_FIELDS']
            self._disabled_fields = fields.split(',') if fields is not None and fields != '' else self._disabled_fields
        AppProcess.disabled_fields = self._disabled_fields


    @property
    def data(self):
        AppProcess.children = []
        keywords = self._keywords
        xs = [ AppProcess.createInstance(pid, keywords) for pid in psutil.pids() ]
        xs = [ x for x in xs if x is not None ]
        xs.extend(AppProcess.children)
        data_list = [ ConstantSysProcessSensor(x.executable, x.name, x._fields).data for x in xs ]
        # self.log("found %d process" % len(xs))
        return data_list
        #try:
        #
        #    xs = decouple_nested_list(data_list)
        #    print("xs = %s" % (str(xs)))
        #    return xs
        #except Exception as e:
        #    print(e)
        #    raise e


SensorClasses = [
    ProcessSensor
]