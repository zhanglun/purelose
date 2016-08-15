import urllib.request,json
root = 'http://api.douban.com//v2/movie/top250'


def fetchJSON ():
  response = urllib.request.urlopen(root)
  data = response.read()  # type: bytes
  string = str(data, encoding='utf-8') # type: string
  dataDict = json.loads(string) # dict
  print(dataDict)


def start():
  fetchJSON()


start()
