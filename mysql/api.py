#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pdb
import datetime
from sqlalchemy import Column, extract, distinct
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, ENUM, TINYINT, DATE, DATETIME, DECIMAL, TIMESTAMP, TEXT, BLOB
from sqlalchemy.sql.expression import func, desc, asc, or_

from settings import DB_OA
from mysql.base import NotNullColumn, Base
from lib.decorator import model_to_dict, models_to_list, filter_update_data


# class Tpl(Base):
#     __tablename__ = 'tpl'
# 
#     id = Column(INTEGER(11), primary_key=True)
#     name = NotNullColumn(VARCHAR(64))


class APIModel(object):

    def __init__(self, pdb):
        self.pdb = pdb
        self.master = pdb.get_session(DB_OA, master=True)
        self.slave = pdb.get_session(DB_OA)

    @model_to_dict
    def add_model(self, model, kv={}):
        c = eval(model)
        m = c(**kv)
        self.master.add(m)
        self.master.commit()
        return m

    @model_to_dict
    def get_model(self, model, filters={}):
        c = eval(model)
        q = self.slave.query(c)
        for kv in filters:
            k, v = list(kv.items())[0]
            if isinstance(v, list):
                q = q.filter(getattr(c, k).in_(tuple(v)))
            else:
                q = q.filter(getattr(c, k)==v)
        return q.scalar()

    def get_model_count(self, model, filters=[]):
        c = eval(model)
        q = self.slave.query(c)
        for kv in filters:
            k, v = list(kv.items())[0]
            if isinstance(v, list):
                q = q.filter(getattr(c, k).in_(tuple(v)))
            else:
                q = q.filter(getattr(c, k)==v)
        v = q.count()
        if v:
            return int(v)
        return 0

    @models_to_list
    def get_models(self, model, filters=[], offset=0, limit=0, page=0, page_size=100, order_by=''):
        c = eval(model)
        q = self.slave.query(c)
        for kv in filters:
            k, v = list(kv.items())[0]
            if isinstance(v, list):
                q = q.filter(getattr(c, k).in_(tuple(v)))
            else:
                q = q.filter(getattr(c, k)==v)

        if not (offset or limit) and not page:
            pass
        else:
            if not offset and not limit:
                # 有offset和limit就用这两个数据
                offset = (page - 1) * page_size
                limit = page_size
            q = q.offset(offset).limit(limit)

        if order_by:
            q = q.order_by(getattr(c, order_by).desc())
        else:
            q = q.order_by(c.create_time.desc())

        return q.all()

    def update_model(self, model, pk, data={}):
        c = eval(model)
        self.master.query(c).filter_by(id=pk).update(data)
        self.master.commit()

    def delete_modal(self, model, filters=[]):
        c = eval(model)
        q = self.master.query(c)
        for kv in filters:
            k, v = list(kv.items())[0]
            if isinstance(v, list):
                q = q.filter(getattr(c, k).in_(v))
            else:
                q = q.filter(getattr(c, k)==v)
        q = q.delete(synchronize_session=False)
        self.master.commit()

