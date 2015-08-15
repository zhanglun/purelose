#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import urllib2
import urllib
import re
import time

from bson import json_util, ObjectId
import json

import datetime
import web
from web.contrib.template import render_jinja

from pymongo import MongoClient
client = MongoClient('mongodb://localhost', 27017)

from views import zhihudaily, music, todo

headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6)Gecko/20091201 Firefox/3.5.6'}

urls = (
    '/(.*)/', 'Redirect',
    '/', 'Index',

    '/movie', 'Movie',
    '/user', 'UserList',
    '/u/(.+)', 'User',
    '/hello-demo', 'HelloDemo',
    '/songs', 'Song',
    '/todo', todo.app,
    '/daily', zhihudaily.app,
    '/music', music.app
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

class HelloDemo:
    def __init__(self):
        pass

    def GET(self):
        return render.hellodemo()



class Song:
    def __init__(self):
        pass


    def GET(self):
        return '[{"name": "Shake", "artist": "zhanglun"}]'


    def POST(self):
        # db = client['bone']
        # SongList = db.Song

        # SongList.insert()

        data = web.data()
        print data
        return data


class Movie:
    def __init__(self):
        pass

    def GET(self):
        return render.movie()


class User:
    def __init__(self):
        pass

    def GET(self, userid):
        data = {'userid': userid}
        return render.user(data=data)

    def POST(self):
        pass


class UserList:
    def __init__(self):
        pass

    def GET(self):
        db = client['bone']
        alluserobj = db.Users.find()
        result = []
        print datetime.datetime.utcnow()
        print str(datetime.datetime.utcnow())

        for item in alluserobj:
            item['_id'] = str(item['_id'])
            result.append(item)

        return json.dumps(result)

    def POST(self):

        db = client['bone']
        # data = dict(web.data())
        user = json.loads(web.data())
        user['createtime'] = str(datetime.datetime.now())
        users_collection = db.Users
        check = db.Users.find_one({'name': user[u'name']})

        if check is None:
            user_id = users_collection.insert(user)
            return 'Hey, man! %s, your id: %s' % (user[u'name'], user_id)
        else:
            return "already existed!"


app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()
elif 'SERVER_SOFTWARE' in os.environ:
    import sae

    application = sae.create_wsgi_app(app.wsgifunc())
