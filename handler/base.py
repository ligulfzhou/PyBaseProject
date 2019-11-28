
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
import logging
import hashlib
import traceback
import datetime

from decimal import Decimal
from tornado import web, gen
from tornado.options import options
from control import ctrl
from settings import ERR
from lib import utils
from urllib.parse import quote


class BaseHandler(web.RequestHandler):

    def initialize(self):
        ctrl.pdb.close()

    def on_finish(self):
        ctrl.pdb.close()

    def set_default_headers(self):
        origin = self.request.headers.get("Origin")
        origin = '*' if not origin else origin
        self.set_header("Access-Control-Allow-Origin", origin)
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
        self.set_header('Access-Control-Allow-Methods', 'OPTIONS, GET, POST, PUT, DELETE')

    def json_format(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        if isinstance(obj, Decimal):
            return ('%.2f' % obj)
        if isinstance(obj, None):
            return ''

    def has_argument(self, name):
        return name in self.request.arguments

    def send_json(self, data={}, errcode=200, errmsg='', status_code=200):
        res = {
            'errcode': errcode,
            'errmsg': errmsg if errmsg else ERR[errcode]
        }
        res.update(data)

        if errcode > 200:
            logging.error(res)

        json_str = json.dumps(res, default=self.json_format)

        if options.debug and not self.request.path.startswith('/utils/upload'):
            logging.info('method: %s, path: %s' % (self.request.method, self.request.path))
            logging.info('arguments %s' % self.request.arguments)
            logging.info('body: %s' % self.request.body)
            logging.info('response: %s' % json_str)
            logging.info('current_user: %s' % self.current_user)

        self.set_header('Content-Type', 'application/json')

        self.set_status(status_code)
        self.write(json_str)
        self.finish()

    def dict_args(self):
        _rq_args = self.request.arguments
        rq_args = dict([(k, _rq_args[k][0]) for k in _rq_args])
        return rq_args

    def write_error(self, status_code=200, **kwargs):
        if 'exc_info' in kwargs:
            err_object = kwargs['exc_info'][1]
            traceback.format_exception(*kwargs['exc_info'])

            if isinstance(err_object, utils.APIError):
                err_info = err_object.kwargs
                self.send_json(**err_info)
                return

        # self.captureException(**kwargs)
        self.send_json(status_code=500, errcode=50001)

    def get_current_user(self):
        test = int(self.get_argument('test', None) or 0)
        if test:
            user = {
                'user_id': int(self.get_argument('user_id', 1)),
                'login': 1
            }
            return user
        try:
            user = {
                'user_id': int(self.get_secure_cookie('user_id')),
                'login': int(self.get_secure_cookie('login')),
            }
        except:
            if options.debug:
                user = {
                    'user_id': 1,
                    'login': 1,
                }
            else:
                raise utils.APIError(errcode=40001)

        return user

    def _login(self, user):
        self.set_secure_cookie('login', str(1))
        self.set_secure_cookie('user_id', str(user.get('id', 0)))

    def options(self):
        self.set_status(204)
        self.finish()
