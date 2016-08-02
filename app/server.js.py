from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello World!'

app.debug = True;

if __name__ == '__main__':
  app.run()
