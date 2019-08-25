#!/usr/bin/env python
#!-*-codiung:utf-8 -*-
#!@Time     :2019/6/27 10:56
#!@File     : .py


import redis


'''
初始化redis
'''
def initRedis(config):
    global r
    print(config.d.get('redis'))
    r = redis.Redis(**config.d.get('redis'))
    r.hset('started', '1', '1')

