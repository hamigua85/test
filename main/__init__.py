#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from redis import Redis

app = Flask(__name__, instance_relative_config=True)
# 加载配置
app.config.from_object('config')
app.config.from_pyfile('config.py')

redis = Redis()

from main.routes import *
