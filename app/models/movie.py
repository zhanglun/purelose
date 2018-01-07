from app.models import mongo

class MovieModel:
    def __init__(self):
        pass

    # 获取列表
    @staticmethod
    def get_list(querys):
        movies = mongo.db.movies.find(querys['search'],
                                      {'title': 1, 'original_title': 1, 'images': 1, 'id': 1, 'alt': 1})

        if 'sort' in querys:
            movies.sort(querys['sort'], querys['order'])

        if 'limit' in querys:
            movies.limit(querys['limit'])
        data = list()

        for movie in movies:
            movie['douban_id'] = movie['id']
            movie['id'] = movie['_id']
            movie.pop('_id', None)
            data.append(movie)

        return data
