# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import json
import logging
import time
import uuid
from functools import wraps
from aiohttp import web
import jsonpickle

from config import config
from .random import str_md5
from .token import Token


def logging_wrapper(f):
    @wraps(f)
    async def decorator(self, *args, **kwargs):
        try:
            data = await self.request.json()
        except Exception as e:
            data = None
        uuid_num = f"{str(uuid.uuid4())[:8]}"
        logging.info(f"""
        request begin ==================  {uuid_num}
            """)
        time_ = time.time()
        resp = await f(self, *args, **kwargs)
        msg = f"""
        method          =======>        {self.request.method}
        url             =======>        {self.request.url}
        func_path       =======>        {f.__module__+'.'+self.__class__.__name__+'.'+f.__name__}
        values          =======>        {dict(self.request.query.items())}
        json            =======>        {data}
        resp            =======>        {resp.__dict__['_body'].decode('utf-8')}
        end json        =======>        {time.time()-time_} S
        request end     =======>        {uuid_num}
        """
        logging.info(msg)
        return resp

    return decorator


async def json_request(request):
    try:
        data = await request.json()
    except Exception as e:
        data = None
    msg = {"path": request.path, "json": data, "values": dict(request.query.items()),
           "token": await Token(request).get_token(),
           "method": request.method}
    str = json.dumps(msg)
    return str_md5(str)


def cache_wrapper(f, conn=None, expired=60 * 60):
    @wraps(f)
    async def decorator(self, *args, **kwargs):
        redis_conn = conn if conn else self.request.app.redis_pool
        md5_str = await json_request(self.request)
        resp_body = await redis_conn.get(f"{config.csrf_redis_path}{md5_str}")
        if resp_body is None:
            resp_new = await f(self, *args, **kwargs)
            print(resp_new.body)
            await redis_conn.setex(f"{config.csrf_redis_path}{md5_str}", expired, resp_new.body)
            return resp_new
        else:
            msg = """
        end cached =================>
            """
            logging.info(msg)
            return web.json_response(body=resp_body,headers={"Access-Control-Allow-Origin":"*"})

    return decorator
