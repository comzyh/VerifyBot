#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MainHandler."""
import sys
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    """Handler."""

    def get(self):
        """get."""
        self.write('VerifyBot.')

    def post(self):
        """set."""
        pass
