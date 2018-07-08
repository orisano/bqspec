# coding: utf-8
from __future__ import unicode_literals

if False:
    from typing import List, Text

ResourcePath = List[Text]

resource_key = "$key"
resource_val = "$val"


def resource_index(i):  # type: (int) -> Text
    return "#{}".format(i)
