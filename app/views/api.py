from flask import request, current_app
from flask import Blueprint
from app.models import mongo

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/', methods=['GET'])
def index():
    users = mongo.db.users.find({})
    for user in users:
        print(user)
    return "{'page': 'API'}"
