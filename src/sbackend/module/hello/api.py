"""
@Author: cgDeepLearn
@Contact:cglearningnow@163.com
@File: api.py
@Time: 2021/9/1 15:48

@docstring: 
"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask_restful import Resource
from .views import HelloView


class HelloAPI(Resource):
    def get(self):
        return HelloView.response()


def hello_add_resources(api):
    api.add_resource(HelloAPI, '/hello')
