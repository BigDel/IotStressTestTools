#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
2018/11/02
del
此类为配置文件类
"""
import os

BASE_DIRS = os.path.dirname(__file__)

# 参数
options = {
    'port': 8888  # 端口
}

# 配置
setting = {
    'static_path': os.path.join(BASE_DIRS, 'static'),
    'template_path': os.path.join(BASE_DIRS, 'templates'),
    'debug': True,
    'return_message': {'Status': None, 'Msg': None, 'Tags': None}  # 返回数据
    # 'autoreload':True
}
