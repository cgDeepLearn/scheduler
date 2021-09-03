"""
@Author: cgDeepLearn
@Contact:cglearningnow@163.com
@File: api.py
@Time: 2021/9/1 15:48

@docstring: 
"""
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from utils.decorator import format_result
from flask_restful import Resource
from .views import HelloView


class HelloAPI(Resource):
    @format_result
    def get(self):
        res = HelloView.response()
        return res


def hello_add_resources(api):
    api.add_resource(HelloAPI, '/hello')
