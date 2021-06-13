#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/5/30 2:12 下午
# @Author : mzt
# @Site : 
# @File : web.py
# @Software: PyCharm

import web
import main

urls = (
    '/(.*)', 'index'
)

# list = "123134"


class index:
    def GET(self, name):
        fo = open("index.html", 'r')

        con = fo.read()
        conlist = con.split('<br>')
        so = main.pre([1, 2, 3, 4])
        out = conlist[0] + "结果为" + str(so) + conlist[2]
        return out


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
