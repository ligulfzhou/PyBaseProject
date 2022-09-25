import os
import sys
from tornado import web
from tornado.options import options
from tornado.httpserver import HTTPServer

URLS = [
    (r'sudo\.madan\.tech',
     (r'/api/tpls', 'handler.api.TplsHandler'),
     (r'/api/apps', 'handler.api.AppListHandler'),
     (r'/api/posts', 'handler.api.PostListHandler'),

     # (r'/api/upyun', 'handler.api.UpyunHandler'),
     )
]


class Application(web.Application):

    def __init__(self):
        settings = {
            'compress_response': True,
            'xsrf_cookies': False,
            'debug': options.debug,
            'static_path': os.path.join(sys.path[0], 'static'),
            'cookie_secret': 'lkjsadlfkjasdlkfjau3po2iup32knsdkfajsdfasdklfasdf\asdfadsf',
        }
        web.Application.__init__(self, **settings)

        for spec in URLS:
            host = '.*$'
            handlers = spec[1:]
            self.add_handlers(host, handlers)


def run():
    application = Application()
    http_server = HTTPServer(application, xheaders=True)
    http_server.listen(options.port)
    print('Running on port %d' % options.port)
