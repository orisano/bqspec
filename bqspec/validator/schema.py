# coding: utf-8
from __future__ import unicode_literals

import types
from collections import OrderedDict
from typing import Any, List, Optional, Text, Tuple

import six
from six.moves import filter, map

from bqspec import SpecError


def schema_error(message, location=None):  # type: (Text, Optional[Tuple[int, int]]) -> SpecError
    return SpecError("SchemaError", message, location)


def missing_error(name, parent=None):  # type: (Text, Optional[Text]) -> SpecError
    if parent:
        return schema_error("{} required to '{}'".format(parent, name))
    else:
        return schema_error("{} is required".format(name))


def type_error(name, type_name):  # type: (Text, Text) -> SpecError
    return schema_error("{} must be {}".format(name, type_name))


def assert_type(obj, t, name, type_name):  # type: (Any, types.TypeType, Text, Text) -> List[SpecError]
    if not isinstance(obj, t):
        return [type_error(name, type_name)]
    return []


def validate_schema(raw_spec):  # type: (Any) -> List[SpecError]
    errors = assert_type(raw_spec, OrderedDict, "top level object", "mapping")
    if errors:
        return errors

    if "query_path" not in raw_spec:
        errors.append(missing_error("query_path"))
    elif not isinstance(raw_spec["query_path"], six.text_type):
        errors.append(type_error("query_path", "unicode"))  # TODO: add location

    if "params" in raw_spec:
        params = raw_spec["params"]
        if not isinstance(params, list):
            errors.append(type_error("params", "sequence"))  # TODO: add location
        else:
            for i, param in enumerate(params):
                errors.extend(validate_param_schema(param))  # TODO: add location

    if "invariants" in raw_spec:
        errors.extend(validate_conditions_schema("invariants", raw_spec["invariants"]))

    if "cases" in raw_spec:
        cases = raw_spec["cases"]
        if not isinstance(cases, list):
            errors.append(type_error("cases", "sequence"))  # TODO: add location
        else:
            for i, case in enumerate(cases):
                errors.extend(validate_case_schema(case))  # TODO: add location

    return errors


def validate_param_schema(raw_param):  # type: (Any) -> List[SpecError]
    errors = assert_type(raw_param, OrderedDict, "param", "mapping")
    if errors:
        return errors

    for field in ["type", "name", "value"]:
        if field not in raw_param:
            errors.append(missing_error(field, parent="param"))
        elif not isinstance(raw_param[field], six.text_type):
            errors.append(type_error(field, "unicode"))

    return errors


def validate_case_schema(raw_case):  # type: (Any) -> List[SpecError]
    errors = assert_type(raw_case, OrderedDict, "case", "mapping")
    if errors:
        return errors

    if "when" not in raw_case:
        errors.append(missing_error("when", parent="case"))
    else:
        errors.extend(validate_conditions_schema("when", raw_case["when"]))

    if "expected" not in raw_case:
        errors.append(missing_error("expected", parent="case"))
    else:
        errors.extend(validate_conditions_schema("expected", raw_case["expected"]))

    return errors


def validate_conditions_schema(container, raw_conditions):  # type: (Text, Any) -> List[SpecError]
    errors = assert_type(raw_conditions, list, container, "sequence")
    if errors:
        return errors

    element_name = "{}'s element".format(container)
    enumerated = enumerate(raw_conditions)
    filtered = filter(lambda x: not isinstance(x[1], six.text_type), enumerated)
    mapped = map(lambda x: type_error(element_name, "unicode"), filtered)
    return list(mapped)
