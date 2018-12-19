# -*- coding: utf-8 -*-
from utils.csrf import CsrfString
from utils.response_msg import ResponseMsg
from utils.token import Token
from utils.views import MyView
from utils.wrapper import logging_wrapper


class CsrfProtection(MyView):
    @logging_wrapper
    async def get(self):
        url = self.request.query.get("url")
        token_obj = Token(self.request)
        token = await token_obj.get_token()
        resp = await CsrfString.set_csrf_string(self.request, url, token)
        if resp:
            return ResponseMsg(data=resp)
        return ResponseMsg(data='false', code=404)
