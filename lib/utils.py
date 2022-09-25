import os
import pdb
import time
import math
import base64
import json
import random
import logging
import datetime

from openpyxl import load_workbook

from decimal import Decimal
from tornado import web, httpclient
from tornado.gen import coroutine
from tornado.httputil import url_concat
from tornado.options import options


if not options.debug:
    httpclient.AsyncHTTPClient.configure('tornado.curl_httpclient.CurlAsyncHTTPClient', max_clients=300)


def dict_filter(target, attr=()):
    result = dict()
    for p in attr:
        if type(p) is dict:
            key = list(p.keys())[0]
            value = list(p.values())[0]
            result[value] = target[key] if key in target else ''
        elif p in target:
            result[p] = target[p]
    return result

class APIError(web.HTTPError):
    '''
    自定义API异常
    '''
    def __init__(self, status_code=200, *args, **kwargs):
        super(APIError, self).__init__(status_code, *args, **kwargs)
        self.kwargs = kwargs

def http_request(url, connect_timeout=10, request_timeout=10, **kwargs):
    return httpclient.HTTPRequest(url=url, connect_timeout=connect_timeout, request_timeout=request_timeout, **kwargs)

def get_async_client():
    http_client = httpclient.AsyncHTTPClient()
    return http_client

async def fetch_api(url, method='GET', params={}, body={}, raw=0):
    url = url_concat(url, params)
    client = get_async_client()
    request = httpclient.HTTPRequest(url=url, method=method, body=None if method=='GET' else json.dumps(body),
                                     connect_timeout=10, request_timeout=10)
    try:
        response = await client.fetch(request)
        response = response.body.decode()
        if raw:
            return response
        response = json.loads(response)
        return response
    except Exception as e:
        logging.error(e)
        logging.error('url: %s, method: %s, params: %s, body: %s'%(url, method, params, body))
        raise

def read_excel(url, tp):
    '''
    todo: nginx需要将文件处理的都指向同一台机器，要不然，读不到这个文件
    url: file url  http://baidu.com/asld/xyz.xlst
    tp: 0/1   attendance / m_pieces的计件/ 老员工导入 / m_pieces 的提成
    0  计薪月度 姓名  证件号码 部门  迟到  早退   旷工
    1  计薪月度 姓名  证件号码  产品名  统计数
    2  员工编号 姓名  手机号  qq号   微信号
    3  计薪月度 姓名  证件号码  产品名  统计数
    4  计薪月度 姓名  证件号码  借款  奖金
    '''
    def get_year(month):
        now = datetime.datetime.now()
        y, m = now.year, now.month
        if month >= m:
            return y - 1
        return y

    file_path =  os.path.dirname(os.path.dirname(__file__)) + '/static/upload/' + url.split('/')[-1]
    wb = load_workbook(file_path)
    sheet = wb.get_active_sheet()

    res = []
    rows = [row for row in sheet.rows]
    if tp==0:
        for row in rows[1:]:
            if not row[0].value:
                break

            month = int(row[0].value)
            year = get_year(month)
            username = row[1].value
            doc_num = row[2].value
            late = float(row[3].value)
            early = float(row[4].value)
            absent = float(row[5].value)
            res.append({
                'year': year,
                'month': month,
                'username': username,
                'doc_num': doc_num,
                'late_hours': late,
                'early_hours': early,
                'absent_hours': absent
            })
        return res
    elif tp==1:
        for row in rows[1:]:
            if not row[0].value:
                break

            month = int(row[0].value)
            year = get_year(month)
            res.append({
                'month': month,
                'year': year,
                'username': row[1].value,
                'doc_num': row[2].value,
                'product_name': row[3].value,
                'count': float(row[4].value)
            })
        return res
    elif tp==2:
        for row in rows[1:]:
            if not row[0].value:
                break

            res.append({
                'number':  row[0].value,
                'username':  row[1].value,
                'phone_num':  row[2].value,
                'qq_account':  row[3].value,
                'wechat_account':  row[4].value
            })
        return res
    elif tp==3:
        for row in rows[1:]:
            if not row[0].value:
                break

            month = int(row[0].value)
            year = get_year(month)
            res.append({
                'month': month,
                'year': year,
                'username': row[1].value,
                'doc_num': row[2].value,
                'product_name': row[3].value,
                'count': float(row[4].value)
            })
        return res
    elif tp==4:
        for row in rows[1:]:
            if not row[0].value:
                break

            month = int(row[0].value)
            year = get_year(month)
            borrow, bonus = 0, 0
            row3, row4 = row[3].value, row[4].value
            if row3:
                borrow = float(row3)
            if row4:
                bonus = float(row4)
            res.append({
                'month': month,
                'year': year,
                'username': row[1].value,
                'doc_num': row[2].value,
                'borrow': borrow,
                'bonus': bonus
            })
        return res

def get_overtime_initial_value(single_week_hours, double_week_hours):
    '''
    工作日加班工时初始值
    (单+双) * 2.175 - 174
    '''
    return (single_week_hours + double_week_hours) * 2.175 - 174

def calc_tax(money):
    to_calc = money - 5000
    res = 0
    if to_calc <= 3000:
        res += to_calc * 0.03
        return res

    res += 3000 * 0.03
    if to_calc <= 12000:
        res += (to_calc - 3000) * 0.1
        return res

    res += (12000 - 3000) * 0.1
    if to_calc <= 25000:
        res + (to_calc - 12000) * 0.2
        return res

    res += (25000 - 12000) * 0.2
    if to_calc <= 35000:
        res += (to_calc - 25000) * 0.25
        return res

    res += (35000 - 25000) * 0.25
    if to_calc <= 55000:
        res += (to_calc - 35000) * 0.3
        return res

    res += (55000 - 35000) * 0.3
    if to_calc <= 80000:
        res += (to_calc - 55000) * 0.35
        return res

    res += (to_calc - 80000) * 0.45
    return res

def sum_list_columns(datas, to_sum_columns=[], attached_dict={}):
    data = {}
    for col in to_sum_columns:
        data.update({
            col: sum([i[col] for i in datas])
        })

    data.update(attached_dict)
    return data

def filter_empty_valued_keys(d, no_use_keys=[]):
    res = {}
    for i, j in d.items():
        if not j or i in no_use_keys:
            continue

        res.update({
            i: j
        })
    return res

def encode_company_id(cid):
    return base64.b64encode(("%03dcid:%s:%04d" % (random.randint(0, 999), (cid**2+5)*1000 + random.randint(0, 999), random.randint(0, 9999))).encode()).decode()

def decode_company_id(cid_str):
    s = base64.b64decode(cid_str.encode()).decode()
    return int(math.sqrt(int(s.split(':')[1]) // 1000 - 5))
