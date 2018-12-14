#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
2018/11/05
del
此方法为标签生产工具
"""


# 制造标签数据
def make_tags(init_tag_no, num):
    ret_l = list()
    init_no = init_tag_no
    for i in range(num):
        ret_l.append(str(init_no))
        init_no += 1
    return ret_l
