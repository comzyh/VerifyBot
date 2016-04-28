#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TelegramBot."""
import json
import sys

from tornado.httpclient import HTTPClient
from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPRequest
from tornado.httpclient import HTTPError


class _Singleton(type):
    """ A metaclass that creates a Singleton base class when called. """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Singleton(_Singleton('SingletonMeta', (object,), {})):
    pass


class TelegramBot(Singleton):
    """docstring for TelegramBot"""

    def __init__(self, bot_token=None):
        if not bot_token:
            self.token = sys.argv[1]
        else:
            self.token = bot_token
        self.api_url = 'https://api.telegram.org/bot{token}/'.format(token=self.token)

    def get_chat_ids(self):
        return [sys.argv[2]]

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
        response = http_client.fetch(request)
        print (response.body)

    def on_receive_captcha(self, captcha):
        http_client = HTTPClient()
        url = self.api_url + 'sendPhoto'
        for chat_id in self.get_chat_ids():
            content_type, body = self.encode_multipart_formdata(
                fields=[('chat_id', chat_id)],
                files=[('photo', captcha['filename'], captcha['body'], captcha['content_type'])]
            )
        headers = {"Content-Type": content_type, 'content-length': str(len(body))}
        request = HTTPRequest(url, "POST", headers=headers, body=body, validate_cert=False)
        try:
            response = http_client.fetch(request)
        except HTTPError as e:
            print (e.response.body)
            raise e
        else:
            pass
        print (response.body)

    def on_receive_result(self):
        pass

    @classmethod
    def encode_multipart_formdata(cls, fields, files):
        """
        fields is a sequence of (name, value) elements for regular form fields.
        files is a sequence of (name, filename, value, content_type) elements for data to be
        uploaded as files.
        Return (content_type, body) ready for httplib.HTTP instance
        """
        BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
        CRLF = b'\r\n'
        L = []
        for (key, value) in fields:
            L.append('--' + BOUNDARY)
            L.append('Content-Disposition: form-data; name="%s"' % key)
            L.append('')
            L.append(value)
        for (key, filename, value, content_type) in files:
            filename = filename
            L.append('--' + BOUNDARY)
            L.append(
                'Content-Disposition: form-data; name="%s"; filename="%s"' % (
                    key, filename
                )
            )
            L.append('Content-Type: %s' % content_type)
            L.append('')
            L.append(value)
        L.append('--' + BOUNDARY + '--')
        L.append('')
        body = CRLF.join(map(lambda x: x.encode('utf8') if isinstance(x, str) else x, L))
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
        return content_type, body

