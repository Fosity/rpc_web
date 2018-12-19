# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import copy

from schema import Schema, And, Use, Optional, SchemaError

from config import config
from utils.csrf import CsrfString
from .field import Field


class BaseForm(object):
    def __init__(self, data):
        self.data = data
        self.fields = {}
        data_ = {}
        for name, field in type(self).__dict__.items():
            if name == 'meta':
                if config.mode != "development" and field.__dict__.get("csrf_token"):
                    self.fields[config.csrf_name] = And(Use(str), CsrfString().check_post_csrf, error="wrong csrf")
                    data_[config.csrf_name] = self.data.get(config.csrf_name)
                continue
            if name.startswith("__") is False:
                data_[name] = self.data.get(name)
                new_field = copy.deepcopy(field)
                if isinstance(new_field, Field):
                    if new_field.optional is None:
                        self.fields[name] = And(Use(new_field.type), new_field.func, error=new_field.errors)
                    else:
                        self.fields[Optional(name, default=None)] = And(Use(new_field.type), new_field.func,
                                                                        error=new_field.errors)
        self.field_schema = Schema(self.fields)
        self.data = data_

    def is_valid(self):
        try:
            json_data = self.field_schema.validate(self.data)
            return json_data, None
        except SchemaError as e:
            error = e.args[0]
            if error[0:12] == 'Missing keys':
                error = error.replace("Missing keys", "缺少参数")
            return None, error
