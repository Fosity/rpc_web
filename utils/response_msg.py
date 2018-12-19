# -*- coding: utf-8 -*-
from aiohttp import web

__all__ = ('ReponseMsg')


class ReqMsg:
    def __call__(self, data, code=200, *args, **kwargs):
        if code == 404:
            self.msg = {"msg": "fail", "data": data, "code": 404}
        elif code == 500:
            self.msg = {"msg": "fail", "data": data, "code": 500}
        else:
            self.msg = {"msg": "success", "data": data, "code": 200}

        return web.json_response(data=self.msg)


ResponseMsg = ReqMsg().__call__
