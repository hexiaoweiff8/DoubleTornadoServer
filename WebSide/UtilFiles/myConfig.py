#!/usr/bin/env python
#!-*-codiung:utf-8 -*-
#!@Time     :2019/6/27 15:05
#!@File     : .py

import json

'''
db 排序列表, 失败次数正序
'''
db_sort_list = []

'''
读取配置
'''
def readConfig(configFile):
    global d
    fin = open(configFile, 'r')
    d = json.load(fin)

