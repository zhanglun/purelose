# -*- coding: utf-8 -*-
# flake8: noqa

from qiniu import Auth, put_file, etag, urlsafe_base64_encode

access_key = 'bLoheoE20UeRGdBhXkXwl3loi0GgQjDeny1LHW57'
secret_key = 'yD06aKKy3GdFvuka0YA89Usfrw9TRq6cHgcc_M53'

q = Auth(access_key, secret_key)
#要上传的空间
bucket_name = 'blog'

