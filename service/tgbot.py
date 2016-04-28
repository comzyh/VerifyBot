#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TelegramBot."""
import json
import mimetypes
import sqlite3
import logging


from tornado import gen
from tornado.httpclient import HTTPClient
from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPRequest
from tornado.httpclient import HTTPError
from tornado.concurrent import Future

from service.singleton import Singleton
from service.config import Config

logger = logging.getLogger('VerifyBot')


class TelegramBot(Singleton):
    """docstring for TelegramBot"""

    def __init__(self):
        config = Config()
        self.token = config.token
        self.api_url = 'https://api.telegram.org/bot{token}/'.format(token=self.token)
        self.db = sqlite3.connect(config.db_filename)
        self.create_db()
        self.load_chat_ids()
        self.unfinshed_task = {}

    def create_db(self):
        cu = self.db.cursor()
        cu.execute('''
            CREATE TABLE IF NOT EXISTS [tg_subscribe] (
            [chat_id] INT NOT NULL ON CONFLICT REPLACE UNIQUE);
            ''')
        cu.close()

    def load_chat_ids(self):
        self.chat_ids = set()
        cu = self.db.cursor()
        cu.execute(
            "SELECT chat_id FROM tg_subscribe;")
        rows = cu.fetchall()
        for chat_id, in rows:
            self.chat_ids.add(chat_id)
        cu.close()
        return self.chat_ids

    def subscribe(self, chat_id):
        logger.info('subscribe {0}'.format(chat_id))
        if chat_id not in self.chat_ids:
            self.chat_ids.add(chat_id)
            cu = self.db.cursor()
            cu.execute("REPLACE INTO tg_subscribe (chat_id) VALUES (?);", (chat_id, ))
            self.db.commit()
            cu.close()

    def unsubscribe(self, chat_id):
        logger.info('unsubscribe {0}'.format(chat_id))
        if chat_id in self.chat_ids:
            self.chat_ids.remove(chat_id)
            cu = self.db.cursor()
            cu.execute("DELETE FROM tg_subscribe WHERE chat_id = ?;", (chat_id, ))
            self.db.commit()
            cu.close()

    def set_web_hook(self, url):
        api_url = self.api_url + 'setWebhook'
        http_client = HTTPClient()
        request = HTTPRequest(
            url=api_url,
            method='POST',
            body=json.dumps({'url': url}),
            headers={
                'content-type': "application/json",
                'cache-control': "no-cache",
            },
        )
        try:
            response = http_client.fetch(request)
        except HTTPError as e:
            print (e.response.body)
            raise e
        else:
            print (response.body)

    @gen.coroutine
    def send_message(self, chat_id, text, reply_to_message_id=None):
        url = self.api_url + 'sendMessage'
        http_client = AsyncHTTPClient()
        body = {
            'chat_id': chat_id,
            'text': text
        }
        if reply_to_message_id:
            body['reply_to_message_id'] = reply_to_message_id
        request = HTTPRequest(
            url=url,
            method='POST',
            headers={
                'content-type': 'application/json'
            },
            body=json.dumps(body)
        )
        response = yield http_client.fetch(request)
        raise gen.Return(response)

    @gen.coroutine
    def on_receive_captcha(self, captcha):
        http_client = AsyncHTTPClient()
        url = self.api_url + 'sendPhoto'
        file_id = None
        for chat_id in self.chat_ids:
            logger.debug('on_receive_captcha: chat_id: {0}'.format(chat_id))
            if file_id is None:
                content_type, body = self.encode_multipart_formdata(
                    fields=[('chat_id', chat_id)],
                    files=[('photo', captcha['filename'], captcha['body'], captcha['content_type'])]
                )
            else:
                content_type = 'application/json'
                body = json.dumps({'chat_id': chat_id, 'photo': file_id})
            headers = {"Content-Type": content_type}
            request = HTTPRequest(url, "POST", headers=headers, body=body, validate_cert=False)
            request = HTTPRequest(url, "POST",)
            try:
                response = yield http_client.fetch(request)
            except HTTPError as e:
                logger.error(e.response.body)
                raise e
            logger.debug(response.body)
            logger.info('Captcha send successfully.')
            if file_id is None:
                result = json.loads(response.body.decode('utf-8'))['result']
                file_id = result['photo'][0]['file_id']
                logger.info('file_id: {0}'.format(file_id))

        future = Future()
        self.unfinshed_task[file_id] = future
        text = yield future
        raise gen.Return(text)

    def on_receive_result(self, file_id, text):
        if file_id in self.unfinshed_task:
            self.unfinshed_task[file_id].set_result(text)

    @classmethod
    def encode_multipart_formdata(cls, fields, files):
        """
        fields is a sequence of (name, value) elements for regular form fields.
        files is a sequence of (name, filename, value, content_type) elements for data to be
        uploaded as files.
        Return (content_type, body) ready for httplib.HTTP instance
        """
        boundary = '----------ThIs_Is_tHe_bouNdaRY_$'
        lines = []
        for (key, value) in fields:
            lines.append('--' + boundary)
            lines.append('Content-Disposition: form-data; name="%s"' % key)
            lines.append('')
            lines.append(str(value))
        for (key, filename, value, content_type) in files:
            filename = filename + mimetypes.guess_extension(content_type)
            lines.append('--' + boundary)
            lines.append(
                'Content-Disposition: form-data; name="%s"; filename="%s"' % (
                    key, filename
                )
            )
            lines.append('Content-Type: %s' % content_type)
            lines.append('')
            lines.append(value)
        lines.append('--' + boundary + '--')
        lines.append('')
        body = b'\r\n'.join(map(lambda x: x.encode('utf8') if isinstance(x, str) else x, lines))
        content_type = 'multipart/form-data; boundary=%s' % boundary
        return content_type, body
