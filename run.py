# coding: utf-8
from __future__ import unicode_literals

import codecs
import sys

import ruamel.yaml

import bqspec.spec


def main():
    with codecs.open(sys.argv[1], encoding="utf-8") as f:
        raw = ruamel.yaml.safe_load(f)

    spec = bqspec.spec.from_dict(raw)
    cases_results, invariants_results = spec.verify()
    print("Invariants Failed Cases::")
    for row, messages in invariants_results:
        print("===========================")
        print(row)
        print("[failed]")
        for message in messages:
            print("{} #==> False".format(message))
        print("")

    print("")
    print("Failed Cases::")
    for i, case in enumerate(spec.cases):
        results = cases_results[i]
        if not results:
            continue
        print("Case: {}".format(i))
        for condition in case.where:
            print("- {}".format(condition.expr))

        for row, messages in results:
            print("===========================")
            print(row)
            print("[failed]")
            for message in messages:
                print("{} #==> False".format(message))
            print("")


if __name__ == "__main__":
    main()
