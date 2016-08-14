import urllib.request,json
root = 'https://api.douban.com/v2/movie/search?tag=%E5%96%9C%E5%89%A7'


def fetchJSON ():
  response = urllib.request.urlopen(root)
  data = response.read()  # type: bytes
  string = str(data, encoding='utf-8') # type: string
  dataDict = json.loads(string) # dict
  print(type(dataDict))


def start():
  fetchJSON()


start()
