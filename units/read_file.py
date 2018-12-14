#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
2018/11/05
del
此类为读取文件工具类，可读取配置文件、以及存储的标签
"""
import os
import yaml


# 读取文件config文件
class ReadConfigs(object):
    config_file = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/profiles/config.yaml'
    if os.path.isfile(config_file):
        configs = yaml.load(open(config_file, 'r', encoding='UTF-8'))

    @classmethod
    def get(cls, head='IoT.Config', key=None):
        if not cls.configs:
            cls.configs = yaml.load(open(cls.config_file, 'r'))
        section = cls.configs.get(head, None)
        if section is None:
            raise NotImplementedError
        value = section.get(key, None)
        if value is None:
            raise NotImplementedError
        return value
