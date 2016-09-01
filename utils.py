from wechat_sdk import WechatBasic,WechatConf
from functools import wraps
from flask import request, redirect
from redis import Redis

redis = Redis()

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
        conf = WechatConf(token="sjqn",
                          appid="wx90e00269b4fcf1da",
                          appsecret="72a8ceb65843072e7c5fa01e1f3ce21b",
                          access_token=access_token,
                          access_token_expires_at=redis.ttl("wechat:access_token"))
        wechat = WechatBasic(conf=conf)
    else:
        conf = WechatConf(token="sjqn",
                          appid="wx90e00269b4fcf1da",
                          appsecret="72a8ceb65843072e7c5fa01e1f3ce21b")
        wechat = WechatBasic(conf=conf)
        access_token = wechat.get_access_token()
        print 'new'
        redis.set("wechat:access_token",access_token['access_token'],7000)
    print access_token
    return wechat