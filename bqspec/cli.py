# coding: utf-8
import os
import os.path
import sys
from typing import List, Text, Tuple

import click

from bqspec.error import SpecError
from bqspec.loader import load_yaml
from bqspec.rstruct import RawSpec
from bqspec.spec import from_struct
from bqspec.validator import validate_schema, validate_values


def report_error(path, errors):  # type: (Text, List[SpecError]) -> None
    click.echo("{}:".format(path))
    for error in errors:
        click.echo("    {} {}: {}".format(error.error_type, ">".join(error.resource_path), error.message))


def run(path):  # type: (Text) -> bool
    with click.open_file(path, encoding="utf-8") as f:
        obj = load_yaml(f)

    errors = validate_schema(obj)
    if errors:
        report_error(path, errors)
        return True

    raw_spec = RawSpec(**obj)
    errors = validate_values(raw_spec)
    if errors:
        report_error(path, errors)
        return True

    spec = from_struct(raw_spec)

    failed = False
    cases_results, invariants_results = spec.verify()
    if invariants_results:
        failed = True
        click.echo("Invariants Failed Cases::")
        _print_results(invariants_results)

    for i, case in enumerate(spec.cases):
        results = cases_results[i]
        if not results:
            continue

        failed = True
        click.echo("Failed Case: {}".format(i))
        for condition in case.where:
            click.echo("- {}".format(condition.expr))
        _print_results(results)

    return failed


def _print_results(results):  # type: (List[Tuple[dict, List[Text]]]) -> None
    for row, messages in results:
        click.echo("===========================")
        click.echo(row)
        click.echo("[failed]")
        for message in messages:
            click.echo("{} #==> False".format(message))
        click.echo("")


@click.command()
@click.option("-f", type=click.Path(dir_okay=False, exists=True))
@click.option("-d", default=".", type=click.Path(file_okay=False, exists=True))
def cli(f, d):
    if f:
        failed = run(f)
    else:
        paths = [
            os.path.join(dirname, filename) for dirname, _, filenames in os.walk(d) for filename in filenames
            if filename.endswith((".yaml", ".yml"))
        ]
        failed = False
        for path in paths:
            if run(path):
                failed = True

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    cli()
