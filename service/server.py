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
        logging.info('Captcha received.')
        status, code = yield self.bot.on_receive_captcha(captcha=self.request.files['captcha'][0])
        if not status:
            self.set_status(404)
        self.finish(code)


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
        elif 'reply_to_message' in message:  # reply
            reply_file_id = message['reply_to_message']['photo'][0]['file_id']
            self.bot.on_receive_result(reply_file_id, text)
