#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TelegramBot."""
import json
import sys
import mimetypes

from tornado.httpclient import HTTPClient
from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPRequest
from tornado.httpclient import HTTPError

from service.singleton import Singleton
from service.config import Config


class TelegramBot(Singleton):
    """docstring for TelegramBot"""

    def __init__(self):
        config = Config()
        self.token = config.token
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
        boundary = '----------ThIs_Is_tHe_bouNdaRY_$'
        lines = []
        for (key, value) in fields:
            lines.append('--' + boundary)
            lines.append('Content-Disposition: form-data; name="%s"' % key)
            lines.append('')
            lines.append(value)
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
