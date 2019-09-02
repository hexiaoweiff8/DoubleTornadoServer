#!/usr/bin/env python
#!-*-codiung:utf-8 -*-
#!@Time     :2019/8/27 16:18
#!@File     : .py

import os

setting = dict(
    template_path=os.path.join(os.path.dirname(__file__), 'WebRoot'),
    static_path=os.path.join(os.path.dirname(__file__), 'WebRoot'),
    autoescape=None
)
