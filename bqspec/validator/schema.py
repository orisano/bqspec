# coding: utf-8
from __future__ import unicode_literals

import datetime
import types
from typing import Any, List, Optional, Set, Text

import six
from six.moves import filter, map

from bqspec.error import SpecError
from bqspec.rcpath import ResourcePath, resource_index, resource_key, resource_val


def schema_error(message, resource_path):  # type: (Text, ResourcePath) -> SpecError
    return SpecError("SchemaError", message, resource_path=resource_path)


def missing_error(name, resource_path, parent=None):
    # type: (Text, ResourcePath, Optional[Text]) -> SpecError
    if parent:
        return schema_error("{} required to '{}'".format(parent, name), resource_path)
    else:
        return schema_error("{} is required".format(name), resource_path)


def insufficient_error(name, either_or_both, resource_path):  # type: (Text, Set[Text], ResourcePath) -> SpecError
    keys = ",".join(sorted(list(either_or_both)))
    return schema_error("{} required to either or both: {}".format(name, keys), resource_path)


def type_error(name, type_name, resource_path):  # type: (Text, Text, ResourcePath) -> SpecError
    return schema_error("{} must be {}".format(name, type_name), resource_path)


def unknown_property_error(got, resource_path):  # type: (Text, ResourcePath) -> SpecError
    return schema_error("'{}' is unknown property".format(got), resource_path + [got, resource_key])


def assert_type(obj, t, name, type_name, resource_path):
    # type: (Any, types.TypeType, Text, Text, ResourcePath) -> List[SpecError]
    if not isinstance(obj, t):
        return [type_error(name, type_name, resource_path)]
    return []


def validate_schema(obj, resource_path=None):  # type: (Any, Optional[ResourcePath]) -> List[SpecError]
    if resource_path is None:
        resource_path = []

    errors = assert_type(obj, dict, "top level object", "mapping", resource_path + [resource_val])
    if errors:
        return errors

    raw_spec = obj  # type: dict

    required = {"query_path"}
    optional = {"params", "columns"}
    either_or_both = {"cases", "invariants"}
    known = required | optional | either_or_both

    if "query_path" not in raw_spec:
        errors.append(missing_error("query_path", resource_path))
    elif not isinstance(raw_spec["query_path"], six.text_type):
        errors.append(type_error("query_path", "unicode", resource_path + ["query_path", resource_val]))

    if "params" in raw_spec:
        params = raw_spec["params"]
        if not isinstance(params, list):
            errors.append(type_error("params", "sequence", resource_path + ["params", resource_val]))
        else:
            for i, param in enumerate(params):
                errors.extend(validate_param_schema(param, resource_path + ["params", resource_index(i)]))

    if "columns" in raw_spec:
        columns = raw_spec["columns"]
        if not isinstance(columns, list):
            errors.append(type_error("columns", "sequence", resource_path + ["columns", resource_val]))
        else:
            for i, column in columns:
                if not isinstance(column, six.text_type):
                    errors.append(
                        type_error("columns's element", "unicode",
                                   resource_path + ["columns", resource_index(i), resource_val]))

    if "invariants" in raw_spec:
        errors.extend(validate_conditions_schema("invariants", raw_spec["invariants"], resource_path))

    if "cases" in raw_spec:
        cases = raw_spec["cases"]
        if not isinstance(cases, list):
            errors.append(type_error("cases", "sequence", resource_path + ["cases", resource_val]))
        else:
            for i, case in enumerate(cases):
                errors.extend(validate_case_schema(case, resource_path + ["cases", resource_index(i)]))

    if not any(key in raw_spec for key in either_or_both):
        errors.append(insufficient_error("top level object", either_or_both, resource_path))

    for key in raw_spec:
        if key not in known:
            errors.append(unknown_property_error(key, resource_path))

    return errors


def validate_param_schema(obj, resource_path):  # type: (Any, ResourcePath) -> List[SpecError]
    errors = assert_type(obj, dict, "param", "mapping", resource_path)
    if errors:
        return errors

    raw_param = obj  # type: dict

    required = {"type", "name"}
    known = required | {"value"}

    for key in required:
        if key not in raw_param:
            errors.append(missing_error(key, resource_path, parent="param"))
        elif not isinstance(raw_param[key], six.text_type):
            errors.append(type_error(key, "unicode", resource_path + [key, resource_val]))

    if "value" not in raw_param:
        errors.append(missing_error("value", resource_path, parent="param"))
    else:
        value = raw_param["value"]
        if not isinstance(value, (six.text_type, int, float, bool, datetime.datetime, datetime.date)):
            errors.append(
                type_error("value", "(unicode,int,float,bool,datetime,date)", resource_path + ["value", resource_val]))

    for key in raw_param:
        if key not in known:
            errors.append(unknown_property_error(key, resource_path))

    return errors


def validate_case_schema(obj, resource_path):  # type: (Any, ResourcePath) -> List[SpecError]
    errors = assert_type(obj, dict, "case", "mapping", resource_path + [resource_val])
    if errors:
        return errors

    raw_case = obj  # type: dict

    required = {"where", "expected"}
    known = required

    for key in required:
        if key not in raw_case:
            errors.append(missing_error(key, resource_path, parent="case"))
        else:
            errors.extend(validate_conditions_schema(key, raw_case[key], resource_path))

    for key in raw_case:
        if key not in known:
            errors.append(unknown_property_error(key, resource_path))

    return errors


def validate_conditions_schema(container, obj, resource_path):
    # type: (Text, Any, ResourcePath) -> List[SpecError]
    errors = assert_type(obj, list, container, "sequence", resource_path + [container, resource_val])
    if errors:
        return errors

    raw_conditions = obj  # type: list

    element_name = "{}'s element".format(container)
    enumerated = enumerate(raw_conditions)
    filtered = filter(lambda x: not isinstance(x[1], six.text_type), enumerated)
    mapped = map(
        lambda x: type_error(element_name, "unicode", resource_path + [container, resource_index(x[0]), resource_val]),
        filtered,
    )
    return list(mapped)
