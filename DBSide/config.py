#!/usr/bin/env python
#!-*-codiung:utf-8 -*-
#!@Time     :2019/6/21 14:41
#!@File     : .py

import json

'''
加载配置文件
'''
def readConfig(configFile):
    global d
    fin = open(configFile, 'r')
    d = json.load(fin)