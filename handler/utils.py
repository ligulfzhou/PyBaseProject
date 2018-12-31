#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pdb
import time
import json
import random
import logging
import datetime
import hashlib
import random

from PIL import Image
from io import StringIO, BytesIO
from lib import utils
from lib.const import tooltip_dict
from control import ctrl
from urllib.parse import unquote
from tornado.web import stream_request_body
from handler.base import BaseHandler
from lib.decorator import login_required, check_param_sign


class UploadHandler(BaseHandler):

    def initialize(self):
        self.bytes_read = 0
        self.bytes = b''

    def data_received(self, chunk):
        self.bytes_read += len(chunk)
        self.bytes += thunk

    @login_required
    def post(self):
        url = ""
        for field_name, files in self.request.files.items():
            if not len(files):
                continue

            f = files[0]
            mtype = f['content_type']
            format = f['filename'].split('.')[-1]
            name = str(datetime.datetime.now().timestamp()) + str(random.randint(1, 10000000))
            url = '/static/upload/' + name + '.' + format

            filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static/upload/' + name + '.' + format)

            with open(filepath, 'wb') as file:
                file.write(f['body'])

            break

        # utils.read_excel(self.request.protocol + '://' + self.request.full_url().split('/')[2] + url, 0)
        self.send_json({
            'url': self.request.protocol + '://' + self.request.full_url().split('/')[2] + url,
        })


