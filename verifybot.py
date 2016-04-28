#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Main."""


def make_app():
    """make_app."""
    from service.server import MainHandler
    import tornado.web
    return tornado.web.Application([
        (r"/", MainHandler),
    ])


if __name__ == "__main__":
    import tornado.ioloop
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
