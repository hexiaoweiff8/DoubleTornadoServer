#!/usr/bin/env python
#!-*-codiung:utf-8 -*-
#!@Time     :2019/8/5 19:00
#!@File     : .py

import os
import time
from hashlib import sha1
import json
from UtilFiles import myConfig as config
from UtilFiles import const
from UtilFiles import error
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse


'''
防止单数据重复请求
'''
class PoofDoubleRequest(MiddlewareMixin):

    '''
    处理请求
    '''
    def process_request(self, request):

        # 是否在排除列表里
        path = request.path
        if path in const.PoofExpectList:
            return None

        if request.session and not request.session.get('userinfo') is None:
            print('ok')
        else:
            return HttpResponse(json.dumps({'retCode': error.ERR_NO_LOGIN},
                                           ensure_ascii=False),
                                        content_type="application/json,charset=utf-8")
        # 获取参数
        # 对比请求index
        # 如果客户端index小于服务器记录的index, 抛弃, 返回错误码
        self.REQUEST_INDEX = config.d.get('request_index')
        index = int(request.GET.get(self.REQUEST_INDEX, 0))
        sess_index = int(request.session.get(self.REQUEST_INDEX, -1))
        if index < sess_index:
            return HttpResponse(json.dumps({'retCode': error.ERR_DOUBLE_REQUEST_ERR}, ensure_ascii=False),
                                content_type="application/json,charset=utf-8")

        # 处理index
        request.session.set(self.REQUEST_INDEX, index + 1)
        return None
