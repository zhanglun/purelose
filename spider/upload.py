# -*- coding: utf-8 -*-
# flake8: noqa

from qiniu import Auth, put_file, etag, urlsafe_base64_encode, put_data

access_key = 'bLoheoE20UeRGdBhXkXwl3loi0GgQjDeny1LHW57'
secret_key = 'yD06aKKy3GdFvuka0YA89Usfrw9TRq6cHgcc_M53'

q = Auth(access_key, secret_key)
# 要上传的空间
bucket_name = 'blog'

# key = 'a\\b\\c"你好.txt' # 保存在七牛的文件名
# data = 'hello bubby!' # 文件的数据
# token = q.upload_token(bucket_name)
# ret, info = put_data(token, key, data)

def putImageData(filename, filedata):
  print('--->put images')
  token = q.upload_token(bucket_name)
  ret, info = put_data(token, filename, filedata)
  return ret

# 作为一个模块文件是必须的
def modelName():
  return __name__
