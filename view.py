#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/5/30 2:12 下午
# @Author : mzt
# @Site : 
# @File : web.py
# @Software: PyCharm

import web

urls = (
    '/(.*)', 'index'
)

list = "123134"

class index:
    def GET(self, name):
        fo = open("index.html", 'w+')
        fo.write("<!DOCTYPE html>\n"
                 "<html lang=\"en\">\n"
                 "<head>\n"
                 "<meta charset=\"UTF-8\">\n"
                 "<title>test</title>\n"
                 "</head>\n"
                 "<body>\n"
                 "<h1>测试</h1>\n"+list+
                 "</body>\n"
                 "</html>"
                 )
        fo.close()
        index_text = open('index.html', 'r')
        out = index_text.read()
        return out


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
