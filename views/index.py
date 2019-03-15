#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
2018/11/01
del
首页
"""
from tornado.web import RequestHandler
import views


class IndexHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.write("暂无主页")


class TestConnectionHandler(RequestHandler):
    def get(self, *args, **kwargs):
        ret = views.setting.get('return_message')
        ret.update({'Status': 0})
        self.write(ret)
