#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
2018/11/01
del
数据制造类
"""
from tornado.escape import json_decode
from tornado.web import RequestHandler
import views
import service


class EventInfoHandler(RequestHandler):
    def get(self, *args, **kwargs):
        ret = views.setting.get('return_message')
        myPortNo = self.get_argument('myPortNo', None)
        tagPortNo = self.get_argument('tagPortNo', None)
        dataType = int(self.get_argument('dataType', None))
        event_ = self.get_argument('event', None)
        parameters = {'myPortNo': myPortNo, 'tagPortNo': tagPortNo, 'event_': event_}
        status, msg = service.MadeData.selct_template(dataType, parameters)
        ret.update({'Status': status, 'Msg': msg, 'Tags': None})
        self.write(ret)


class HbInfoHandler(RequestHandler):
    def get(self, *args, **kwargs):
        ret = views.setting.get('return_message')
        myPortNo = self.get_argument('myPortNo', None)
        tagPortNo = self.get_argument('tagPortNo', None)
        dataType = int(self.get_argument('dataType', None))
        modes = self.get_argument('modes', None)
        parameters = {'myPortNo': myPortNo, 'tagPortNo': tagPortNo, 'modes': modes}
        status, msg = service.MadeData.selct_template(data_type=dataType, dict_=parameters)
        ret.update({'Status': status, 'Msg': msg, 'Tags': None})
        self.write(ret)


class DataInfoHandler(RequestHandler):
    def post(self, *args, **kwargs):
        ret = views.setting.get('return_message')
        data = json_decode(self.request.body)
        myPortNo = data.get('myPortNo', None)
        tagPortNo = data.get('tagPortNo', None)
        dataType = int(data.get('dataType', None))
        parameters = {'myPortNo': myPortNo, 'tagPortNo': tagPortNo}
        status, msg = service.MadeData.selct_template(dataType, parameters)
        ret.update({'Status': status, 'Msg': msg, 'Tags': None})
        self.write(ret)
