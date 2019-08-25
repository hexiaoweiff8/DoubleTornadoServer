#!/usr/bin/env python
#!-*-codiung:utf-8 -*-
#!@Time     :2019/6/20 16:37
#!@File     : .py

import sys
import tornado
import logging
import error
import db, config
import cmd
import _log
import json
from tornado.options import define, options
from tornado import ioloop, web, gen, httpserver, httpclient, websocket
from traceback import print_exc, format_exc
from urllib import parse
from UtilFiles import dbs
import utilTools


define('cfg', default='./config.json', help='debug log path', type=str)
define('sid', default=1, help='db server id', type=int)

'''
代码热加载
'''

# class ReloadCode(tornado.web.RequestHandler):
#     def get(self):
#         logging.info('reload code')
#         logging.info(self.request.remote_ip)
#         reload(handler)


'''
请求处理类
使用tornado进行接收http
'''
class Process(tornado.web.RequestHandler):
    @gen.coroutine
    def dispatch(self, msgid, raw_data, start, count):
        res = {'retCode': 0, 'msgid': msgid}
        if raw_data is None or msgid is None:
            res['retCode'] = error.ERR_PREAM_ERR
            raise gen.Return(res)
        handler = cmd.REQUEST_HANDLERS.get(msgid)
        if handler is None:
            res['retCode'] = error.ERR_INVALID_MSGID
            raise gen.Return(res)

        if start is None or count is None:
            raise gen.Return((yield handler(self.request, msgid, raw_data)))
        else:
            raise gen.Return((yield handler(self.request, msgid, raw_data, int(start), int(count))))


    '''
    get请求
    '''
    @gen.coroutine
    def get(self):
        # print(self.request.headers)
        msg_id = self.get_argument('msgid', None)

        res = {'retCode': 0, 'msgid': msg_id}

        try:
            # 过滤, 防注入
            data_str = self.get_argument('data')
            start = utilTools.sql_filter(self.get_argument('start', None))
            count = utilTools.sql_filter(self.get_argument('count', None))
            if data_str is not None:
                parse.unquote(data_str)
            raw_data = json.loads(data_str)
            # 过滤, 防注入
            for key, val in raw_data.items():
                raw_data[key] = utilTools.sql_filter(val)

            res = yield self.dispatch(msg_id, raw_data, start, count)

        except:
            print_exc()
            logging.info(format_exc())
            res['retCode'] = error.ERR_CODE_EXCEPTION

        self.write(res)
        self.finish()
    '''
    post请求
    '''
    @gen.coroutine
    def post(self):
        a = yield self.get()


    '''
    关闭清理
    '''
    def cleanup(self):
        # 关闭所有连接
        db.closeAll()
        exit()


'''
启动
'''
if __name__ == '__main__':
    app = tornado.web.Application([
        ('/process', Process)
    ])
    # 处理配置参数
    options.parse_command_line()
    config.readConfig(options.cfg)
    # 初始化日志
    _port = config.d['db']['base_port']
    logFile = '%s_db.log' % (config.d['serv_id'])
    _log.init_log(config.d.get('log') + logFile, _port)
    # 初始化db
    # mongoConfig = config.d.get('mongodb')
    # uri = 'mongodb://'
    # user = mongoConfig.get('user', None)
    # pwd = mongoConfig.get('pwd', None)
    # if user and pwd:
    #     uri += '%s:%s@'%(user, pwd)
    # uri += '%s:%s/admin'%(mongoConfig.get('host'), mongoConfig.get('port'))
    # db.connect_mongo(uri, mongoConfig.get('db'))
    # db.initRedis(config.d.get('redis'))
    # 初始化mysqlDb
    mysqlConfig = config.d.get('mysql')
    # 只读
    ip = mysqlConfig.get('ipR')
    port = mysqlConfig.get('portR')
    userName = mysqlConfig.get('userR')
    pwd = mysqlConfig.get('pwdR')
    dbName = mysqlConfig.get('dbR')
    minConn = mysqlConfig.get('minConnR')
    maxConn = mysqlConfig.get('maxConnR')
    db.connect_read_mysql(ip, port, userName, pwd, dbName, minConn, maxConn)
    # 只写
    ip = mysqlConfig.get('ipW')
    port = mysqlConfig.get('portW')
    userName = mysqlConfig.get('userW')
    pwd = mysqlConfig.get('pwdW')
    dbName = mysqlConfig.get('dbW')
    minConn = mysqlConfig.get('minConnW')
    maxConn = mysqlConfig.get('maxConnW')
    db.connect_write_mysql(ip, port, userName, pwd, dbName, minConn, maxConn)
    # print(db.execute('select * from User;'))
    # 注册消息
    cmd.init_request_handlers()

    logging.info('----------------db-server Start-------------------')

    # 监听端口
    app.listen(_port)
    tornado.ioloop.IOLoop.instance().start()
