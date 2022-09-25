# redis
REDIS = {
    'host': '127.0.0.1',
    'port': 6379,
    'db': 0,
    'password': None
}

# mysql
DB_OA = 'db'
MYSQL_DB = {
    DB_OA: {
        'master': {
            'host': '127.0.0.1',
            'user': 'zlg',
            'pass': 'MYSQLzlg153',
            'port': 3306
        },
        'slaves': [
            {
                'host': '127.0.0.1',
                'user': 'zlg',
                'pass': 'MYSQLzlg153',
                'port': 3306
            }
        ]
    }
}

A_MINUTE = 60
A_HOUR = 3600
A_DAY = 24 * A_HOUR
A_WEEK = A_DAY * 7
A_MONTH = A_DAY * 30

UPYUN = {
    'api': 'http://v0.api.upyun.com/',
    'bucket': 'madan-image',
    'secret': '***********',
    'cdn': 'http://madan-image.b0.aicdn.com',
    'username': '*******',
    'password': '********'
}

# error msg
ERR = {
    200: '请求成功',
    10001: '请求参数错误',
    10002: '验证码错误',
    10003: '签名错误',

    40001: '未登录',
    40003: '无权限',
    50001: '服务器错误',
    50006: '访问频率过高'
}

WX_GRANT_URL = 'https://api.weixin.qq.com/sns/userinfo?appid={appid}&secret={secret}&code={code}&grant_type=authorization_code'
WX_USER_INFO_URL = 'https://api.weixin.qq.com/sns/userinfo?access_token={access_token}&openid={openid}'
WX_REFRESH_TOKEN_URL = 'https://api.weixin.qq.com/sns/oauth2/refresh_token?appid={appid}&grant_type=refresh_token&refresh_token={refresh_token}'

# try to load debug settings
try:
    from tornado.options import options
    if options.debug:
        exec(compile(open('settings.debug.py')
             .read(), 'settings.debug.py', 'exec'))
except:
    pass

