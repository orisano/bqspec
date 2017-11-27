# coding: utf-8
from __future__ import unicode_literals

from typing import Any, Text


class Spec(object):
    def __init__(self, query_path, params=None, invariants=None, cases=None):
        # type: (Text, Any, Any, Any) -> None
        self.query_path = query_path
        self.params = params
        self.invariants = invariants
        self.cases = cases


def from_dict(d):  # type: (dict) -> Spec
    query_path = d["query_path"]
    params = d["params"]
    invariants = d["invariants"]
    cases = d[""]
