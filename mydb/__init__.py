import random
import logging
from settings import MY_DB
from mydb.api import APIModel
from tornado.options import options
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


def create_session(engine):
    if not engine:
        return None

    session = scoped_session(sessionmaker(bind=engine))
    return session()


class Database(object):

    def __init__(self):
        self.session = {
            'm': {},
            's': {}
        }
        self.kwargs = {
            'pool_recycle': 3600,
            'echo': options.debug,
            'echo_pool': options.debug
        }

        self.init_session()
        self.api = APIModel(self)

    def _session(self, db_str, master=True):
        engine = create_engine(db_str, **self.kwargs)
        session = create_session(engine)
        print('%s: %s' % ('master' if master else 'slave', db_str))
        return session

    def init_session(self):
        for db, value in MY_DB.items():
            self.session['s'][db] = []

            master = value.get('master')
            session = self._session(master)
            self.session['m'][db] = session
            slaves = value.get('slaves')

            for slave in slaves:
                session = self._session(slave, master=False)
                self.session['s'][db].append(session)

    def get_session(self, db, master=False):
        if not master:
            sessions = self.session['s'][db]
            if len(sessions) > 0:
                session = random.choice(sessions)
                return session
        session = self.session['m'][db]
        return session

    @classmethod
    def instance(cls):
        name = 'singleton'
        if not hasattr(cls, name):
            setattr(cls, name, cls())
        return getattr(cls, name)

    def close(self):
        def shut(ins):
            try:
                ins.commit()
            except:
                logging.error('DB server has gone away. ignore.')
            finally:
                ins.close()

        for db in MY_DB:
            shut(self.session['m'][db])
            for session in self.session['s'][db]:
                shut(session)

# global, called by control
pdb = Database.instance()
