# coding: utf-8
import codecs
from typing import List, Optional, Text, Tuple

import embexpr
import google.cloud.bigquery as bq
from six.moves import map
from tqdm import tqdm

from .rstruct import RawSpec


class Case(object):
    def __init__(self, where, expected):  # type: (List[embexpr.Expr], List[embexpr.Expr]) -> None
        self.where = where  # type: List[embexpr.Expr]
        self.expected = expected  # type: List[embexpr.Expr]


class Spec(object):
    def __init__(
            self,
            query_path,  # type: Text
            params=None,  # type: Optional[List[bq.ScalarQueryParameter]]
            columns=None,  # type: Optional[List[Text]]
            invariants=None,  # type: Optional[List[embexpr.Expr]]
            cases=None  # type: Optional[List[Case]]
    ):  # (...) -> None
        if params is None:
            params = []
        if columns is None:
            columns = []
        if invariants is None:
            invariants = []
        if cases is None:
            cases = []

        self.query_path = query_path  # type: Text
        self.params = params  # type: List[bq.ScalarQueryParameter]
        self.columns = columns  # type: List[Text]
        self.invariants = invariants  # type: List[embexpr.Expr]
        self.cases = cases  # type: List[Case]

    def execute_query(self):
        with codecs.open(self.query_path, encoding="utf-8") as f:
            query = f.read()
        client = bq.Client()

        job_config = bq.QueryJobConfig()
        job_config.query_parameters = self.params
        query_job = client.query(query, job_config=job_config)

        query_job.result()
        destination_table_ref = query_job.destination
        table = client.get_table(destination_table_ref)

        def convert_dict(row):
            return {field.name: row[field.name] for field in table.schema}

        return map(convert_dict, client.list_rows(table))

    def verify(self):  # type: () -> Tuple[List[List[Tuple[dict, List[Text]]]], List[Tuple[dict, List[Text]]]]
        cases = [[] for _ in range(len(self.cases))]
        messages = []
        first = True
        for row in tqdm(self.execute_query()):
            if first:
                first = False
                unknown_columns = [key for key in row.keys() if key not in self.columns]
                if unknown_columns:
                    messages.append(
                        (row, ['"{}" is unknown column'.format(unknown_column) for unknown_column in unknown_columns]))

            failed = [invariant.expr for invariant in self.invariants if not invariant(**row)]
            if failed:
                messages.append((row, failed))

            for i, case in enumerate(self.cases):
                if all(condition(**row) for condition in case.where):
                    unexpected = [condition.expr for condition in case.expected if not condition(**row)]
                    if unexpected:
                        cases[i].append((row, unexpected))
        return cases, messages


def to_conditions(conditions):  # type: (List[Text]) -> List[embexpr.Expr]
    return [embexpr.Expr(condition) for condition in conditions]


def from_dict(d):  # type: (dict) -> Spec
    return from_struct(RawSpec(**d))


def from_struct(raw_spec):  # type: (RawSpec) -> Spec
    query_path = raw_spec.query_path
    params = [
        bq.ScalarQueryParameter(param.name.encode("latin-1"), param.type.encode("latin-1"), param.value)
        for param in raw_spec.params
    ]
    invariants = to_conditions(raw_spec.invariants)
    cases = [Case(to_conditions(case.where), to_conditions(case.expected)) for case in raw_spec.cases]

    return Spec(query_path, params, raw_spec.columns, invariants, cases)
