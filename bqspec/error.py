# coding: utf-8
from __future__ import unicode_literals

from .rcpath import ResourcePath

if False:
    from typing import Optional, Text


class SpecError(object):
    def __init__(self, error_type, message, resource_path=None):  # type: (Text, Text, Optional[ResourcePath]) -> None
        self.error_type = error_type  # type: Text
        self.message = message  # type: Text
        self.resource_path = resource_path  # type: Optional[ResourcePath]
