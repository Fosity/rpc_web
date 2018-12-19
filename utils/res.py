# -*- coding: utf-8 -*-
import datetime
from decimal import Decimal


def underscore_to_camelcase(s):
    """Take the underscore-separated string s and return a camelCase
    equivalent.  Initial and final underscores are preserved, and medial
    pairs of underscores are turned into a single underscore."""

    def camelcase_words(words):
        first_word_passed = False
        for word in words:
            if not word:
                yield "_"
                continue
            if first_word_passed:
                yield word.capitalize()
            else:
                yield word.lower()
            first_word_passed = True

    return ''.join(camelcase_words(s.split('_')))


class ResponseModel(object):

    def dict(self):
        dict = self.__dict__
        # # 如果 实例化对象中没有类定义的内容，就会报错，启到限制api的dict名称。
        # cls_dict = self.__class__.__dict__
        obj = {}
        for key in dict.keys():
            val = dict[key]
            # if key not in cls_dict:
            #     raise KeyError('{0} out of < class: {1} > range!'.format(key,self.__class__.__name__))
            if isinstance(val, datetime.datetime):
                val = str(val)
            elif isinstance(val, Decimal):
                val = float(val)
            elif key == '_sa_instance_state':
                continue
            obj[underscore_to_camelcase(key)] = val
        return obj


### example
class Res(ResponseModel):
    pass


def obj_to_dict(obj):
    if isinstance(obj, dict):
        dict_ = {}
        for k, v in obj.items():
            resp = obj_to_dict(v)
            dict_[k] = resp
        return dict_
    elif isinstance(obj, list):
        list_ = []
        for item in obj:
            resp = obj_to_dict(item)
            list_.append(resp)
        return list_
    elif isinstance(obj, str):
        return str(obj)
    elif isinstance(obj, int):
        return str(obj)
    else:
        dict_ = obj.__dict__
        # # 如果 实例化对象中没有类定义的内容，就会报错，启到限制api的dict名称。
        # cls_dict = self.__class__.__dict__
        obj_ = {}
        for key in dict_.keys():
            val = dict_[key]
            # if key not in cls_dict:
            #     raise KeyError('{0} out of < class: {1} > range!'.format(key,self.__class__.__name__))
            if isinstance(val, datetime.datetime):
                val = str(val)
            elif isinstance(val, Decimal):
                val = float(val)
            elif key == '_sa_instance_state':
                continue
            obj_[key] = val
        return obj_
