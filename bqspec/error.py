# coding: utf-8


class SpecError(object):
    def __init__(self, error_type, message, location):
        self.error_type = error_type
        self.message = message
        self.location = location
