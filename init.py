import app
import tornado.ioloop
from tornado.options import define, options

define('port', default=8000, help='run on this port', type=int)
define('debug', default=True, help='enable debug mode')

options.parse_command_line()


def runserver():
    app.run()
    loop = tornado.ioloop.IOLoop.instance()
    loop.start()


if __name__ == '__main__':
    runserver()
