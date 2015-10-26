#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import web
from web.contrib.template import render_jinja

if 'SERVER_SOFTWARE' in os.environ:
    app_root = os.path.dirname(__file__)
    sys.path.insert(0, os.path.join(app_root, 'beautifulsoup4-4.4.1'))

from views import zhihudaily, music, tools
# from views import todo

headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6)Gecko/20091201 Firefox/3.5.6'}

urls = (
    '/(.*)/', 'Redirect',
    '/', 'Index',
    '/daily', zhihudaily.app,
    '/music', music.app,
    # '/todo', todo.app,
    '/tools', tools.app
)

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = render_jinja('templates', encoding='utf-8')


# Routers

class Redirect:
    def __init__(self):
        pass

    def GET(self, path):
        web.seeother('/' + path)


class Index:
    def __init__(self):
        pass

    def GET(self):
        title = u'Web实践 | 张小伦爱学习|'
        result = {}
        result['title'] = title
        return render.index(result)


app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()
elif 'SERVER_SOFTWARE' in os.environ:
    import sae

    application = sae.create_wsgi_app(app.wsgifunc())

