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

from lib.const import NotifyType, ALL_NOTIFY_TYPES, UserXXXX, ALL_USER_XXXX_TYPES


class ApiCtrl(object):

    def __init__(self, ctrl):
        self.ctrl = ctrl
        self.api = ctrl.pdb.api

    def __getattr__(self, name):
        return getattr(self.api, name)

    def get_all_tpl_key(self):
        # list of tpl_id
        return 'all_tpls'

    def get_tpl_key(self, tpl_id):
        return 'tpl_%s' % tpl_id

    def get_all_tpls(self):
        key = self.get_all_tpl_key_ctl()
        v = self.ctrl.rs.lrange(key, 0, -1)
        if v:
            v = [int(i) for i in v]
            return self.get_multi_tpls_ctl(v)

        tpls = self.api.get_models('Tpl')
        if tpls:
            self.put_multi_tpls_to_redis_ctl(tpls)
        return tpls

    def refactor_page(self, page, page_size=20):
        mpage = page // 5 + 1
        ipage = page % 5
        offset, limit = (ipage - 1) * page_size, page_size
        return mpage, ipage, offset, limit

    # put multi items to redis
    def _put_multi_items_to_redis(self, get_item_key_func, items=[]):
        if not items:
            return

        k_v_dict = {get_item_key_func(item['id']): pickle.dumps(item) for item in items}
        pl = self.ctrl.rs.pipeline(transaction=True)
        pl.mset(k_v_dict)
        for k in k_v_dict:
            pl.expire(k, A_DAY)
        pl.execute()

    def put_multi_tpls_to_redis(self, tpls):
        return self._put_multi_items_to_redis_ctl(self.get_tpl_key_ctl, tpls)

    # merge more fields to items
    def tpl_merge_more_fields(self, tpls):
        return tpls

    # get multi items
    def get_multi_tpls(self, tpl_ids):
        tpls = self._get_multi_items_ctl('Tpl', tpl_ids, self.get_tpl_key_ctl, self.tpl_merge_more_fields_ctl, self.put_multi_tpls_to_redis_ctl)
        return tpls

    def _get_multi_items(self, tb_name, ids, get_item_key_func, merge_item_func, put_items_to_rs):
        if not ids:
            return []

        multi_key = [get_item_key_func(i) for i in ids]
        cached = [pickle.loads(item) if item else None for item in self.ctrl.rs.mget(multi_key)]
        multi_items = dict(zip(multi_key, cached))
        miss_ids = [i for i in ids if not multi_items[get_item_key_func(i)]]
        if not miss_ids:
            return [multi_items[get_item_key_func(i)] for i in ids]

        miss_items = self.api.get_models(tb_name, {'id': miss_ids})
        miss_items = merge_item_func(miss_items)
        miss_ids = [i['id'] for i in miss_items]

        miss_multi_key = [get_item_key_func(i) for i in miss_ids]
        miss_items = dict(zip(miss_multi_key, miss_items))

        if miss_items:
            put_items_to_rs(list(miss_items.values()))

        multi_items.update(miss_items)
        return [multi_items[get_item_key_func(i)] for i in ids if get_item_key_func(i) in multi_items]

    def _rpush_multi_ids_to_key(self, key, ids):
        pl = self.ctrl.rs.pipeline(transaction=True)
        pl.delete(key)
        pl.rpush(key, *ids)
        pl.expire(key, A_DAY)
        pl.execute()

    def get_posts_of_cate(self, cate_id, page=1, page_size=20):
        mpage, ipage, offset, limit = self.refactor_page_ctl(page, page_size)
        key = self.get_posts_of_cate_key_ctl(cate_id, mpage)
        v = self.ctrl.rs.lrange(key, offset, offset+limit-1)
        if v:
            post_ids = [int(i) for i in v]
            return self.get_multi_posts_ctl(post_ids)

        posts = self.api.get_posts_of_cate(cate_id, mpage)
        if posts:
            post_ids = [i['id'] for i in posts]
            posts = self.post_merge_more_fields_ctl(posts)
            posts = self.get_posts_comments_counts_ctl(posts)
            posts = self.get_posts_likes_counts_ctl(posts)
            self.put_multi_posts_to_redis_ctl(posts)

            self._rpush_multi_ids_to_key_ctl(key, post_ids)
            return posts[offset: offset+limit]
        return []

