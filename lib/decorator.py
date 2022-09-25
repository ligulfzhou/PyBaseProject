import pdb
import hashlib
from lib import utils
from tornado.options import options
from sqlalchemy.orm import class_mapper

def model2dict(model):
    if not model:
        return {}
    fields = class_mapper(model.__class__).columns.keys()
    return dict((col, getattr(model, col)) for col in fields)

def model_to_dict(func):
    def wrap(*args, **kwargs):
        ret = func(*args, **kwargs)
        return model2dict(ret)
    return wrap

def models_to_list(func):
    def wrap(*args, **kwargs):
        ret = func(*args, **kwargs)
        return [model2dict(r) for r in ret]
    return wrap

def filter_update_data(func):
    def wrap(*args, **kwargs):
        if 'data' in kwargs:
            data = kwargs['data']
            data = dict([(key, value) for key, value in data.items() if value or value == 0])
            kwargs['data'] = data
        return func(*args, **kwargs)
    return wrap

def check_param_sign(func):
    def wrap(*args, **kw):
        if options.debug:
            return func(*args, **kw)

        self = args[0]
        params = self.request.arguments
        if not params:
            return func(*args, **kw)

        params = {i: j[0].decode() for i, j in params.items()}
        sign = params.get('sign', '')

        if not sign:
            raise utils.APIError(errcode=10003)
        del params['sign']

        params_str = '&'.join(['%s=%s'%(i, params[i]) for i in sorted(list(params.keys()))])
        if sign != hashlib.md5(params_str.encode()).hexdigest():
            raise utils.APIError(errcode=10003)

        return func(*args, **kw)
    return wrap

def login_required(func):
    def wrap(*args, **kw):
        self = args[0]
        login = self.current_user['login']
        if not login:
            raise utils.APIError(errcode=40001)
        return func(*args, **kw)
    return wrap

def permission_required(roles=[]):
    def decorator(func):
        def wrap(*args, **kw):
            self = args[0]
            login = int(self.current_user['login'])
            if not login:
                raise utils.APIError(errcode=40001)

            if roles and self.current_user['role_code'] not in roles:
                raise utils.APIError(errcode=40003)
            return func(*args, **kw)
        return wrap
    return decorator

def user_required(func):
    return permission_required(roles=['user', 'incharger', 'personel'])(func)

def fzr_required(func):
    return permission_required(roles=['incharger'])(func)

def personel_required(func):
    return permission_required(roles=['personel'])(func)

def manager_required(func):
    '''
    manager: 管理
    personel / fzr 都有权限
    '''
    return permission_required(roles=['personel', 'incharger'])(func)

# def forbid_frequent_api_call(seconds=[]):
#     def decorator(func):
#         def wrap(*args, **kw):
#             self = args[0]
#             sign = self.get_argument('sign', '')
#             user_id = self.get_argument('user_id', 0)
#             path = self.request.path
#             key = '%s_%s_%s' % (sign, user_id, path)
#             if not ctrl.rs.setnx(key, 1, seconds):
#                 raise utils.APIError(errcode=10001, errmsg='调用太多次')
#             return func(*args, **kw)
#         return wrap
#     return decorator
