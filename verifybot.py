#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Main."""
import logging
import tornado.ioloop
from service.server import MainHandler
from service.server import BotHandler
from service.config import Config
from service.tgbot import TelegramBot

logger = logging.getLogger('VerifyBot')


def configure_logger():
    config = Config()
    hdr = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(name)s:%(levelname)s: %(message)s')
    hdr.setFormatter(formatter)
    logger.addHandler(hdr)
    if config.args.verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.ERROR)


def make_app():
    """make_app."""
    import tornado.web
    return tornado.web.Application([
        (r"/", MainHandler),
        (r'/update', BotHandler)
    ])


def main():
    config = Config()
    if config.args.set_web_hook:
        bot = TelegramBot()
        bot.set_web_hook(config.args.set_web_hook)
    if config.args.demon:
        app = make_app()
        app.listen(config.port)
        tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
