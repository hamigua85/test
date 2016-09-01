from wechat_sdk import WechatBasic
from functools import wraps
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
    wechat = WechatBasic(   token="sjqn",
                            appid="wx90e00269b4fcf1da",
                            appsecret="72a8ceb65843072e7c5fa01e1f3ce21b")
    return wechat