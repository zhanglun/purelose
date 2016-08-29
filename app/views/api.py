from flask import request, current_app, Response
from flask import Blueprint
from app.models import mongo
import json
from bson.objectid import ObjectId

api = Blueprint('api', __name__, url_prefix='/api')


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        else:
            return obj


@api.route('/movies', methods=['GET'])
def index():
    movies = mongo.db.movies.find({})
    data = list()
    for movie in movies:
        data.append(movie)

    return Response(json.dumps(data, cls=Encoder), mimetype='application/json')
