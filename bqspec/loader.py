# coding: utf-8
from __future__ import unicode_literals

from typing import Any, BinaryIO

import ruamel.yaml
import six

yaml = ruamel.yaml.YAML(typ="safe")
if six.PY2:

    def _construct_yaml_str(self, node):
        return self.construct_scalar(node)

    yaml.constructor.add_constructor("tag:yaml.org,2002:str", _construct_yaml_str)


def load_yaml(stream):  # type: (BinaryIO) -> Any
    return yaml.load(stream)
