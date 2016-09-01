# -*- coding:utf-8 -*- 
from utils import init_wechat_sdk
from sqlite import *
import re,os

curentpath = os.getcwd()
DataBasePath = curentpath + '/test/UserInfo.db'

def wechat_response(data):
    global message, openid, wechat

    wechat = init_wechat_sdk()
    wechat.parse_data(data)
    message = wechat.get_message()
    openid = message.source

    try:
        get_resp_func = msg_type_resp[message.type]
        response = get_resp_func()
    except KeyError:
        response = 'success'
    return response

msg_type_resp = {}

def set_msg_type(msg_type):
    def decorator(func):
        msg_type_resp[msg_type] = func
        return func
    return decorator

@set_msg_type('subscribe')
def subscribe_resp():
    response = subscribe()
    return response

@set_msg_type('text')
def text_resp():
    commands = {
        "szxm": set_user_name,
        "szdz": set_user_address,
        "szdh": set_user_phone_number,
        "bdsn": binding_sn
    }
    response = 'UnkownCommand'
    for key_word in commands:
        if re.match(key_word,message.content):
            response = commands[key_word]()
            break
    return response


@set_msg_type('click')
def click_resp():
    """菜单点击类型回复"""
    commands = {
        'Account_Info': account_info,
        'Balance_Inquiry': balance_inquiry,
        'Account_Recharge': account_recharge,
        'Command_Info': command_info,
        'Member_Activity': member_activity,
        'Failure_Report': failure_report
    }
    response = commands[message.key]()
    return response

def subscribe():
    content =u"您好，欢迎来到世纪青年送水站！"
    data = []
    insertDataInDB(DataBasePath,message)
    return wechat.response_text(content)

def set_user_name():
    """设置用户姓名"""
    username = message.content[4:]
    username = username.strip()    
    result = updataDataInDB(DataBasePath,message.source,username,None,None,None)
    if result == True:
        content = u"姓名，设置成功！"
    else:
        content = u"姓名，设置失败！"
    return wechat.response_text(content)

def set_user_address():
    """设置用户地址"""
    address = message.content[4:]
    address = address.strip()
    result = updataDataInDB(DataBasePath,message.source,None,address,None,None)
    if result == True:
        content = u"地址，设置成功！"
    else:
        content = u"地址，设置失败！"
    return wechat.response_text(content)

def set_user_phone_number():
    """设置用户电话"""
    phonenumber = message.content[4:]
    phonenumber = phonenumber.strip()
    result = updataDataInDB(DataBasePath,message.source,None,None,phonenumber,None)
    if result == True:
        content = u"电话，设置成功！"
    else:
        content = u"电话，设置失败！"
    return wechat.response_text(content)

def binding_sn():
    """绑定SN"""
    sn = message.content[4:]
    sn = sn.strip()
    result = updataDataInDB(DataBasePath,message.source,None,None,None,sn)
    if result == True:
        content = u"SN，绑定成功！"
    else:
        content = u"SN，绑定失败！"
    return wechat.response_text(content)

def account_info():
    """查看账户信息，包括openid，姓名，地址，手机号"""
    result = queryDB(DataBasePath,message.source)
    if len(result) == 1:
        content = u"姓名:  " + result[0][1] + "\r\n" + u"地址:  " + result[0][2] + "\r\n" + u"电话:   " + result[0][3] + "\r\n" + u"SN:   " + result[0][4] + "\r\n"
    return wechat.response_text(content)

def balance_inquiry():
    """查看账户余额"""
    content = u"该功能尚未开通"
    return wechat.response_text(content)

def account_recharge():
    """账户充值"""
    content = u"该功能尚未开通"
    return wechat.response_text(content)

def command_info():
    """命令说明"""
    content = u"输入：szxm + 姓名，设置用户名称\r\n输入：szdz + 地址，设置用户地址\r\n输入：szdh + 电话，设置用户电话\r\n输入：bdsn + SN号码，设置用户SN\r\n"
    return wechat.response_text(content)

def member_activity():
    """会员活动"""
    content = u"该功能尚未开通"
    return wechat.response_text(content)

def failure_report():
    """故障报修"""
    content = u"请拨打12345热线，报修故障"
    return wechat.response_text(content)
