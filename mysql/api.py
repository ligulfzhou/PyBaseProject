from settings import DB_OA
from typing import Dict, List, Optional
from mysql.base import NotNullColumn, Base
from lib.decorator import model_to_dict, models_to_list, filter_update_data
from sqlalchemy import Column, extract, distinct
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, ENUM, TINYINT, DATE, DATETIME, DECIMAL, TIMESTAMP, TEXT, BLOB
from sqlalchemy.sql.expression import func, desc, asc, or_


class App(Base):
    __tablename__ = 'app'

    id = Column(INTEGER(11), primary_key=True)
    icon = NotNullColumn(VARCHAR(1024))
    name_cn = NotNullColumn(VARCHAR(128))
    name_en = NotNullColumn(VARCHAR(128))
    des_cn = NotNullColumn(VARCHAR(1024))
    des_en = NotNullColumn(VARCHAR(1024))
    appleid = NotNullColumn(INTEGER(11))
    status = NotNullColumn(TINYINT(1))
    url_scheme = NotNullColumn(VARCHAR(32))


class User(Base):
    __tablename__ = 'user'

    id = Column(INTEGER(11), primary_key=True)
    uuid = NotNullColumn(VARCHAR(32))
    github_id = NotNullColumn(INTEGER(11))
    username = NotNullColumn(VARCHAR(64))
    gender = NotNullColumn(TINYINT(1))
    city = NotNullColumn(VARCHAR(256))
    province = NotNullColumn(VARCHAR(256))
    country = NotNullColumn(VARCHAR(256))
    avatarurl = NotNullColumn(VARCHAR(1024))
    unionid = NotNullColumn(VARCHAR(64))
    device_token = NotNullColumn(VARCHAR(64))
    title = NotNullColumn(VARCHAR(1024))


class Post(Base):
    __tablename__ = 'post'

    id = Column(INTEGER(11), primary_key=True)
    user_id = NotNullColumn(INTEGER(11))
    company_id = NotNullColumn(INTEGER(11))
    title = NotNullColumn(VARCHAR(1024))
    content = NotNullColumn(TEXT)


class Company(Base):
    __tablename__ = 'company'

    id = Column(INTEGER(11), primary_key=True)
    name = NotNullColumn(VARCHAR(64))
    url = NotNullColumn(VARCHAR(1024))
    city = NotNullColumn(VARCHAR(64))
    country = NotNullColumn(VARCHAR(64))
    dt = NotNullColumn(VARCHAR(32))
    tt = NotNullColumn(VARCHAR(1024))
    tp = NotNullColumn(TINYINT(1))


class Ref(Base):
    __tablename__ = 'ref'

    id = Column(INTEGER(11), primary_key=True)
    company_id = NotNullColumn(INTEGER(11))
    title = NotNullColumn(VARCHAR(1024))
    url = NotNullColumn(VARCHAR(1024))


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
