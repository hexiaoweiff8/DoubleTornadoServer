#!/usr/bin/env python
#!-*-codiung:utf-8 -*-
#!@Time     :2019/6/21 15:00
#!@File     : .py

import sys
import json
import random
import math
import copy
import base64
import time
import error
import db
import utilTools


from tornado import gen


# -------------------------用户----------------------------------
@gen.coroutine
def query_user(request, msgid, data, start=0, count=sys.maxsize):
    res = {'retCode': 0}

    order = data.pop('orderBy', None)
    searchUid = data.pop('search-uid', None)
    # 解析请求数据
    # print(data)
    # 混合条件
    sql = 'select id, nickName, sex, icon, tagList, contents, followOtherCount, follows, fabulous, createTime, isSealed '
    if searchUid:
        sql += ', (select count(1) from Follow where uid = %s and targetUid = User.id) as isFollow' % searchUid
    sql += ' from User where 1=1'
    for key, val in data.items():
        if val is None:
            continue
        qoute = ''
        if utilTools.need_qoute(val):
            qoute = "'"
        sql += ' and ' + str(key) + '=' + qoute + str(val) + qoute
    # 分页
    if order:
        sql += ' order by ' + order
    sql += ' limit %s, %s' % (start, count)
    pack = db.execute(sql)
    udata = pack['data']
    fields = pack['fields']

    if udata is None or len(udata) == 0:
        res['retCode'] = error.ERR_USER_NOT_EXIST
        raise gen.Return(res)

    # 返回数据
    dataList = trans_data(udata, fields)

    res['data'] = json.dumps(dataList)
    raise gen.Return(res)


'''
设置用户数据
'''
def set_user_info(request, msgid, data, start=0, count=sys.maxsize):
    res = {'retCode': 0}
    uid = data['uid']
    nick_name = data['nickName']
    icon = data['icon']
    sex = data['sex']
    sql = "update User set nickName = '%s', sex = %s,icon = '%s' where id=%s" % (
        nick_name, sex, icon, uid
    )
    pack = db.execute(sql)

    res['data'] = json.dumps(pack)
    raise gen.Return(res)


'''
用户是否存在
'''
def user_exist(request, msgid, data, start=0, count=sys.maxsize):
    result = {'retCode': 0}
    uid = data['uid']
    count = count_user(uid)
    result['data'] = count > 0
    raise gen.Return(result)


'''
用户数量
'''
def count_user(uid):
    sql = "select count(1) as count from User where id = " + str(uid)
    pack = db.execute(sql)
    count = int(str(pack['data'][0][0]))
    return count

# '''
# openId获取登录
# '''
# @gen.coroutine
# def login_with_openId(request, msgid, data, start=0, count=sys.maxsize):
#     res = {'retCode': 0}
#     open_id = data['openId']
#     sql = "select * from User join WxInfo on User.wxInfoId = WxInfo.id where WxInfo.openId = '" + open_id + "'"
#     pack = db.execute(sql)
#
#     udata = pack['data']
#     fields = pack['fields']
#     data_list = trans_data(udata, fields)
#     res['data'] = json.dumps(data_list)
#     raise gen.Return(res)


'''
注册微信用户
'''
@gen.coroutine
def reg_user_by_wxinfo(request, msgid, data, start=0, count=sys.maxsize):
    res = {'retCode': 0}
    open_id = data['openId']
    nick_name = data['nickName']
    head_url = data['headUrl']
    sql = "insert into User (openId, nickName, icon) values ('%s', '%s', '%s')" % (
        open_id, nick_name, head_url
    )
    pack = db.execute(sql)

    udata = pack['data']
    # fields = pack['fields']
    # data_list = trans_data(udata, fields)
    res['data'] = udata
    raise gen.Return(res)


'''
刷新微信数据
'''
@gen.coroutine
def refresh_user_wxinfo(request, msgid, data, start=0, count=sys.maxsize):
    res = {'retCode': 0}
    open_id = data['openId']
    nick_name = data['nickName']
    head_url = data['headUrl']
    # TODO sql文名称去重添加_数字
    sql = "update User set nickName = '%s', icon = '%s' where openId='%s'" % (
        nick_name, head_url, open_id
    )
    pack = db.execute(sql)

    res['data'] = json.dumps(pack)
    raise gen.Return(res)


'''
转换数据
'''
def trans_data(data, fields):
    dataList = []
    for val in data:
        one_data = {}
        count = 0
        for field in fields:
            one_data[field[0]] = utilTools.get_db_data_filed(val[count])
            count += 1
        dataList.append(one_data)
    return dataList