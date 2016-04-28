#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MainHandler."""
import json
import logging

from tornado import gen
from tornado.web import RequestHandler

from service.tgbot import TelegramBot

logger = logging.getLogger('VerifyBot')


class MainHandler(RequestHandler):
    """Handler."""

    def initialize(self):
        self.bot = TelegramBot()

    def get(self):
        """get."""
        self.write('VerifyBot.')

    @gen.coroutine
    def post(self):
        """set."""
        print (self.request.body)
        self.bot.on_receive_captcha(captcha=self.request.files['captcha'][0])


class BotHandler(RequestHandler):

    def initialize(self):
        self.bot = TelegramBot()

    @gen.coroutine
    def post(self):
        logger.debug(self.request.body)
        message = json.loads(self.request.body.decode('utf-8'))['message']
        message_id = message['message_id']
        chat_id = message['chat']['id']
        text = message['text']
        if text.startswith('/'):
            command = text.split('@')[0][1:]
            logger.debug('Got command {command} from chat {chat_id}'.format(command=command, chat_id=chat_id))
            if command == 'subscribe':
                self.bot.subscribe(chat_id)
                yield self.bot.send_message(chat_id, 'Subscribe successfully.', message_id)
            elif command == 'unsubscribe':
                self.bot.subscribe(chat_id)
                yield self.bot.send_message(chat_id, 'Unsubscribe successfully.', message_id)
            else:
                yield self.bot.send_message(chat_id, 'Unknown command.', message_id)
