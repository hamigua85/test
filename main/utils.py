#!/usr/bin/env python
# -*- coding: utf-8 -*-
from wechat_sdk import WechatBasic,WechatConf
from functools import wraps
from . import app,redis
from flask import request, redirect

def check_signature(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        signature = request.args.get('signature', '')
        timestamp = request.args.get('timestamp', '')
        nonce = request.args.get('nonce', '')

        wechat = init_wechat_sdk()
        if not wechat.check_signature(signature=signature,
                                      timestamp=timestamp,
                                      nonce=nonce):
            if request.method == 'POST':
                return "signature failed"
            else:
                return redirect("http://baidu.com")

        return func(*args, **kwargs)

    return decorated_function

def init_wechat_sdk():
    access_token = redis.get("wechat:access_token")
    if access_token != None:
        conf = WechatConf(token=app.config['TOKEN'],
                          appid=app.config['APP_ID'],
                          appsecret=app.config['APP_SECRET'],
                          access_token=access_token,
                          encrypt_mode="normal",
                          access_token_expires_at=redis.ttl("wechat:access_token"))
        wechat = WechatBasic(conf=conf)
    else:
        conf = WechatConf(token=app.config['TOKEN'],
                          appid=app.config['APP_ID'],
                          encrypt_mode="normal",
                          appsecret=app.config['APP_SECRET'])
        wechat = WechatBasic(conf=conf)
        access_token = wechat.get_access_token()
        redis.set("wechat:access_token",access_token['access_token'],7000)
    return wechat