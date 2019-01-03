# -*- coding: utf-8 -*-
from config import config
from forms.auth_form import AuthForm, AuthRegisterForm
from service import Auth
from utils.response_msg import ResponseMsg
from utils.token import Token
from utils.views import MyView
from utils.wrapper import logging_wrapper, cache_wrapper


class AuthLogin(MyView):
    """
    用户登录 username password
    """

    @logging_wrapper
    async def post(self):
        data = await self.request.json()
        name = data.get("username")
        password = data.get("password")
        flag, error = AuthForm(data).is_valid()
        if error is not None:
            return ResponseMsg(data=error, code=404)
        auth_obj = Auth(self.request)
        resp, user_id = await auth_obj.login(name=name, password=password)
        permission_dict = await auth_obj.get_user_permission(user_id=user_id)
        token_obj = Token(self.request)
        token = await token_obj.random_token()
        msg = {"token": token, "permission": permission_dict, "user_id": str(user_id)}
        await token_obj.set_token(token=token, data=msg, expire=config.token_expire)
        if resp:
            return ResponseMsg(data='auth permission', code=404)
        return ResponseMsg(data=msg)


class AuthRegister(MyView):
    """
    用户注册 username password
    """

    @logging_wrapper
    async def post(self):
        flag, error = AuthRegisterForm(await self.request.json()).is_valid()
        if error is not None:
            return ResponseMsg(data=error, code=404)
        auth_obj = Auth(self.request)
        resp = await auth_obj.register(username=flag.get("username"), password=flag.get("password"))
        if resp:
            return ResponseMsg(data="register right", code=200)
        return ResponseMsg(data="register wrong", code=404)


class AuthLogout(MyView):
    """
    用户登出,清除 redis中token
    """

    @logging_wrapper
    async def get(self):
        token_obj = Token(self.request)
        token = await token_obj.get_token()
        resp = await token_obj.delete_token(token=token)
        if resp:
            return ResponseMsg(data="logout right", code=200)
        return ResponseMsg(data="logout wrong", code=404)


class AuthRouterMap(MyView):
    """
    获取 前端路由 权限map
    """

    @logging_wrapper
    @cache_wrapper
    async def get(self):
        auth_obj = Auth(self.request)
        resp = await auth_obj.get_router_map()
        if resp:
            return ResponseMsg(data=resp, code=200)
        return ResponseMsg(data="router map wrong,try again", code=500)


class AuthInfo(MyView):
    """
    获取用户详细权限map
    """

    @logging_wrapper
    @cache_wrapper
    async def get(self):
        token_obj = Token(self.request)
        auth_dict = await token_obj.get_auth_by_token()
        user_id = auth_dict.get("user_id") if auth_dict else None
        if user_id is None:
            return ResponseMsg(data="try again", code=500)
        auth_obj = Auth(self.request)
        resp = await auth_obj.get_user_permission(user_id)
        if resp:
            return ResponseMsg(data=resp, code=200)
        return ResponseMsg(data="try again", code=500)
