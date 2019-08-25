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
转换数据类型
'''
def get_db_data_filed(var):
    if var is not None:
        typeStr = var.__class__.__name__
        if typeStr == 'int' or typeStr == 'str' or typeStr == 'float':
            return var
        elif typeStr == 'byte'\
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

# --------------------------WX-------------------------------

