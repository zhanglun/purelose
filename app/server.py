from flask import Flask, render_template, request
from flask_script import Manager

app = Flask(__name__, template_folder="./templates")

app.debug = True


@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    data = {}
    data['user_agent'] = user_agent
    return render_template('index.html', data=data)


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


manager = Manager(app)

# 确保服务器只会在该脚本被 Python 解释器直接执行的时候才会运行，而不是作为模块导入的时候
if __name__ == '__main__':
    manager.run()
