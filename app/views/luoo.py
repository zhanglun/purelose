import json
from flask import make_response, jsonify, request, current_app, Response, Blueprint
from bson.objectid import ObjectId
from app.models import luoo
from app.helper import tool

music = Blueprint('music', __name__, url_prefix='/api/music')


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        else:
            return obj


@music.route('/vols', methods=['GET'])
def index():
    query_args = request.args.to_dict(False)
    querys = tool.format_query_args(query_args)

    model = luoo.Model()

    data = model.get_list(querys)

    return Response(json.dumps(data, cls=Encoder), mimetype='application/json')
