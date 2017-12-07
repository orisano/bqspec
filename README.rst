BQSpec
===================================
| SQL testing tool for Google BigQuery.
| this library is pre-alpha. not recommended to production use.
| (under construction now)

Getting Started
--------
.. code:: bash

    pip install bqspec

.. code:: bash

    gcloud auth application-default login

How to Use
--------
spec.yaml

.. code:: yaml

    # test target SQL filepath
    query_path: ./sample.sql
    # any BigQuery query parameters (optional). more details: https://cloud.google.com/bigquery/docs/parameterized-queries
    params:
        - type: DATE
          name: date
          value: 2017-11-30
    # conditions which all rows must met (optional).
    invariants:
        - total >= 0  # write python expression
        - a + b == c
    # any test cases
    cases:
        - where:
          - id == 1
          expected:
          - total == 15
          - a == 2
          - b == 3
          - c == 5

.. code:: bash

    bqspec -f spec.yaml

or

.. code:: bash

    bqspec -d .


License
--------
MIT
