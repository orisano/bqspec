# coding: utf-8
from __future__ import unicode_literals

import ruamel.yaml
import six

if six.PY2:

    def _construct_yaml_str(self, node):
        return self.construct_scalar(node)

    ruamel.yaml.SafeLoader.add_constructor("tag:yaml.org,2002:str", _construct_yaml_str)


def load_yaml(stream):
    return ruamel.yaml.safe_load(stream)
