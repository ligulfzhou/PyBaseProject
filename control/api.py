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

    def get_post_list_key(self, page):
        return 'post_p%s' % page

    def get_app_list_key(self):
        return 'all_apps'

    def get_app_list(self):
        key = self.get_app_list_key_ctl()
        ids = self.ctrl.rs.lrange(key, 0, -1)
        if ids:
            ids = [int(i) for i in ids]
            return self.ctrl.base._get_multi_items_ctl('App', ids)

        apps = self.api.get_models('App', [])
        if apps:
            self.ctrl.base._put_multi_items_to_redis_ctl('App', apps)
            cids = [c['id'] for c in apps]
            self.ctrl.base._rpush_multi_ids_to_key_ctl(key, cids)
        return apps

    def get_post_list(self, page=1, page_size=20):
        key = self.get_post_list_key_ctl(page)
        ids = self.ctrl.rs.lrange(key, 0, -1)
        if ids:
            ids = [int(i) for i in ids]
            return self.ctrl.base._get_multi_items_ctl('Post', ids)

        posts = self.api.get_models('Post', [], page=page, page_size=page_size)
        posts = self.ctrl.base.post_merge_more_fields_ctl(posts)
        if posts:
            self.ctrl.base._put_multi_items_to_redis_ctl('Post', posts)
            pids = [c['id'] for p in posts]
            self.ctrl.base._rpush_multi_ids_to_key_ctl(key, pids)
        return posts

