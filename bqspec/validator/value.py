# coding: utf-8
from __future__ import unicode_literals

from typing import List, Text

from bqspec.error import SpecError
from bqspec.rcpath import ResourcePath
from bqspec.struct import RawSpec


def value_error(message, resource_path):  # type: (Text, ResourcePath) -> SpecError
    return SpecError("ValueError", message, resource_path)


def validate_values(raw_spec):  # type: (RawSpec) -> List[SpecError]
    return []
