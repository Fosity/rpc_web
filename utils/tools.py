# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import functools


class Const():
    class ConstError(TypeError): pass

    def __setattr__(self, name, value):
        if self.__dict__.has_key(name):
            raise self.ConstError("Can't rebind const.%s" % name)
        self.__dict__[name] = value


def singleton(cls):
    instances = {}
    @functools.wraps(cls)
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance
