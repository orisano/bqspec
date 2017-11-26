# coding: utf-8
from __future__ import unicode_literals

import types
from typing import Any, List, Optional, Text

import six
from six.moves import filter, map

from bqspec.error import ResourcePath, SpecError


def schema_error(message, resource_path):  # type: (Text, ResourcePath) -> SpecError
    return SpecError("SchemaError", message, resource_path=resource_path)


def missing_error(name, resource_path, parent=None):
    # type: (Text, ResourcePath, Optional[Text]) -> SpecError
    if parent:
        return schema_error("{} required to '{}'".format(parent, name), resource_path)
    else:
        return schema_error("{} is required".format(name), resource_path)


def type_error(name, type_name, resource_path):  # type: (Text, Text, ResourcePath) -> SpecError
    return schema_error("{} must be {}".format(name, type_name), resource_path)


def unknown_property_error(got, resource_path):  # type: (Text, ResourcePath) -> SpecError
    return schema_error("'{}' is unknown property".format(got), resource_path)


def assert_type(obj, t, name, type_name, resource_path):
    # type: (Any, types.TypeType, Text, Text, ResourcePath) -> List[SpecError]
    if not isinstance(obj, t):
        return [type_error(name, type_name, resource_path)]
    return []


def validate_schema(obj):  # type: (Any) -> List[SpecError]
    errors = assert_type(obj, dict, "top level object", "mapping", [])
    if errors:
        return errors

    raw_spec = obj  # type: dict

    required = {"query_path"}
    optional = {"params"}
    either_or_both = {"cases", "invariants"}
    known = required | optional | either_or_both

    if "query_path" not in raw_spec:
        errors.append(missing_error("query_path", []))
    elif not isinstance(raw_spec["query_path"], six.text_type):
        errors.append(type_error("query_path", "unicode", ["query_path", "$val"]))

    if "params" in raw_spec:
        params = raw_spec["params"]
        if not isinstance(params, list):
            errors.append(type_error("params", "sequence", ["params", "$val"]))
        else:
            for i, param in enumerate(params):
                errors.extend(validate_param_schema(param, ["params", "#{}".format(i)]))

    if "invariants" in raw_spec:
        errors.extend(validate_conditions_schema("invariants", raw_spec["invariants"]))

    if "cases" in raw_spec:
        cases = raw_spec["cases"]
        if not isinstance(cases, list):
            errors.append(type_error("cases", "sequence", ["cases", "$val"]))  # TODO: add location
        else:
            for i, case in enumerate(cases):
                errors.extend(validate_case_schema(case))  # TODO: add location

    return errors


def validate_param_schema(raw_param, resource_path):  # type: (Any, ResourcePath) -> List[SpecError]
    errors = assert_type(raw_param, dict, "param", "mapping", resource_path)
    if errors:
        return errors

    for field in ["type", "name", "value"]:
        if field not in raw_param:
            errors.append(missing_error(field, resource_path, parent="param"))
        elif not isinstance(raw_param[field], six.text_type):
            errors.append(type_error(field, "unicode", resource_path + [field, "$val"]))

    return errors


def validate_case_schema(raw_case, resource_path):  # type: (Any, ResourcePath) -> List[SpecError]
    errors = assert_type(raw_case, dict, "case", "mapping", resource_path + ["val"])
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
