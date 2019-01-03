# -*- coding: utf-8 -*-
import grpc
import sqlalchemy as sa

from models.models import redis_info
from service import redis_obj_pb2, redis_obj_pb2_grpc


class GrpcService(object):
    def __init__(self, request, id=None, db_num=None):
        self.request = request
        self.db = request.app.db
        if id:
            yield from self.get_redis(id)
        if db_num:
            self.db_num = db_num

    async def get_redis_info(self):
        async with self.db.acquire() as conn:
            resp = await (await conn.execute(
                sa.select([redis_info])
            )).fetchall()
            return resp

    async def put_redis_info(self, host, port, token):
        async with self.db.acquire() as conn:
            resp = await (await redis_info.insert().values(
                host=host, port=port, token=token
            ))
            print(resp)
            return redis_obj_pb2

    async def get_redis(self, id):
        async with self.db.acquire() as conn:
            resp = await (await conn.execute(
                sa.select([redis_info]).where(
                    redis_info.c.id == id
                )
            )).fetchone()
            self.url = f"{resp.host}:{resp.port}"
            self.token = resp.token
            return resp

    async def post_redis(self, host, port, token):
        async with self.db.acquire() as conn:
            resp = await conn.execute(redis_info.insert().values(host=host, port=port, token=token))
            url = f"{host}:{port}"
            return url

    async def get_all_from_db(self):
        msg = {
            "list": [],
            "string": [],
            "hash": [],
            "set": []
        }
        keys = self.keys()
        for key in keys:
            item = {
                "key": key,
                "type": self.type(name=key),
                "value": None
            }
            if item["type"] == "string":
                item["value"] = self.get(name=key)
                msg["string"].append(item)
            elif item["type"] == "list":
                len_ = self.llen(name=key)
                item["value"] = self.lrange(name=key, self=0, len=len_)
                msg["list"].append(item)
            elif item["type"] == "set":
                item["value"] = self.smembers(name=key)
                msg["set"].append(item)
            elif item["type"] == "hash":
                item["type"] = {
                    self.hkeys(name=key): self.hvals(name=key)
                }
                msg["hash"].append(item)
            else:
                pass
        return msg

    def excute(self, method, *args, **kwargs):
        """
        grpc_path = "localhost:50051"
        :param method:
        :param In:
        :param args:
        :param kwargs:
        :return:
        """
        kwargs['db'] = self.db_num
        kwargs['salt_pwd'] = self.token
        with grpc.insecure_channel(self.url) as channel:
            stub = redis_obj_pb2_grpc.RedisObjStub(channel)
            obj = getattr(stub, method)
            response = obj(getattr(redis_obj_pb2, f"{method}In")(**kwargs))
            return getattr(response, args[0])

    def keys(self, pattern="*"):
        keys = self.excute('keys', 'key', pattern=pattern)
        return keys

    def type(self, name):
        key_type = self.excute('type', 'type', name=name)
        return key_type

    def llen(self, name):
        length = self.excute('llen', 'len', name=name)
        return length

    def lrange(self, name, start, len):
        key_value = self.excute('lrange', 'values', name=name, start=start, len=len)
        return key_value

    def smembers(self, name):
        key_value = self.excute('smembers', 'values', name=name)
        return key_value

    def get(self, name):
        key_value = self.excute('get', 'value', name=name)
        return key_value

    def hkeys(self, name):
        key_value = self.excute('hkeys', 'keys', name=name)
        return key_value

    def hvals(self, name):
        key_value = self.excute('hvals', 'values', name=name)
        return key_value

    def set(self, name, value):
        flag = self.excute('set', 'isok', name=name, value=value)
        return flag

    def getset(self, name, value):
        key_value = self.excute('getset', 'value', name=name, value=value)
        return key_value

    def mget(self, name):
        values = self.excute('mget', 'values', name=name)
        return values

    def setnx(self, name):
        pass
