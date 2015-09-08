#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __init__ import *

urls = (
    # daily route
    '', 'Daily',
    # zhihu API
    '/api/save_image', 'SaveImage',
    '/api/start_image', 'APIStartImage',
    '/api/news_latest', 'APINewsLatest',
    '/api/news_hot', 'APINewsHot',
    '/api/news_sections', 'APINewsSections'
)

# variable
imagePath = './static/images'
APIPaths = {
    'start_image': 'http://news-at.zhihu.com/api/3/start-image/1080*1776',
    'news_latest': 'http://news-at.zhihu.com/api/3/news/latest',
    'news_hot': 'http://news-at.zhihu.com/api/3/news/hot',
    'news_sections': 'http://news-at.zhihu.com/api/3/sections'
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6)Gecko/20091201 Firefox/3.5.6'}


app = web.application(urls, locals())

# methods

def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isexists = os.path.exists(path)
    # 判断结果
    if not isexists:
        # 如果不存在则创建目录
        print path + u' 创建成功'
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print path+ u' 目录已存在'
        return False


def saveimagetostorage(url):
    # 去掉 ‘http://’
    file_path = url[6:]

    dir_path = re.match(r'/\w+(\.\w+){0,}\/', file_path).group(0)
    # 获取文件名
    file_name = file_path[len(dir_path):]
    # 文件目录
    save_path = imagePath + dir_path

    if 'SERVER_SOFTWARE' in os.environ:
        # import sae
        from sae.storage import Bucket
        bucket = Bucket("zhihudaily")
        # 存取一个文件到bucket中
        fr = urllib.urlopen(url)
        stream = fr.read()
        bucket.put_object(dir_path[1:] + file_name, stream)
        return bucket

    else:
        mkdir(save_path)
        urllib.urlretrieve(url, imagePath + file_path)
        return "LocalHost"


class Daily:
    def __init__(self):
        pass

    def GET(self):
        return render.zhihu()


# zhihu API
class APIStartImage:
    def __init__(self):
        pass

    def GET(self):
        req = urllib2.Request(url=APIPaths['start_image'], headers=headers)
        stream = urllib2.urlopen(req)
        start_image = json.load(stream)
        start_image = json.dumps(start_image, encoding='utf-8')
        start_image = start_image.replace('"img": "http://', '"img": "http://pureloser-zhihudaily.stor.sinaapp.com/')
        return start_image


class APINewsLatest:
    def __init__(self):
        pass

    def GET(self):
        req = urllib2.Request(url=APIPaths['news_latest'], headers=headers)
        stream = urllib2.urlopen(req)
        # to dict
        news_latest = json.load(stream)
        # to json
        news_latest = json.dumps(news_latest, encoding='utf-8')
        # replace image url
        news_latest = news_latest.replace('"images": ["http://', '"images": ["http://pureloser-zhihudaily.stor.sinaapp.com/')
        return news_latest


class APINewsHot:
    def __init__(self):
        pass

    def GET(self):
        req = urllib2.Request(url=APIPaths['news_hot'], headers=headers)
        stream = urllib2.urlopen(req)
        # to dict
        news_hot = json.load(stream)
        # to json
        news_hot = json.dumps(news_hot, encoding='utf-8')
        # replace image url
        news_hot = news_hot.replace('"thumbnail": "http://','"thumbnail": '
                                                           '"http://pureloser-zhihudaily.stor.sinaapp.com/')
        return news_hot


class APINewsSections:
    def __init__(self):
        pass

    def GET(self):
        req = urllib2.Request(url=APIPaths['news_sections'], headers=headers)
        stream = urllib2.urlopen(req)
        news_sections = json.load(stream)
        news_sections = json.dumps(news_sections, encoding='utf-8')
        return news_sections


class SaveImage:
    def __init__(self):
        pass

    def GET(self):
        # start image
        print APIPaths['start_image']
        req = urllib2.Request(url=APIPaths['start_image'], headers=headers)
        print req
        stream = urllib2.urlopen(req)
        start_image = json.load(stream)
        saveimagetostorage(start_image['img'])
        # news latest
        req = urllib2.Request(url=APIPaths['news_latest'], headers=headers)
        stream = urllib2.urlopen(req)
        news_latest = json.load(stream)
        top_news_list = news_latest['top_stories']

        for item in news_latest['top_stories']:
            data = saveimagetostorage(item['image'])

        for item in news_latest['stories']:
            if item.get('images') is not None:
                for url in item['images']:
                    data = saveimagetostorage(url)

        # return "Done"
        print "clock2:%s" % time.clock()
        if 'SERVER_SOFTWARE' in os.environ:
            # from sae.storage import Bucket
            # bucket = Bucket("zhihudaily")
            # # 存取一个文件到bucket中
            # updatetime = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
            # bucket.put_object("log/"+updatetime+".txt", updatetime+"\n")
            return "SAE"+" Update Time:"+time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
        else:
            return "LocalHost"+" Update Time:"+time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())


