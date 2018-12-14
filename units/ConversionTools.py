#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
2018/11/05
del
此类为字符转换工具类
"""


class Int2all(object):
    def __init__(self):
        pass

    # int转hex位数为2
    @staticmethod
    def int2hex_2(num):
        hex_num = hex(num)
        if len(hex_num) == 3:
            return str(hex_num).replace('x', '')
        return hex_num[2:]

    # int 转hex位数为4
    @staticmethod
    def int2hex_4(num):
        len_num = len(num)
        if len_num == 3:
            nun = str(num).replace('x', '00')
        elif len_num == 4:
            nun = str(num).replace('x', '0')
        elif len_num == 5:
            nun = str(num).replace('x', '')
        else:
            nun = num[2:4] + num[4:]
        return nun


"""
此类为偏移类，使数据看上去更加真实。主要用于体温监护体温偏移计算，冷链温度、湿度偏移计算
"""


# 数据偏移增长
class Transfer(object):
    def __init__(self):
        pass

    # 体温
    def Temperature(self):
        pass

    # 冷链
    def Cold_chain(self):
        pass

    # 温度上升
    def temperature_up(self, tag_type):
        pass

    # 湿度变化
    def humidity_change(self):
        pass
