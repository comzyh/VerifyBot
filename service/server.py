#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MainHandler."""
import tornado.web

from service.tgbot import TelegramBot


class MainHandler(tornado.web.RequestHandler):
    """Handler."""

    def initialize(self):
        self.bot = TelegramBot()

    def get(self):
        """get."""
        self.write('VerifyBot.')

    def post(self):
        """set."""
        print (self.request.body)
        self.bot.on_receive_captcha(captcha=self.request.files['captcha'][0])

