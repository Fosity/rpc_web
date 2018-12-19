# -*- coding: utf-8 -*-
import logging

from aiomysql.sa import create_engine

from config import config


async def setup_db(app):
    engine = await create_engine(
        db=config.database.get('db'),
        user=config.database.get("user"),
        host=config.database.get("host"),
        port=config.database.get("port"),
        password=config.database.get("password"),
        autocommit=True
    )
    app.db = engine
    logging.info("db is start")


async def close_db(app):
    app.db.close()
    await app.db.await_close()
    logging.info("db is closed")
