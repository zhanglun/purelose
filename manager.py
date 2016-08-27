#! /usr/bin/env python
import os
from app import create_app
from flask_script import Manager

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

manager = Manager(app)

# 确保服务器只会在该脚本被 Python 解释器直接执行的时候才会运行，而不是作为模块导入的时候
if __name__ == '__main__':
    manager.run()