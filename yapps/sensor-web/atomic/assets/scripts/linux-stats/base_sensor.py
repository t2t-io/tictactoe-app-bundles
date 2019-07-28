#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
import re
import os

# Helper classes and functions
#
from sensor_util import SensorData

class BaseSensor:
    def __init__(self):
        self._base = SensorData()
        self._logger = None
        self._last_data = []
        self._unit_length_defs = {}
        self._exclusive_list = []
        self._preferred_period = None    # preferred period to perform measurement: 1 second
        self._default_period = 1
        pass

    def measure(self):
        # always need to implement
        pass

    def filter(self, props):
        elist = set(self._exclusive_list)
        key_values = [ (k, v) for k, v in props.items() if k not in elist ]
        return dict(key_values)

    def transform(self, props):
        return props

    def produce(self, data_type, value):
        defs = self._unit_length_defs
        u = defs[data_type] if data_type in defs else None
        return self._base.duplicate(data_type=data_type, value=value, unit_length=u)

    def get_classname_tokens(self):
        name = self.__class__.__name__
        return re.findall(r'[A-Z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', name)

    def get_upper_classname_tokens(self):
        return [ x.upper() for x in self.get_classname_tokens() ]

    def set_logger(self, logger):
        self._logger = logger

    def log(self, message):
        self._logger(message)
        # p = print if self._logger is None else self._logger
        # return p(message)

    @property
    def preferred_period(self):
        p = 1 if self._preferred_period is None else self._preferred_period
        v = None
        tokens = self.get_upper_classname_tokens()
        tokens = [ 'SYS_STATS' ] + tokens + [ 'PERIOD' ]
        var_name = "_".join(tokens)
        try:
            self.log("%s: checking ..." % (var_name))
            if var_name in os.environ:
                v = int(os.environ[var_name])
                self.log("%s: %ds" % (var_name, v))
        except Exception as e:
            pass
        p = p if v is None else v
        return p


    @property
    def data(self):
        self._last_data = self.transform(self.filter(self.measure()))
        return [ self.produce(k, v) for k, v in self._last_data.items() ]



class DataTypeTransformSensor(BaseSensor):
    def __init__(self, data_type_aliases=None):
        super().__init__()
        self._data_type_aliases = data_type_aliases if data_type_aliases is not None else {}

    def find_data_type_alias(self, data_type):
        aliases = self._data_type_aliases
        return aliases[data_type] if data_type in aliases else data_type

    def transform(self, props):
        ps = super().transform(props)
        return dict([ (self.find_data_type_alias(k), v) for k, v in props.items() ])



class ConstantBaseSensor(BaseSensor):
    def __init__(self, board_type, board_id, sensor, constant_data, exclusive_list=None, unit_length_defs=None):
        super().__init__()
        self._base.board_type = board_type
        self._base.board_id = board_id
        self._base.sensor = sensor
        self._constant_data = constant_data
        if exclusive_list is not None:
            self._exclusive_list = self._exclusive_list + exclusive_list
        if unit_length_defs is not None:
            self._unit_length_defs.update(unit_length_defs)

    def measure(self):
        return self._constant_data

