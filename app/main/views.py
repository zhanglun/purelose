from flask import render_template, request
from . import main


@main.route('/', methods=['GET'])
def index():
    user_agent = request.headers.get('User-Agent')
    data = dict()
    data['user_agent'] = user_agent
    return render_template('./index.html', data=data)
