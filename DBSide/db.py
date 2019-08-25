#!/usr/bin/env python
#!-*-codiung:utf-8 -*-
#!@Time     :2019/6/21 14:33
#!@File     : .py

import pymysql
from DBUtils.PooledDB import PooledDB
import redis
import logging
from traceback import print_exc, format_exc

'''
连接只读mysql
'''
def connect_read_mysql(dbIp,
                  dbPort,
                  dbUser,
                  dbPwd,
                  dbName,
                  minCount = 5,
                  maxCount = 1000):
    global myReadSqlDbPool
    myReadSqlDbPool = PooledDB(pymysql,
                           minCount,
                           int(maxCount / 2),
                           int(maxCount / 4),
                           maxCount,
                           host=dbIp,
                           user=dbUser,
                           passwd=dbPwd,
                           db=dbName,
                           port=dbPort)
    conn = myReadSqlDbPool.connection()

'''
连接只写mysql
'''
def connect_write_mysql(dbIp,
                  dbPort,
                  dbUser,
                  dbPwd,
                  dbName,
                  minCount = 5,
                  maxCount = 1000):
    global myWriteSqlDbPool
    myWriteSqlDbPool = PooledDB(pymysql,
                           minCount,
                           int(maxCount / 2),
                           int(maxCount / 4),
                           maxCount,
                           host=dbIp,
                           user=dbUser,
                           passwd=dbPwd,
                           db=dbName,
                           port=dbPort)
    conn = myWriteSqlDbPool.connection()

'''
获取mysql连接执行器
'''
def get_mysql_conn(type):
    if type == 'R':
        return myReadSqlDbPool.connection()
    elif type == 'W':
        return myWriteSqlDbPool.connection()

'''
关闭所有连接
'''
def closeAll():
    if myWriteSqlDbPool:
        myWriteSqlDbPool.close()
    if myReadSqlDbPool:
        myReadSqlDbPool.close()

'''
判断读写
'''
def analyze_sql_state(sql):
    if "select" in sql:
        return "R"
    else:
        return "W"

'''
执行sql
'''
def execute(sql):
    # TODO 判断是否为变更, 如果是变更则推入缓存中等待执行
    sql_type = analyze_sql_state(sql)
    conn = get_mysql_conn(sql_type)
    cursor = conn.cursor()
    data = cursor.execute(sql)
    fields = cursor.description
    if sql_type == "R":
        data = cursor.fetchall()
    elif sql_type == "W":
        conn.commit()

    cursor.close()
    # TODO 是否关闭连接?
    # conn.close()
    return {'data': data, 'fields': fields, 'lastId': cursor.lastrowid }
