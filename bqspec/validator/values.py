# coding: utf-8
from __future__ import unicode_literals

import os.path
from typing import List, Text

import embexpr

from bqspec.error import SpecError
from bqspec.rcpath import ResourcePath, resource_index, resource_val
from bqspec.struct import RawSpec, RawParam
from bqspec.bqtype import SUPPORT_TYPES


def value_error(message, resource_path):  # type: (Text, ResourcePath) -> SpecError
    return SpecError("ValueError", message, resource_path)


def validate_param_values(param, resource_path):  # type: (RawParam, ResourcePath) -> List[SpecError]
    errors = []  # type: List[SpecError]
    if param.type.upper() not in SUPPORT_TYPES:
        errors.append(value_error("unsupported type: {}".format(param.type), resource_path))
    else:
        t = SUPPORT_TYPES[param.type.upper()]
        if not isinstance(param.value, t):
            errors.append(value_error("value is invalid {}".format(param.type), resource_path))
    return errors


def validate_conditions_values(container, conditions, resource_path):
    # type: (Text, List[Text], ResourcePath) -> List[SpecError]
    errors = []  # type: List[SpecError]
    for i, condition in enumerate(conditions):
        try:
            embexpr.parse(condition)
        except embexpr.ParseError as e:
            errors.append(value_error(e.message, resource_path + [container, resource_index(i), resource_val]))

    return errors


def validate_values(raw_spec, resource_path=None):  # type: (RawSpec, ResourcePath) -> List[SpecError]
    if resource_path is None:
        resource_path = []

    errors = []  # type: List[SpecError]
    if not os.path.isfile(raw_spec.query_path):
        errors.append(value_error("query_path is not file", resource_path + ["query_path", resource_val]))

    for i, param in enumerate(raw_spec.params):
        errors.extend(validate_param_values(param, resource_path + ["params", resource_index(i), resource_val]))

    return errors
