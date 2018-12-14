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
            (r"/", views.IndexHandler),
            (r'/Test', views.TestConnectionHandler),
            (r'/PostMyPortNo', views.InitializationHandler),
            (r'/GetTag', views.InitializationHandler),
            (r'/GetEvent', views.EventInfoHandler),
            (r'/GetHb', views.HbInfoHandler),
            (r'/GetData', views.DataInfoHandler),
            (r'/PostData', views.DataInfoHandler),
        }
        super(Application, self).__init__(handlers, **config.setting)
