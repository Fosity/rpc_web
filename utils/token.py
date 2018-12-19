# -*- coding: utf-8 -*-
import jsonpickle

from config import config
from .random import random_ten_str


class Token:
    def __init__(self,request):
        self.request = request

    async def random_token(self):
        return random_ten_str()


    async def get_token(self):
        return self.request.headers.get(config.token_header)


    async def set_token(self, token, data, expire=None):
        data_json = jsonpickle.dumps(data)
        resp = await self.request.app.redis_pool.setex(config.auth + token, expire if expire else config.token_expire,
                                                  data_json)
        return False


    async def check_token(self):
        flag = False
        token = self.request.headers.get(config.token_header)
        if token is None:
            return flag
        resp = await self.request.app.redis_pool.get(config.auth + token)
        if resp is None:
            return flag
        return True


    async def get_auth_by_token(self):
        flag = False
        token = self.request.headers.get(config.token_header)
        if token is None:
            return flag
        resp = await self.request.app.redis_pool.get(config.auth + token)
        if resp is None:
            return flag
        return jsonpickle.loads(resp)


    async def delete_token(self, token):
        resp = await self.request.app.redis_pool.delete(config.auth + token)
        return resp
