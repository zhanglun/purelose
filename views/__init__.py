#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'CrispElite'

import web
import urllib2
import urllib
import time
import json
import re
import os


from web.contrib.template import render_jinja
render = render_jinja('./templates', encoding='UTF-8')
