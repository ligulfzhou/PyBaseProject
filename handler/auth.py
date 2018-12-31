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

from lib import utils
from control import ctrl
from handler.base import BaseHandler
from lib.decorator import login_required, permission_required, check_param_sign


class VerifyCodeHandler(BaseHandler):

    @login_required
    async def get(self):
        try:
            phone_num = self.get_argument('phone_num')
        except Exception as e:
            logging.error(e)
            raise utils.APIError(errcode=10001)

        code = await ctrl.api.send_verify_code_ctl(phone_num)
        self.send_json()


class LoginHandler(BaseHandler):

    async def post(self):
        try:
            phone_num = self.get_argument('phone_num')
            code = self.get_argument('code')

        except Exception as e:
            logging.error(e)
            raise utils.APIError(errcode=10001)

        if not ctrl.api.check_verify_code_ctl(phone_num, code):
            raise utils.APIError(10002)

        user = ctrl.api.get_user_ctl(phone_num=phone_num)
        if not user:
            user = ctrl.api.add_model('User', {
                'phone_num': phone_num
            })

        self._login(user)
        self.send_json({
            'user': user
        })


class LogoutHandler(BaseHandler):

    @login_required
    def post(self):
        self.clear_all_cookies()
        self.send_json()
