#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
2018/11/01
del
此类是服务启动类
"""
import tornado.ioloop
import tornado.httpserver
import config

from application import Application

if __name__ == "__main__":
    print('启动...')
    app = Application()  # 实例化application类
    httpServer = tornado.httpserver.HTTPServer(app)
    # httpServer.listen(8888)
    # 绑定端口
    httpServer.bind(config.options['port'])
    # 开启5个子进程（默认1，若为None或者小于0，开启对应硬件的CPU核心数个子进程）
    httpServer.start(1)
    tornado.ioloop.IOLoop.current().start()
