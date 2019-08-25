#!/usr/bin/env python
#!-*-codiung:utf-8 -*-
#!@Time     :2019/6/27 10:44
#!@File     : .py

from UtilFiles import dbs
import json
import time
from UtilFiles import const
from UtilFiles import utilTools
from DBSide import packet_ids
from UtilFiles import myConfig as config
from urllib import parse
from UtilFiles import error


'''
构建缓存key
'''
def rkeyInRedis(uid):
    return "%s%s" %(const.rkeyPrefix, uid)


# '''
# 获取redis缓存
# '''
# def inRedis(r, uid):
#     cacheKey = rkeyInRedis(uid)
#     raw = r.hgetall(cacheKey)
#     if raw:
#         r.expire(cacheKey, 1800)
#         return({k:json.loads(v) for k,v in raw.items()})



'''
获取redis缓存
'''
def inRedis(r, key, value, time_key, ctime):
    # cacheKey = key
    # raw = r.hgetall(cacheKey)
    # if raw:
    #     r.expire(cacheKey, time)
    #     return({k:json.loads(v) for k,v in raw.items()})
    result = None
    now = int(time.time())
    cache_time_str = r.hget(time_key, value)
    if cache_time_str is None:
        cache_time_str = 0
    cache_time = int(cache_time_str)
    if now - cache_time <= ctime:
        result = r.hget(key, value)
    else:
        r.delete(key)
    return result


'''
获取name-pwd影射uid
'''
# def namePwdInRedis(r, name, pwd):
#     return r.get(name + '-' + pwd)


'''
获取openId影射uid
'''
def openIdInRedis(r, open_id):
    if open_id is None:
        return None
    return r.hget(const.OpenIdMappingUserIdKey, open_id)


'''
获取用户信息
'''
def getUserByUid(uid):
    # 读取缓存
    userData = inRedis(dbs.r, const.UserRedisKey, str(uid), const.UserTimeRedisKey, const.RecommendUserTime)

    # 请求http胸口
    if userData is None:
        # http请求db
        paramStr = '?msgid=%s&data=' \
              % packet_ids.db_msg_query_user
        paramStr += parse.quote(json.dumps({'id': uid}))
        userData = utilTools.requestDbSide(config, paramStr)

        # 缓存数据
        dbs.r.hset(const.UserRedisKey, uid, userData)
        dbs.r.expire(const.UserRedisKey, const.RecommendUserTime * 2)
        # 设置缓存时间
        dbs.r.hset(const.UserTimeRedisKey, uid, int(time.time()))

    if userData is None:
        return None

    return json.loads(userData)

