#!/usr/bin/env python
# -*- coding: utf-8 -*-

DEBUG = False

WELCOME_TEXT = u"您好，欢迎来到世纪青年送水站！"

#微信消息模板
WEIXIN_TEMPLATE_MSG_ID = "Sh1SCvFf3csFGpqwBGZM5Q27n99ZJF2njPijyY59DPA"
WEIXIN_TEMPLATE_MSG_FIRST = u"主人，家里缺水了。"
WEIXIN_TEMPLATE_MSG_KEYWORD1 = u"珍茗金龙水。"
WEIXIN_TEMPLATE_MSG_REMARK = u"我们将为你安排送水师傅尽快送水上门，如果暂时不需要送水，请回复N。如果需设定送水时间，例如09:00送到，请回复0900。"

#回复信息
COMMAND_INFO = u"szxm + 姓名，设置用户名称\r\nszdz + 地址，设置用户地址\r\nszdh + 电话，设置用户电话\r\nbdsn + SN，设置用户SN\r\n"
WATER_DELIVERY_TIME = u"主人，您的预约已收到，我们将在 %02d:%02d 为您送达。"
WATER_DELIVERY_TIME_EER = u"输入有误，例如需要在09:00送达，请输入0900。"
CANCEL_DELIVERY = u"您已取消了本次送水。"
FAILURE_REPORT = u"请拨打12345热线，报修故障"
