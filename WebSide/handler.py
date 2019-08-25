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
from Model import User as userMod


from tornado import gen


# -------------------------用户----------------------------------
@gen.coroutine
def login(request, msgid, data):
    res = {'retCode': 0}
    id = data.get('id', None)
    if id:
        udata = userMod.getUserByUid(id)

        if udata['retCode'] != 0:
            res['retCode'] = udata['retCode']
        else:
            res['data'] = udata

            # TODO 保存Session

    raise gen.Return(res)

