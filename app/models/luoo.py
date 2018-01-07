from app.models import mongo


class Model:
    def __init__(self):
        pass

    @staticmethod
    def get_list(querys):

        vols = mongo.db.luoo.find({})

        if 'limit' in querys:
            vols.limit(querys['limit'])

        data = list()

        for vol in vols:
            data.append(vol)

        return data
