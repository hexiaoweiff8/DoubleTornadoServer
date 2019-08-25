#!/usr/bin/env python
#!-*-codiung:utf-8 -*-
#!@Time     :2019/6/27 11:29
#!@File     : .py

import json
import requests
import time
from urllib import request
from urllib import parse
import traceback
from UtilFiles import error
from UtilFiles import const
from UtilFiles import dbs


'''
请求http
'''
def httpRequest(url, params = None, type = 'POST'):
    data = None
    if params is not None:
        data = parse.urlencode(params).encode('utf-8')
    req = request.Request(url)
    response = request.urlopen(req, data)
    return response.read()


'''
请求db节点
'''
def requestDbSide(config, paramsStr):
    # http请求db
    db_side_list = config.d['dbList']
    # db_sort_list = config.db_sort_list

    # 失败次数排序优先级
    # for_list = []
    is_success = True
    response = None
    for index in range(len(db_side_list)):
        data_item = db_side_list[index]
        try:
            url = 'http://%s:%s/process' % (data_item['ip'], data_item['port'])
            url += paramsStr
            response = httpRequest(url)
            is_success = True
        except:
            import traceback
            # 打印异常信息
            traceback.print_exc()
            is_success = False
            # db_sort_list[index] = db_sort_list[index] + 1
            pass
        # 请求成功
        if is_success:
            break

    if response is None:
        response = '{\'retCode\': %s}' % error.ERR_DB_OPERATION_FAIL

    return response


'''
转换数据类型
'''
def get_db_data_filed(var):
    if var is not None:
        typeStr = var.__class__.__name__
        if typeStr == 'int' or typeStr == 'str' or typeStr == 'float':
            return var
        elif typeStr == 'bytes'\
                or typeStr == 'datetime'\
                or typeStr == 'tuple'\
                or typeStr == 'dict'\
                or typeStr == 'set':
            return str(var)

    return None


'''
是否需要添加引号
'''
def need_qoute(var):
    typeStr = var.__class__.__name__
    if typeStr == 'int' or typeStr == 'float':
        return False
    return True


'''
判断空或空串
'''
def is_none_or_empty(argStr):
    return argStr is None or str(argStr).strip() == ''


'''
判断变量类型
'''
# def typeof(var):
#     typeName = None
#     type_tmp = type(var)
#     typeStr = str(var.__class__.__name__)
#     if isinstance(var, int):
#         typeName = 'int'
#     elif isinstance(var, str):
#         typeName = 'str'
#     elif isinstance(var, float):
#         typeName = 'float'
#     elif isinstance(var, list):
#         typeName = 'list'
#     elif isinstance(var, tuple):
#         typeName = 'tuple'
#     elif isinstance(var, dict):
#         typeName = 'dict'
#     elif isinstance(var, set):
#         typeName = 'set'
#     return typeName


'''
sql防注入
'''
def sql_filter(sql):
    if not isinstance(sql, str):
        return sql
    dirty_stuff = ["\"", "\\", "*", "'", "#", "<", ">", "+", "$", "(", ")", "@", "!"]
    for stuff in dirty_stuff:
        sql = sql.replace(stuff, "")
    return sql


'''
生成redis的key
'''
def gen_redis_key(query, page):
    result = ''
    if query:
        for k, v in query.item():
            result += k + '-' + v + ','
    if page:
        result += '-' + page

    return result

# --------------------------WX-------------------------------


'''
获取用户openId
'''
def getOpenId(code):
    try:
        print(code)
        resp = requests.get(const.WXCodeToOpenId + ('appid=%s&secret=%s&js_code=%s' % (const.WXAppId, const.WXAppSecret, code)))
        if resp.status_code == 200:
            print(resp.text)
            return json.loads(resp.text)['openid']
        else:
            print('error:' + resp.status_code)
            return 'testOpenId'
    except:
        print('getOpenIdError')
        traceback.print_exc()


'''
获取微信Token
'''
def getAccessToken():
    # 判断redis中有并且未超时直接返回
    cacheToken = dbs.r.get(const.CacheWXAccessTokenKey)
    cacheTime = dbs.r.get(const.CacheWXAccessTokenTime)
    now = int(time.time())
    if cacheToken is None or cacheTime is None or (int(cacheTime) + 3600 < now):
        resp = requests.get(const.WXAccessToken + ('appid=%s&secret=%s' % (const.WXAppId, const.WXAppSecret)))
        if resp.status_code == 200:
            cacheToken = json.loads(resp.text)['access_token']
            dbs.r.set(const.CacheWXAccessTokenKey, cacheToken)
            dbs.r.set(const.CacheWXAccessTokenTime, now)
        else:
            print('error:' + resp.status_code)
    return cacheToken
