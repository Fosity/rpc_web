# -*- coding: utf-8 -*-
from aiohttp import hdrs
from aiohttp import web

from config import config
from middleware.auth import auth_check


class MyView(web.View):
    async def _iter(self):
        if self.request.method not in hdrs.METH_ALL:
            self._raise_allowed_methods()

        if config.mode != "development":
            resp = await auth_check(self.request)
            if resp is False:
                return web.json_response({"msg": "fail", "data": "auth wrong", "status": 401})
        method = getattr(self, self.request.method.lower(), None)
        if method is None:
            self._raise_allowed_methods()
        resp = await method()
        return resp
