#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests


def main():
    url = raw_input('Please enter your VerifyBot url:\n')
    s = requests.session()
    while True:
        resp = s.get('https://www.zhihu.com/captcha.gif')
        print('Got a captcha.')
        resp = s.post(url, files={
            'captcha': ('captcha.gif', resp.content, 'image/gif')
        })
        print('code is: "{code}"'.format(code=resp.text))

if __name__ == '__main__':
    main()
