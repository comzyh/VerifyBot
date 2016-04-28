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
        logger.setLevel(logging.INFO)


def make_app():
    """make_app."""
    config = Config()
    import tornado.web
    logger.info('Main url is {0}'.format(config.url_prefix + "/"))
    return tornado.web.Application([
        (config.url_prefix + "/", MainHandler),
        (config.url_prefix + '/update', BotHandler)
    ])


def main():
    configure_logger()
    config = Config()
    if config.args.set_web_hook:
        bot = TelegramBot()
        webhook_url = 'https://{hostname}{url_prefix}/update'.format(
            hostname=config.args.hostname,
            url_prefix=config.url_prefix,
        )
        logger.info('webhook_url: {0}'.format(webhook_url))
        bot.set_web_hook(webhook_url)
    if config.args.demon:
        app = make_app()
        app.listen(config.port)
        tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
