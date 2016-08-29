from flask import jsonify
from flask import Blueprint
from app.models import mongo
from bson import json_util
import json

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/', methods=['GET'])
def index():
    movies = mongo.db.movies.find({})
    result = [];
    for movie in movies:
        result.append(movie)

    print(type(json.loads(json_util.dumps(result))))
    print(type(json_util.dumps(result)))
    return jsonify(json.loads(json_util.dumps(result)))
