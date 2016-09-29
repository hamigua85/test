#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import app,redis
from utils import check_signature
from response import wechat_response
from accessDataBase import *
import threading
import socket,select
from utils import *
import os
import time

curentpath = os.getcwd()
DataBasePath = curentpath + '/UserInfo.db'

def tcp_listening():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  #生成socket对象
  
    port = 30001  
    s.bind(("0.0.0.0", port)) #绑定套接字接口地址
    s.listen(5)          #开始服务器端监听
      
    inputs = [s]  
    while True:
        rs, ws, es = select.select(inputs, [], []) #使用select方法
        for r in rs:
            if r is s:
                c, addr = s.accept() #处理连接
                print 'Get connection from', addr
                inputs.append(c)
            else:
                try:
                    data = r.recv(1024) #接收数据
                    if data != "":
                        data = str(data).strip()
                        send_weixin_msg_to_user(data)
                    disconnected = not data
                except Exception, e:
                    disconnected = True
                try:
                    if disconnected:
                        print r.getpeername(), 'disconnected'
                        inputs.remove(r)
                    else:
                        print data #打印接收到的数据
                except Exception, e:
                    print e
  
t = threading.Thread(target=tcp_listening)
t.start()  

def send_weixin_msg_to_user(data):
    sn = redis.get(data)
    if sn == None:
        redis.set(data,data,3600)
        openids = queryOpenID(DataBasePath,data)
        wechat = init_wechat_sdk()
        try:
            if openids != None:
                for openid in openids:
                    result = wechat.send_template_message(str(openid[0]),app.config['WEIXIN_TEMPLATE_MSG_ID'], wechat_template_message())
        except Exception,e:
            print e

def wechat_template_message():
    data = {
                "first": {
                    "value": app.config['WEIXIN_TEMPLATE_MSG_FIRST'],
                    "color": "#173177"
                },
                "keyword1":{
                    "value": app.config['WEIXIN_TEMPLATE_MSG_KEYWORD1'],
                    "color": "#173177"
                },
                "keyword2": {
                    "value": time.strftime('%Y-%m-%d %X',(time.localtime())),
                    "color": "#173177"
                },
                "remark":{
                    "value": app.config['WEIXIN_TEMPLATE_MSG_REMARK'],
                    "color": "#173177"
                }
            }
    return data


@app.route('/',methods=['POST', 'GET'])
@check_signature
def handle_wechat_request():
    """
    response weixin message
    """
    if request.method == 'POST':
        return wechat_response(request.data)
    else:
        return request.args.get('echostr', '')
