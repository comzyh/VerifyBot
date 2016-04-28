#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TelegramBot."""
import json
import sys

from tornado.httpclient import HTTPClient
from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPRequest

class TelegramBot(object):
    """docstring for TelegramBot"""

    def __init__(self, bot_token=None):
        if not bot_token:
            self.token = sys.argv[1]
        else:
            self.token = bot_token
        self.api_url = 'https://api.telegram.org/bot{token}/'.format(self.token)

    def set_web_hook(self, url):
        api_url = self.api + 'setWebhook'
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

    def on_receive_picture(self):
        pass

    def on_receive_result(self):
        pass
