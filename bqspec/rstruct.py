# coding: utf-8
from __future__ import unicode_literals

import datetime
from typing import List, Optional, Text, Union


class RawCase(object):
    def __init__(self, where=None, expected=None):  # type: (Optional[List[Text]], Optional[List[Text]]) -> None
        if where is None:
            where = []
        if expected is None:
            expected = []
        self.where = where  # type: List[Text]
        self.expected = expected  # type: List[Text]


class RawParam(object):
    def __init__(self, type="", name="", value=""):  # type: (Text, Text, Text) -> None
        self.type = type  # type: Text
        self.name = name  # type: Text
        self.value = value  # type: Union[Text, int, float, bool, datetime.datetime, datetime.date]


class RawSpec(object):
    def __init__(self, query_path, params=None, columns=None, invariants=None, cases=None):
        # type: (Text, Optional[List[dict]], Optional[List[Text]], Optional[List[Text]], Optional[List[dict]]) -> None
        if params is None:
            params = []
        if columns is None:
            columns = []
        if invariants is None:
            invariants = []
        if cases is None:
            cases = []

        self.query_path = query_path  # type: Text
        self.params = [RawParam(**param) for param in params]  # type: List[RawParam]
        self.columns = columns  # type: List[Text]
        self.invariants = invariants  # type: List[Text]
        self.cases = [RawCase(**case) for case in cases]  # type: List[RawCase]
