import re


def format_query_args(args):
    query = {}
    if 'q' in args.keys():
        list_q = args['q'][0].split(' ')
        dict_q = {}
        for l in list_q:
            item = l.split(':')
            dict_q[item[0]] = item[1]

        # title 模糊搜索
        if 'title' in dict_q:
            reg_title = re.compile(dict_q['title'])
            dict_q['title'] = {'$regex': reg_title}
        query['search'] = dict_q

    if 'sort' in args.keys():
        query['sort'] = args['sort']

    if 'order' in args.keys():
        query['order'] = args['order'] == 'asc' and 1 or -1

    print(query)
    return query
