#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pdb
import json
import random
import pickle
import datetime
import logging
import hashlib
from copy import deepcopy
from decimal import Decimal
from tornado import gen
from lib import utils
from settings import A_DAY
from tornado.gen import coroutine
from tornado.options import options
from tornado import httputil


class ApiCtrl(object):

    def __init__(self, ctrl):
        self.ctrl = ctrl
        self.api = ctrl.pdb.api

    def __getattr__(self, name):
        return getattr(self.api, name)

