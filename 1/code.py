#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import urllib2
import urllib
import re
import time
import json

import web
from web.contrib.template import render_jinja

from views import zhihudaily
from views import music

headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6)Gecko/20091201 Firefox/3.5.6'}

urls = (
    '/(.*)/', 'Redirect',
    '/', 'Index',
    '/movie', 'Movie',
    '/user', 'User',
    '/daily', zhihudaily.app,
    '/music', music.app,
    '/test', 'Gitcafe'
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
        title = 'Web实践 | 张小伦爱学习|'
        return render.index()


class Movie:
    def __init__(self):
        pass

    def GET(self):

        return render.movie()


class User:
    def __init__(self):
        pass

    def GET(self):
        return 'Hello, user!'

    def POST(self):
        return 'Hey, man!'

class Gitcafe:
    def __init__(self):
        pass

    def GET(self):
        return 'Hello, test for gitcafe!'


app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()
elif 'SERVER_SOFTWARE' in os.environ:
    import sae
    application = sae.create_wsgi_app(app.wsgifunc())


# this is the head link