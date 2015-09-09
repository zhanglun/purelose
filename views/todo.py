#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __init__ import *
from bson import json_util, ObjectId
from pymongo import MongoClient

client = MongoClient('mongodb://localhost', 27017)
db = client['bone']

urls = (
    '', 'TodoApp',
    '/item', 'Todo',
    '/item/(\d+\w+)', 'TodoItem',
    '/list', 'TodoList',
)


app = web.application(urls, locals())


class TodoList:
    def __init__(self):
        pass

    def GET(self):
        list = db.Todo.find()
        print list
        result = []
        for item in list:
            result.append({
                'id': str(item['_id']),
                'title': item['title'],
                'order': item['order'],
                'done': item['done']
            })
        return json_util.dumps(result)

    def POST(self):
        list_len = db['Todo'].find().count()
        data = web.data()
        data = json.loads(data)
        data['order'] = list_len + 1
        return data


class TodoItem:
    def __init__(self):
        pass

    def GET(self, item_id=None):
        db = client['bone']
        result = None;
        item = db.Todo.find_one(id=item_id)
        if item is not None:
            print item
            result = {
                'id': str(item['_id']),
                'title': item['title'],
                'order': item['_order'],
                'done': item['done'] == 1
            }
            return json.dumps(result)
        else:
            return {}

    def POST(self, item_id=None):
        return item_id

    def PUT(self, item_id=None):
        db = client['bone']
        data = web.data()
        item = json.loads(data)
        item['_order'] = item.pop('order')
        # update collection
        db['Todo'].update({'_id': ObjectId(item['id'])}, {'$set': {'done': item['done'], 'title': item['title']}})
        return "success"

    def DELETE(self, item_id=None):
        db['Todo'].remove({'_id': ObjectId(item_id)})
        return 'delete'

class TodoApp:
    def __init__(self):
        pass

    def GET(self):
        return render.todo()

    def POST(self):
        return 'post'


class Todo:
    def __init__(self):
        pass

    def GET(self):
        return ''

    def POST(self):
        list_len = db['Todo'].find().count()
        data = web.data()
        data = json.loads(data)
        print '---------------'
        print type(data)
        data['order'] = list_len + 1
        print db['Todo'].insert(data)
        print data
        return data
