from settings import DB_OA
from typing import Dict, List, Optional
from sqlalchemy.ext.declarative import declarative_base
from lib.decorator import model_to_dict, models_to_list
from sqlalchemy import Column, extract, distinct
from sqlalchemy.sql.expression import func, desc, asc, or_
from sqlalchemy.dialects.postgresql import TEXT, BIGINT, INTEGER

Base = declarative_base()


class App(Base):
    __tablename__ = 'app'

    id = Column(INTEGER, primary_key=True)
    icon = Column(TEXT)
    name_cn = Column(TEXT)
    name_en = Column(TEXT)
    des_cn = Column(TEXT)
    des_en = Column(TEXT)
    appleid = Column(INTEGER)
    status = Column(INTEGER)
    url_scheme = Column(TEXT)


class User(Base):
    __tablename__ = 'user'

    id = Column(INTEGER, primary_key=True)
    uuid = Column(TEXT)
    github_id = Column(INTEGER)
    username = Column(TEXT)
    gender = Column(INTEGER)
    city = Column(TEXT)
    province = Column(TEXT)
    country = Column(TEXT)
    avatarurl = Column(TEXT)
    unionid = Column(TEXT)
    device_token = Column(TEXT)
    title = Column(TEXT)


class Post(Base):
    __tablename__ = 'post'

    id = Column(INTEGER, primary_key=True)
    user_id = Column(INTEGER)
    company_id = Column(INTEGER)
    title = Column(TEXT)
    content = Column(TEXT)


class Company(Base):
    __tablename__ = 'company'

    id = Column(INTEGER, primary_key=True)
    name = Column(TEXT)
    url = Column(TEXT)
    city = Column(TEXT)
    country = Column(TEXT)
    dt = Column(TEXT)
    tt = Column(TEXT)
    tp = Column(INTEGER)


class APIModel(object):

    def __init__(self, pdb):
        self.pdb = pdb
        self.master = pdb.get_session(DB_OA, master=True)
        self.slave = pdb.get_session(DB_OA)

    @model_to_dict
    def add_model(self, model, kv: Dict):
        c = eval(model)
        m = c(**kv)
        self.master.add(m)
        self.master.commit()
        return m

    @models_to_list
    def add_models(self, model, kv_list: List[Dict]):
        c = eval(model)
        models = [c(**kv) for kv in kv_list]
        # [self.master.add(m) for m in models]
        self.master.bulk_add_objects(models)
        self.master.commit()
        return models

    @model_to_dict
    def get_model(self, model, filters: List[Dict]) -> Optional[Dict]:
        '''
        filters = [{'name':xxx}, {'sex': 1}]
        '''
        c = eval(model)
        q = self.slave.query(c)
        for kv in filters:
            k, v = list(kv.items())[0]
            if isinstance(v, list):
                q = q.filter(getattr(c, k).in_(tuple(v)))
            else:
                q = q.filter(getattr(c, k) == v)
        return q.scalar()

    def get_model_count(self, model, filters: Optional[Dict]) -> int:
        c = eval(model)
        q = self.slave.query(c)
        for kv in filters:
            k, v = list(kv.items())[0]
            if isinstance(v, list):
                q = q.filter(getattr(c, k).in_(tuple(v)))
            else:
                q = q.filter(getattr(c, k) == v)
        v = q.count()
        if v:
            return int(v)
        return 0

    @models_to_list
    def get_models(self, model: str, filters: List[Dict], offset: int = 0, limit: int = 0, page: int = 0,
                   page_size: int = 100, order_by: str = '') -> List[Dict]:
        c = eval(model)
        q = self.slave.query(c)
        for kv in filters:
            k, v = list(kv.items())[0]
            if isinstance(v, list):
                q = q.filter(getattr(c, k).in_(tuple(v)))
            else:
                q = q.filter(getattr(c, k) == v)

        if order_by:
            q = q.order_by(getattr(c, order_by).desc())
        else:
            q = q.order_by(c.id.desc())

        if not (offset or limit) and not page:
            pass
        else:
            if not offset and not limit:
                # 有offset和limit就用这两个数据
                offset = (page - 1) * page_size
                limit = page_size
            q = q.offset(offset).limit(limit)

        return q.all()

    def update_model(self, model, pk, data: Dict) -> None:
        c = eval(model)
        self.master.query(c).filter_by(id=pk).update(data)
        self.master.commit()

    def delete_modal(self, model, filters: List[Dict]) -> None:
        c = eval(model)
        q = self.master.query(c)
        for kv in filters:
            k, v = list(kv.items())[0]
            if isinstance(v, list):
                q = q.filter(getattr(c, k).in_(v))
            else:
                q = q.filter(getattr(c, k) == v)
        q = q.delete(synchronize_session=False)
        self.master.commit()
