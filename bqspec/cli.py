# coding: utf-8
import os
import os.path
from typing import List, Text

import click

from bqspec.error import SpecError
from bqspec.loader import load_yaml
from bqspec.struct import RawSpec
from bqspec.validator import validate_schema, validate_values


def report_error(path, errors):  # type: (Text, List[SpecError]) -> None
    click.echo("{}:".format(path))
    for error in errors:
        click.echo("    {} {}: {}".format(error.error_type, ">".join(error.resource_path), error.message))


def run(path):  # type: (Text) -> None
    with click.open_file(path, encoding="utf-8") as f:
        obj = load_yaml(f)

    errors = validate_schema(obj)
    if errors:
        report_error(path, errors)
        return

    raw_spec = RawSpec(**obj)
    errors = validate_values(raw_spec)
    if errors:
        report_error(path, errors)
        return

    click.echo("run {}".format(path))


@click.command()
@click.option("-f", type=click.Path(dir_okay=False, exists=True))
@click.option("-d", default=".", type=click.Path(file_okay=False, exists=True))
def cli(f, d):
    if f:
        paths = [f]
    else:
        paths = [
            os.path.join(dirname, filename) for dirname, _, filenames in os.walk(d) for filename in filenames
            if filename.endswith((".yaml", ".yml"))
        ]
    for path in paths:
        run(path)


if __name__ == "__main__":
    cli()
