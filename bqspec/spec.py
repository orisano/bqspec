# coding: utf-8
from typing import Any, Optional, Text


class Spec(object):
    def __init__(self, query_path, params=None, invariants=None, cases=None):
        # type: (Text, Any, Any, Any) -> None
        self.query_path = query_path
        self.params = params
        self.invariants = invariants
        self.cases = cases


def from_dict(d):  # type: (dict) -> Optional[Spec]
    pass
