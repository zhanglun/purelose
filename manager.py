#! /usr/bin/env python
import os
from flask_script import Manager,Server
from app import create_app
from config import config

env = os.getenv('FLASK_CONFIG') or 'default'
app = create_app(env)

manager = Manager(app)
manager.add_command("runserver", Server(host=config[env].HOST, port=config[env].PORT))

# 确保服务器只会在该脚本被 Python 解释器直接执行的时候才会运行，而不是作为模块导入的时候
if __name__ == '__main__':
    manager.run()
