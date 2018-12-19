# -*- coding: utf-8 -*-
import logging

import aioredis

from config import config


async def setup_redis(app):
    # 注册redis
    pool = await aioredis.create_redis_pool(
        (
            config.redis_host,
            config.redis_port
        ),
        db=config.redis_db,
    )
    app.redis_pool = pool
    logging.info("redis is register")


async def close_redis(app):
    app.redis_pool.close()
    await app.redis_pool.wait_closed()
    logging.info("redis is closed")
