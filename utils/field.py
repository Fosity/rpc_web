# -*- coding: utf-8 -*-
class Field(object):
    def __str__(self):
        if self.value:
            self.widget.attrs['value'] = self.value
        return str(self.widget)


class CharField(Field):
    def __init__(self, func=None, errors=None, optional=None):
        self.type = str
        self.value = None
        self.func = func
        self.errors = errors
        self.optional = optional


class IntField(Field):
    def __init__(self, func=None, errors=None, optional=None):
        self.value = None
        self.func = func
        self.errors = errors
        self.optional = optional
        self.type = int
