import re


def format_query_args(args):
    query = {}
    if 'q' in args.keys():
        list_q = args['q'][0].split(';')
        dict_q = {}
        for l in list_q:
            item = l.split(':')
            dict_q[item[0]] = item[1]

        # title 模糊搜索
        if 'title' in dict_q:
            print(type(dict_q['title']))
            reg_title = re.compile('|'.join(dict_q['title'].split(' ')))
            dict_q = {'$or': [
                {'title': {'$regex': reg_title}},
                {'original_title': {'$regex': reg_title}},
            ]}
        query['search'] = dict_q
    else:
        query['search'] = {}

    if 'sort' in args.keys():
        query['sort'] = args['sort'][0]

    if 'limit' in args.keys():
        query['limit'] = int(args['limit'][0]) > 20 and 20 or int(args['limit'][0])
    else:
        query['limit'] = 20

    if 'order' in args.keys():
        query['order'] = args['order'][0] == 'asc' and 1 or -1
    else:
        query['order'] = 1

    print(query)
    return query
