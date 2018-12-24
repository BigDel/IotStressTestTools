#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
2018/11/05
del
此类为控制器类,控制请求的方向并分发
"""
import tornado.web
import views
import config


class Application(tornado.web.Application):
    def __init__(self):
        handlers = {
            (r"/", views.IndexHandler),  # 首页
            (r'/Test', views.TestConnectionHandler),  # 测试连接
            (r'/PostMyPortNo', views.InitializationHandler),  # 上传基站portNo
            (r'/GetTag', views.InitializationHandler),  # 获取标签
            (r'/GetEvent', views.EventInfoHandler),  # 获取事件
            (r'/GetHb', views.HbInfoHandler),  # 获取心跳
            (r'/GetData', views.DataInfoHandler),  # 获取事件
            (r'/PostData', views.DataInfoHandler),  # 接收数据处理
        }
        super(Application, self).__init__(handlers, **config.setting)
