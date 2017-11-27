# coding: utf-8
from __future__ import unicode_literals

from typing import List, Text

import six

from bqspec.error import SpecError
from bqspec.rcpath import ResourcePath


def value_error(message, resource_path):  # type: (Text, ResourcePath) -> SpecError
    return SpecError("ValueError", message, resource_path)


def validate_values(d):  # type: (dict) -> List[SpecError]
    return []
