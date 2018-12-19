# -*- coding: utf-8 -*-
import jsonpickle

from config import config
from .random import random_ten_str
from .token import Token


class CsrfString:

    @staticmethod
    async def get_csrf_string():
        return random_ten_str()

    @staticmethod
    async def set_csrf_string(request, url, token=None):
        string = await CsrfString.get_csrf_string()
        msg = {"url": url, "token": token}
        resp = await request.app.redis_pool.setex(config.csrf + string, config.csrf_expire, jsonpickle.dumps(msg))
        if resp:
            return string
        else:
            return False

    @staticmethod
    async def check_post_csrf(request, csrf):
        flag = False
        path = request.path
        resp = await request.app.redis_pool.get(config.csrf + csrf)
        if resp:
            resp_ = jsonpickle.loads(resp)
            path_ = resp_.get("url")
            if path in config.white_url:
                if path == path_:
                    flag = True
            else:
                token_ = resp_.get("token")
                token = await Token.get_token(request)
                if token == token_ and path_ == path:
                    flag = True
        if flag is True:
            await request.app.redis_pool.delete(config.csrf + csrf)
        return flag
