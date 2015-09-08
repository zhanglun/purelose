#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __init__ import *

app_path = os.getcwd()

media_path = os.path.join(app_path, 'static', 'media')


def readfiles(dir):
    result = []
    for filename in os.listdir(dir):
        result.append(filename)
    return result

urls = (
    '', 'Music'
)

app = web.application(urls, locals())


class Music:
    def __init__(self):
        pass

    def GET(self):
        readfiles(media_path)
        data = {}
        data['songlist'] = readfiles(media_path)
        return render.music(data=data)




