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


class AppListHandler(BaseHandler):

    def get(self):
        apps = ctrl.api.get_app_list_ctl()
        self.send_json({
            'apps': apps
        })

    def post(self):
        try:
            name_cn = self.get_argument('name_cn')
            name_en = self.get_argument('name_en')
        except Exception as e:
            logging.error(e)
            raise utils.APIError(errcode=10001)

        ctrl.api.add_model("App", {
            'name_cn': name_cn,
            'name_en': name_en
        })
        ctrl.rs.delete(ctrl.api.get_app_list_key_ctl())
        self.send_json()


class PostListHandler(BaseHandler):

    def get(self):
        try:
            page = int(self.get_argument('page', 1))
            page_size = int(self.get_argument('page_size', 20))
        except Exception as e:
            logging.error(e)
            raise utils.APIError(errcode=10001)

        posts = ctrl.api.get_post_list_ctl(page, page_size)
        self.send_json({
            'posts': posts
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

        self.send_json(dict(upyun=upyun_data, CDN_HOST=UPYUN['cdn']))
