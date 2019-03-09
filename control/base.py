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
from functools import partial


class BaseCtrl(object):

    def __init__(self, ctrl):
        self.ctrl = ctrl
        self.api = ctrl.pdb.api

    def __getattr__(self, name):
        return getattr(self.api, name)

    def get_model_key(self, model, model_id):
        return '%s_%s' % (model.lower(), model_id)

    def get_all_model_key(self, model):
        return 'all_%ss' % model.lower()

    def _put_ids_to_key(self, key, ids):
        if not ids:
            return

        pl = self.ctrl.rs.pipeline(transaction=True)
        pl.delete(key)
        pl.rpush(key, *ids)
        pl.execute()

    def refactor_page(self, page, page_size=20):
        mpage = page // 5 + 1
        ipage = page % 5
        offset, limit = (ipage - 1) * page_size, page_size
        return mpage, ipage, offset, limit

    # put multi items to redis
    def _put_multi_items_to_redis(self, tb_name, items=[], get_item_key_func=None):
        if not items:
            return

        if not get_item_key_func:
            get_item_key_func = partial(self.get_model_key_ctl, model=tb_name)

        k_v_dict = {get_item_key_func(model_id=item['id']): pickle.dumps(item) for item in items}
        pl = self.ctrl.rs.pipeline(transaction=True)
        pl.mset(k_v_dict)
        for k in k_v_dict:
            pl.expire(k, A_DAY)
        pl.execute()

    # 🌰 merge more fields to items
    def tpl_merge_more_fields(self, tpls):
        [tpl.update({
            'sentences': tpl.get('sentences', '').split(';')
        }) for tpl in tpls if isinstance(tpl.get('sentences', ''), str)]
        return tpls

    def effi_merge_more_fields(self, effis):
        if not effis:
            return
        effi_ids = [i['id'] for i in effis]
        id_hot_dict = self.ctrl.api.get_effi_hot_cnts_ctl(effi_ids)
        print("===============returned id_hot_dict================")
        print(id_hot_dict)
        [effi.update({
            'hot': id_hot_dict.get(effi['id'], 0)
        }) for effi in effis]
        return effis

    def _get_multi_items(self, tb_name, ids, get_item_key_func=None, merge_item_func=None, put_items_to_rs=None):
        if not ids:
            return []

        if not get_item_key_func:
            get_item_key_func = partial(self.get_model_key_ctl, model=tb_name.lower())
        if not merge_item_func:
            if hasattr(self, '%s_merge_more_fields_ctl' % tb_name.lower()):
                merge_item_func = getattr(self, '%s_merge_more_fields_ctl' % tb_name.lower())
        if not put_items_to_rs:
            put_items_to_rs = partial(self._put_multi_items_to_redis_ctl, tb_name=tb_name.lower())

        multi_key = [get_item_key_func(model_id=i) for i in ids]
        cached = [pickle.loads(item) if item else None for item in self.ctrl.rs.mget(multi_key)]
        multi_items = dict(zip(multi_key, cached))
        miss_ids = [i for i in ids if not multi_items[get_item_key_func(model_id=i)]]
        # if not miss_ids:
        #     return [multi_items[get_item_key_func(model_id=i)] for i in ids]
        if miss_ids:
            miss_items = self.api.get_models(tb_name.capitalize(), [{'id': miss_ids}])
            miss_ids = [i['id'] for i in miss_items]

            miss_multi_key = [get_item_key_func(model_id=i) for i in miss_ids]
            miss_items = dict(zip(miss_multi_key, miss_items))

            if miss_items and put_items_to_rs:
                put_items_to_rs(items=list(miss_items.values()))

            multi_items.update(miss_items)

        items = [multi_items[get_item_key_func(model_id=i)] for i in ids if get_item_key_func(model_id=i) in multi_items]
        if merge_item_func:
            items = merge_item_func(items)
        return items

    def _rpush_multi_ids_to_key(self, key, ids):
        pl = self.ctrl.rs.pipeline(transaction=True)
        pl.delete(key)
        pl.rpush(key, *ids)
        pl.expire(key, A_DAY)
        pl.execute()

    def update_model(self, tb_name, pk, data):
        self.api.update_model(tb_name, pk, data)
        key = self.get_model_key_ctl(tb_name, pk)
        self.ctrl.rs.delete(key)

