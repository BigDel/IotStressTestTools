#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
2018/11/01
del
客户端初始化类
"""
from tornado.escape import json_decode
from tornado.web import RequestHandler
import views
import service


class InitializationHandler(RequestHandler):

    def get(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:返回获生产标签的值
        """
        ret = views.setting.get('return_message')
        num = int(self.get_argument('Num'))
        first_tag = int(self.get_argument('First'))
        type_ = self.get_argument('Type')
        status, msg = service.Initialization_.init_tag(first_tag, num, type_)
        ret.update({'Status': status, 'Tags': msg, 'Msg': None})
        self.write(ret)

    def post(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:返回post状态
        """
        ret = views.setting.get('return_message')
        data = json_decode(self.request.body)
        bs_portno = data['MyPortNo']
        ip_ = self.request.remote_ip
        status, msg = service.Initialization_.init_bs(bs_portno, ip_)
        ret.update({'Status': status, 'Msg': msg, 'Tags': None})
        self.write(ret)
