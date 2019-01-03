# -*- coding: utf-8 -*-
import logging
from aiohttp import web

from init import setup_logger, setup_redis, setup_db, close_db, close_redis, setup_new_signal
from routes import setup_routes


async def init_app(debug=False):
    app = web.Application(debug=debug)
    setup_routes(app)  # 路由
    setup_logger()  # 日志
    my_signal(app)  # signal
    return app


def my_signal(app):
    app.on_startup.append(setup_db)  # 注册 数据库
    app.on_startup.append(setup_new_signal)  # 注册 新信号
    app.on_startup.append(setup_redis)  # 注册 redis
    logging.info("signal is register")
    app.on_cleanup.append(close_db)  #
    app.on_cleanup.append(close_redis)


def main(host='127.0.0.1', port=5000, debug=False):
    app = init_app(debug=debug)
    web.run_app(app, host=host, port=port)


if __name__ == "__main__":
    main(debug=True)
