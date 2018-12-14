#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
2018/11/01
del
初始化类
"""
import base
import units


class Initialization_(object):
    def __init__(self):
        base.inits_()

    @staticmethod
    def init_bs(port_no, ip_):
        """
        初始化基站
        :param port_no:基站portNo
        :param ip_:客户端ip地址
        :return:  0成功 1失败，None
        """
        if port_no is not None:
            base.inits_.init_bs(port_no, ip_)
            return 0, None
        else:
            return 1, None

    @staticmethod
    def init_tag(first_portno, num, type_=0):
        """
        初始化标签
        :param first_portno:第一个标签号
        :param num: 标签数量
        :param type_: 标签类型
        :return: 0成功 1失败，tag是标签列表，None
        """
        if first_portno is not None and num > 0:
            tags = units.make_tags(first_portno, num)
            for tag in tags:
                base.inits_.init_tag(tag, type_)
            return 0, tags
        return 1, None
