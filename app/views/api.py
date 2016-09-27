import json
from flask import request, current_app, Response, Blueprint
from bson.objectid import ObjectId
from app.models import mongo
from app.helper import tool

api = Blueprint('api', __name__, url_prefix='/api/v1.0')


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        else:
            return obj


@api.route('/movies', methods=['GET'])
def index():
    query_args = request.args.to_dict(False)
    querys = tool.format_query_args(query_args)
    movies = mongo.db.movies.find(querys['search'], {'title': 1, 'images': 1, 'id': 1, 'alt': 1})
    if 'sort' in querys:
        movies.sort(querys['sort'], querys['order'])
    if 'limit' in querys:
        movies.limit(querys['limit']);
    data = list()
    for movie in movies:
        movie['douban_id'] = movie['id']
        movie['id'] = movie['_id']
        movie.pop('_id', None)
        data.append(movie)

    return Response(json.dumps(data, cls=Encoder), mimetype='application/json')


@api.route('/search/movies', methods=['GET'])
def search():
    query_args = request.args.to_dict(False)
    if not query_args:
        return Response(json.dumps({"message": "Validation Failed",
                                    "errors": [
                                        {
                                            "resource": "Search",
                                            "field": "q",
                                            "code": "missing"
                                        }
                                    ]}, cls=Encoder), mimetype='application/json')
    querys = tool.format_query_args(query_args)
    movies = mongo.db.movies.find(querys['search'], {'title': 1, 'images': 1, 'id': 1})
    data = list()
    for movie in movies:
        movie['douban_id'] = movie['id']
        movie['id'] = movie['_id']
        movie.pop('_id', None)
        data.append(movie)

    return Response(json.dumps(data, cls=Encoder), mimetype='application/json')
