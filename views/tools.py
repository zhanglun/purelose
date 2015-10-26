#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __init__ import *
from bs4 import BeautifulSoup

app_path = os.getcwd()

media_path = os.path.join(app_path, 'static', 'media')

headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6)Gecko/20091201 Firefox/3.5.6'}

imagePath = './static/images'
url_aladd_image = 'http://aladd.net/datu'


def readfiles(dir):
    result = []
    for filename in os.listdir(dir):
        result.append(filename)
    return result


urls = (
    '', 'Tools',
    '/aladd/images_everyday', 'AladdImages'
)

app = web.application(urls, locals())


def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号

    print(path)
    path = path.rstrip("\\")
    print(path)

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
        print path + u' 目录已存在'
        return False


# 获取 aladd 每日图片 url
def getAladdImageUrlList():
    req = urllib2.Request(url=url_aladd_image, headers=headers)
    stream = urllib2.urlopen(req)
    page = BeautifulSoup(stream, 'html.parser')
    page = page.body.find_all('div', class_='page')
    urls = []
    page = page[0]
    img_list = page.find_all('img')
    for img in img_list:
        urls.append(img.get('src'))
    return urls


# 保存图片
def saveAladdImages(url, path):
    # 去掉 ‘http://’
    file_path = url[6:]

    # 获取文件名
    file_name = re.search(r'[0-9a-zA-Z]*\.(jpg|png|jpeg)', file_path).group()
    print file_name
    # YYYY-MM-DD
    ctime = time.strftime('%Y/%m/%d', time.localtime())
    # 文件目录
    save_path = imagePath + '/Aladd/' + ctime + '/'

    if 'SERVER_SOFTWARE' in os.environ:
        # import sae
        from sae.storage import Bucket
        bucket = Bucket("album")
        # 存取一个文件到bucket中
        fr = urllib.urlopen(url)
        stream = fr.read()
        bucket.put_object('Aladd/' + ctime + '/' + file_name, stream)
        return bucket

    else:
        mkdir(save_path)
        urllib.urlretrieve(url, save_path + file_name)
        return "LocalHost"


class Tools:
    def __init__(self):
        pass

    def GET(self):
        return 'Tools!!'


# Aladd 每日大图
class AladdImages:
    def __init__(self):
        pass

    def GET(self):
        imgs = getAladdImageUrlList()
        for url in imgs:
            saveAladdImages(url, '')

        return u'Aladd 每日大图'
