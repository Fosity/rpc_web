# -*- coding: utf-8 -*-
import logging
from logging.handlers import RotatingFileHandler


def setup_logger():
    # 注册 logger
    handler = RotatingFileHandler(filename='logs/app.log',
                                  mode='a',
                                  maxBytes=1 * 1024 * 1024,
                                  backupCount=5,
                                  encoding='utf-8')

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)

    LOG = logging.getLogger()
    LOG.setLevel(logging.INFO)
    LOG.addHandler(handler)
