# -*- coding: utf-8 -*-
import logging

from aiohttp import Signal


async def setup_new_signal(app):
    signal_obj = NewSignal()
    signal_obj.new_signal = Signal("new_signal")
    app.signal = signal_obj
    signal_obj.new_signal.append(each)
    signal_obj.new_signal.freeze()


class NewSignal(object):
    pass


async def each(round):
    logging.info("Round %s!" % round)


async def round_two(round):
    print("This is round two.")
