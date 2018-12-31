#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pdb
import time
import json
import random
import logging
import datetime
import hashlib
import random

from lib import utils, upyun
from control import ctrl
from settings import UPYUN
from tornado.options import options
from handler.base import BaseHandler
from lib.decorator import login_required
from lib.const import NotifyType, ALL_NOTIFY_TYPES, str_to_notify_type, UserXXXX, str_to_user_xxxx_type


class TplsHandler(BaseHandler):

    def get(self):
        '''
        /api/tpl
        获取所有模版
        '''
        tpls = ctrl.api.get_tpls_ctl()
        self.send_json({
            'tpls': tpls
        })


class UpyunHandler(BaseHandler):

    @login_required
    def get(self):
        upyun_data = upyun.form_signature_policy({
            'save-key': '{filemd5}{.suffix}',
            'bucket': 'madan-image',
            'content-length-range': '1, 1073741824'
        })

        # origin = self.request.headers.get("Origin")
        # origin = '*' if not origin else origin
        # self.set_header("Access-Control-Allow-Origin", origin)
        # self.set_header("Access-Control-Allow-Credentials", "true")
        # self.set_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
        # self.set_header('Access-Control-Allow-Methods', 'OPTIONS, GET, POST, PUT, DELETE')
        self.send_json(dict(upyun=upyun_data, CDN_HOST=UPYUN['cdn']))
