# -*- coding:utf-8 -*- 

from datetime import datetime
from flask import render_template
from flask import render_template, request, jsonify, Flask, redirect, url_for
from utils import check_signature
from response import wechat_response
from sqlite import *
import threading
import socket,select
from utils import *
import os
import time
app = Flask(__name__)

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

                if disconnected:
                    print r.getpeername(), 'disconnected'
                    inputs.remove(r)
                else:
                    print data #打印接收到的数据
  
t = threading.Thread(target=tcp_listening)
t.start()  


def send_weixin_msg_to_user(data):
    sn = redis.get(data)
    if sn == None:
        redis.set(data,data,3600)
        openids = queryOpenID(DataBasePath,data)
        wechat = init_wechat_sdk()
        content = u"主人，家里缺水了，我将为你安排送水师傅尽快送水上门，如果暂时不需要送水，请回复N"
        try:
            if openids != None:
                for openid in openids:
                    result = wechat.send_template_message(str(openid[0]),"Sh1SCvFf3csFGpqwBGZM5Q27n99ZJF2njPijyY59DPA", wechat_template_message())
        except Exception,e:
            print e

def wechat_template_message():
    data = {
                "first": {
                    "value": "主人，家里缺水了。",
                    "color": "#173177"
                },
                "keyword1":{
                    "value": "云南山泉",
                    "color": "#173177"
                },
                "keyword2": {
                    "value": time.strftime('%Y-%m-%d %X',(time.localtime())),
                    "color": "#173177"
                },
                "remark":{
                    "value": "我们将为你安排送水师傅尽快送水上门，如果暂时不需要送水，请回复N",
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

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=False)
