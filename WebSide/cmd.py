#!/usr/bin/env python
#!-*-codiung:utf-8 -*-
#!@Time     :2019/6/21 14:52
#!@File     : .py

import handler
import packet_ids


REQUEST_HEANDLERS = {}

def init_request_handlers():
    global REQUEST_HANDLERS
    REQUEST_HANDLERS = {

        # ----------------用户-------------------
        packet_ids.Login:               handler.login,             # 查询用户
    }
