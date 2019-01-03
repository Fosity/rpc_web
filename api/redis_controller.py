# -*- coding: utf-8 -*-
from service.grpc_service import GrpcService,create_grpc
from utils.response_msg import ResponseMsg
from utils.views import MyView
from utils.wrapper import logging_wrapper


class RedisDetailController(MyView):
    """
    single key value option
    """

    async def get(self):
        """
        获取 单个 key 的值
        @id-> int     which machine redis which can be found from mysql
        @db-> int     redis's db num
        @type-> string   list or string or hash or set
        @key-> string
        :return:
        @value-> any   json data
        # todo @ttl->int      ttl time
        """
        json_data = await self.request.json()
        id_num = json_data.get("id")
        db_num = json_data.get("db")
        type_str = json_data.get("type")
        key_str = json_data.get("key")
        grpc_obj = GrpcService(self.request, id_num, db_num)
        value = None
        if type_str == "string":
            value = grpc_obj.get(name=key_str)
        elif type_str == "hash":
            pass
            value = grpc_obj.hgetall(name=key_str)
        elif type_str == "list":
            pass
        elif type_str == "set":
            pass
        else:
            pass
        return ResponseMsg(data=value)

    async def post(self):
        """
        插入 单个 key 的值
        @id-> int   which machine redis
        @db-> int   redis's db num
        @type-> string  list or string or hash or set
        @key-> string
        @value-> any  maybe a json data
        @ttl-> int   ttl time
        :return: @flag -> bool  post True or False
        """
        json_data = await self.request.json()
        id_num = json_data.get("id")
        db_num = json_data.get("db")
        type_str = json_data.get("type")
        key_str = json_data.get("key")
        value = json_data.get("value")
        ttl = json_data.get("ttl")
        grpc_obj = GrpcService(self.request, id_num, db_num)
        flag = None
        if type_str == "string":
            pass
        elif type_str == "hash":
            pass
        elif type_str == "list":
            pass
        elif type_str == "set":
            pass
        else:
            pass
        return ResponseMsg(data=flag)

    async def delete(self):
        """
        删除 单个 key 的值
        @id-> int which machine redis
        @db-> int redis's db num
        @:type-> string  list or string or hash or set
        @:key-> string
        :return: @flag -> bool delete True or False
        """
        json_data = await self.request.json()
        id_num = json_data.get("id")
        db_num = json_data.get("db")
        type_str = json_data.get("type")
        key = json_data.get("key")
        grpc_obj = GrpcService(self.request, id_num, db_num)
        # flag = grpc_obj.delete()
        # todo
        return ResponseMsg(data="")

    async def put(self):
        """
        修改 单个 key 的值
        @id-> int which machine redis
        @db-> int redis's db num
        @:type-> string  list or string or hash or set
        @:key-> string
        @:value-> any  json data
        @:ttl-> int   time ttl
        :return: @flag -> bool  update True or False
        """
        json_data = await self.request.json()
        id_num = json_data.get("id")
        db_num = json_data.get("db")
        type_str = json_data.get("type")
        key = json_data.get("key")
        value = json_data.get("value")
        ttl = json_data.get("ttl")
        grpc_obj = GrpcService(self.request, id_num, db_num)
        pass
        # todo
        return ResponseMsg(data="")


class RedisDbListController(MyView):
    """
    db option
    """

    @logging_wrapper
    async def get(self):
        """
        获取 db 中的所有信息，归类返回
        @id-> int which machine redis
        @db-> int  redis's db num  0-16
        :return: {"list":[],"string":[],"hash":[],"set":[]}
        """

        data = self.request.match_info
        id_num = data.get("id")
        db_num = data.get("db")
        grpc_obj = await create_grpc(self.request, id_num, db_num)
        resp = await grpc_obj.get_all_from_db()
        return ResponseMsg(data=resp)


class RedisListController(MyView):
    """
    redis
    """

    @logging_wrapper
    async def get(self):
        """
        获取 配置的 redis 信息
        :return:
        @id->int  redis uuid
        @host->string redis host
        @port->string redis port
        @token->string redis password
        @status->bool  redis is ok?
        @delay_time->int delay time
        """
        grpc_obj = GrpcService(self.request)
        resp = await grpc_obj.get_redis_info()
        return ResponseMsg(data=resp)

    @logging_wrapper
    async def post(self):
        """
        注册 配置的redis信息
        @host->string redis host
        @port->string redis port
        @token->string redis password
        :return:
        @id->int  redis uuid
        @status->bool  redis is ok?
        @delay_time->int delay time
        """
        json_data = await self.request.json()
        host = json_data.get("host")
        port = json_data.get("port")
        token = json_data.get("token")
        grpc_obj = GrpcService(self.request)
        resp = await grpc_obj.put_redis_info(host=host, port=port, token=token)
        return ResponseMsg(data=resp)
