from config import config
from utils.token import Token


async def auth_check(request):
    # 这里做token判断
    path = request.path  # 判断是否在白名单中
    if path in config.white_url:
        return True
    else:
        token_obj = Token(request)
        return await token_obj.check_token()

# def auth_wrapper(f):
#     def wrapper(self,*args, **kwargs):
#         auth = auth_check(self.request)
#         if auth is False:
#             return web.json_response({"msg": "fail", "data": "auth wrong", "status": 401})
#         else:
#             resp = web.json_response(f(*args, **kwargs))
#             return resp
#
#     return wrapper
