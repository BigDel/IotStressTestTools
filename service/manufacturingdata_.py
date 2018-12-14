#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
2018/11/01
del
数据制造类
"""
import random
import re
import units

import base
import threading


class Manufacturingdata_(object):
    Lock = threading.Lock()  # 设定锁

    # 选择模板并制造数据
    def selct_template(self, data_type, dict_):
        if data_type is None:
            return 1, None
        else:
            if data_type == 0:
                temp = base.data_init_.get_masterEdition('BaseStationHeartbeat')  # 基站心跳模板
            elif data_type == 1:
                temp = base.data_init_.get_masterEdition('TaggedHeartbeat')  # 标签心跳模板
            elif data_type == 2:
                temp = base.data_init_.get_masterEdition('ActionRequest')  # action请求
            elif data_type == 3:
                temp = base.data_init_.get_masterEdition('TagData')  # 标数据模板
            elif data_type == 4:
                temp = base.data_init_.get_masterEdition('TagEvent')  # 标签事件数据
            elif data_type == 5:
                temp = base.data_init_.get_masterEdition('ResponseGetServer')  # 获取参数返回
            elif data_type == 6:
                temp = base.data_init_.get_masterEdition('ResponseSetServer')  # 设置参数返回
            else:
                temp = base.data_init_.get_masterEdition('HairMedicine')  # 下达用药数据返回
        return self.make_msg(temp, dict_)
        # 制造数据

    # 数据生成
    def make_msg(self, template, dict_):
        new_data = ""
        bs_port_no = dict_.get('myPortNo')
        tag_port_no = dict_.get('tagPortNo')
        event_ = dict_.get('event_')
        working_mode = dict_.get('modes')
        action_sq = dict_.get('actionSq')
        self.Lock.acquire()
        if bs_port_no is not None and '<00>' in template:
            new_data = re.sub('<00>', bs_port_no, template)
        if tag_port_no is not None and '<01>' in new_data:
            new_data = re.sub('<01>', tag_port_no, new_data)
        if '<02>' in new_data:
            if action_sq is None:
                sq_ = base.DataInit.get_tag_sq(tag_port_no)
            else:
                sq_ = action_sq
            if sq_ is None:
                self.Lock.release()
                return 1, None
            new_data = re.sub('<02>', sq_, new_data)
        if '<03>' in new_data:
            id_ = base.data_init_.get_tag_id(tag_port_no)
            if id_ is None:
                self.Lock.release()
                return 1, None
            new_data = re.sub('<03>', id_, new_data)
        if '<05>' in new_data and working_mode is not None:
            new_data = re.sub('<05>', working_mode, new_data)
        if '<06>' in new_data:
            specific_value = self.generate_data_values(tag_port_no)
            if specific_value is False:
                self.Lock.release()
                return 1, None
            elif specific_value is None:
                self.Lock.release()
                return 2, 'End'
            new_data = re.sub('<06>', specific_value, new_data)
        if '<08>' in new_data and event_ is not None:
            eventJdata = self.event_tag(tag_port_no, event_)
            if eventJdata is None:
                self.Lock.release()
                return 1, None
            new_data = re.sub('<08>', eventJdata, new_data)
        if '<07>' in new_data:
            len_ = int(((len(new_data) - 2) / 2) - 2)
            len_ = units.Int2all.int2hex_2(len_)
            if len_ is not False:
                new_data = re.sub('<07>', str(len_), new_data)
        if '<04>' in new_data:
            new_data = re.sub('<04>', self.get_crc(
                re.sub(r'(?<=\w)(?=(?:\w\w)+$)', " ", re.search('3E(.*)<04>', new_data).group(1)).upper()),
                              new_data)
            self.Lock.release()
            return 0, re.sub(r'(?<=\w)(?=(?:\w\w)+$)', " ", new_data).upper()

    # 制造输液、体温、冷链基础数据
    def generate_data_values(self, tag_port_no):
        tag_type = base.data_init_.get_tag_type(tag_port_no)
        if tag_type == 'Infusion':  # 4个字节
            specific_values = self.infusion_(tag_port_no)
        elif tag_type == 'Temperature':  # 3个字节
            specific_values = self.temperature_()
        else:
            specific_values = self.cold_chain_(tag_type)
        return specific_values

        # 输液

    # 制造数据数据
    @staticmethod
    def infusion_(tag_port_no):
        dict_infusion_ = base.data_init_.get_work(tag_port_no)  # 获取输液的工作字典
        if dict_infusion_ is not None:
            drip_speed = dict_infusion_.get('Dripspeed')  # 滴速
            remaining_capacity = dict_infusion_.get('Remainingcapacity')  # 当前剩余容量
            if remaining_capacity <= base.data_init_.get_infusion('Endml'):
                return None
            reduced_amount = round(drip_speed * 0.05, 2)  # 求容量减少量
            remaining_capacity = remaining_capacity - reduced_amount  # 减少后剩余容量
            dict_infusion_.update({'Remainingcapacity': remaining_capacity})
            base.data_init_.upd_work({tag_port_no: dict_infusion_})  # 更新容量信息
            digit = int(round(remaining_capacity - int(remaining_capacity), 2) * 10)  # 个位数
            hundred = int(remaining_capacity) // 265  # 百位数
            ten = int(remaining_capacity - (hundred * 256))  # 十位数
            real_data = units.Int2all.int2hex_2(hundred) + units.Int2all.int2hex_2(
                ten) + units.Int2all.int2hex_2(digit) + units.Int2all.int2hex_2(drip_speed)
            return real_data  # 输液数据
        return False

        # 体温

    # 制造体温数据
    @staticmethod
    def temperature_():
        temperatures = base.data_init_.get_temperature('Temperaturerange')  # 获取体温温度取值的区间
        temperature = round(random.uniform(temperatures[0], temperatures[1]), 2)  # 随机体温
        ten = int(temperature)  # 获取十位数
        decimal = int((temperature - ten) * 10)  # 获取个位数
        temperature = units.Int2all.int2hex_2(ten) + units.Int2all.int2hex_2(decimal)  # 转换拼接温度
        return temperature  # 温度值

        # 冷链

    # 制造冷链数据
    @staticmethod
    def cold_chain_(tag_type):
        if tag_type == "One-pieceColdChain":  # 一体冷链
            One_pCC = base.data_init_.get_coldchain('One-pieceColdChain')
            humiditys = One_pCC.get('humidity')  # 获取湿度区间
            humidity = random.randint(humiditys[0], humiditys[1])  # 获取湿度
            humidity = units.Int2all.int2hex_2(humidity)  # 转换湿度为16进制
            temperatures = One_pCC.get('temperature')  # 获取温度范围
            temperature = round(random.uniform(temperatures[0], temperatures[1]), 2)  # 获取温度
            ten = int(temperature)  # 取值温度（十位数）
            decimal = int(round(temperature - ten, 2) * 10)  # 取温度的个位数
            if ten > 0:  # 如果十位数为负数的话数反转，反之直接计算
                ten = units.Int2all.int2hex_2(ten % 256)  # 负数反转
            else:
                ten = units.Int2all.int2hex_2(ten)
            if decimal > 0:  # 如果个位数小于0则进行负数反转，反之则直接计算
                decimal = units.Int2all.int2hex_2(decimal % 256)  # 负数反转
            else:
                decimal = units.Int2all.int2hex_2(decimal)
            return ten + decimal + humidity  # 返回数据为温度加湿度  表现为 十位数+个位数+湿度
        elif tag_type == "ProbeTypeColdChain":  # 探针冷链
            PTCC = base.data_init_.get_coldchain('ProbeTypeColdChain')  # 探针冷链
            temperatures = PTCC.get('temperature')  # 获取温度范围
            temperature = round(random.randint(temperatures[0], temperatures[1]), 2)  # 随机获取温度
            ten = int(temperature)  # 十位数
            decimal = int(round(temperature - ten, 2) * 10)  # 个位数
            temperature = units.Int2all.int2hex_2(ten) + units.Int2all.int2hex_2(decimal)  # 温度值
            return temperature  # 温度值

    # 标签事件制造
    @staticmethod
    def event_tag(tag_post_no, event_num):
        """
        :param tag_post_no: 标签的portno号
        :param event_num: 事件代码：01 输液开始 02 输液结束，04 输液中断（未写），10 低电量（未写）
        :return: 标签事件加data
        """
        if event_num is not None:
            events_ = event_num
            if event_num == '01':  # 输液开始
                type_ = random.sample(base.data_init_.get_infusion('Type'), 1)  # 随机获取包装类型
                type_ = type_.pop()
                data = random.sample(base.data_init_.get_infusion('Size').keys(), 1)  # 随机获取包装大小
                data = data.pop()
                events_ += type_ + data  # 包装类型和包装大小（已经转换成16进制的str）
                size = base.data_init_.get_infusion('Size').get(data)  # 通过包装类型获取输液瓶容量
                dripspeeds = base.data_init_.get_infusion('Dripspeed')  # 获取滴速范围
                dripspeed = random.randint(dripspeeds[0], dripspeeds[1])  # 随机滴速  后续加滴速仿真
                work_dict = {
                    tag_post_no: {'Size': size, 'Dripspeed': dripspeed, 'Remainingcapacity': size}}  # 包装类型 ，滴速，剩余容量
                base.data_init_.upd_work(work_dict)  # 更新或者添加工作字典
            elif event_num == '02':
                events_ = event_num
            return events_  # 返回事件和事件数据没有则只返回事件
        else:
            return None

    # 获取crc
    def get_crc(self, buf):
        try:
            crc_reg = hex(self._crc_16_ccitt_(buf))  # 计算crc
            return units.Int2all.int2hex_4(crc_reg)  # 返回4位数的16进制str类型的crc值
        except Exception as ex:
            print(ex)

    # 计算crc buf:16进制
    @staticmethod
    def _crc_16_ccitt_(buf):
        """
        :param buf:需要计算的值
        :return:crc值
        """
        try:
            buf = bytes.fromhex(buf)
            crc_reg = 0x0000
            for i in range(len(buf)):
                CURRENT = buf[i]
                for j in range(8):
                    if (crc_reg ^ CURRENT) & 0x0001 != 0:
                        crc_reg = (crc_reg >> 1) ^ 0x8408
                    else:
                        crc_reg >>= 1
                    CURRENT >>= 1
            return crc_reg
        except Exception as ex:
            print(ex)
