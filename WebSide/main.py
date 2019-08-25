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
    def dispatch(self, msgid, raw_data):
        res = {'retCode': 0, 'msgid': msgid}
        if raw_data is None or msgid is None:
            res['retCode'] = error.ERR_PREAM_ERR
            raise gen.Return(res)
        handler = cmd.REQUEST_HANDLERS.get(msgid)
        if handler is None:
            res['retCode'] = error.ERR_INVALID_MSGID
            raise gen.Return(res)

        raise gen.Return((yield handler(self.request, msgid, raw_data)))

    '''
    get请求
    '''
    @gen.coroutine
    def get(self):
        # print(self.request.headers)
        msg_id = self.get_argument('msgid', None)

        res = {'retCode': 0, 'msgid': msg_id}

        # TODO 处理OSS
        # TODO 处理多次请求
        # TODO 路由Post与Get请求的许可列表
        try:
            # 过滤, 防注入
            data_str = self.get_argument('data')
            if data_str is not None:
                parse.unquote(data_str)
            raw_data = json.loads(data_str)

            res = yield self.dispatch(msg_id, raw_data)

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
    # 注册消息
    cmd.init_request_handlers()
    # 初始化redis
    dbs.initRedis(config)
    # 注册消息
    cmd.init_request_handlers()

    logging.info('----------------db-server Start-------------------')

    # 监听端口
    app.listen(_port)
    tornado.ioloop.IOLoop.instance().start()
