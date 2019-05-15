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


class CompanyListHandler(BaseHandler):

    def get(self):
        try:
            tp = int(self.get_argument('tp', None) or 0)
            page = int(self.get_argument('page', 1))
            page_size = int(self.get_argument('page_size', 20))
        except Exception as e:
            logging.error(e)
            raise utils.APIError(errcode=10001)

        companies = ctrl.api.get_company_list_ctl(tp, page, page_size)
        self.send_json({
            'companies': companies
        })


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
