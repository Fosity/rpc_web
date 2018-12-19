# -*- coding: utf-8 -*-
import logging

from aiohttp.web import middleware


@middleware
async def mymiddleware(request, handler):
    logging.info("middle first")
    resp = await handler(request)
    logging.info("middle end")
    return resp
