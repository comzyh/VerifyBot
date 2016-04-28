#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import os
from service.singleton import Singleton


class Config(Singleton):

    def __init__(self):
        parser = self.__get_praser()
        self.args = parser.parse_args()
        self.port = self.args.port
        self.token = self.args.token
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_filename = os.path.join(self.base_dir, 'verify_bot.db')
        self.url_prefix = self.args.url_prefix
        if not self.__check_args():
            parser.print_help()
            sys.exit(1)

    def __get_praser(self):
        parser = argparse.ArgumentParser(description='VerifyBot')
        parser.add_argument('-t', '--token', help='Telegram Bot token.')
        parser.add_argument('-p', '--port', help='Port to listen.')
        parser.add_argument('-d', '--demon', help='Run as demon.', action='store_true')
        parser.add_argument('--url-prefix', help='Working url prefix. e.g. "/verifybot"', default='')
        parser.add_argument('--set-web-hook', help='Set web hook.', action='store_true')
        parser.add_argument('--hostname', help='WebHook hostname.')
        parser.add_argument('-v', '--verbose', action='store_true', dest='verbose',
                            help='Enable debug info')

        return parser

    def __check_args(self):
        if len(sys.argv) == 1:
            return False
        if self.args.demon:
            if not self.args.port or not self.args.token:
                return False
        if self.args.set_web_hook:
            if not self.args.token or not self.args.hostname:
                return False
        return True
