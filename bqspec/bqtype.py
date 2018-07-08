# coding: utf-8
from __future__ import unicode_literals

import datetime
import types

import six

if False:
    from typing import Dict, Text


SUPPORT_TYPES = {  # type: Dict[Text, types.TypeType]
    "STRING": six.text_type,
    "INT64": int,
    "FLOAT64": float,
    "BOOL": bool,
    "TIMESTAMP": datetime.datetime,
    "DATETIME": datetime.datetime,
    "DATE": datetime.date,
}
