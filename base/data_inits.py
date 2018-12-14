#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
2018/11/01
del
此类是基础数据初始化类
"""

import base
import units


class data_init_(object):

    @staticmethod
    def upd_bs(dict_):
        """
        更新或者添加基站信息
        :param dict_: 字典
        """
        base.Bs.update(dict_)

    @staticmethod
    def upd_work(dict_):
        """
        添加或者更新工作字典
        :param dict_: 工作字典
        """
        base.Work.update(dict_)

    @staticmethod
    def upd_tags(dict_):
        """
        更新或者添加标签
        :param dict_: 字典
        """
        base.Tags.update(dict_)

    @staticmethod
    def upd_masterEdition(dict_):
        """
        更新或者添加模板信息
        :param dict_: 模板字典
        """
        base.MasterEdition.update(dict_)

    @staticmethod
    def upd_infusion(dict_):
        """
        输液配置信息
        :param dict_:输液配置信息字典
        :return:
        """
        base.Infusion.update(dict_)

    @staticmethod
    def upd_temperature(dict_):
        """
        体温配置信息
        :param dict_:体温配置信息字典
        :return:
        """
        base.Temperature.update(dict_)

    @staticmethod
    def upd_coldchain(dict_):
        """
        冷链配置信息
        :param dict_:冷链配置信息字典
        """
        base.Coldchain.update(dict_)

    @staticmethod
    def get_masterEdition(key_=None):
        """
        获取模板信息
        :param key_: 模板key
        :return: None或值
        """
        if key_ is None:
            return base.MasterEdition
        return base.MasterEdition.get(key_)

    @staticmethod
    def get_coldchain(key_=None):
        """
               获取冷链输液配置信息
               :param key_: 键
               """
        if key_ is None:
            return base.Coldchain
        return base.Coldchain.get(key_)

    @staticmethod
    def get_tag_type(portno):
        """
        :param portno: 标签号
        :return: 标签类型
        """
        if portno:
            taginfo = base.Tags.get(portno)
            if taginfo:
                return taginfo.get('type')
        return None

    @staticmethod
    def get_temperature(key_=None):
        """
               获取体温输液配置信息
               :param key_: 键
               """
        if key_ is None:
            return base.Temperature
        return base.Temperature.get(key_)

    @staticmethod
    def get_infusion(key_=None):
        """
               获取输液配置信息
               :param key_: 键
               """
        if key_ is None:
            return base.Infusion
        return base.Infusion.get(key_)

    @staticmethod
    def get_bs(key_=None):
        """
        :param key_:键
        :return: 返回整个字典或None或键对应的值
        """
        if key_ is None:
            return base.Bs
        return base.Bs.get(key_)

    @staticmethod
    def get_work(key_=None):
        """
        :param key_: 键
        :return: 返回整个字典或None或键对应的值
        """
        if key_ is None:
            return base.Work
        return base.Work.get(key_)

    @staticmethod
    def get_tag(key_=None):
        """
        :param key_: 键
        :return: 返回整个字典或None或键对应的值
        """
        if key_ is None:
            return base.Tags
        return base.Tags.get(key_)

    def get_tag_sq(self, portno):
        """
        获取标签的sq
        :param portno: sq
        :return:None 或者sq号
        """
        taginfo = base.Tags.get(portno)
        if taginfo:
            sq = taginfo.get('sq')
            sq_ = units.Int2all.int2hex_2(sq)  # 转化为16进制的str
            self.upd_tag_sq(portno, sq)
            return sq_
        return None

    @staticmethod
    def get_tag_id(portno):
        """
        获取tag的id
        :param portno:标签portno
        :return:
        """
        taginfo = base.Tags.get(portno)
        if taginfo:
            id_ = taginfo.get('id')
            id_ = units.Int2all.int2hex_2(id_)
            return id_
        return None

    def upd_tag_id(self, portno, id_):
        """
               更新标签id
               :param portno: 标签的portno号码
               :param id_: id号
               """
        taginfo = self.get_tag(portno)
        if taginfo:
            taginfo.update({'id': id_})

    def upd_tag_sq(self, portno, sq_):
        """
        标签标签的sq
        :param portno: 标签portno号码
        :param sq_: sq号码
        """
        if sq_ < 255:
            new_sq = sq_ + 1
        else:
            new_sq = 0
        taginfo = self.get_tag(portno)
        if taginfo:
            taginfo.update({'sq': new_sq})


class inits_(object):
    def __init__(self):
        base.data_init_.upd_masterEdition(units.ReadConfigs.get(key='MessageTemplates'))  # 初始化模板信息
        base.data_init_.upd_infusion(units.ReadConfigs.get(key='Infusion'))  # 初始化输液配置信息
        base.data_init_.upd_temperature(units.ReadConfigs.get(key='Temperature'))  # 初始化体温配置信息
        base.data_init_.upd_coldchain(units.ReadConfigs.get(key='Coldchain'))  # 初始化冷链配置信息

    @staticmethod
    def init_bs(portno, ip_='0.0.0.0'):
        """
        初始化基站信息
        :param portno: 基站的portNo
        :param ip_: ip地址
        :return:
        """
        id_ = len(base.data_init_.get_bs())
        base.data_init_.upd_bs({portno: (id_, ip_)})

    @staticmethod
    def init_tag(portno, type_):
        """
        初始化标签
        :param portno: 标签的portNo
        :param type_: 标签类型
        :return:
        """
        id_ = 0
        sq = 0
        base.data_init_.upd_tags({portno: {'id': id_, 'type': type_, 'sq': sq}})
