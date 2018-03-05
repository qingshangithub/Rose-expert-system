#!flask/bin/env python
#coding:utf-8

__author__ = 'kikay'

from flask import Flask
from flask.ext.bootstrap import Bootstrap

#定义app对象
app=Flask(__name__)
#定义Bootstrap对象
bootstrap=Bootstrap(app)
#启动配置文件
app.config.from_object('config')

from app import views