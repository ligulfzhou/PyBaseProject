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

        # not implemented
        code = await ctrl.api.send_verify_code_ctl(phone_num)
        self.send_json()


class LoginHandler(BaseHandler):

    def post(self):
        self.send_json()


class LogoutHandler(BaseHandler):

    @login_required
    def post(self):
        self.send_json()
