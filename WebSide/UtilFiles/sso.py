#!/usr/bin/env python
# !-*-codiung:utf-8 -*-
# !@Time     :2019/6/28 15:26
# !@File     : .py

import os
import time
from hashlib import sha1
import json
import myConfig as config
import dbs, error

'''
session类
'''


class session(object):
    '''
    初始化
    '''

    def __init__(self, data={}, session_id=None):
        self.data = data
        self.modified = False
        self.time = int(time.time())
        self.is_empty = False
        self.session_id = session_id

    def update_time(self):
        self.time = int(time.time())

    '''
    设置数据
    '''

    def set(self, key, val):
        self.data[key] = val
        self.modified = True

    '''
    获取数据
    '''

    def get(self, key, default=None):
        return self.data.get(key, default)

    '''
    获取更新时间
    '''

    def get_time(self):
        return self.time

    '''
    返回数据字典
    '''

    def get_all_data(self):
        return self.data

    '''
    是否变更
    '''

    def is_modified(self):
        return self.modified

    '''
    设置是否为空
    '''

    def set_empty(self, is_empty):
        self.is_empty = is_empty
        self.modified = True

    '''
    是否为空
    '''

    def get_is_empty(self):
        return self.is_empty

    '''
    清空session
    '''

    def clear(self):
        self.data = {}
        self.modified = True
        self.time = int(time.time())
        self.is_empty = False


'''
单点登录控制类
'''
class SSO(object):
    '''
        第一步: 判断是否有cookie, 如果没有cookie则登录
        第二步: 如果有cookie, 从内存数据库中获取是否已登录, 否则跳回第一步
    '''

    '''
    初始化
    '''
    def __init__(self, get_response=None):
        print('init SSO')
        self.get_response = get_response
        # 连接redis
        # 预处理数据
        self.SESSION_COOKIE_NAME = config.d.get('cookie_name')
        self.COOKIE_SECRET = config.d.get('cookie_secret')
        self.SESSION_LIST_NAME = config.d.get('session_list_name')
        self.SESSION_TIME_OUT = int(config.d.get('session_time_out'))
        # self.SESSION_TIME_LIST = config.d.get('session_time_list_name')

        self.sessionDic = {}

    '''
    生成sessionId
    '''
    def generate_session_id(self, request):
        secret_key = config.d.get('cookie_secret')
        ip = request.META['REMOTE_ADDR']
        while True:
            rand = os.urandom(16)
            now = time.time()
            session_id = sha1(("%s%s%s%s" % (rand, now, ip, secret_key)).encode('utf8'))
            session_id = session_id.hexdigest()
            if not dbs.r.hexists(self.SESSION_LIST_NAME, session_id):
                break
        return session_id

    '''
    处理请求
    '''
    def process_request(self, request):
        # 禁止get请求
        if request.method == 'GET':
            return redirect("/auth/loginWithWX/")
        session_key = request.COOKIES.get(self.SESSION_COOKIE_NAME, None)
        if session_key is None:
            # 从url中获取ssk
            session_key = request.GET.get(self.SESSION_COOKIE_NAME, None)
            if session_key is None:
                request.session = session({}, session_key)
                session_key = self.generate_session_id(request)
                request.COOKIES[self.SESSION_COOKIE_NAME] = session_key
                # 设置sessionId列表
                self.update_session_time(session_key, request.session.get_time())
                # return None

        # 获取session内容
        sess = self.sessionDic.get(session_key, None)
        now = int(time.time())
        # 检测超时
        if sess is not None and now - sess.get_time() > self.SESSION_TIME_OUT:
            sess.clear()
            sess.update_time()

        request.session = sess

        if request.session is None:
            request.session = session(self.get_session_store(session_key), session_key)
            self.sessionDic[session_key] = request.session

        # 更新时间
        if request.session:
            request.session.update_time()
            self.update_session_time(session_key, request.session.get_time())
        # else:
        #     return HttpResponse(json.dumps({'retCode': error.ERR_NO_LOGIN}, ensure_ascii=False),
        #                  content_type="application/json,charset=utf-8")
            # 未登录重定向
            # if request.path_info == "/auth/loginWithWX/":
            #     return None
            # else:
            #     return redirect("/auth/loginWithWX/")

        return None

    '''
    处理反馈
    '''
    def process_response(self, request, response):
        '''
        如果session有变更则将其保存
        如果session是空, 则删除对应的ssk
        '''
        session_key = request.COOKIES.get(self.SESSION_COOKIE_NAME, None)
        if session_key is None:
            # 从url中获取ssk
            session_key = request.GET.get(self.SESSION_COOKIE_NAME, None)
            if session_key is None:
                return response

        sess = request.session
        if sess.is_modified():
            if sess.get_is_empty():
                # 删除
                del self.sessionDic[session_key]
                response.delete_cookie(self.SESSION_COOKIE_NAME)
            else:
                self.update_session_store(session_key, sess.get_all_data())
        if response.status_code != 500:
            response.set_cookie(self.SESSION_COOKIE_NAME,
                                session_key,
                                max_age=self.SESSION_TIME_OUT)

        return response

    '''
    更新session时间
    '''
    def update_session_time(self, session_id, init_time):
        if dbs.r:
            # dbs.r.hset(self.SESSION_TIME_LIST, session_id, init_time)
            dbs.r.expire(session_id, self.SESSION_TIME_OUT)

    '''
    更新session数据
    '''
    def update_session_store(self, ssk, data):
        if dbs.r:
            dbs.r.set(ssk, json.dumps(data))
            dbs.r.expire(ssk, self.SESSION_TIME_OUT)

    '''
    删除session数据
    '''
    def del_session_store(self, ssk):
        if dbs.r:
            dbs.r.delete(ssk)

    '''
    获取session内容
    '''
    def get_session_store(self, ssk):
        if dbs.r:
            data_str = dbs.r.get(ssk)
            if data_str:
                return json.loads(data_str)
        return {}


'''
初始化单点登录
'''
# def init_sso():
#     global sso
#     sso = SSO()
