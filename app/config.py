#! /usr/bin/env python
import os
from app import create_app, db
from flask.ext.script import Manager

manager = Manager(app)

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == '__main__':
    manager.run()